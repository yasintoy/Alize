from django.core.cache import cache

from visualize.usecases.get_user_info import GetUserInfo
from visualize.usecases.get_users_repository_info import GetUserRepoInfo
from visualize.usecases.get_user_ranking import GetUserRanking
from visualize.usecases.get_user_commits import GetUserCommits


class Analysis(object):
	"""
		@params : repo_info -> [] (all repo names)

	"""

	def _get_user_info(self, username):
		get_user_info = GetUserInfo()
		response = get_user_info.execute(username)
		cache.set(username, response)
		return response

	def _get_user_repository_info(self, username):
		get_user_repo_info = GetUserRepoInfo()
		response = get_user_repo_info.execute(username)
		cache.set(username + "_repo", response)
		return response

	def _get_user_ranking(self, username):
		ranking = GetUserRanking()
		response = ranking.execute(username)
		cache.set(username + "_ranking", response)
		return response

	def _get_user_commits_info(self, username, repo_info):
		commits = GetUserCommits([repo["name"] for repo in repo_info["repos"] if not repo["is_fork"] ])
		response = commits.execute(username)
		cache.set(username + "_commits", response)
		return response

	def execute(self, username):
		if username in cache:
			user_info = cache.get(username)
			repo_info = cache.get(username + "_repo")
			user_raking = cache.get(username + "_ranking")
			commits_info = cache.get(username + "_commits")
		else:
			user_info = self._get_user_info(username)
			repo_info = self._get_user_repository_info(username)
			user_raking = self._get_user_ranking(username)
			commits_info = self._get_user_commits_info(username, repo_info)

		return {
			"user_info": user_info,
			"user_raking": user_raking,
			"repo_info": repo_info,
			"commits_info": commits_info,
		}
