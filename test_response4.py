import json
with open('04_eval/M4_UGL_1.ipynb', 'r') as f: nb = json.load(f)
cells_to_run = [c['source'] for c in nb['cells'] if c['cell_type'] == 'code'][:3]
exec(''.join(cells_to_run[0]))
exec(''.join(cells_to_run[1]))
prompt = "Find 2 recent papers about recent developments in black hole science"
messages = [{"role": "user", "content": prompt}]
tools = [research_tools.arxiv_search_tool, research_tools.tavily_search_tool, research_tools.wikipedia_search_tool]
response = client.chat.completions.create(
    model="openai:gemini-3.5-flash",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    max_turns=10,
)
print("Intermediate messages length:", len(response.choices[0].intermediate_messages) if hasattr(response.choices[0], "intermediate_messages") else 0)
for i, m in enumerate(response.choices[0].intermediate_messages if hasattr(response.choices[0], "intermediate_messages") else []):
    print(f"Message {i}: {m}")
print("Final Content:", response.choices[0].message.content)
