import json
with open('04_eval/M4_UGL_1.ipynb', 'r') as f: nb = json.load(f)
cells_to_run = [c['source'] for c in nb['cells'] if c['cell_type'] == 'code'][:3]
exec(''.join(cells_to_run[0]))
exec(''.join(cells_to_run[1]))
result, messages = find_references("Find 2 recent papers about recent developments in black hole science", return_messages=True)
print("Final result:", result)
print("Intermediate messages length:", len(messages))
for i, m in enumerate(messages):
    print(f"Message {i}: {m}")
