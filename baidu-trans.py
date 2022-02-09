from bdtr import bdtr
print(bdtr('hello world'))  # -> '你好，世界'
print(bdtr('hello world', to_lang='de'))  # ->'Hallo Welt'
print(bdtr('hello world', to_lang='jp'))  # ->'ハローワールド'