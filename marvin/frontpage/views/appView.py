from django.shortcuts import render, get_object_or_404
from frontpage.models import App

import frontpage.settings
import frontpage.apk_storage
import frontpage.constants


def app(request, app_id):
	myApp = get_object_or_404 (App, pk=app_id)
	return render(request, 'frontpage/app.html', {'app':myApp, 'severities':constants.SEVERITY_PRIORITIES})
