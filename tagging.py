def call_with_tags(team: str, project: str, message: str):
    with tracer.start_as_current_span("agent.run") as span:
        span.set_attribute("company.team", team)
        span.set_attribute("company.project", project)
        return run(message)
