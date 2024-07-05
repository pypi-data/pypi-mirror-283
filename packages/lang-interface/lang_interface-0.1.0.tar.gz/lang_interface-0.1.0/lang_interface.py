import inspect
import re
import warnings
from typing import Type

from tenacity import retry, stop_after_attempt

try:
    from pydantic import BaseModel

    has_pydantic = True
except:
    has_pydantic = False

debug = False

CHAT_PROMPT = """
You are an AI assistant connecting a user and a following programming interface:
## Description:
{description}
## Operations:
{interface}

Your goal is to convert user's request into a python function call with parameters.
If user's request is clear respond in the following format:
<CALL>function(**parameters)</CALL>
If it's not clear what function to call and what parameters to pass, respond with clarification message:
<CLARIFY>question</CLARIFY>

Also, if one interface call is not enough to retrieve needed info, anyway provide the first required call.

User might ask questions, not related to provided interface, so act as a simple AI assistant, answer:
<ANOTHER>answer</ANOTHER>
"""
FUNCTION_PROMPT = """
You are an AI assistant connecting a user and a following programming interface:

## Description:
{description}
## Operations:
{interface}

Your goal is to convert user's request into a python function call with parameters.
You will receive user's question, the last called operation and the output from that operations in the following format:
<QUESTION>question</QUESTION>
<OPERATION>operation</OPERATION>
<OUTPUT>output</OUTPUT>

You have three options:
1. Respond with a given output, if output from operation seem to satisfy user's request, but reformat it to make read-friendly and get cut not relevant data.
2. Call another operation, or same operation with different parameters
3. Respond with clarification question to a user, if output from operation is not the answer to his question, but it's not clear what operation needs to be called instead.

Depending on the option respond in 3 different ways:
1. <OUTPUT> output here </OUTPUT>
2. <CALL>function(**params)</CALL>
3. <CLARIFY>question</CLARIFY>
"""
FUNCTION_PROMPT_USER = """
<QUESTION>question</QUESTION>
<OPERATION>{operation}</OPERATION>
<OUTPUT>{output}</OUTPUT>
"""


class LLMWrapper:
    """LLM client wrapper

    Has a single method __call_ that accepts messages and returns response string
    """

    def __call__(self, messages) -> str:
        raise NotImplemented


class Assistant:
    handler: Type
    llm: LLMWrapper
    max_context: int

    def __init__(
        self,
        handler,
        llm: LLMWrapper,
        *,
        max_context: int = 50_000,
        methods_prefix: str = 'do_',
    ):
        """
        LLM Assistant interface for python class
        :param handler: a class that implements a programing interface
        :param llm: Can be either OpenAI client or Custom LLM Wrapper, see LLMWrapper
        :param max_context: maximum number of chars allowed in a context
        :param methods_prefix: prefix string to indicate public interface methods
        """
        self.handler = handler
        self.llm = _get_llm_wrapper(llm)
        self.max_context = max_context
        self._spec = _parse_interface(handler, methods_prefix)
        self._interface_md = _get_interface_md(self._spec)
        if debug:
            print('Interface:\n' + self._interface_md)

        description = inspect.getdoc(self.handler) or "Interface"
        self.chat_prompt = CHAT_PROMPT.format(
            interface=self._interface_md,
            description=description
        )
        self.function_prompt = FUNCTION_PROMPT.format(
            interface=self._interface_md,
            description=description
        )
        self._messages = [{'role': 'system', 'content': self.chat_prompt}]

    def __call__(self, question: str) -> str:
        self._messages.append({'role': 'user', 'content': question})
        call_context = []
        self._trim_messages()
        final_result = None
        response = self._llm(messages=self._messages)
        action, text = _parse_response(response)

        if action in ['clarify', 'another']:
            final_result = text
        else:
            operation = text
            output = self.call_method(text)

        # call cycle
        while final_result is None:
            final_result = text
            action, text = self._process_output(operation, output)
            if action == 'call':
                output = self.call_method(text)
            else:
                final_result = text
        self._messages.append({'role': 'assistant', 'content': final_result})
        return final_result

    def _trim_messages(self):
        char_used = 0
        new_messages = []
        for message in self._messages[:0:-1]:
            char_used += len(message['content'])
            if char_used < self.max_context:
                new_messages.append(message)
        new_messages = [self._messages[0]] + new_messages[::-1]
        self._messages = new_messages


    @retry(stop=stop_after_attempt(3))
    def _process_output(self, operation, output):
        messages = [
            {'role': 'system', 'content': self.function_prompt},
            *self._messages[1:],
            {'role': 'user', 'content': FUNCTION_PROMPT_USER.format(
                operation=operation, output=output, question=self._messages[-1]['content']
            )}
        ]
        resp = self._llm(messages=messages)
        return _parse_response(resp)

    def call_method(self, method):
        run_code = f'self.handler.{method}'
        try:
            for definition, obj in self._spec['definitions'].items():
                locals()[definition] = obj
            result = eval(run_code)
            if debug:
                print(f'DEBUG: called method: {method}')
            return result or "Operation succeeded"
        except Exception as e:
            if debug:
                print(f'Exception running method: {method}: {e}')
            return f"When calling this operation, the exception was caught: {e}"

    def _validate_method_call(self, method):
        method, params = method.split('(')
        assert method in self._operations
        assert ';' not in params

    def _llm(self, messages):
        response = self.llm(messages=messages)
        if debug:
            print(f'\033[2mDEBUG: assistant: {response}\033[0m')
        return response


def _parse_response(text):
    tags = _parse_tags(text)
    if not tags:
        return 'another', text
    return list(tags.items())[0]


def _parse_tags(text):
    # Pattern to match the structure: [TAG]content[/TAG]
    pattern = r"\<(\w+)\>(.*?)\<\/\1\>"
    # Find all matches and store them in a dictionary
    matches = re.findall(pattern, text, re.DOTALL)
    return {tag.lower(): content.strip() for tag, content in matches}


def _get_interface_md(specs):
    text = ""
    for signature, doc in specs['operations'].values():
        text += f"#### {signature}\n{doc}\n\n"
    if specs.get('models'):
        text += f"### Models:\n"
        for model_name, schema in specs['models'].items():
            text += f"- {model_name}\n{schema}"

    return text


def _parse_interface(cls, prefix):
    """Recursively parse the class methods signatures to create python specification"""
    operations = {}
    models = []
    models_dict = {}
    # model definitions are needed to set it in local() when generated function call is executed.
    models_definitions = {}
    methods = inspect.getmembers(cls, predicate=inspect.ismethod)
    do_methods = {name: func for name, func in methods if name.startswith(prefix)}

    for name, func in do_methods.items():
        doc = inspect.getdoc(func)
        signature = inspect.signature(func)
        operations[name] = (f"{name}{signature}", doc)

        for param_name, param_type in signature.parameters.items():
            if has_pydantic:
                models = _parse_hints(param_type.annotation)

        models += _parse_hints(signature.return_annotation)

        for model in models:
            models_dict[model.__name__] = model.schema()
            models_definitions[model.__name__] = model

    return {'operations': operations, 'models': models_dict, 'definitions': models_definitions}


def _parse_hints(annotation):
    models = []
    if hasattr(annotation, '__args__'):
        for arg in annotation.__args__:
            models += _parse_hints(arg)
    elif issubclass(annotation, BaseModel):
        models.append(annotation)
    return models


class _OpenAIWrapper:
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def __call__(self, messages):
        resp = self.client.chat.completions.create(
            messages=messages, model='gpt-4o'
        )
        return resp.choices[0].message.content


def _get_llm_wrapper(llm, model=None):
    if str(type(llm)) == 'OpenAI':
        return _OpenAIWrapper(llm, model=model)
    elif isinstance(llm, LLMWrapper):
        return _OpenAIWrapper(llm, model=model)
    else:
        warnings.warn('LLM is not a subclass of OpenAI or LLMWrapper')
        return llm
