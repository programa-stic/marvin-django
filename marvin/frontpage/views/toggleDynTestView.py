from django.contrib.auth.decorators import login_required

@login_required
def toggleDynTest(request, pk):
	myVulnResult = get_object_or_404 (VulnerabilityResult,pk=pk)
	print "toggleDynTest: vuln #"+ str(pk)
	print "  name: " + myVulnResult.name
	print "  scheduled: " + str(myVulnResult.scheduledForDT)
	if myVulnResult.scheduledForDT == True:
		myVulnResult.scheduledForDT = False
	else:
		myVulnResult.scheduledForDT = True
	myVulnResult.save()
	#context = {'result':myVulnResult.scheduledForDT}
	response = HttpResponse()
	response['sched'] = myVulnResult.scheduledForDT
	return response