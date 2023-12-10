from django.db import transaction 
from .models import Applications




@transaction.atomic
def create_app(*, name:str , app_id: str , category: str ) -> Applications:
    application = Applications.objects.create( name=name  , app_id = app_id , category = category )
    return application
