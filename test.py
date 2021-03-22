# this is a prototype(the logic) to detect same job postings throught multiple websites
# before inserting them to database, thus preventing data redundancy 

import json

jobs = {}

jobs[0] = {}
jobs[0] = {
  'titulli': 'pizzaman',
  'company': 'sachpizza'
}
jobs[1] = {}
jobs[1] = {
  'titulli': 'pizzaman',
  'company': 'proper'
}

jobs[2] = {}
jobs[2] = {
  'titulli': 'pizzaman',
  'company': 'agora'
}

tempTitulli = 'pizzaman'
tempCompany = 'agora'

for i in range(len(jobs)):
  if jobs[i]['titulli'] == tempTitulli and jobs[i]['company'] == tempCompany:
    print('te njejta')
  else:
    print('jo te njejta')

with open('data.json', 'w') as outfile:
  json.dump(jobs, outfile)