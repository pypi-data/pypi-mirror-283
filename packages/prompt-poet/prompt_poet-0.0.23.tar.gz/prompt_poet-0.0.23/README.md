# Project Description

### Prompt Poet (PP)

The simplest way of using control flow (like if statements and for loops) to build production-grade prompts for LLMs.

---


### Installation

```shell
python3.10 -m venv --clear .pp
source .pp/bin/activate

python -m pip install prompt-poet
```

**Optional**: if you want tokenization capability you will need to install the default Character.AI tokenizer separately (below) or provide your own.

```shell
python -m pip install chartok@https://characterai.io/py_wheels/chartok/chartok-0.4.3-py3-none-any.whl
```

### Basic Usage

Below is an example a basic chat template. Copy and paste this into a file `chat_template.yml.j2` on your local filesystem.

Filename: **chat_template.yml.j2**

```yaml
- name: instructions
  raw_string: |
    You are {{ character_name }}. You are a chatbot created by Character.AI. You are meant to be helpful and never harmful to humans.

{% if examples %}
{% for example in examples %}
- name: example_{{ loop.index }}
  raw_string: |
    {{ sep }}{{ example }}
{% endfor %}
{% endif %}

{% for message in messages %}
- name: message_{{ loop.index }}
  truncation_priority: 5
  raw_string: |
    {{ sep }}{{ message }}
{% endfor %}

- name: reply_prompt
  raw_string: |
    {{ sep }}{{ character_name }}:
```

Instantiate a python shell from the same directory that you saved the file `chat_template.yml.j2` to.

```python
from prompt_poet import Prompt

prompt = Prompt(
    template_name="chat_template.yml.j2",
    template_data={
        "sep": "<|sep|>",
        "character_name": "Balderdash",
        "messages": ["Jeff: Hi there!"]
    }
)
print(prompt.string)
>>> '<|bod|>You Balderdash are a chatbot created by Character.AI. You are meant to be helpful and never harmful to humans.<|bom|>Jeff: Hi there!<|eom|><|bom|>Balderdash:'
```

If you have installed the tokenizer separately you can extract the raw tokens from the prompt.

```python
prompt.tokenize()
print(prompt.tokens)
>>> [3616, 413, 9772, 602, 44641, 23, 686, 413, 267, 6630, 10780, 4630, 539, 26865, 23, 27872, 23, 686, 413, 3662, 296, 337, 6498, 308, 1046, 20577, 296, 6954, 23, 1432, 84900, 1429, 40714, 35, 5251, 604, 10, 1432, 84900, 1429, 44762, 602, 44641, 35]
```

You can play with the cache-friendly truncation algorithm out of the box to maximize KV cache utilization on successive messages.

**Note**: notice the `truncation_priority` set in the chat_template.yml.j2. Not setting a `truncation_priority` or setting it to 0 on a given part will preclude it from truncation.

```python
prompt = Prompt(
    template_name="chat_template.yml.j2",
    template_data={
        "sep": "<|sep|>",
        "character_name": "Balderdash",
        "messages": [
            "Jeff: Hi there!",
            "Balderdash: Hi! How can I help you today?",
            "Jeff: I need help with my homework.",
            "Balderdash: Sounds great. I am a fantastic choice to help you with your homework. What is it?"
        ]
    }
)
prompt.tokenize()
prompt.truncate(token_limit=80, truncation_step=5)
print(prompt.string)
>>> 'You are Balderdash. You are a chatbot created by Character.AI. You are meant to be helpful and never harmful to humans.<|sep|>Jeff: I need help with my homework.<|sep|>Balderdash: Sounds great. I am a fantastic choice to help you with your homework. What is it?<|sep|>Balderdash:'

print(prompt.tokens)
>>> [3616, 413, 9772, 602, 44641, 23, 686, 413, 267, 6630, 10780, 4630, 539, 26865, 23, 27872, 23, 686, 413, 3662, 296, 337, 6498, 308, 1046, 20577, 296, 6954, 23, 1432, 84900, 1429, 40714, 35, 297, 756, 1067, 377, 465, 23842, 23, 1432, 84900, 1429, 44762, 602, 44641, 35, 6837, 1125, 23, 297, 650, 267, 8309, 3777, 296, 1067, 326, 377, 501, 23842, 23, 984, 334, 336, 40, 1432, 84900, 1429, 44762, 602, 44641, 35]

prompt.truncate(token_limit=100, truncation_step=5)
print(prompt.string)
>>> 'You are Balderdash. You are a chatbot created by Character.AI. You are meant to be helpful and never harmful to humans.<|sep|>Jeff: Hi there!<|sep|>Balderdash: Hi! How can I help you today?<|sep|>Jeff: I need help with my homework.<|sep|>Balderdash: Sounds great. I am a fantastic choice to help you with your homework. What is it?<|sep|>Balderdash:

print(prompt.tokens)
>>> [3616, 413, 9772, 602, 44641, 23, 686, 413, 267, 6630, 10780, 4630, 539, 26865, 23, 27872, 23, 686, 413, 3662, 296, 337, 6498, 308, 1046, 20577, 296, 6954, 23, 1432, 84900, 1429, 40714, 35, 5251, 604, 10, 1432, 84900, 1429, 44762, 602, 44641, 35, 5251, 10, 1171, 473, 297, 1067, 326, 2272, 40, 1432, 84900, 1429, 40714, 35, 297, 756, 1067, 377, 465, 23842, 23, 1432, 84900, 1429, 44762, 602, 44641, 35, 6837, 1125, 23, 297, 650, 267, 8309, 3777, 296, 1067, 326, 377, 501, 23842, 23, 984, 334, 336, 40, 1432, 84900, 1429, 44762, 602, 44641, 35]
```

Or use a batteries included example template provided for you:
```python
from prompt_poet import Prompt, CAIMessage
template_data = {
    "timestamp": "2024 06 24",
    "username": "Jeff",
    "character": {
        "title": "The title",
        "description": "The description",
        "definition": "The definition\nWith multiple lines\nIn the definition",
        "participant__name": "Alice",
    },
    "persona_definition": "The persona definition",
    "cai_messages": [
        CAIMessage(author="Alice", text="The first message"),
        CAIMessage(author="Jeff", text="The second message"),
        CAIMessage(author="Alice", text="The third message", is_pinned=True),
        CAIMessage(author="Jeff", text="The fourth message"),
    ],
    "reply_prompt": "Alice:"
}
prompt = Prompt(template_name="cai.yml.j2", from_examples=True, template_data=template_data)
print(prompt.string)
>>> '<|beginningofdialog|>2024 06 24 Alice: The title - The description<|endofmessage|><|beginningofmessage|>narrator: The definition<|endofmessage|><|beginningofmessage|>narrator: With multiple lines<|endofmessage|><|beginningofmessage|>narrator: In the definition<|endofmessage|><|beginningofmessage|>Jeff: The persona definition<|endofmessage|><|beginningofmessage|>Alice: The third message<|endofmessage|><|beginningofmessage|>Alice: The first message<|endofmessage|><|beginningofmessage|>Jeff: The second message<|endofmessage|><|beginningofmessage|>Alice: The third message<|endofmessage|><|beginningofmessage|>Jeff: The fourth message<|endofmessage|><|beginningofmessage|>Alice:'
```

---

### Goals & Requirements

1. Centralized: By centralizing the prompt construction into one place, Prompt Poet (PP) aims to simplify the prompt construction mechanics.
2. Extensible: Make it as easy as possible to create new prompts for new use cases.
3. Experimentation: Must be easy to experiment with wholly different prompt formats and content.

Fundamentally, Prompt Poet (PP) is split into two layers -- the Templating Layer and the Logical Layer. We aim to keep a clear separation between these layers such that the Templating Layer exclusively handles the representation of the prompt and the Logical Layer handles the mechanics of constructing the prompt.

---

### Templating Layer

#### Templates
Prompt templates are expressive and human-readable files defined with a combination of YAML and Jinja2 syntax that define the prompt structure, data placements, and formatting.

Once the Jinja2 rendered, a prompt template is just YAML with a repeating sequence of simple parts. A part can consist of:
- `name`: a unique name given to the prompt part used for readability and sometimes used functionally such as for truncation.
- `raw_string`: the string payload representing the content to be tokenized for this prompt part.
- `truncation_priority`: (optional) the priority given to the prompt part during truncation. No value or a value of 0 means this part will never be truncated from the prompt.

##### Alternatives considered
- Langchain: PromptTemplate, AIMessage, SystemMessage, and HumanMessage abstractions. Basically just f-strings wrapped in a Python class, not expressive enough as it does not handle control flow well.
- LMQL: Not very readable, non-trivial to reason about what the final interpolated prompt would look like.
- Raw Python f-strings: Better readability but not very expressive.
- Jinja: Probably the best standalone bet found so far but leaves several things to be desired. See an example here.
- YAML: Could also work by rolling our own basic interpreter. See an example here.
- Several OSS “prompt management” solutions: Pezzo, Agenta, PromptHub (paid), Langflow. These all miss the mark in terms of extensibility of the core templating language and infrastructure and focus on using external APIs rather than needing to truncate and tokenize, which is crucial for us as we host our own models.

---

### Logical Layer

The Logical Layer renders templates and constructs the final prompt in the form of a string or tokens if desirable.

#### 1. Rendering:
The rendering process takes a template and fills in the necessary data to produce a final prompt. This involves:

- Data binding: Interpolating data into the template.
- Evaluation: Processing Jinja2 control flow defined in the template.

#### 2. Tokenization
Tokenization is the process of breaking down the final prompt into tokens that the LLM can understand.

#### 3. Truncation
Truncation ensures the prompt fits within the specified `token_limit`. This involves:
- Prioritizing parts: Using the `truncation_priority` to define the order of truncation.
- Smart truncation: The truncation algorithm uses a smart buffer to truncate more than is strictly needed to meet the token limit in order to maximize KV Cache utilization on the model servers.
