from cat_manager.manager import scheduler
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from enums import JobTypes
from http import HTTPStatus
import pytz


class CatScheduleView(View):

    UTC_TIMEZONE = pytz.utc

    def post(self, request, *args, **kwargs):
        delay = int(request.GET.get('delay', 5))
        run_date = datetime.now(pytz.utc) + timedelta(seconds=delay)
        scheduler.add_job(func='cat_manager.jobs.cat:write_cat_to_file', trigger='date', run_date=run_date,
                          kwargs={'key': JobTypes.CAT, 'file_name': 'cat_file.txt'}, misfire_grace_time=None)

        run_date = run_date.strftime(settings.DEFAULT_DATETIME_FORMAT)
        print(f'[API] Will write cat to file at {run_date}')
        return JsonResponse({'message': f'Job will run at {run_date}'}, status=HTTPStatus.CREATED)
