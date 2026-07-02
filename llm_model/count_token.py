import tiktoken

# 建立 tiktoken 的計算器
enc = tiktoken.get_encoding("cl100k_base")


def count_tokens(messages: str) -> int:
    print(f"\n Message Token : {messages} \n Count: [{len(enc.encode(messages))}] \n")
    if isinstance(messages, str):
        return len(enc.encode(messages))
    
    text = "\n".join(
        getattr(message, "content", "")
        for message in messages
    )
    
    return len(enc.encode(text))




        # # 修剪 Message 的內容，避免超過 token 限制
        # # 最多保留 7500 個 Token，且必須保留最後一筆訊息，使用 tiktoken 來計算
        # self.trimmer = trim_messages(
        #     max_tokens=7500,
        #     strategy='last',
        #     token_counter=count_tokens, # 用來算 token
        #     include_system=True, # 保留 system prompt
        #     allow_partial=False
        # )