from gpApi import googleplay
from django.shortcuts import render
from frontpage.models import App
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
import tempfile
import logging
from frontpage.queue_handler import queue_for_dl

def app_fetch_queued(request, pk):
	myToken = csrf(request)
	server = googleplay.GooglePlayAPI('es_AR', 'America/Buenos_Aires')
	server.login('gpagent001.fsadosky@gmail.com', 'grok984sanfason', None, None)
	details = server.details(pk)
	queue_for_dl(pk, details)
	return HttpResponseRedirect('/frontpage/')