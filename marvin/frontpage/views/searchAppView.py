from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render
from frontpage.forms import SearchForm

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
			return render(request, 'frontpage/index2.html', context)
		else:
			return HttpResponseRedirect('frontpage/search_source.html/',myDict)
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, 'title': "Buscar app en Marvin"}
		myDict.update(myToken)
		return render(request, 'frontpage/search_source.html/',myDict)