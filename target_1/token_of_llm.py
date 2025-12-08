import tiktoken

models = [
    "gpt-3.5-turbo",
    "gpt-4o",
]
for model in models:
    enc = tiktoken.encoding_for_model(model)
    print(f"-----------------Model: {model}, Encoding: {enc.name}--------------")
    ret = enc.encode("生日快乐")
    print("Encoded:", ret)
    dec = enc.decode(ret)
    print("Decoded:", dec)