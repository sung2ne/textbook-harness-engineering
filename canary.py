import random

def call_with_canary(input, canary_percent: int = 5):
    if random.random() * 100 < canary_percent:
        model = NEW_MODEL
        is_canary = True
    else:
        model = OLD_MODEL
        is_canary = False

    result = call(input, model)
    log_result(model=model, is_canary=is_canary, result=result)
    return result
