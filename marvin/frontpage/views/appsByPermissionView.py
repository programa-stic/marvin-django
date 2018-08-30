def appsByPermission(request, pk):
	myPerm = get_object_or_404 (Permission, pk=pk)
	object_list = myPerm.app.all()
	paginator = Paginator(object_list, 10)
	page = request.GET.get('page')
	try:
		packages = paginator.page(page)
	except PageNotAnInteger:
		packages = paginator.page(1)
	except EmptyPage:
		packages = paginator.page(paginator.num_pages)
	context = {'packages': packages, 'perm':myPerm}
	#context.update(csrf(request))
	return render(request, 'frontpage/apps_by_permission.html', context)
