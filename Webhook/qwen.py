import ollama
modelfile='''
FROM llama3
SYSTEM  would like you to talk to a client requesting the configurations of networking, remembering that the client knows nothing about computer networks, and transform these commands into network intentions.

'''

ollama.create(model='example', modelfile=modelfile)