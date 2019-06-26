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

hostname='ionic.cs.princeton.edu'
port=22
username='cmbishop'
password='**Cb12751010**'
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname,port,username,password)

def upload_pic(request):

	template = loader.get_template('model/model.html')
	image = forms.ImageField()
	projectid = id

	context = {
		'image': image,
		}

	if request.method == 'POST':

		objectpath = 'model/objects/computer.obj'
		return serve(request, os.path.basename(objectpath), os.path.dirname(objectpath))

		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			if os.path.exists("model/images/{}".format(form.cleaned_data['image'].name)):
				os.remove("model/images/{}".format(form.cleaned_data['image'].name))
			m = ImageModel(model_pic = form.cleaned_data['image'], name = form.cleaned_data['image'].name, objname=form.cleaned_data['image'].name.replace(".png",".obj"))
			m.save()

			# CHANGE THE NAME HERE AND PASS IN CONTEXT
			imageName = m.name

			image = imageName.replace(".obj",".png")
			filepath = 'model/images/{}'.format(image)

			# The Image to Put and the Object to Get
			
			obj = image.replace(".png",".obj")
			objectpath = 'model/objects/{}'.format(obj)

			# Creates SCP Client and puts image
			scp = SCPClient(ssh.get_transport())
			time.sleep(5)

			scp.put(filepath, remote_path='/n/fs/donatello/Pixel2Mesh/pixel2mesh/image.png')
			print("Image transferred")
			stdin,stdout,stderr=ssh.exec_command('cd /n/fs/donatello/Pixel2Mesh/pixel2mesh; rm image.obj')
			# outlines=stdout.readlines()
			# resp=''.join(outlines)
			# print(resp)

			stdin,stdout,stderr=ssh.exec_command('cd /n/fs/donatello/Pixel2Mesh/pixel2mesh; sbatch ./generate.slurm')
			# outlines=stdout.readlines()
			# resp=''.join(outlines)
			# print(resp)

			context = {
				'objname': obj,
			}

			return render(request, 'model/serve.html', context)

	return HttpResponse(template.render(context,request))

def download_pic(request, imageName):

	return HttpResponse("This shouldn't be used")


def serve_obj(request, objname):

	if request.method == 'POST':
		objectpath = 'model/objects/computer.obj'
		return serve(request, os.path.basename(objectpath), os.path.dirname(objectpath))

		# hostname='ionic.cs.princeton.edu'
		# port=22
		# username='****'
		# password='************'
		# ssh=paramiko.SSHClient()
		# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# ssh.connect(hostname,port,username,password)
		# print("Connection to server established")
		#Creates SCP Client and puts image
		scp = SCPClient(ssh.get_transport())
		objectpath = 'model/objects/{}'.format(objname)

		if os.path.exists(objectpath):
			os.remove(objectpath)

		context = {
			'objname': objname,
		}

		while True:
			try:
				scp.get(remote_path='/n/fs/donatello/Pixel2Mesh/pixel2mesh/image.obj', local_path='{}'.format(objectpath))
				print("Object downloaded")
			except:
				print("SCP GET failed")
				return HttpResponse("Sorry: there is currently no GPU available. Please try again later.")
			else:
				 #the rest of the code
				 break

		return serve(request, os.path.basename(objectpath), os.path.dirname(objectpath))

def index(request):
	return HttpResponse("Hello, world. You're at the model page.")

