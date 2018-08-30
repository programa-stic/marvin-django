from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render
from frontpage.forms import SearchForm
from frontpage.models import Sourcefile

def search_source(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterms = request.POST['terms']
			filesFound = Sourcefile.objects.search.query('match', _all=searchterms)
			newFF = filesFound.params(size=min(filesFound.count(), 100)).execute()
			newFF.sort(key=lambda file: file.app.app_name)
			context = {'sourcefiles':newFF, 'search_result': True}
			return render(request, 'frontpage/sourcefile_list.html', context)
		else:
			return HttpResponseRedirect('frontpage/search_source.html',myDict)
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, "title":"Buscar en codigo fuente"}
		myDict.update(myToken)
		return render(request, 'frontpage/search_source.html',myDict)
