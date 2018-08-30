def source_file_contents(request,pk):
	mySourceFile = get_object_or_404 (Sourcefile, pk=pk)
	mySourceFile.file_contents = mySourceFile.file_contents.replace("\\n", "\n") 
	context = {'file': mySourceFile}
	return render(request, 'frontpage/sourcefile_contents.html', context)