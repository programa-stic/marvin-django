from frontpage.models import App
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.context_processors import csrf
from django.shortcuts import render

def index(request):
	#allObjs = App.objects.count()
	object_list = App.objects.all().order_by('-id')
	paginator = Paginator(object_list, 10)

	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'last_packages': last_packages}
	context.update(csrf(request))
	return render(request, 'frontpage/index2.html', context)