import json
with open('04_eval/M4_UGL_1.ipynb', 'r') as f: nb = json.load(f)
cells_to_run = [c['source'] for c in nb['cells'] if c['cell_type'] == 'code'][:2]
exec(''.join(cells_to_run[0]))
exec(''.join(cells_to_run[1]))
prompt = "Find 2 recent papers about black holes"
messages = [{"role": "user", "content": prompt}]
tools = [research_tools.arxiv_search_tool, research_tools.tavily_search_tool, research_tools.wikipedia_search_tool]
response = client.chat.completions.create(
    model="openai:gemini-3.5-flash",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    max_turns=5,
)
print("Content:", response.choices[0].message.content)
print("Tool calls:", getattr(response.choices[0].message, 'tool_calls', None))
