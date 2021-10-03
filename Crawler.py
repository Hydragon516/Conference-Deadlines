from selenium import webdriver
import natsort
from pandas import *
import datetime
from github import Github
import time
from slack import *

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

t = datetime.datetime.now()
buffer = []

while True:
    time.sleep(60)
    delta = datetime.datetime.now()-t
    if delta.seconds >= 3600:
        try:
            target_url = []

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument("--disable-gpu")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--log-level=3')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')

            driver = webdriver.Chrome('/HDD1/mvpservereight/minhyeok/chromedriver/chromedriver', options=options)
            driver.implicitly_wait(5)

            driver.get(url='https://research.com/conference-rankings/computer-science/2021')

            for i in range(100):
                search = driver.find_element_by_xpath('//*[@id="rankingItems"]/div[{}]/span[2]/h4/a'.format(i + 1))
                target_url.append(search.get_attribute('href'))

            driver.close()

            ai_dict = {}

            dt = datetime.datetime.today()
            current_year = int(dt.year)
            current_month = int(dt.month)
            current_day = int(dt.day)

            for i in range(100):
                driver = webdriver.Chrome('/HDD1/mvpservereight/minhyeok/chromedriver/chromedriver', options=options)
                driver.implicitly_wait(5)

                driver.get(url=target_url[i])

                name = (driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/h1')).text
                deadline = (driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/p[2]/strong')).text
                rank = (driver.find_element_by_xpath('//*[@id="tab-1"]/div/div[2]/div[2]/span[2]')).text

                url = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/a')
                get_url = url.get_attribute('href')
                
                year = int(deadline.split(" ")[3])
                month = int(month_string_to_number(deadline.split(" ")[2]))
                day = int(deadline.split(" ")[1])

                target_date = "{}_{}_{}".format(year, month, day)

                title = "[{}]({})".format(name, get_url)

                if datetime.date(current_year, current_month, current_day) <= datetime.date(year, month, day):
                    ai_dict[rank, title] = target_date
                    print(name, target_date)
                    driver.close()
                else:
                    driver.close()
                    continue

            ai_dict = natsort.natsorted(ai_dict.items(), key=lambda x:x[1], reverse=False)

            conference_rank = []
            conference_name = []
            conference_deadline = []

            for i in ai_dict:
                conference_rank.append((i[0])[0])
                conference_name.append((i[0])[1])
                conference_deadline.append(i[1])

            raw_data = {'rank': conference_rank,
                        'name': conference_name,
                        'deadline': conference_deadline,
                        }

            data = DataFrame(raw_data)

            new_buffer = data.to_markdown()

            if new_buffer != buffer:
                send_mdg_to_slack(new_buffer)
                buffer = new_buffer

                g = Github("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")

                output = "# Conference-Deadlines-Crawler \n\n This repository contains code that crawls deadline information for various computer science conferences. Conference names, rankings, deadlines, and links are crawled from [Guide2Research](https://www.guide2research.com/topconf/machine-learning). Conferences up to the top 100 are displayed and the table below will be updated in the future."

                output = output + "\n\n" + data.to_markdown()

                repo = g.get_repo("Hydragon516/Conference-Deadlines")
                contents = repo.get_contents("README.md")
                repo.update_file(contents.path, "Update README.md", output, contents.sha, branch="main")

            t = datetime.datetime.now()

        except:
            t = datetime.datetime.now()
