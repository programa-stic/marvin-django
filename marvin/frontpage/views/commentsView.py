def addComment(request,pk):
	myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
	if request.method == "POST":
		myForm = CommentForm(request.POST)
		#myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
		if myForm.is_valid():
			comment = myForm.cleaned_data['text']
			user = request.user
			new_comment = App_comments(author = request.user,
									   contents = comment,
									   vuln = myVuln,
									   app = myVuln.app)
			new_comment.save()
		context = {'object':myVuln, 'form':myForm}
		return render_to_response('frontpage/vulnerabilityresult_detail.html', RequestContext(request, context))
	else:
		myForm = CommentForm()
		context = {'object':myVuln, 'form':myForm}
		return render_to_response('frontpage/vulnerabilityresult_detail.html', RequestContext(request, context))

def deleteComment(request,pk):
	myComment = get_object_or_404 (App_comments, pk=pk)
	myVuln = myComment.vuln
	myComment.delete()
	myForm = CommentForm(request.POST)
	context = {'object':myVuln, 'form':myForm}
	return render_to_response('frontpage/vulnerabilityresult_detail.html', RequestContext(request, context))
