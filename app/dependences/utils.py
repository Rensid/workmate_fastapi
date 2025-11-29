from datetime import time, datetime, timedelta


def count_ttl():
    now = datetime.now()
    clear_time = time(14, 11)
    today_clear = datetime.combine(now.date(), clear_time)

    target = today_clear if now < today_clear else today_clear + timedelta(days=1)
    return int((target - now).total_seconds())
