from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
from django.template import loader
from django import forms
from .forms import SearchForm, ImageUploadForm
from django.shortcuts import get_object_or_404, render
from .models import ImageModel
from django.views.static import serve
import os
import paramiko
from scp import SCPClient
import sys
import time

def upload_pic(request):

	template = loader.get_template('model/model.html')
	image = forms.ImageField()
	projectid = id

	context = {
		'image': image,
		}

	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			if os.path.exists("model/images/{}".format(form.cleaned_data['image'].name)):
				os.remove("model/images/{}".format(form.cleaned_data['image'].name))
			m = ImageModel(model_pic = form.cleaned_data['image'], name = form.cleaned_data['image'].name, objname=form.cleaned_data['image'].name.replace(".png",".obj"))
			m.save()

			# CHANGE THE NAME HERE AND PASS IN CONTEXT

			context = {
			'image': m,
			}
			return render(request, 'model/download.html', context)

	return HttpResponse(template.render(context,request))

def download_pic(request, imageName):

	if request.method == 'POST':

		image = imageName.replace(".obj",".png")
		filepath = 'model/images/{}'.format(image)
		print(request)
		hostname='ionic.cs.princeton.edu'
		port=22
		username='cmbishop'
		password='**Cb12751010**'

		# The Image to Put and the Object to Get
		
		obj = image.replace(".png",".obj")
		objectpath = 'model/objects/{}'.format(obj)

		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname,port,username,password)

		# Creates SCP Client and puts image
		scp = SCPClient(ssh.get_transport())

		while True:
		    try:
		        scp.put(filepath, remote_path='/n/fs/donatello/Pixel2Mesh/pixel2mesh/image.png')
		    except:
		         continue
		    else:
		         #the rest of the code
		         break

		stdin,stdout,stderr=ssh.exec_command('cd /n/fs/donatello/Pixel2Mesh/pixel2mesh; rm image.obj')
		outlines=stdout.readlines()
		resp=''.join(outlines)
		print(resp)

		stdin,stdout,stderr=ssh.exec_command('cd /n/fs/donatello/Pixel2Mesh/pixel2mesh; sbatch ./generate.slurm')
		outlines=stdout.readlines()
		resp=''.join(outlines)
		print(resp)

		if os.path.exists(objectpath):
			os.remove(objectpath)

		while True:
		    try:
		        scp.get(remote_path='/n/fs/donatello/Pixel2Mesh/pixel2mesh/image.obj', local_path='{}'.format(objectpath))
		    except:
		         continue
		    else:
		         #the rest of the code
		         break

		return serve(request, os.path.basename(objectpath), os.path.dirname(objectpath))

def index(request):
	return HttpResponse("Hello, world. You're at the model page.")

