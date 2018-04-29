import json
import requests

from visualize.utils.api import Client
from visualize.usecases.generate_wordcloud import GenerateWordCloud


class GetUserCommits():
	"""docstring for GetUserCommits"""
	def __init__(self, repo_info):
		self.repo_names = repo_info
		self.result = {"total_commits": 0, "last_5_commits": [], "all_commits": []}

	def count_user_commits(self, user):
		for repo in self.repo_names:
			yield repo, self.count_repo_commits(user, repo)

	def extract_more_info(self, repo_name, commits):
		for c in commits:
			self.result["all_commits"].append({
				"name": repo_name,
				"message": c["commit"]["message"] if "commit" in c else "",
				"date": c["commit"]["committer"]["date"] if "commit" in c else ""
			})

	def most_popular_words(self):
		generate = GenerateWordCloud()
		self.result["word_cloud_file"] = generate.execute("".join([i["message"] for i in self.result["all_commits"]]))

	def count_repo_commits(self, user, repo, _acc=0, page=1):
		request = Client().user_commits(url_params={"username": user, "repo_name": repo, "page": page}, pure=True)
		commits = request.json()
		self.extract_more_info(repo, commits)
		commit_count = len(commits)
		if commit_count == 0:
			return _acc
		link = request.headers.get('link')
		if link is None:
			return _acc + commit_count
		next_url = self.find_next(request.headers['link'])
		if next_url is None:
			return _acc + commit_count
		return self.count_repo_commits(user, repo, _acc + commit_count, page=page+1)

	def find_next(self, link):
		for l in link.split(','):
			a, b = l.split(';')
			if b.strip() == 'rel="next"':
				return a.strip()[1:-1]

	def execute(self, user):
		for repo_name, commit_count in self.count_user_commits(user):
			self.result["total_commits"] += commit_count
			print ("Repo %s has %d commits" % (repo_name, commit_count))
		print ("Total commits: %d" % self.result["total_commits"])
		self.result["all_commits"].sort(key=lambda item: item["date"], reverse=True)
		self.result["last_5_commits"].extend(self.result["all_commits"][:5])
		self.most_popular_words()
		return self.result

