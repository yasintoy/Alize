import requests
from django.conf import settings

from visualize.utils.api import Client


class GetUserRepoInfo(object):
	"""
		{
		"id": 63062837,
		"name": "Slack-Gitsin",
		"full_name": "yasintoy/Slack-Gitsin",
		"owner": {
			...
		},
		"private": false,
		"html_url": "https://github.com/yasintoy/Slack-Gitsin",
		"description": "A beautiful Slack command line interface.",
		"fork": false,
		"url": "https://api.github.com/repos/yasintoy/Slack-Gitsin",
		...some unneccessary urls
		"created_at": "2016-07-11T11:38:25Z",
		"updated_at": "2018-04-10T18:19:49Z",
		"pushed_at": "2017-06-14T15:39:36Z",
		"git_url": "git://github.com/yasintoy/Slack-Gitsin.git",
		"ssh_url": "git@github.com:yasintoy/Slack-Gitsin.git",
		"clone_url": "https://github.com/yasintoy/Slack-Gitsin.git",
		"svn_url": "https://github.com/yasintoy/Slack-Gitsin",
		"homepage": "",
		"size": 8934,
		"stargazers_count": 617,
		"watchers_count": 617,
		"language": "Python",
		"has_issues": true,
		"has_projects": true,
		"has_downloads": true,
		"has_wiki": true,
		"has_pages": false,
		"forks_count": 22,
		"mirror_url": null,
		"archived": false,
		"open_issues_count": 7,
		"license": {
		"key": "gpl-3.0",
		"name": "GNU General Public License v3.0",
		"spdx_id": "GPL-3.0",
		"url": "https://api.github.com/licenses/gpl-3.0"
		},
		"forks": 22,
		"open_issues": 7,
		"watchers": 617,
		"default_branch": "master",
		"permissions": {
		}
		},
	"""
	def _calculate_repo_per_language(self, data):
		total_repos = float(sum(data["languages"].values()))
		return {key: round((value/total_repos)*100) for (key, value) in data["languages"].items()}

	def _extract_infos(self, data):
		response = {"most_popular_project": {"stars": 0}, "languages": {}, "repos": [], "total_stars": 0, "total_forks": 0}
		for repo in data:
			response["repos"].append({"name": repo["name"], "is_fork": repo["fork"]})
			language = repo["language"] if repo["language"] is not None else "Unknown"
			response["languages"][language] = response["languages"].get(language, 0) + 1
			if repo["stargazers_count"] > response["most_popular_project"]["stars"]:
				response["most_popular_project"] = {
					"name": repo["name"],
					"url": repo["html_url"],
					"description": repo["description"],
					"stars": repo["stargazers_count"],
					"forks": repo["forks"],
					"created_at": repo["created_at"]
				}
			response["total_stars"] += repo["stargazers_count"] 
			response["total_forks"] += repo["forks"] 
		return response

	def execute(self, username):
		request = Client().user_repo_info(url_params={"username": username}, pure=True)
		response = self._extract_infos(request.json())
		response.update({"languages_per_repos": self._calculate_repo_per_language(response)})
		return response