from bs4 import BeautifulSoup
import requests
from pandas import *
from tabulate import tabulate
import natsort

def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12
        }

    s = string.strip()[:3].lower()
    out = m[s]

    return out

html = requests.get('http://www.guide2research.com/topconf/')

soup = BeautifulSoup(html.text, 'html.parser')

data1 = soup.find_all('td', {'colspan':'3'})
data2 = soup.find_all('div', {'style':'padding:0px;margin:0px;'})
data3 = soup.find_all('td', {'width':'220px'})
data4 = soup.find_all('a', {'target':'_blank'})
data5 = soup.find_all('b', {'style':'font-size:22px;'})

ai_dict = {}

for i in range(len(data1)):
    name = ((data1[i].text).replace(" ","").replace("\n","").split(":"))[0]
    deadline = (data3[i].text).replace("\n","").split(" ")
    link = (data4[i].text).replace("\n","")
    rank = (data5[i].text).replace("\n","")

    if len(deadline) == 7:
        date = deadline[-3:]
        m = month_string_to_number(date[1])
        date[1] = str(m)
        date = date[::-1]

        ai_dict[rank, name, link] = '_'.join(date)

ai_dict = natsort.natsorted(ai_dict.items(), key=lambda x:x[1], reverse=False)

conference_rank = []
conference_name = []
conference_deadline = []
conference_link = []

for i in ai_dict:
    conference_rank.append((i[0])[0])
    conference_name.append((i[0])[1])
    conference_deadline.append(i[1])
    conference_link.append((i[0])[2])

raw_data = {'rank': conference_rank,
            'name': conference_name,
            'deadline': conference_deadline,
            'link': conference_link
            }

data = DataFrame(raw_data)
print(data.to_markdown())
