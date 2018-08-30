
from django.views.generic import ListView, DetailView
from frontpage.models import App, VulnerabilityResult, Permission


class PermsListView (ListView):
	model = Permission

	# def get_context_data(self, **kwargs):
	# 	context = super(Applist, self).get_context_data(**kwargs)
	# 	user = self.request.user
	# 	context['myuser']= user
	# 	return context

class AppDetailView(DetailView):
	model = App

class VulnDetailView(DetailView):
	model = VulnerabilityResult