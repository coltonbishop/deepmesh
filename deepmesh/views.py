from django.http import HttpResponse
from django.template import loader
from django import forms
from django.shortcuts import get_object_or_404, render

def landing(request):
	context = {
	}
	return render(request, 'model/holly.html', context)