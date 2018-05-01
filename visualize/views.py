from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
 
from visualize.usecases.get_user_info import GetUserInfo
from visualize.usecases.analysis import Analysis


CACHE_TTL = settings.CACHE_TTL


class HomeView(View):
	template_name = 'home.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
	

class VisualizeView(View):
	template_name = 'index.html'

	def get(self, request, *args, **kwargs):
		username = self.kwargs["username"]
		analysis = Analysis()
		response = analysis.execute(username)
		return render(request, self.template_name, {"info": response["user_info"], 
													"user_raking": response["user_raking"],
													"repo_info": response["repo_info"],
													"commits_info": response["commits_info"]}) 
