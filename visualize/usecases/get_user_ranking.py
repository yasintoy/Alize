import requests


class GetUserRanking(object):
	""" 
		params: username
		example response: 
		{
				"user": {
				"id": 12545392,
				"login": "yasintoy",
				"gravatar_url": "https://avatars1.githubusercontent.com/u/8049196?v=4",
				"city": "istanbul",
				"country": "turkey",
				"rankings": [
					{
					"language": "python",
					"repository_count": 7,
					"stars_count": 801,
					"city_rank": 3,
					"city_count": 436,
					"country_rank": 4,
					"country_count": 1173,
					"world_rank": 2099,
					"world_count": 587255
					},
				]
			}
		}
	"""
	def execute(self, username):
		url = "http://git-awards.com/api/v0/users/{username}.json".format(username=username)
		response = requests.get(url).json()
		return response["user"]
