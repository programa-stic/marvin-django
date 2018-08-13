from django.shortcuts import render, get_object_or_404
from frontpage.models import App

import frontpage.settings
import frontpage.apk_storage
from frontpage.constants import *


def app(request, app_id):
	myApp = get_object_or_404 (App, pk=app_id)
	return render(request, 'frontpage/app.html', {'app':myApp, 'severities':SEVERITY_PRIORITIES})
