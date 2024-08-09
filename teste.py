import ollama
x = ollama.chat(model='example2', messages=[{'role': 'user', 'content': 'me ajude'}])
print(x)