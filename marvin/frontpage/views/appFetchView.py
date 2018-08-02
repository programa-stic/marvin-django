def app_fetch(request, pk):
	myToken = csrf(request)
	api = GooglePlay().auth()
	myFile = tempfile.NamedTemporaryFile()
	success = api.download(pk, myFile.name)
	if success:
		details = api.details(pk)
		myApp = process_package(myFile, details)
		return HttpResponseRedirect('/frontpage/')
		# if isinstance(myApp, App):
		# 	return HttpResponseRedirect('/frontpage/'+str(myApp.id)+'/')
		# else:
		# 	context = {"errmsg": myApp}
		# 	return render_to_response('frontpage/error.html', RequestContext(request, context))
	else:
		return HttpResponseRedirect('/frontpage/error/')
