def appsByPackage2(request, pk, package_name):
	#myApp = get_object_or_404 (App, pk=pkApp)
	myPackages = Java_package.objects.filter(package_name__startswith = package_name)
	object_list = []
	for package in myPackages:
		object_list.extend(package.app.all())
	paginator = Paginator(object_list, 10)
	page = request.GET.get('page')
	try:
		packages = paginator.page(page)
	except PageNotAnInteger:
		packages = paginator.page(1)
	except EmptyPage:
		packages = paginator.page(paginator.num_pages)
	context = {'packages': packages, 'package':package_name}
	#context.update(csrf(request))
	return render(request, 'frontpage/apps_by_package.html', context)
