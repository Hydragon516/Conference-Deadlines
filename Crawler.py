from selenium import webdriver
import natsort
from pandas import *
import datetime
import chromedriver_autoinstaller

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

target_url = []

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=3')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)   
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)

driver.implicitly_wait(5)

ai_dict = {}

dt = datetime.datetime.today()
current_year = int(dt.year)
current_month = int(dt.month)
current_day = int(dt.day)

driver.get(url='https://raw.githubusercontent.com/paperswithcode/ai-deadlines/gh-pages/_data/conferences.yml')
data = (driver.find_element_by_xpath('/html/body/pre')).text
split_data = data.split('\n')

for idx in range(len(split_data)):
    if "title:" in split_data[idx]:
        name = split_data[idx].split(': ')[1]

        cnt = 0
        while True:
            cnt += 1

            try:
                if "deadline:" in split_data[idx + cnt]:
                    deadline = split_data[idx + cnt].split(': ')[1]
                    break
            except:
                break
        
        cnt = 0
        while True:
            cnt += 1

            try:
                if "hindex:" in split_data[idx + cnt]:
                    hindex = split_data[idx + cnt].split(': ')[1]
                    break
            except:
                break
        
        cnt = 0
        while True:
            cnt += 1

            try:
                if "link:" in split_data[idx + cnt]:
                    link = split_data[idx + cnt].split(': ')[1]
                    break
            except:
                break
        
        target_date = (deadline.split(' ')[0]).replace('-', '_')

        year = int(target_date.split('_')[0].replace("'", ""))
        month = int(target_date.split('_')[1].replace("'", ""))
        day = int(target_date.split('_')[2].replace("'", ""))

        title = "[{}]({})".format(name, link)

        if datetime.date(current_year, current_month, current_day) <= datetime.date(year, month, day):
            ai_dict[hindex, title] = target_date.replace("'", "")
            print(name, target_date)

ai_dict = natsort.natsorted(ai_dict.items(), key=lambda x:x[1], reverse=False)

conference_rank = []
conference_name = []
conference_deadline = []

for i in ai_dict:
    conference_rank.append((i[0])[0])
    conference_name.append((i[0])[1])
    conference_deadline.append(i[1])

raw_data = {'hindex': conference_rank,
            'name': conference_name,
            'deadline': conference_deadline,
            }

data = DataFrame(raw_data)
print(data.to_markdown())
