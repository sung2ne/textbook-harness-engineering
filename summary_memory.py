class SummaryMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.summary = self._load()

    def _load(self) -> str:
        return db.get_summary(self.user_id) or ""

    def update(self, conversation: list[dict]):
        new_summary = call_memory_summarizer(
            previous_summary=self.summary,
            new_conversation=conversation,
        )
        self.summary = new_summary
        db.save_summary(self.user_id, new_summary)

    def to_system_prompt(self) -> str:
        if not self.summary:
            return ""
        return f"\n\n[이 사용자에 대해 알려진 정보]\n{self.summary}"
