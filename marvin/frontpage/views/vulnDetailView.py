from django.contrib.auth.decorators import login_required

@login_required
def vulnDetail(request, pk):
#	if request.method == "GET":
	myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
	myForm = CommentForm()
	context = {'object':myVuln, 'form':myForm}
	return render_to_response('frontpage/vulnerabilityresult_detail.html', RequestContext(request, context))
	