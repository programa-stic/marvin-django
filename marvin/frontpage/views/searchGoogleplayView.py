from frontpage.settings import gp_server, gp_authenticated
from gpApi import utils
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render
from frontpage.forms import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

def dirtybastard(numDownloadsString):
	ret = 0
	if numDownloadsString:
		ret = int(re.search(r'\d+', numDownloadsString.replace(',', '')).group())+10*len(numDownloadsString)
	return ret

def search_googleplay(request):
	myToken = csrf(request)
	global appsRetrieved
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid() and gp_authenticated:
			searchterms = request.POST['terms']
			appsFound = gp_server.search(searchterms, 15, None)
			appsFound.sort(key=lambda app: dirtybastard(app['numDownloads']), reverse=True)
			context = {'packages':appsFound}
			return render(request, 'frontpage/gpresults.html', context)
		else:
			reason = {}
			if not gp_authenticated:
				reason = {'errmsg':'No se pudo hacer login a Google Play'}
			return render(request, 'frontpage/error.html', reason)
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, 'title':"Buscar en Google Play"}
		myDict.update(myToken)
		appsRetrieved = False
		return render(request, 'frontpage/search_source.html/',myDict)