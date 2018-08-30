from frontpage.models import App
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.shortcuts import render
from frontpage.forms import UploadFileForm
from frontpage.packageinfo import process_package, vuln_analysis_retry


@login_required
def upload_file(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			print repr(request.FILES['file'])
			myApp = process_package(request.FILES['file'], None)
			if isinstance(myApp, App):
				return HttpResponseRedirect('/frontpage/'+str(myApp.id)+'/')
			else:
				context = {"errmsg": myApp}
				return render(request, 'frontpage/error.html', context)
				#process_package(form.fileField)
				#return HttpResponseRedirect('/frontpage/')
	else:
		form = UploadFileForm()
		myDict = {'form':form, 'title': "Subir archivo"}
		myDict.update(myToken)
		return render(request, 'frontpage/upload.html', myDict)