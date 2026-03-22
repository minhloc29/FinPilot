import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, how are you?"

tokens = enc.encode(text)

print(tokens)        # list of token IDs
print(len(tokens))   # number of tokens