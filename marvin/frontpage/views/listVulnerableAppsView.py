from frontpage.models import App, VulnerabilityResult, Permission, Sourcefile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def list_vulnerable_apps(request, vuln_name):
	appsFound = set(App.objects.filter(vulnerabilityresult__name=vuln_name))
	appsFound = list(appsFound)
	#context = {'last_packages':appsFound}
	paginator = Paginator(appsFound, 20)
	page = request.GET.get('page')
	try:
		last_packages = paginator.page(page)
	except PageNotAnInteger:
		last_packages = paginator.page(1)
	except EmptyPage:
		last_packages = paginator.page(paginator.num_pages)
	context = {'packages':last_packages,'vuln':vuln_name}
	return render(request, 'frontpage/apps_by_vuln.html',context)