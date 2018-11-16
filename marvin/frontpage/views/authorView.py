from frontpage.models import App
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404


def author(request, pk):
	appsFound = App.objects.filter(app_metadata__author = pk).order_by("app_name")
	context = {'last_packages':appsFound}
	paginator = Paginator(appsFound, 20)
	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'last_packages':last_packages}
	return render(request, 'frontpage/index2.html', context)