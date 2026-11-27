def evaluate_new_model(new_model: str, golden_set):
    results = []
    for case in golden_set:
        result = run_with_model(case, new_model)
        results.append(result)
    return aggregate(results)
