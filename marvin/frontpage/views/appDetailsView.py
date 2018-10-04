from gpApi import googleplay
from django.shortcuts import render
from frontpage.models import App

def app_details(request, pk):
	server = googleplay.GooglePlayAPI('es_AR', 'America/Buenos_Aires')
	server.login('gpagent001.fsadosky@gmail.com', 'grok984sanfason', None, None)
	details = server.details(pk)
	import pdb; pdb.set_trace()
	package_name = details['docId']
	version = details['versionString']
	present = App.objects.filter(package_name=package_name, version=version)
	if len(present)>0:
		inBase = True
		context = {'details':details, 'present': inBase, 'app':present[0]}
	else:
		inBase = False
		context = {'details':details, 'present': inBase}
	return render(request, 'frontpage/app_metadata.html', context)
