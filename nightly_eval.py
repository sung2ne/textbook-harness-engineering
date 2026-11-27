NOISE_BAND = 0.05  # 예시 값. PART 05 Ch 04의 반복 측정으로 잰 변동 폭으로 바꿔 쓴다


def nightly_regression_check():
    yesterday_score = read_score_from_yesterday()
    today_score = run_eval_on_golden_set()

    save_score(today_score)

    drop = (yesterday_score - today_score) / yesterday_score
    if drop > NOISE_BAND:  # 변동 폭보다 크게 떨어지면
        send_alert(f"Quality dropped {drop*100:.1f}%")
