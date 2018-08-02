def apk(request, app_id):
	myApp = get_object_or_404 (App, pk=app_id)
	#TODO: Cambiar por uno que te baje el APK
	filepath = apk_storage.get_filepath(myApp.package_name, myApp.md5)
	filesize = getsize(filepath)
	wrapper = FileWrapper(file(filepath))
	response = HttpResponse(wrapper, content_type = "application/vnd.android.package-archive")
	response ['Content-Disposition'] = 'attachment; filename="'+myApp.package_name+'.apk"'
	response ['Content-Length'] = filesize
	return response
