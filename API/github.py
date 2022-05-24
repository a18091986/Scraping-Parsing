from pprint import pprint
import requests
import os
import shutil

# if os.path.isdir('MachineLearning'):
#   shutil.rmtree('MachineLearning')

url = "https://api.github.com/users/a18091986/repos"

response = requests.get(url)

data = response.json()

for repo in data:
  pprint(repo['full_name'])

#склонировать репозиторий (работает в colab):
# for repo in data:
#   if repo['full_name'] == 'a18091986/MachineLearning':
#     clone_link = repo['clone_url']

# !git clone $clone_link