from cronjobs_api.views.cat_schedule_view import CatScheduleView
from cronjobs_api.views.file_view import FileView
from cronjobs_api.views.files_view import FilesView
from cronjobs_api.views.job_view import JobView
from cronjobs_api.views.jobs_view import JobsView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


app_name = 'cronjobs_api'

urlpatterns = [
    path('cat_schedule/',  csrf_exempt(CatScheduleView.as_view()), name='cat_schedule'),
    path('file/<int:pk>',   csrf_exempt(FileView.as_view()), name='file'),
    path('files/',         csrf_exempt(FilesView.as_view()), name='files'),
    path('job/<int:pk>',   csrf_exempt(JobView.as_view()), name='job'),
    path('jobs/',          csrf_exempt(JobsView.as_view()), name='jobs'),
]
