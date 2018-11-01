from frontpage.settings import gp_server, gp_authenticated
from django.shortcuts import render
from frontpage.models import App
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
import tempfile
import logging
from frontpage.queue_handler import queue_for_dl

def app_fetch_queued(request, pk):
	if gp_authenticated:
		myToken = csrf(request)
		details = gp_server.details(pk)
		queue_for_dl(pk, details)
		return HttpResponseRedirect('/frontpage/')
	else:
		logging.info("Not logged in googleplay")
		return render(request, 'frontpage/error.html', {})