from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse
from frontpage.models import App
from wsgiref.util import FileWrapper
import tempfile, zipfile

def src(request, app_id):
	myApp = get_object_or_404 (App, pk=app_id)
	mySources = myApp.sourcefile_set.all()
	temp = tempfile.NamedTemporaryFile(delete=False)
	arch = zipfile.ZipFile(temp, 'w')
	#old *working* code ffollows
	#myFileObj = io.BytesIO()
	#myZipFile = zipfile.ZipFile(myFileObj, 'w')
	for item in mySources:
		fname = item.file_name
		actualname = fname + '.java'
		src = (item.file_contents).encode('ascii','replace').replace("\\n", "\n")
		arch.writestr(actualname, src)
	arch.close()
	temp.seek(0)
	wrapper = FileWrapper(temp)
	response = HttpResponse(wrapper, content_type = "application/zip")
	# response ['Content-Length'] = temp.tell()
	response['Content-Disposition'] = 'attachment; filename="'+myApp.package_name+'.zip"'
	return response