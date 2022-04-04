from django.contrib import admin
from django.urls import path, include
from rest_framework import routers 
from images.views import *
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('images/', getImages, name="getImages"),
    path('images/search/<str:pk>', searchImages, name="searchImages"),
    path('upload/', MyFileView.as_view(), name='image-upload'),
    path('upload/stdin/<str:pk>', pipeBuild, name='pipe-upload'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)