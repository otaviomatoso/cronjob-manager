from cronjobs.models.file import File
from datetime import datetime
from django.conf import settings
import pytz


def write_cat_to_file(file_name: str, key=None):
    file_record = File.objects.filter(name=file_name).first()
    if not file_record:
        file_record = File(location=settings.FILES_LOCATION, name=file_name)
        file_record.save()
    with open(f'{file_record.location}/{file_name}', "a") as file:
        run_date = datetime.now(pytz.utc).strftime(settings.DEFAULT_DATETIME_FORMAT)
        file.write(f'[{run_date}] cat\n')
        print(f"Wrote 'cat' to file at {run_date}")
