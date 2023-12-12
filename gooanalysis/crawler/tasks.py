from celery import shared_task

@shared_task
def hello2():
    print("Helloooooooooooooooooooooooooooooooooooo")


