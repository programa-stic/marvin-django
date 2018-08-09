def show_package_sources(request, pk, package_name):
	myApp = App.objects.get(pk=pk)
	# if package_name.endswith('.java'):
	# 	package_name = package_name[0:len(package_name)-5]
	# 	classpath = activity_name.replace('.','/')
	# 	gitname = myApp.package_name.replace('.','-').lower()
	# 	url = settings.gitlab_url+'/marvin/'+gitname+'/tree/'+myApp.version+'/'+classpath+'.java'	
	# 	return HttpResponseRedirect(url)	
	# else:
	try:
		classpath = package_name.replace('.','/')
		#mySF = myApp.sourcefile_set.get(file_name=classpath)
		gitname = myApp.package_name.replace('.','-').lower()
		myVersion = myApp.version.replace(' ','_')
		url = settings.gitlab_url+'/marvin/'+gitname+'/tree/'+myVersion+'/'+classpath
		return HttpResponseRedirect(url)
	except Exception as errmsg:
		context = {"errmsg": "La clase "+ package_name+" no se halla en el repositorio, puede suceder que haya .DEX suplementarios. "+ str(errmsg)}
		return render_to_response('frontpage/error.html', RequestContext(request, context))
