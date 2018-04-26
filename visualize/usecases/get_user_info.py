import requests
from django.conf import settings

from visualize.utils.api import Client

class GetUserInfo(object):
	"""
	 	GetUserInfo : 
	 	params : username
	 	response : 
			{
				"login": "torvalds",
				"id": 1024025,
				"avatar_url": "https://avatars0.githubusercontent.com/u/1024025?v=4",
				"gravatar_id": "",
				"url": "https://api.github.com/users/torvalds",
				"html_url": "https://github.com/torvalds",
				"followers_url": "https://api.github.com/users/torvalds/followers",
				"following_url": "https://api.github.com/users/torvalds/following{/other_user}",
				"gists_url": "https://api.github.com/users/torvalds/gists{/gist_id}",
				"starred_url": "https://api.github.com/users/torvalds/starred{/owner}{/repo}",
				"subscriptions_url": "https://api.github.com/users/torvalds/subscriptions",
				"organizations_url": "https://api.github.com/users/torvalds/orgs",
				"repos_url": "https://api.github.com/users/torvalds/repos",
				"events_url": "https://api.github.com/users/torvalds/events{/privacy}",
				"received_events_url": "https://api.github.com/users/torvalds/received_events",
				"type": "User",
				"site_admin": false,
				"name": "Linus Torvalds",
				"company": "Linux Foundation",
				"blog": "",
				"location": "Portland, OR",
				"email": null,
				"hireable": null,
				"bio": null,
				"public_repos": 6,
				"public_gists": 0,
				"followers": 72049,
				"following": 0,
				"created_at": "2011-09-03T15:26:22Z",
				"updated_at": "2017-11-14T16:54:03Z"
			}
	"""

	def _extract_infos(self, data):
		return {
			"id": data["id"],
			"name": data["name"],
			"username": data["login"],
			"html_url": data["html_url"],
			"url": data["url"],
			"avatar": data["avatar_url"],
			"total_repos": data["public_repos"],
			"followers": data["followers"],
			"following": data["following"],
			"created_at": data["created_at"],
			"company": data["company"],
			"bio": data["bio"],
			"email": data["email"],
			"location": data["location"],
		}

	def validate(self, username):
		if not username:
			raise Exception("Invalid username")

	def execute(self, username):
		self.validate(username)
		api_response = Client().user_info(url_params={"username": username})
		response = self._extract_infos(api_response)
		return response

