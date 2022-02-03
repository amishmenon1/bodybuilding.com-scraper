from bs4 import BeautifulSoup as soup
import requests
import sys

muscle = "chest"  # hardcoded muscle argument
muscle_arg = input('Which muscle do you want exercises for? (must use " "): ') #sys.argv[1]  # muscle input from terminal
limit_arg = input('Enter max # search results: ') #sys.argv[2] # limit number of exercises returned
domain = "https://www.bodybuilding.com"
resource_link = "/exercises/finder/?muscle=" + muscle_arg
exercises_html = []
exercises_text = []    
first_iteration = True
limit = int(limit_arg) if type(limit_arg) == int else None
count = 0
while resource_link is not None:
    if(first_iteration):
        print("Fetching exercises from bodybuilding.com...")
        print("Sit tight. This may take a few minutes...")
        first_iteration = False
    
    url = domain + resource_link
    r = requests.get(url)

    webpage = soup(r.content, 'lxml')
    exercises_html.extend(webpage.findAll("a",{"itemprop":"name"}))
    
    for i in exercises_html:
        text = i.text.strip().encode("utf-8")
        if text not in exercises_text:
            exercises_text.append(text)
            count += 1
        if(count == limit):
            break
    
    if(count == limit):
            break

    next_button = webpage.find("button",{"data-bb-label":"loadMore"})

    if next_button is not None:
        resource_link = next_button.get('data-link')
    else:
        break

for exercise in exercises_text:
    print(exercise)

print("Loading complete.")


