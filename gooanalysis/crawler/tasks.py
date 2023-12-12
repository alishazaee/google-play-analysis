from celery import shared_task
from gooanalysis.applists.selectors import get_application_ids
from .AppRepository import APP_INTO_DB
@shared_task
def hello2():
    print("Helloooooooooooooooooooooooooooooooooooo")
