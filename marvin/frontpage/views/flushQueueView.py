from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from frontpage.queue_handler import flush_queue


def flush(request):
	flush_queue()
	return HttpResponseRedirect('/frontpage/')
