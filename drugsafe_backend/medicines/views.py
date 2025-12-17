from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Drug
from .serializers import DrugListSerializer

# Create your views here.
@api_view(['GET'])
def drug_list(request):
    drugs = Drug.objects.all()
    serializer = DrugListSerializer(drugs, many=True)
    return Response(serializer.data)