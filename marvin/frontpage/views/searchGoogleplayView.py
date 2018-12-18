from frontpage.settings import gp_server, gp_authenticated
from gpApi import utils
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render
from frontpage.forms import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

appsFound = []
appsRetrieved = False

def dirtybastard(numDownloadsString):
	return int(re.search(r'\d+', numDownloadsString.replace(',', '')).group())+10*len(numDownloadsString)

def search_googleplay(request):
	myToken = csrf(request)
	global appsRetrieved
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid() and gp_authenticated:
			searchterms = request.POST['terms']
			if not appsRetrieved:				
				global appsFound
				appsFound = gp_server.search(searchterms, 15, None)
				appsRetrieved = True
				appsFound.sort(key=lambda app: dirtybastard(app['numDownloads']), reverse=True)
			paginator = Paginator(appsFound, 1000)
			page = request.GET.get('page')
			try:
				last_packages = paginator.page(page)
			except PageNotAnInteger:
				last_packages = paginator.page(1)
			except EmptyPage:
				last_packages = paginator.page(paginator.num_pages)
			context = {'packages':last_packages, 'terms':searchterms}
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