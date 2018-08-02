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
	paginator = Paginator(myList,20)
	page = request.GET.get('page')
	try:
		vulns = paginator.page(page)
	except PageNotAnInteger:
		vulns = paginator.page(1)
	except EmptyPage:
		vulns = paginator.page(paginator.num_pages)
	context = {'vulns':vulns}
	# return render_to_response('frontpage/static_vulns.html', RequestContext(request, context))
	return render(request, 'frontpage/static_vulns.html', context)