def list_sourcefiles(request, pk):
	#allObjs = App.objects.count()
	myApp = get_object_or_404 (App, pk=pk)
	sanitized_package_name = myApp.package_name.replace(".",'-').lower()
	gitlab_url = settings.gitlab_url+'/marvin/'+sanitized_package_name+'/tree/'+myApp.version
	return HttpResponseRedirect(gitlab_url)