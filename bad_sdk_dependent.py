def store_conversation(messages):
    db.save("conv", messages)  # Anthropic의 messages 형식이 그대로 DB에 저장됨
