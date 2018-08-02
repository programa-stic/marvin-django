def search_googleplay(request):
	api = GooglePlay().auth()
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