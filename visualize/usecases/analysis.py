from django.core.cache import cache

from visualize.usecases.get_user_info import GetUserInfo
from visualize.usecases.get_users_repository_info import GetUserRepoInfo


class Analysis(object):
	"""docstring for Analysis"""

	def _get_user_info(self, username):
		get_user_info = GetUserInfo()
		response = get_user_info.execute(username)
		cache.set(username, response)

	def _get_user_repository_info(self, username):
		get_user_repo_info = GetUserRepoInfo()
		response = get_user_repo_info.execute(username)
		cache.set(username+"_repo", response)

	def execute(self, username):
		if username in cache:
			user_info = cache.get(username)
			repo_info = cache.get(username+"_repo")
		else:
			user_info = self._get_user_info(username)
			repo_info = self._get_user_repository_info(username)

		return {
			"user_info": user_info
		}
