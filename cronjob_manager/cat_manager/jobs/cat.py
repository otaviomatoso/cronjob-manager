from cronjobs.models.file import File
from cronjobs.models.job import Job as JobModel
from datetime import datetime
from django.conf import settings
from http import HTTPStatus
import pytz


def _store_job_return(function):

    def job_handler(*args, **kwargs):
        job_model_id = kwargs.pop('model_id')
        if not job_model_id:
            return

        try:
            status_and_result_tuple = function(*args, **kwargs)
        except Exception as e:
            status_and_result_tuple = HTTPStatus.INTERNAL_SERVER_ERROR, str(e)
        print(f'result: {status_and_result_tuple}')

        job_model = JobModel.objects.filter(id=job_model_id).first()
        job_model.result = str(status_and_result_tuple)
        job_model.save()

    print('starting _store_job_return')
    return job_handler


@_store_job_return
def write_cat_to_file(file_name: str, key=None):
    file_record = File.objects.filter(name=file_name).first()
    if not file_record:
        file_record = File(location=settings.FILES_LOCATION, name=file_name)
        file_record.save()
    with open(f'{file_record.location}/{file_name}', "a") as file:
        run_date = datetime.now(pytz.utc).strftime(settings.DEFAULT_DATETIME_FORMAT)
        file.write(f'[{run_date}] cat\n')
        print(f"Wrote 'cat' to file at {run_date}")

    return HTTPStatus.OK, 'ok'
