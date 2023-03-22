from cat_manager.jobs import write_cat_to_file
from cat_manager.manager import scheduler
from datetime import datetime, timedelta
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
        scheduler.add_job(func=write_cat_to_file, trigger='date', run_date=run_date,
                          kwargs={'key': JobTypes.CAT, 'file_name': 'cat_file.txt'},
                          misfire_grace_time=None)

        run_date_pst = run_date.astimezone(tz=pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        print(f'[API] Will write cat to file at {run_date_pst}')
        return JsonResponse({'message': f'Job will run at {run_date_pst}'}, status=HTTPStatus.CREATED)
