# 🔗 🐍 Lang Interface

Super lightweight helper to turn your python interface
into an AI assistant.

### 🚀 Quick start:
```python
from dotenv import load_dotenv
from os import environ
from openai import OpenAI

from lang_interface import Assistant
environ['OPENAI_API_KEY'] = '<api_key>'


class MyAPI:
    """Api for managing user's list of contacts (mobile numbers)"""
    contacts = {'John': '000-000', 'Bill': '111-111'}

    def do_get_contact_list(self, name_starts_with: str = None) -> dict[str, str]:
        """Get contacts names and phones"""
        return {
            name: phone
            for name, phone in self.contacts.items()
            if name.startswith(name_starts_with)
        }

    def do_add_contact(self, name: str, phone: str) -> str:
        """Add new contact"""
        if name in self.contacts:
            raise Exception(f'Contact with name {name} already exists!')
        self.contacts[name] = phone
        

llm = OpenAI()
api = MyAPI()
assistant = Assistant(api, llm)
print(assistant('Do I have Bob in my contacts?'))
```

### 💬 Example interactive mode:

```python
def example_chat():
    while True:
        try:
            q = input('\033[1;36m> ')
            print('\033[0m', end='')
            answer = assistant(q)
            print(f'\033[0massistant: {answer}')
        except KeyboardInterrupt:
            print('\033[0;32mBuy!')


example_chat()
```

### 📝 Basics
Lang Interface uses python **docstrings** and **type hints** to create a short specification
of the programming API for LLM.

The quality of outputs depends on well-structured class, where docstrings are laconic and not ambiguous.
It is recommended to use python typing hits to describe parameters and return values.
If you need to specify complicated input/output format use Pydantic models:
```python
from pydantic import BaseModel

class MyContact(BaseModel):
    id: int
    name: str
    phone_number: str
    created_at: datetime

class Interface:
    def do_create_contact(self, contact: MyContact):
        ...
```
However, using dictionaries would still be more reliable, but remember to write a comprehensible docstring.
