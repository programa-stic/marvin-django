from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from frontpage.models import VulnerabilityResult
from frontpage.forms import CommentForm


@login_required
def vulnDetail(request, pk):
#	if request.method == "GET":
	myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
	myForm = CommentForm()
	context = {'object':myVuln, 'form':myForm}
	return render(request, 'frontpage/vulnerabilityresult_detail.html', context)
	