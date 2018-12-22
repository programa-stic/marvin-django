from frontpage.models import App
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.shortcuts import render
from frontpage.forms import UploadFileForm
from frontpage.packageinfo import process_package, vuln_analysis_retry, store_apk
from frontpage.queue_handler import queue_for_androlyze
from django.http import HttpResponse, HttpResponseRedirect
from gpApi import googleplay


@login_required
def upload_file(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			print repr(request.FILES['file'])
			queue_for_androlyze(request.FILES['file'])
			return HttpResponseRedirect('/frontpage/')
	else:
		form = UploadFileForm()
		myDict = {'form':form, 'title': "Subir archivo"}
		myDict.update(myToken)
		return render(request, 'frontpage/upload.html', myDict)