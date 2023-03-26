from cronjobs.models.file import File
from django.http import JsonResponse
from django.views import View
from http import HTTPStatus


class FileView(View):

    def get(self, request, *args, **kwargs):
        if not kwargs.get('pk'):
            return JsonResponse({'message': 'Missing file id'}, status=HTTPStatus.BAD_REQUEST)

        if file := File.objects.filter(id=kwargs.get('pk')).first():
            file_dict = file.to_dict()
            return JsonResponse({'file': file_dict}, status=HTTPStatus.OK)
        return JsonResponse({'message': 'No file found with the given id', 'file': None}, status=HTTPStatus.OK)

    def delete(self, request, *args, **kwargs):
        if File.objects.filter(id=(file_id := kwargs.get('pk'))).delete()[0] > 0:
            return JsonResponse({'message': f'File with id {file_id} deleted'}, status=HTTPStatus.NO_CONTENT)

        return JsonResponse({'message': 'No file found with the given id'}, status=HTTPStatus.NOT_FOUND)
