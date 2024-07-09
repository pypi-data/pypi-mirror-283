import os
import sys
import uuid

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from django.db import transaction

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CURRENT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

#  celery -A server worker --loglevel=info -P gevent --concurrency 1 -E
app = Celery("server")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks()

# workers with active websocket connection are in the separate queue
app.conf.task_routes = {
    "apps.ws.tasks.task_start_websocket_worker": {"queue": "ws"}
}


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        # add scale down task only in cloud env
        if os.environ.get("MERCURY_CLOUD", "0") == "1":
            sender.add_periodic_task(
                    crontab(
                        minute="*",
                        hour="*",
                        day_of_month="*",
                        month_of_year="*",
                        day_of_week="*",
                    ),
                    scale_down_task.s(),
                )

        # from apps.notebooks.models import Notebook

        # # get all notebooks with not empty schedule
        # notebooks = Notebook.objects.exclude(schedule__isnull=True).exclude(
        #     schedule__exact=""
        # )

        # for n in notebooks:
        #     schedule_str = n.schedule
        #     schedule_arr = schedule_str.split(" ")
        #     minute, hour, day_of_month, month, day_of_week = (
        #         schedule_arr[0],
        #         schedule_arr[1],
        #         schedule_arr[2],
        #         schedule_arr[3],
        #         schedule_arr[4],
        #     )
        #     sender.add_periodic_task(
        #         crontab(
        #             minute=minute,
        #             hour=hour,
        #             day_of_month=day_of_month,
        #             month_of_year=month,
        #             day_of_week=day_of_week,
        #         ),
        #         execute_notebook.s(n.id),
        #     )
    except Exception as e:
        print("Problem with periodic tasks setup")
        print(str(e))


@app.task
def scale_down_task():
    import django
    django.setup()
    from apps.workers.utils import scale_down
    scale_down()

@app.task
def execute_notebook(notebook_id):
    import django

    django.setup()
    from apps.notebooks.models import Notebook
    from apps.tasks.models import Task
    from apps.tasks.tasks import task_execute

    with transaction.atomic():
        task = Task(
            session_id=f"scheduled-{uuid.uuid4().hex[:8]}",
            state="CREATED",
            notebook=Notebook.objects.get(pk=notebook_id),
            params="{}",
        )
        task.save()
        job_params = {"db_id": task.id}
        transaction.on_commit(lambda: task_execute.delay(job_params))
