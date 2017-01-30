import sys
import requests
import ConfigParser

issuesURL =   'https://api.github.com/repos/mentii/mentii/issues'
projectsURL =  'https://api.github.com/repos/mentii/mentii/projects'

configFile = sys.argv[1]
config = ConfigParser.ConfigParser()
config.read(configFile)
username = config.get('login', 'username')
password = config.get('login', 'password')

s = requests.Session()
s.auth = (username, password)
s.headers.update({'Accept': 'application/vnd.github.inertia-preview+json'})
response = s.get(projectsURL)
projects = response.json()

for p in projects:
    print p['name']
    columnsURL =  p['columns_url']
    response = s.get(columnsURL)
    columns = response.json()

    pointsPerCol = {}

    for col in columns:
        colName = col['name']
        print '\t', colName
        cardURL =  col['cards_url']
        response = s.get(cardURL)
        cards = response.json()
        colPoints = 0

        for card in cards:
            note = card['note']
            if not note:
                contentURL = card['content_url']
                response = s.get(contentURL)
                content = response.json()
                note = content['title']
            divide = note.rfind("(")
            name = note[:divide]
            points = note[divide+1:-1]
            points = int(points)
            colPoints += points
            print '\t\t', name, points

        print '\t', 'Total', colName, 'Points:', colPoints, '\n'
        pointsPerCol[colName] = colPoints

print pointsPerCol
