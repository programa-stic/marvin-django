from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from frontpage.models import App
from frontpage.packageinfo import *


def vuln_check(request, pk):
	myApp = get_object_or_404 (App, pk=pk)
	vuln_analysis_retry(myApp)
	return HttpResponseRedirect('/frontpage/'+pk+'/')