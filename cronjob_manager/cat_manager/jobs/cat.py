from cronjobs.models.file import File
from datetime import datetime
import os
import pytz


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_LOCATION = os.path.join(BASE_DIR, 'files/')
PST_TIMEZONE = pytz.timezone('US/Pacific')

def write_cat_to_file(file_name: str, key=None):
    file_record = File.objects.filter(name=file_name).first()
    if not file_record:
        file_record = File(location=FILES_LOCATION, name=file_name)
        file_record.save()
    with open(f'{file_record.location}{file_name}', "a") as file:
        run_date = datetime.now(PST_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        file.write(f'[{run_date}] cat\n')
        print(f"Wrote 'cat' to file at {run_date}")
