from cronjobs.models.job import Job
from django.http import JsonResponse
from django.views import View
from http import HTTPStatus


class JobView(View):

    def get(self, request, *args, **kwargs):
        if job := Job.objects.filter(id=kwargs.get('pk')).first():
            job_dict = job.to_dict()
            return JsonResponse(job_dict, status=HTTPStatus.OK)

        return JsonResponse({'message': 'No job found with the given id'}, status=HTTPStatus.NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        if Job.objects.filter(id=(job_id := kwargs.get('pk'))).delete()[0] > 0:
            return JsonResponse({'message': f'Job with id {job_id} deleted'}, status=HTTPStatus.NO_CONTENT)

        return JsonResponse({'message': 'Job not found with the given id'}, status=HTTPStatus.NOT_FOUND)
