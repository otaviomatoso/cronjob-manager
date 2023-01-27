from apscheduler.schedulers.background import BackgroundScheduler
from cat_manager.jobs import write_cat_to_file
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views import View
from cat_manager import manager


class CatScheduleView(View):

    def post(self, request, *args, **kwargs):
        delay = int(request.GET.get('delay', 5))
        scheduler = BackgroundScheduler()
        next_run_date = datetime.now() + timedelta(seconds=delay)
        scheduler.add_job(func=write_cat_to_file, trigger='date', run_date=next_run_date)
        scheduler.start()
        next_run_date = datetime.strftime(next_run_date, '%H:%M:%S')
        return JsonResponse({'message': f'Job will run at {next_run_date}'})
