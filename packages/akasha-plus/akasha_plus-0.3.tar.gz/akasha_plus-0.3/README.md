# akasha-plus

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python version : 3.9 3.10 3.11](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/downloads/release/python-390/)

<br/>

Akasha-plus is an external-plugin for [akasha](https://github.com/iii-org/akasha), which includes various kind of extended applications like model quantisation, agent-tools and others.

<br/>
<br/>

# Installation

We recommend using Python 3.9 to run our akasha-plus package. You can use Anaconda to create virtual environment.

```bash
# create virtual environment
conda create --name py3-9 python=3.9
activate py3-9

# install akasha-plus
pip install git+https://gitlab-devops.iii.org.tw/iiidevops/akasha-plus-dev.git
```

<br/>
<br/>

# Python API
## Agent Tools
Use customized tools to speed-up application development.
For each tool, there are two ways to use it, include "apply tool function directly" and "use akasha agent". The main difference between these two ways mentioned above is that the first requires the developer to set individual parameters manually, while the second allows for a conversational description, enabling the agent to determine the corresponding parameters on its own automatically.

### Database-Query Tool
This tool is used for question-answering based on specific given database table.
#### Apply function directly
```python
# import module
from akasha_plus.agents.tools import set_connection_config, db_query_func
# define question, table_name
question = '<my-question-to-ask>'
table_name = '<my-target-table>'
# define column description json (in json-like string or path of json file) if needed
column_description_json = {}
# set database connection
connection_config = set_connection_config(sql_type='SQLITE', database='database.db')
# use tool to get answer
answer = db_query_func(question=question, table_name=table_name, simplified_answer=True, connection_config=connection_config, model='openai:gpt-4')
print(answer) # the answer to the user question based on database query
```
#### Use akasha agent
```python
import akasha
from akasha_plus.agents.tools import db_query_tool
agent = akasha.test_agent(verbose=True, tools=[db_query_tool], model='openai-gpt-4')
# put all information in plain language
question = '''
    我要查詢一個"SQLITE"資料庫 名為 "database.db", 裡面有一個table="<my-target-table>",
    欄位意義說明如下:
    ---
    1. <column-1>: <descriotion-of-column-1>
    2. <column-2>: <descriotion-of-column-2>
    ...
    ---
    <my-question-to-ask>
    '''   
# let akasha agent to consider the rest of the process       
answer = agent(question, messages=[])
print(f'agent回答：{answer}')
```

### Webpage Summary Tool
This tool is used for retrieving summary contents from specific webpage with given url.
#### Apply function directly
```python
from akasha_plus.agents.tools import webpage_summary_func
summarized_result = webpage_summary_func(url='https://www.ptt.cc/bbs/Tech_Job/M.1719665577.A.A92.html', model='openai:gpt-4')
print(summarized_result) # the summary for webpage
```
#### Use akasha agent
```python
import akasha
from akasha_plus.agents.tools import webpage_summary_tool
agent = akasha.test_agent(verbose=True, tools=[webpage_summary_tool], model='openai-gpt-4')
# put all information in plain language
question = '''請告訴我網站 "https://www.ptt.cc/bbs/Tech_Job/M.1719665577.A.A92.html" 的重點'''   
# let akasha agent to consider the rest of the process       
answer = agent(question, messages=[])
print(f'agent回答：{answer}')
```

### Dialogue Information Collection Tool
This tool is used for collecting information of specific items/categories assigned by user through dialogue. The generated output will be the latest reply in order to continue dialogue for data collection.
#### Apply function directly
```python
from akasha_plus.agents.tools import collect_dialogue_info_func
reply = collect_dialogue_info_func(dialogue_history='''
    由於我們系統回報您的用電量異常升高，我們想了解一下您最近有開關哪些電器呢？'\n 
    我開了冷氣\n
    瞭解，您最近有開冷氣。請問您開冷氣的原因是什麼呢？\n
    天氣很熱\n
    請問除了冷氣以外，您還有開啟其他電器嗎？\n
    沒有\n
    ''', 
    collect_item_statement='想要蒐集使用者操作哪些電器，操作是開還是關，以及其背後的原因', 
    interview_background='系統回報用電量異常升高'
)
print(reply) # The next reply for this dialogue
```

#### Use akasha agent
```python
import akasha
from akasha_plus.agents.tools import collect_dialogue_info_tool
agent = akasha.test_agent(verbose=True, tools=[collect_dialogue_info_tool], model='openai-gpt-4')
# put all information in plain language
question = '''我收到來自異常偵測模型的警示，發現使用者用電量異常升高，因此想要透過對話蒐集使用者操作哪些電器，操作是開還是關，以及其背後的原因'''   
# let akasha agent to consider the rest of the process       
answer = agent(question, messages=[])
print(f'agent回答：{answer}')
```

# Console mode API

### to-gguf
Change model directory downloaded from [huggingface](https://huggingface.co/) into [gguf format](https://huggingface.co/docs/hub/gguf)
<br/>
Usage:
```bash
akasha-plus to-gguf --model "<your-model-directory>" --outtype "<floating-point-precision>" --verbose --pad-vocab
```

### quantize-gguf
Quantize gguf model into smaller bit of precision
<br/>
To successfully quantize model, make sure you have a gguf-formatted model, or use `akasha-plus to-gguf` api to transfer the model into gguf format.
<br/>
Usage:
```bash
akasha-plus quantize-gguf --model "<gguf-model-path>" --method "<quantization-method>" --verbose
```

### quantize-gptq
Quantize model into smaller bit of precision by [auto-gptq](https://github.com/AutoGPTQ/AutoGPTQ)
<br/>
Usage:
```bash
akasha-plus quantize-gptq --model "<model-path>" --bits "<quantizat-bits>"
```
