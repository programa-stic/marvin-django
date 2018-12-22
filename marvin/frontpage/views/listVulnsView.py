from frontpage.packageinfo import process_package, vuln_analysis_retry
import MarvinStaticAnalyzer
from frontpage.models import App, VulnerabilityResult
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def list_static_vulns(request):
	return list_vulns(request, MarvinStaticAnalyzer.settings.STATIC_VULN_TYPES.keys())

def list_dynamic_vulns(request):
	return list_vulns(request, MarvinStaticAnalyzer.settings.DYNAMIC_VULN_TYPES.keys())	

def list_vulns(request, vuln_list):
	myList = []
	for vt in vuln_list:
		positives = VulnerabilityResult.objects.all().filter(name=vt)
		apps = set(App.objects.filter(vulnerabilityresult__name=vt))
		myList.append({"name":vt, "count":positives.count, "appcount":len(apps)})
		myList.sort(key= lambda vt:vt['appcount'], reverse=True)
	context = {'vulns':myList}
	return render(request, 'frontpage/static_vulns.html', context)

def list_verified_vulns(request):
	vulnsFound = VulnerabilityResult.objects.filter(dynamictestresults__status="SUCCESS").order_by('-dynamictestresults__last_check')
	context = {'vulns':vulnsFound}
	return render(request, 'frontpage/discovered_vulns.html', context)

def list_enabled_vulns(request):
	vulnsFound = VulnerabilityResult.objects.filter(scheduledForDT=True).order_by('-app__uploaded')
	context = {'vulns':vulnsFound}
	return render(request, 'frontpage/enabled_vulns.html', context)
