from django.urls import path
from cronjobs_api.views.cat_schedule_view import CatScheduleView
from django.views.decorators.csrf import csrf_exempt


app_name = 'cronjobs_api'

urlpatterns = [
    path('cat_schedule/', csrf_exempt(CatScheduleView.as_view()), name='cat_schedule'),
]
