from django.db import transaction 
from .models import Applications




@transaction.atomic
def create_app(*, name:str) -> Applications:
    application = Applications.objects.create( name=name )
    return application
