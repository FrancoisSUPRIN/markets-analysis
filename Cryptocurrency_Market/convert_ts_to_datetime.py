from datetime import datetime
import pytz
    
def convert_ts_to_datetime(ts):
    ts_as_datetime = datetime.fromtimestamp(ts/1000, tz=pytz.timezone('Europe/Paris'))
    return ts_as_datetime