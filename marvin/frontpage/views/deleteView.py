from django.contrib.auth.decorators import login_required
from frontpage.models import App
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


@login_required
def delete(request, app_id):
	last_packages = App.objects.all()
	myApp = get_object_or_404(App, pk=app_id)
	try:
		borrar_repo(myApp.package_name)
	except Exception as foo:
		print repr(foo)
	myApp.delete()
	return HttpResponseRedirect('/frontpage/')
#	return render(request, 'frontpage/index.html', {'last_packages': last_packages})