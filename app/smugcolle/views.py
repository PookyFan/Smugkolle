# -*- coding: UTF-8 -*-
import random
import string
import urllib2
from os import listdir, remove
from os.path import isfile, join
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from PIL import Image
from forms import LoginForm, ChangePasswordForm
from models import UploadedImage

def index(request):
	context = {'smug': settings.MEDIA_URL + random.choice(get_smug_collection())}
	return HttpResponse(loader.get_template('index.html').render(context, request))

def log_in(request):
	if request.POST:
		login_form = LoginForm(request.POST)
		if not login_form.errors:
			login(request, login_form.user)
			return redirect(manage_smugs)
	elif request.user.is_anonymous(): login_form = LoginForm()
	else: return redirect(manage_smugs)
	template = loader.get_template('form.html')
	context = {'form': login_form, 'action': reverse('login')}
	return HttpResponse(template.render(context, request))

def log_out(request):
	logout(request)
	return redirect(index)

@login_required(login_url='/login/')
def change_password(request):
	message = None
	if request.POST:
		change_form = ChangePasswordForm(request.user, request.POST)
		if not change_form.errors:
			change_form.save()
			message = "Hasło zmienione."
			change_form = ChangePasswordForm(request.user)
	else: change_form = ChangePasswordForm(request.user)
	template = loader.get_template('form.html')
	context = {'form': change_form, 'action': reverse('change_password'), 'message': message}
	return HttpResponse(template.render(context, request))

def get_random_smug(request):
	smugs = get_smug_collection()
	data = {'url': settings.MEDIA_URL + random.choice(smugs)}
	return JsonResponse(data)

@login_required(login_url='/login/')
def manage_smugs(request):
	template = loader.get_template('manage_images.html')
	context = {'images': UploadedImage.objects.all()}
	return HttpResponse(template.render(context, request))

@require_http_methods(['POST'])
@api_view(['POST'])
def add_smug(request):
	record = None
	if request.POST:
		url = request.POST.get('url', None)
		source = request.POST.get('source', '')
	else: raise HttpResponseBadRequest()
	if request.user.is_anonymous() or not url:
		raise HttpResponseBadRequest()
	try:
		smugs = get_smug_collection()
		filename = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
		if filename in smugs: filename += '1'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
		content = urllib2.urlopen(req).read()
		filename = filename + url[url.rfind('.'):]
		path = settings.MEDIA_ROOT + '/' + filename
		with open(path, 'wb') as file:
			file.write(content)
		if not check_image(open(path, 'r')):
			remove(path)
			return JsonResponse({'status': 'not an image'})
		record = UploadedImage()
		record.file.name = filename
		record.source = source
		record.save()
		return JsonResponse({'status': 'ok'})
	except:
		if record: record.delete()
		return JsonResponse({'status': 'error'})

@login_required(login_url='/login/')
def add_many_smugs(request):
	if request.FILES:
		smugs = get_smug_collection()
		for file in request.FILES.getlist('myfiles'):
			if not check_image(file): continue
			filename = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
			if filename in smugs: filename += '1'
			file.name = filename + file.name[file.name.rfind('.'):]
			UploadedImage.objects.create(file=file, source=request.user.username)
			smugs.append(filename)
	return redirect(manage_smugs)

@login_required(login_url='/login/')
def delete_smug(request, img_id):
	try: UploadedImage.objects.get(id=img_id).delete()
	except: pass
	return redirect(manage_smugs)

def get_smug_collection():
	return [f for f in listdir(settings.MEDIA_ROOT) if isfile(join(settings.MEDIA_ROOT, f))]

def check_image(file):
	try:
		image= Image.open(file)
		if image.format != 'JPEG' and image.format != 'PNG' and image.format != 'GIF':
			return False
		image.verify()
		return True
	except: return False