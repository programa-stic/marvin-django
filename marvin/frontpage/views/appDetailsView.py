def app_details(request, pk):
	api = GooglePlay().auth()
	details = api.details(pk)
	context = {'details':details}
	return render_to_response('frontpage/app_metadata.html', RequestContext(request, context))
