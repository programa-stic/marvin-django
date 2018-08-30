from gpApi import googleplay
from django.shortcuts import render
from frontpage.models import App
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
import tempfile
import logging

def app_fetch(request, pk):
	myToken = csrf(request)
	server = googleplay.GooglePlayAPI('es_AR', 'America/Buenos_Aires')
	server.login('gpagent001.fsadosky@gmail.com', 'grok984sanfason', None, None)
	myFile = tempfile.NamedTemporaryFile()
	logging.info( "Attempting to download \n" + pk)
	fl = server.download(pk)
	with open(docid + '.apk', 'wb') as apk_file:
		for chunk in fl.get('file').get('data'):
			apk_file.write(chunk)
	if success:
		logging.info( "Download succesfull\n")
		details = server.details(pk)
		myApp = process_package(myFile, details)
		return HttpResponseRedirect('/frontpage/')
	else:
		return HttpResponseRedirect('/frontpage/error/')

def app_fetch_queued(request, pk):
	myToken = csrf(request)
	details = api.details(pk)
	queue_for_dl(pk, details)
	return HttpResponseRedirect('/frontpage/')