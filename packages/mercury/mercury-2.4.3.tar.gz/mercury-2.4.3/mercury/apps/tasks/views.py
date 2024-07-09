import json
import os
import shutil
import uuid

from celery.result import AsyncResult
from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notebooks.models import Notebook
from apps.notebooks.views import notebooks_queryset
from apps.storage.models import WorkerFile
from apps.storage.s3utils import S3
from apps.storage.storage import StorageManager
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer
from apps.tasks.tasks import task_execute
from apps.tasks.tasks_export import export_to_pdf

from apps.workers.models import Worker
from apps.ws.tasks import task_start_websocket_worker

from apps.tasks.models import RestAPITask

from rest_framework import permissions
from apps.accounts.views.permissions import HasEditRights, apiKeyToUser


class TaskCreateView(CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        notebook = get_object_or_404(
            notebooks_queryset(self.request), pk=self.kwargs["notebook_id"]
        )
        try:
            with transaction.atomic():
                instance = serializer.save(
                    state="CREATED",
                    notebook=notebook,
                )
                job_params = {"db_id": instance.id}
                transaction.on_commit(lambda: task_execute.delay(job_params))
        except Exception as e:
            raise APIException(str(e))


class GetLastTaskView(RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_object(self):
        notebook = get_object_or_404(
            notebooks_queryset(self.request), pk=self.kwargs["notebook_id"]
        )
        try:
            if notebook.schedule is None or notebook.schedule == "":
                return Task.objects.filter(
                    notebook_id=self.kwargs["notebook_id"],
                    session_id=self.kwargs["session_id"],
                ).latest("id")
            else:
                return Task.objects.filter(
                    notebook_id=self.kwargs["notebook_id"]
                ).latest("id")

        except Task.DoesNotExist:
            raise Http404()


class ListOutputFilesView(APIView):
    def get(self, request, session_id, task_id, format=None):
        files_urls = []
        try:
            output_dir = os.path.join(
                settings.MEDIA_ROOT, session_id, f"output_{task_id}"
            )
            for f in os.listdir(output_dir):
                if os.path.isfile(os.path.join(output_dir, f)):
                    files_urls += [
                        f"{settings.MEDIA_URL}/{session_id}/output_{task_id}/{f}"
                    ]
        except Exception as e:
            print(
                f"Trying to list files for session_id {session_id} and task_id {task_id}"
            )
            print("Exception occured", str(e))
        return Response(files_urls)


class ListWorkerOutputFilesView(APIView):
    def get(self, request, session_id, worker_id, notebook_id, format=None):
        files_urls = []
        sm = StorageManager(session_id, worker_id, notebook_id)
        if settings.STORAGE == settings.STORAGE_MEDIA:
            files_urls = sm.list_worker_files_urls()
        elif settings.STORAGE == settings.STORAGE_S3:
            output_dir = sm.worker_output_dir()
            files = WorkerFile.objects.filter(
                created_by__id=worker_id, output_dir=output_dir
            )
            s3 = S3()
            for f in files:
                files_urls += [s3.get_presigned_url(f.filepath, "get_object")]

        return Response(files_urls)


class ClearTasksView(APIView):
    def post(self, request, notebook_id, session_id, format=None):
        try:
            tasks = Task.objects.filter(notebook_id=notebook_id, session_id=session_id)

            for task in tasks:
                output_file = os.path.join(
                    settings.MEDIA_ROOT, session_id, f"output_{task.id}.html"
                )
                output_dir = os.path.join(
                    settings.MEDIA_ROOT, session_id, f"output_{task.id}"
                )

                try:
                    if os.path.isfile(output_file):
                        os.remove(output_file)
                    if os.path.isdir(output_dir):
                        shutil.rmtree(output_dir)
                except Exception as e:
                    print(f"Trying to delete {output_file} and {output_dir}")
                    print(str(e))

            tasks.delete()

        except Exception as e:
            print(
                f"Trying to clear tasks for notebook_id {notebook_id} and session_id {session_id}"
            )
            print("Exception occured", str(e))

        return Response(status=status.HTTP_204_NO_CONTENT)



class ExportPDF(APIView):
    def post(self, request):
        try:
            # check if user can access the notebook
            notebook = notebooks_queryset(request, request.data.get("site_id")).get(
                pk=request.data["notebook_id"]
            )
        except Notebook.DoesNotExist:
            raise Http404()
        try:
            celery_job = export_to_pdf.delay(request.data)
            print(celery_job.id)
            return Response({"job_id": celery_job.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise APIException(str(e))


class GetPDFAddress(APIView):
    def get(self, request, job_id):
        res = AsyncResult(job_id)
        fileUrl, title, error = "", "", ""
        if res.ready():
            if res.state == "FAILURE":
                error = str(res.result)
            elif res.state == "SUCCESS":
                fileUrl, title = res.result
        return Response(
            {"ready": res.ready(), "url": fileUrl, "title": title, "error": error}
        )


class ExecutionHistoryView(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        # check if user has access to the notebook
        notebook = get_object_or_404(
            notebooks_queryset(self.request), pk=self.kwargs["notebook_id"]
        )

        return Task.objects.filter(
            notebook_id=notebook.id,
            session_id=self.kwargs["session_id"],
        )


class CreateRestAPITask(APIView):
    def post(self, request, site_id, notebook_slug):
        apiKeyToUser(request)
        try:
            notebook = (
                notebooks_queryset(request, site_id).filter(slug=notebook_slug).latest("id")
            )
        except Notebook.DoesNotExist:
            raise Http404()
        try:
            with transaction.atomic():
                task = RestAPITask(
                    session_id=uuid.uuid4().hex,
                    state="CREATED",
                    notebook=notebook,
                    params=json.dumps(request.data),
                )
                if not request.user.is_anonymous:
                    task.created_by = request.user
                task.save()

                worker = Worker(
                    session_id=task.session_id,
                    notebook_id=notebook.id,
                    state="Queued",
                )
                if not request.user.is_anonymous:
                    worker.run_by = request.user
                worker.save()
                
                server_address = request.build_absolute_uri('/')
                job_params = {
                    "notebook_id": notebook.id,
                    "session_id": task.session_id,
                    "worker_id": worker.id,
                    #
                    # ugly hack for docker deployment
                    #
                    "server_url": server_address
                    if "0.0.0.0" not in server_address
                    else server_address + ":9000",
                }
                
                transaction.on_commit(lambda: task_start_websocket_worker.delay(job_params))

            return Response({"task_id": task.session_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise APIException(str(e))


class GetRestAPITask(APIView):
    def get(self, requset, task_id):
        try:
            task_id = task_id.replace("/", "")
            tasks = RestAPITask.objects.filter(
                session_id=task_id
            )
            if not tasks:
                raise Http404()
            task = tasks.latest("id")
            
            if task.state == "DONE":
                result = {"state": "done", "message": "Request successfully computed", "result": {}}
                if task.response != "":
                    result["result"] = json.loads(task.response)
                #if task.nb_html_path != "":
                #    result["notebook_html"] = task.nb_html_path

                return Response(result, status=status.HTTP_200_OK)
            if task.state == "ERROR":
                return Response(
                    {"state": "error", "message": f"Error when processing task, {task.response}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response({"state": "running", "message": "Still processing your request, please retry in 3 seconds"}, status=status.HTTP_202_ACCEPTED)
        except RestAPITask.DoesNotExist:
            raise Http404()

class ListRestAPITasks(APIView):
    
    permission_classes = [permissions.IsAuthenticated, HasEditRights]
    
    def get(self, requset, site_id, notebook_id):
        try:
            
            tasks = RestAPITask.objects.filter(notebook_id=notebook_id)
            
            tasks_data = []
            for t in tasks:
                task = {
                    "id": t.id,
                    "state": t.state,
                    "params": t.params,
                    "response": t.response,
                    "session_id": t.session_id,
                    "created_at": t.created_at,
                    "updated_at": t.updated_at
                }
                tasks_data += [task]
            return Response(tasks_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            raise Http404()