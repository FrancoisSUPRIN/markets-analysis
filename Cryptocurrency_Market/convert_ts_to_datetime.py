from datetime import datetime
import pytz
    
def convert_ts_to_datetime(ts):
    ts_as_datetime = datetime.fromtimestamp(ts/1000, tz=pytz.timezone('Europe/Paris'))
    return ts_as_datetime

def format_elapsed_time(ms):
    # Conversion des millisecondes en secondes
    total_seconds = ms / 1000
    
    # Calculer le nombre de jours
    days = int(total_seconds // (24 * 3600))
    remainder_seconds = total_seconds % (24 * 3600)
    
    # Calculer le nombre d'heures
    hours = int(remainder_seconds // 3600)
    remainder_seconds %= 3600
    
    # Calculer le nombre de minutes
    minutes = int(remainder_seconds // 60)
    remainder_seconds %= 60
    
    # Les secondes restantes
    seconds = int(remainder_seconds)
    
    # Formatage en "jours HH:MM:SS"
    formatted_time = f"{days}days {hours:02}h:{minutes:02}m:{seconds:02}s"
    
    return formatted_time