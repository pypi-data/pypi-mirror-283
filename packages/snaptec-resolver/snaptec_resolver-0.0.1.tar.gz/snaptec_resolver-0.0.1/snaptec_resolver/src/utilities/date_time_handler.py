from datetime import datetime, timezone, timedelta
from snaptec_resolver.src.utilities.singleton import Singleton

class DateTimeHandler:
    def get_utc_plus3():
        # Getting the current date and time in UTC
        dt_utc = datetime.datetime.now(timezone.utc)
        # Adding a UTC+3 offset
        utc_plus3 = (dt_utc + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
        return utc_plus3
    @staticmethod
    def get_current_datetime(timezone_offset=0):
        dt_utc = datetime.now(timezone.utc)
        dt_with_offset = dt_utc + timedelta(hours=timezone_offset)
        formatted_time = dt_with_offset.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time