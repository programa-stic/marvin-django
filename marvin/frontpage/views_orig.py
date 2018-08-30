# Copyright (c) 2015, Fundacion Dr. Manuel Sadosky
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from os.path import getsize
import tempfile, zipfile
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from frontpage.models import *
# from django.template import RequestContext
from django.views.generic import ListView, DetailView
from django.template.context_processors import csrf
from wsgiref.util import FileWrapper
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .forms import UploadFileForm, SearchForm, CommentForm
from packageinfo import process_package, vuln_analysis_retry
import packagetree as pt
from git_interface import borrar_repo
from queue_handler import queue_for_dl
import constants
import MarvinStaticAnalyzer
import io
import logging

import settings

import apk_storage

#api = GooglePlay().auth()

# Create your views here.


class PermsListView (ListView):
	model = Permission

	# def get_context_data(self, **kwargs):
	# 	context = super(Applist, self).get_context_data(**kwargs)
	# 	user = self.request.user
	# 	context['myuser']= user
	# 	return context

class AppDetailView(DetailView):
	model = App

class VulnDetailView(DetailView):
	model = VulnerabilityResult

@login_required
def vulnDetail(request, pk):
#	if request.method == "GET":
	myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
	myForm = CommentForm()
	context = {'object':myVuln, 'form':myForm}
	return render_to_response('frontpage/vulnerabilityresult_detail.html', RequestContext(request, context))
	# else:
	# 	if request.method == "POST":
	# 		myForm = CommentForm(request.POST)
	# 		myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
	# 		if form.is_valid():
	# 			comment = myForm.cleaned_data['text']
	# 			user = request.user
	# 			new_comment = App_comments(contents = comment,
	# 									   author = request.user,
	# 									   vuln = myVuln,
	# 									   app = myVuln.app)
	# 			new_comment.save()

def addComment(request,pk):
	myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
	if request.method == "POST":
		myForm = CommentForm(request.POST)
		#myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
		if myForm.is_valid():
			comment = myForm.cleaned_data['text']
			user = request.user
			new_comment = App_comments(author = request.user,
									   contents = comment,
									   vuln = myVuln,
									   app = myVuln.app)
			new_comment.save()
		context = {'object':myVuln, 'form':myForm}
		return render_to_response('frontpage/vulnerabilityresult_detail.html', RequestContext(request, context))
	else:
		myForm = CommentForm()
		context = {'object':myVuln, 'form':myForm}
		return render_to_response('frontpage/vulnerabilityresult_detail.html', RequestContext(request, context))

def deleteComment(request,pk):
	myComment = get_object_or_404 (App_comments, pk=pk)
	myVuln = myComment.vuln
	myComment.delete()
	myForm = CommentForm(request.POST)
	context = {'object':myVuln, 'form':myForm}
	return render_to_response('frontpage/vulnerabilityresult_detail.html', RequestContext(request, context))


def appsByPermission(request, pk):
	myPerm = get_object_or_404 (Permission, pk=pk)
	object_list = myPerm.app.all()
	paginator = Paginator(object_list, 10)
	page = request.GET.get('page')
	try:
		packages = paginator.page(page)
	except PageNotAnInteger:
		packages = paginator.page(1)
	except EmptyPage:
		packages = paginator.page(paginator.num_pages)
	context = {'packages': packages, 'perm':myPerm}
	#context.update(csrf(request))
	return render_to_response('frontpage/apps_by_permission.html', RequestContext(request, context))

def appsByPackage(request, pk):
	myPackage = get_object_or_404 (Java_package, pk=pk)
	object_list = myPackage.app.all()
	paginator = Paginator(object_list, 10)
	page = request.GET.get('page')
	try:
		packages = paginator.page(page)
	except PageNotAnInteger:
		packages = paginator.page(1)
	except EmptyPage:
		packages = paginator.page(paginator.num_pages)
	context = {'packages': packages, 'package':myPackage}
	#context.update(csrf(request))
	return render_to_response('frontpage/apps_by_package.html', RequestContext(request, context))

def appsByPackage2(request, pk, package_name):
	#myApp = get_object_or_404 (App, pk=pkApp)
	myPackages = Java_package.objects.filter(package_name__startswith = package_name)
	object_list = []
	for package in myPackages:
		object_list.extend(package.app.all())
	paginator = Paginator(object_list, 10)
	page = request.GET.get('page')
	try:
		packages = paginator.page(page)
	except PageNotAnInteger:
		packages = paginator.page(1)
	except EmptyPage:
		packages = paginator.page(paginator.num_pages)
	context = {'packages': packages, 'package':package_name}
	#context.update(csrf(request))
	return render_to_response('frontpage/apps_by_package.html', RequestContext(request, context))


def vuln_check(request, pk):
	myApp = get_object_or_404 (App, pk=pk)
	vuln_analysis_retry(myApp)
	return HttpResponseRedirect('/frontpage/'+pk+'/')

@login_required
def toggleDynTest(request, pk):
	myVulnResult = get_object_or_404 (VulnerabilityResult,pk=pk)
	print "toggleDynTest: vuln #"+ str(pk)
	print "  name: " + myVulnResult.name
	print "  scheduled: " + str(myVulnResult.scheduledForDT)
	if myVulnResult.scheduledForDT == True:
		myVulnResult.scheduledForDT = False
	else:
		myVulnResult.scheduledForDT = True
	myVulnResult.save()
	#context = {'result':myVulnResult.scheduledForDT}
	response = HttpResponse()
	response['sched'] = myVulnResult.scheduledForDT
	return response


@login_required
def upload_file(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			print repr(request.FILES['file'])
			myFile = tempfile.NamedTemporaryFile()
			contents = request.FILES['file'].read()
			myFile.write(contents)
			myFile.seek(0)
			myApp = process_package(myFile, None)
			#myApp = process_package(request.FILES['file'], None)
			if isinstance(myApp, App):
				return HttpResponseRedirect('/frontpage/'+str(myApp.id)+'/')
			else:
				context = {"errmsg": myApp}
				return render_to_response('frontpage/error.html', RequestContext(request, context))
				#process_package(form.fileField)
				#return HttpResponseRedirect('/frontpage/')
	else:
		form = UploadFileForm()
		myDict = {'form':form, 'title': "Subir archivo", 'user':request.user}
		myDict.update(myToken)
		return render_to_response('frontpage/upload.html', myDict)

def detected_as_malware(request):
	appsFound = App.objects.all().filter(bayesResult = True).order_by("bayesConfidence").reverse()
	context = {'last_packages':appsFound}
	paginator = Paginator(appsFound, 20)
	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'last_packages':last_packages}
	return render_to_response('frontpage/index2.html', RequestContext(request, context))

def author(request, pk):
	appsFound = App.objects.filter(app_metadata__author = pk).order_by("app_name")
	context = {'last_packages':appsFound}
	paginator = Paginator(appsFound, 20)
	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'last_packages':last_packages}
	return render_to_response('frontpage/index2.html', RequestContext(request, context))


def list_vulnerable_apps(request, vuln_name):
	vulnsFound = VulnerabilityResult.objects.filter(name=vuln_name).order_by('-id')
	#context = {'last_packages':appsFound}
	paginator = Paginator(vulnsFound, 20)
	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'packages':last_packages,'vuln':vuln_name}
	return render_to_response('frontpage/apps_by_vuln.html', RequestContext(request, context))


def list_verified_vulns(request):
	vulnsFound = VulnerabilityResult.objects.filter(dynamictestresults__status="SUCCESS").order_by('-dynamictestresults__last_check')
	#context = {'last_packages':appsFound}
	#appsFound = map(lambda vuln:vuln.app, vulnsFound)
	paginator = Paginator(vulnsFound, 20)
	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'vulns':last_packages}
	return render_to_response('frontpage/discovered_vulns.html', RequestContext(request, context))

def list_enabled_vulns(request):
	vulnsFound = VulnerabilityResult.objects.filter(scheduledForDT=True).order_by('-app__uploaded')
	#context = {'last_packages':appsFound}
	#appsFound = map(lambda vuln:vuln.app, vulnsFound)
	paginator = Paginator(vulnsFound, 20)
	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'vulns':last_packages}
	return render_to_response('frontpage/enabled_vulns.html', RequestContext(request, context))



def list_static_vulns(request):
	return list_vulns(request, MarvinStaticAnalyzer.settings.STATIC_VULN_TYPES.keys())

def list_dynamic_vulns(request):
	return list_vulns(request, MarvinStaticAnalyzer.settings.DYNAMIC_VULN_TYPES.keys())	

def list_vulns(request, vuln_list):
	myList = []
	for vt in vuln_list:
		positives = VulnerabilityResult.objects.all().filter(name=vt)
		apps = set(App.objects.filter(vulnerabilityresult__name=vt))
		myList.append({"name":vt, "count":positives.count, "appcount":len(apps)})
		myList.sort(key= lambda vt:vt['appcount'], reverse=True)
	paginator = Paginator(myList,20)
	page = request.GET.get('page')
	try:
		vulns = paginator.page(page)
	except PageNotAnInteger:
		vulns = paginator.page(1)
	except EmptyPage:
		vulns = paginator.page(paginator.num_pages)
	context = {'vulns':vulns}
	return render_to_response('frontpage/static_vulns.html', RequestContext(request, context))

def search_source(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterms = request.POST['terms']
			filesFound = Sourcefile.objects.search.query('match', _all=searchterms)
			newFF = filesFound.params(size=filesFound.count()).execute()
			newFF = filter((lambda x: x!=None), newFF)
			paginator = Paginator(newFF, 20)
			page = request.GET.get('page')
			try:
				newFF2 = paginator.page(page)
				#newFF = filesFound.params(size=20, from_=(page-1)*20).execute()
			except PageNotAnInteger:
				#newFF = filesFound.params(size=20).execute()
				newFF2 = paginator.page(1)			
			except EmptyPage:
				newFF2 = paginator.page[paginator.num_pages]
#			except TypeError: 
#				newFF2 = newFF.params(size=20).execute()
			#newFF2.sort(key=lambda file: file.app.app_name)
			context = {'sourcefiles':newFF2, 'search_result': True, 'terms':searchterms}
			return render_to_response('frontpage/sourcefile_list.html', RequestContext(request, context))
		else:
			return HttpResponseRedirect('/frontpage/search_source/')
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, "title":"Buscar en codigo fuente"}
		myDict.update(myToken)
		return render_to_response('frontpage/search_source.html',myDict)

def search_sourcefile(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterms = request.POST['terms']
			filesFound = Sourcefile.objects.filter(file_name=searchterms)
			newFF = filesFound.params(size=filesFound.count()).execute()
			newFF = filter((lambda x: x!=None), newFF)
			paginator = Paginator(newFF, 20)
			page = request.GET.get('page')
			try:
				newFF2 = paginator.page(page)
				#newFF = filesFound.params(size=20, from_=(page-1)*20).execute()
			except PageNotAnInteger:
				#newFF = filesFound.params(size=20).execute()
				newFF2 = paginator.page(1)			
			except EmptyPage:
				newFF2 = paginator.page[paginator.num_pages]
#			except TypeError: 
#				newFF2 = newFF.params(size=20).execute()
			#newFF2.sort(key=lambda file: file.app.app_name)
			context = {'sourcefiles':newFF2, 'search_result': True, 'terms':searchterms}
			return render_to_response('frontpage/sourcefile_list.html', RequestContext(request, context))
		else:
			return HttpResponseRedirect('/frontpage/search_source/')
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, "title":"Buscar en codigo fuente"}
		myDict.update(myToken)
		return render_to_response('frontpage/search_source.html',myDict)



# Si el nombre de la clase termina en .java, ya sabemos que el codigo esta en Gitlab.
# Si no, buscamos la clase decompilada: si esta persistida, ya sabemos que existe en gitlab.

def show_activity(request, pk, activity_name):
	myApp = App.objects.get(pk=pk)
	myVersion = myApp.version.replace(' ','_')
	if activity_name.endswith('.java'):
		activity_name = activity_name[0:len(activity_name)-5]
		classpath = activity_name.replace('.','/')
		gitname = myApp.package_name.replace('.','-').lower()
		url = settings.gitlab_url+'/marvin/'+gitname+'/tree/'+myVersion+'/'+classpath+'.java'	
		return HttpResponseRedirect(url)	
	else:
		try:
			classpath = activity_name.replace('.','/')
			#mySF = myApp.sourcefile_set.get(file_name=classpath)
			print ("Empiezo a buscar archivos\n")
			filesFound = Sourcefile.objects.search.query('match', _all=classpath)
			print ("Fin busqueda de archivos\n")
			if len(filesFound) > 0:
				gitname = myApp.package_name.replace('.','-').lower()
				url = settings.gitlab_url+'/marvin/'+gitname+'/tree/'+myVersion+'/'+classpath+'.java'	
				return HttpResponseRedirect(url)
			else:
				context = {"errmsg": "La clase "+ activity_name+" no se halla en el repositorio, puede suceder que haya .DEX suplementarios. "+ str(errmsg)}
				return render_to_response('frontpage/error.html', RequestContext(request, context))
		except Exception as errmsg:
			context = {"errmsg": "La clase "+ activity_name+" no se halla en el repositorio, puede suceder que haya .DEX suplementarios. "+ str(errmsg)}
			return render_to_response('frontpage/error.html', RequestContext(request, context))

def show_package_sources(request, pk, package_name):
	myApp = App.objects.get(pk=pk)
	# if package_name.endswith('.java'):
	# 	package_name = package_name[0:len(package_name)-5]
	# 	classpath = activity_name.replace('.','/')
	# 	gitname = myApp.package_name.replace('.','-').lower()
	# 	url = settings.gitlab_url+'/marvin/'+gitname+'/tree/'+myApp.version+'/'+classpath+'.java'	
	# 	return HttpResponseRedirect(url)	
	# else:
	try:
		classpath = package_name.replace('.','/')
		#mySF = myApp.sourcefile_set.get(file_name=classpath)
		gitname = myApp.package_name.replace('.','-').lower()
		myVersion = myApp.version.replace(' ','_')
		url = settings.gitlab_url+'/marvin/'+gitname+'/tree/'+myVersion+'/'+classpath
		return HttpResponseRedirect(url)
	except Exception as errmsg:
		context = {"errmsg": "La clase "+ package_name+" no se halla en el repositorio, puede suceder que haya .DEX suplementarios. "+ str(errmsg)}
		return render_to_response('frontpage/error.html', RequestContext(request, context))

def search_app(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterms = request.POST['terms']
			appsFound = App.objects.search.query('match', _all=searchterms)
			newAF = appsFound.params(size=min(appsFound.count(), 100)).execute()
			newAF.sort(key=lambda app: app.app_name)
			context = {'last_packages':newAF}
			return render_to_response('frontpage/index2.html', RequestContext(request, context))
		else:
			return HttpResponseRedirect('frontpage/search_source.html/',myDict)
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, 'title': "Buscar app en Marvin"}
		myDict.update(myToken)
		return render_to_response('frontpage/search_source.html/',myDict)

def dirtybastard(numDownloadsString):
	return int(int(re.search(r'\d+', numDownloadsString).group()))+10*len(numDownloadsString)

def search_googleplay(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterms = request.POST['terms']
			appsFound = api.search(searchterms)
			appsFound.sort(key=lambda app: dirtybastard(app.details.appDetails.numDownloads), reverse=True)
			#appsDict = api.toDict(appsFound)
			#appsFound.sort(key=lambda app: app.details.appDetails.numDownloads)
			paginator = Paginator(appsFound, 20)
			page = request.GET.get('page')
			try:
				last_packages = paginator.page(page)
			except PageNotAnInteger:
				last_packages = paginator.page(1)
			except EmptyPage:
				last_packages = paginator.page(paginator.num_pages)
			context = {'packages':last_packages}
			return render_to_response('frontpage/gpresults.html', RequestContext(request, context))
		else:
			return HttpResponseRedirect('frontpage/search_source.html/',myDict)
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, 'title':"Buscar en Google Play"}
		myDict.update(myToken)
		return render_to_response('frontpage/search_source.html/',myDict)

def app_details(request, pk):
#	api = GooglePlay().auth()
	details = api.details(pk)
	package_name = details.docV2.details.appDetails.packageName
	version = details.docV2.details.appDetails.versionString
	present = App.objects.filter(package_name=package_name, version=version)
	if len(present)>0:
		inBase = True
		context = {'details':details, 'present': inBase, 'app':present[0]}
	else:
		inBase = False
		context = {'details':details, 'present': inBase}
	return render_to_response('frontpage/app_metadata.html', RequestContext(request, context))

def error(request):
	return render_to_response('frontpage/error.html', RequestContext(request))

def app_fetch_queued(request, pk):
	myToken = csrf(request)
	details = api.details(pk)
	queue_for_dl(pk, details)
	return HttpResponseRedirect('/frontpage/')

def app_fetch(request, pk):
	myToken = csrf(request)
#	api = GooglePlay().auth()
	myFile = tempfile.NamedTemporaryFile()
	success = api.download(pk, myFile.name)
	if success:
		details = api.details(pk)
		myApp = process_package(myFile, details)
		return HttpResponseRedirect('/frontpage/')
		# if isinstance(myApp, App):
		# 	return HttpResponseRedirect('/frontpage/'+str(myApp.id)+'/')
		# else:
		# 	context = {"errmsg": myApp}
		# 	return render_to_response('frontpage/error.html', RequestContext(request, context))
	else:
		return HttpResponseRedirect('/frontpage/error/')

# def list_sourcefiles(request, pk):
# 	#allObjs = App.objects.count()
# 	myApp = get_object_or_404 (App, pk=pk)
# 	object_list = myApp.sourcefile_set.all()
# 	paginator = Paginator(object_list, 20)
# 	page = request.GET.get('page')
# 	try:
# 		sourcefiles = paginator.page(page)
# 	except PageNotAnInteger:
# 		sourcefiles = paginator.page(1)
# 	except EmptyPage:
# 		sourcefiles = paginator.page(paginator.num_pages)
# 	context = {'sourcefiles': sourcefiles, 'app':myApp}
# 	return render_to_response('frontpage/sourcefile_list.html', RequestContext(request, context))

def list_sourcefiles(request, pk):
	#allObjs = App.objects.count()
	myApp = get_object_or_404 (App, pk=pk)
	sanitized_package_name = myApp.package_name.replace(".",'-').lower()
	gitlab_url = settings.gitlab_url+'/marvin/'+sanitized_package_name+'/tree/'+myApp.version.replace(' ','_')
	return HttpResponseRedirect(gitlab_url)

def source_file_contents(request,pk):
	mySourceFile = get_object_or_404 (Sourcefile, pk=pk)
	mySourceFile.file_contents = mySourceFile.file_contents.replace("\\n", "\n") 
	context = {'file': mySourceFile}
	return render_to_response('frontpage/sourcefile_contents.html', RequestContext(request, context))	

def index(request):
	#allObjs = App.objects.count()
	object_list = App.objects.all().order_by('-id')
	paginator = Paginator(object_list, 10)
	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'last_packages': last_packages}
	context.update(csrf(request))
	return render_to_response('frontpage/index2.html', RequestContext(request, context))

def app(request, app_id):
	myApp = get_object_or_404 (App, pk=app_id)
	packagetree = pt.getpackagetree(myApp.java_package_set.all())
	justlevel2 = pt.get_level_2(packagetree)
	return render(request, 
		'frontpage/app.html', 
		{'app':myApp, 
		'severities':constants.SEVERITY_PRIORITIES, 
		'ptree':justlevel2}
		)

def apk(request, app_id):
	myApp = get_object_or_404 (App, pk=app_id)
	#TODO: Cambiar por uno que te baje el APK
	filepath = apk_storage.get_filepath(myApp.package_name, myApp.md5)
	filesize = getsize(filepath)
	wrapper = FileWrapper(file(filepath))
	response = HttpResponse(wrapper, content_type = "application/vnd.android.package-archive")
	response ['Content-Disposition'] = 'attachment; filename="'+myApp.package_name+'.apk"'
	response ['Content-Length'] = filesize
	return response

def src(request, app_id):
	myApp = get_object_or_404 (App, pk=app_id)
	mySources = myApp.sourcefile_set.all()
	temp = tempfile.TemporaryFile()
	arch = zipfile.ZipFile(temp, 'w')
	#old *working* code follows
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
	response=HttpResponse(wrapper, content_type = "application/zip")
	response['Content-Disposition'] = 'attachment; filename="'+myApp.package_name+'.zip"'
	response ['Content-Length'] = temp.tell()
	return response	

@login_required
def delete(request, app_id):
	last_packages = App.objects.all()
	myApp = get_object_or_404 (App, pk=app_id)
	try:
		borrar_repo(myApp.package_name)
	except Exception as foo:
		print repr(foo)
	myApp.delete()
	return HttpResponseRedirect('/frontpage/')
#	return render(request, 'frontpage/index.html', {'last_packages': last_packages})

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/frontpage/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Polls account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('frontpage/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/frontpage/')
