from django.db import transaction 
from .models import Applications




@transaction.atomic
def create_app(*, name:str , app_id: str , category: str ) -> Applications:
    application = Applications.objects.create( name=name  , app_id = app_id , category = category )
    return application

@transaction.atomic
def delete_app(*,app_id:str):
    Applications.objects.get(app_id=app_id).delete()

@transaction.atomic
def update_app(*,app_id:str, category:str , name:str ) -> Applications:
    app = Applications.objects.get(app_id=app_id)
    app.category=category
    app.name=name
    app.save()
    return app

