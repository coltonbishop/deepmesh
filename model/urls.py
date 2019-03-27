from django.urls import path

from . import views

urlpatterns = [
	path('', views.upload_pic),
	path('download_pic/<str:imageName>', views.download_pic),
	path('upload_pic/', views.upload_pic),
]