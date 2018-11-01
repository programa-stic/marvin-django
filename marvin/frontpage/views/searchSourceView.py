from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render
from frontpage.forms import SearchForm
from frontpage.models import Sourcefile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def search_source(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterms = request.POST['terms']
			filesFound = Sourcefile.objects.filter(file_name__icontains=searchterms).order_by('file_name')
			# filesFound = Sourcefile.objects.filter(file_contents__icontains=searchterms).order_by('file_name')
			# newFF = filesFound.params(size=min(filesFound.count(), 100)).execute()
			paginator = Paginator(filesFound, 20)
			page = request.GET.get('page')
			try:
				last_files = paginator.page(page)
			except PageNotAnInteger:
				last_files = paginator.page(1)
			except EmptyPage:
				last_files = paginator.page(paginator.num_pages)
			context = {'sourcefiles':last_files, 'search_result': True}
			return render(request, 'frontpage/sourcefile_list.html', context)
		else:
			return HttpResponseRedirect('frontpage/sourcefile_list.html',{})
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, "title":"Buscar en codigo fuente"}
		myDict.update(myToken)
		return render(request, 'frontpage/search_source.html',myDict)
