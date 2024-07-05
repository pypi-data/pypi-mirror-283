from datetime import datetime, timedelta

now = datetime.now()
now_cleaned = now.replace(minute=0, second=0, microsecond=0)
