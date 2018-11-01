from frontpage.settings import gp_server, gp_authenticated
from django.shortcuts import render
from frontpage.models import App
import logging

def app_details(request, pk):
	if gp_authenticated:
		details = gp_server.details(pk)
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
	else:
		logging.info("Not sign in to google play")
		return render(request, 'frontpage/error.html', {})