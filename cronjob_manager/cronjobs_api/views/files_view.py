from cronjobs.models.file import File
from django.http import JsonResponse
from django.views import View
from http import HTTPStatus


class FilesView(View):

    def get(self, request, *args, **kwargs):
        if files := File.objects.all():
            files_dict_list = [file.to_dict() for file in files]
            return JsonResponse(files_dict_list, status=HTTPStatus.OK, safe=False)

        return JsonResponse({'message': 'No file found'}, status=HTTPStatus.NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        delete_files_response = File.objects.all().delete()
        deleted_amount = delete_files_response[0]
        return JsonResponse({'message': f'{deleted_amount} file(s) deleted'}, status=HTTPStatus.OK)

