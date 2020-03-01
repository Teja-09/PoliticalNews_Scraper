from flask import Flask, render_template
import urllib3
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    quote_page = 'https://www.livemint.com/elections'
    http = urllib3.PoolManager()
    page = http.request('GET', quote_page)
    soup = BeautifulSoup(page.data, 'html.parser')

    # Extracting Headlines
    # name_box = soup.find_all(lambda tag: (tag.name == 'h1' or tag.name == 'h2') and tag['class'] == ['headline'])
    # name_box = soup.find_all(re.compile(r'(h2|h1)'))
    name_box = soup.find_all(['h1', 'h2'], attrs={'class':'headline'})
    print(len(name_box))
    for i in range(len(name_box)):
        name_box[i] = name_box[i].text

    # Extracting date and Time of posted
    dateTime = soup.find_all('span', attrs={'data-sectionname': 'Elections 2019'})
    print(len(dateTime))
    for i in range(len(dateTime)):
        dateTime[i] = dateTime[i].text

    textlist = []
    ind = 0
    highlights = soup.find_all(['ul','p'], attrs={'class': ['highlights','summary']})
    for i in range(len(highlights)):
        highlights[i] = highlights[i].text
    for i in range(len(highlights)-1):
        if highlights[i] != highlights[i+1]:
            textlist.append(highlights[i]) 
    textlist.append(highlights[-1])


    # Adding all the data as per news into finalData list
    finalData = []
    for i in range(len(name_box)):
        finalData.append((dateTime[i], name_box[i], textlist[i]))
        print(finalData[i])
        print()

    with open('index.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        # The for loop
        for date, title, summary in finalData:
            writer.writerow([date, title, summary, datetime.now()])

    return render_template('index.html', dataset = finalData)

