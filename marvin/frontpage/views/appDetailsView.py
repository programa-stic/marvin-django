def app_details(request, pk):
	api = GooglePlay().auth()
	details = api.details(pk)
	context = {'details':details}
	return render(request, 'frontpage/app_metadata.html', context)
