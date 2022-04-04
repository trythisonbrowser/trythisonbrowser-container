from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import subprocess

from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import MyFileSerializer


# registry url
BASE_URL = 'http://127.0.0.1:5000/'

# /images
@api_view(['GET', 'POST'])
def getImages(request):
    # http://localhost:5000/v2/_catalog
    response = requests.get(BASE_URL + 'v2/_catalog')
    if str(response.status_code) == '404':
        return Response(status=status.HTTP_404_NOT_FOUND)
    response_json = response.json()
    return Response(response_json)

# search with image name, response tag
# /images/search/<str:tag>
@api_view(['GET', 'POST'])
def searchImages(request, pk):
    # http://localhost:5000/v2/centos/tags/list
    response = requests.get(BASE_URL + 'v2/' + pk + '/tags/list')
    if str(response.status_code) == '404':
        return Response(status=status.HTTP_404_NOT_FOUND)
    response_json = response.json()
    return Response(response_json)

# build and push Dockerfile to registry from file
# /upload {file}
class MyFileView(APIView):
    # MultiPartParser AND FormParser
    # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
    # "You will typically want to use both FormParser and MultiPartParser together in order to fully support HTML form data."
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = MyFileSerializer(data=request.data)
        # read & save Dockerfile 
        # 파일 이름
        if file_serializer.is_valid():
            file_serializer.save()

            # build Docker image from file
            rc = subprocess.call("docker build ../media/Dockerfile", shell=True)

            # change tag and push to registry
            rc = subprocess.call("echo ''", shell=True)

            # remove Dockerfile from media
            rc = subprocess.call("echo ''", shell=True)

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