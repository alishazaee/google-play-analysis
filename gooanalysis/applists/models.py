from django.db import models
from gooanalysis.common.models import BaseModel
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class Applications(BaseModel):
    name=models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255 , unique=True)
    
    def __str__(self) -> str:
        return self.name
    