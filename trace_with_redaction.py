def safe_record_input(span, input_text: str):
    masked = mask_secrets(input_text)
    truncated = masked[:500] + "..." if len(masked) > 500 else masked
    span.set_attribute("app.input.preview", truncated)
