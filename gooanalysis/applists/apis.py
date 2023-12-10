from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.core.validators import MinLengthValidator
from gooanalysis.users.models import BaseUser , Profile
from gooanalysis.api.mixins import ApiAuthMixin
from .selectors import get_apps
from .services import create_app
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from drf_spectacular.utils import extend_schema
from gooanalysis.api.pagination import  get_paginated_response, LimitOffsetPagination, get_paginated_response_context

from .models import Applications

class AppApi(APIView):
    class InputAppSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        app_id = serializers.CharField(max_length=255)
        category = serializers.CharField(max_length=255)

    class OutputAppSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        app_id = serializers.CharField(max_length=255)
        category = serializers.CharField(max_length=255)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(request=InputAppSerializer, responses=OutputAppSerializer)
    def post(self, request):
        serializer = self.InputAppSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            app = create_app(
                    name=serializer.validated_data.get("name"),
                    app_id=serializer.validated_data.get("app_id"),
                    category=serializer.validated_data.get("category"),
                    )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(self.OutputAppSerializer(app, context={"request":request}).data)


    @extend_schema(responses=OutputAppSerializer)
    def get(self,request):
        try:
            query = get_apps()
          
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutputAppSerializer,
            queryset=query,
            request=request,
            view=self,
        )
    
    


