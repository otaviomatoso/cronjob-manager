from cronjobs.models.job import Job
from django.http import JsonResponse
from django.views import View
from http import HTTPStatus


class JobsView(View):

    def get(self, request, *args, **kwargs):
        if jobs := Job.objects.all():
            jobs_dict_list = [job.to_dict() for job in jobs]
            return JsonResponse(jobs_dict_list, status=HTTPStatus.OK, safe=False)

        return JsonResponse({"message": "No job found"}, status=HTTPStatus.NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        delete_jobs_response = Job.objects.all().delete()
        deleted_amount = delete_jobs_response[0]
        if deleted_amount > 0:
            return JsonResponse({'message': f'{deleted_amount} job(s) deleted'}, status=HTTPStatus.NO_CONTENT)

        return JsonResponse({'message': 'There are no jobs to delete.'}, status=HTTPStatus.NOT_FOUND)
