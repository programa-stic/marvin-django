def error(request):
	return render_to_response('frontpage/error.html', RequestContext(request))
