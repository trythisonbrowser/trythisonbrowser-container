from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import requests
import subprocess

from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import MyFileSerializer

# registry url
BASE_URL = 'http://127.0.0.1:5000/'

# /images
# http://localhost:5000/v2/_catalog
@api_view(['GET', 'POST'])
def getImages(request):
    response = requests.get(BASE_URL + 'v2/_catalog')
    if str(response.status_code) == '404':
        return Response(status=status.HTTP_404_NOT_FOUND)
    response_json = response.json()
    return Response(response_json)

# search with image name, response tag
# http://localhost:5000/v2/centos/tags/list
# /images/search/<str:tag>
@api_view(['GET', 'POST'])
def searchImages(request, pk):
    response = requests.get(BASE_URL + 'v2/' + pk + '/tags/list')
    if str(response.status_code) == '404':
        return Response(status=status.HTTP_404_NOT_FOUND)
    response_json = response.json()
    return Response(response_json)

# build and push Dockerfile to registry from file
# /upload {file}
class MyFileView(APIView):
    # MultiPartParser AND FormParser
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = MyFileSerializer(data=request.data)
        
        # read & save Dockerfile 
        if file_serializer.is_valid():
            file_serializer.save()

            # build Docker image from file

            # change tag and push to registry

            # remove Dockerfile from media

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#pipe-dockerfile-through-stdin
# build and push Dockerfile to registry from stdin
# /upload/stream {stdin}
@api_view(['GET', 'POST'])
def pipeBuild(request, pk):
    response = requests.get(BASE_URL + 'v2/' + pk + '/tags/list')
    if str(response.status_code) == '404':
        return Response(status=status.HTTP_404_NOT_FOUND)
    response_json = response.json()

    buildStream = 'echo -e' + pk + "| docker build -"
    rc = subprocess.call(pk, shell=True)
    return Response(status=status.HTTP_201_CREATED)