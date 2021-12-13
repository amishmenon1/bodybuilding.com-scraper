from bs4 import BeautifulSoup as soup
import requests
import json
from collections import defaultdict

muscles = ['chest', 'forearms', 'lats',
'middle-back', 'lower-back', 'neck',
'quadriceps', 'hamstrings', 'calves',
'triceps', 'traps', 'shoulders',
'abdominals', 'glutes', 'biceps',
'adductors', 'abductors']

# muscles = ['chest', 'forearms']

first_iteration = True
DOMAIN = "https://www.bodybuilding.com"

def fetch_exercises(limit):
	for muscle in muscles:
		exercises = get_exercises_for_muscle(muscle, limit)
		write_exercises_to_json(muscle, exercises)

def get_exercises_for_muscle(muscle, limit):
	resource_link = f'/exercises/finder/?muscle={muscle}'
	first_iteration = True
	muscle_to_exercises = defaultdict(list)
	exercises_html = []
	exercises_found = set()
	while resource_link is not None:
		if(first_iteration):
			print(f'Fetching exercises for {muscle} from bodybuilding.com...')
			first_iteration = False

		url = DOMAIN + resource_link
		r = requests.get(url)

		webpage = soup(r.content, 'lxml')
		exercises_html.extend(webpage.findAll("a", {"itemprop": "name"}))

		for i in exercises_html:
			text = i.text.strip()
			if text not in exercises_found:
				muscle_to_exercises[muscle].append(text)
				exercises_found.add(text)
			if len(exercises_found) == limit:
				break

		if len(exercises_found) == limit:
			break

		next_button = webpage.find("button", {"data-bb-label": "loadMore"})

		if next_button is not None:
			resource_link = next_button.get('data-link')
		else:
			break

	return muscle_to_exercises

def write_exercises_to_json(muscle, exercises):
	with open(f'{muscle}.json', 'w') as outfile:
		json.dump(exercises, outfile)

print("Loading complete.")

if __name__ == "__main__":
	# limit number of exercises returned
	# enter something ridiculous to override for now
	limit_arg = input('Enter max # search results: ')
	# could also do a muscle arg
	fetch_exercises(int(limit_arg))
