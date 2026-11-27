def answer(user_id: str, query: str) -> str:
    # 1. RAG에서 공통 지식 검색
    common_facts = rag_system.search(query)

    # 2. 사용자 메모리에서 개인 정보 검색
    user_memory = UserMemory(user_id, mem_store)
    personal_facts = user_memory.recall(query)

    # 3. 둘을 *분명히 구분*해 컨텍스트에 합침
    context = f"""\
[공통 지식]
{format_facts(common_facts)}

[이 사용자에 대한 정보]
{format_facts(personal_facts)}
"""

    return call_model(query, system=context)
