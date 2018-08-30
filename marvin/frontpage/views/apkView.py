from os.path import getsize
from django.shortcuts import render, get_object_or_404, render_to_response
from wsgiref.util import FileWrapper
from django.http import HttpResponse

from frontpage.models import App
from frontpage.apk_storage import *

def apk(request, app_id):
	myApp = get_object_or_404 (App, pk=app_id)
	#TODO: Cambiar por uno que te baje el APK
	filepath = get_filepath(myApp.package_name, myApp.md5)
	filesize = getsize(filepath)
	wrapper = FileWrapper(file(filepath))
	response = HttpResponse(wrapper, content_type = "application/vnd.android.package-archive")
	response ['Content-Disposition'] = 'attachment; filename="'+myApp.package_name+'.apk"'
	response ['Content-Length'] = filesize
	return response
