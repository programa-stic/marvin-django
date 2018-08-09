def appsByPackage(request, pk):
	myPackage = get_object_or_404 (Java_package, pk=pk)
	object_list = myPackage.app.all()
	paginator = Paginator(object_list, 10)
	page = request.GET.get('page')
	try:
		packages = paginator.page(page)
	except PageNotAnInteger:
		packages = paginator.page(1)
	except EmptyPage:
		packages = paginator.page(paginator.num_pages)
	context = {'packages': packages, 'package':myPackage}
	#context.update(csrf(request))
	return rendder(request, 'frontpage/apps_by_package.html', context)
