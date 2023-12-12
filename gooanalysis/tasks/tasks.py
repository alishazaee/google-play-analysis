from celery import shared_task
from gooanalysis.applists.selectors import get_application_ids

from gooanalysis.crawler.AppRepository import APP_INTO_DB


@shared_task
def test1():
    print("HI")



@shared_task
def crawl_and_save_into_db():
    app_ids = get_application_ids()
    for id in app_ids:
        APP_INTO_DB(app_id=id)