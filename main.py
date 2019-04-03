import numpy as np
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def scrape_donations():
    base_url = "https://gamesdonequick.com/tracker/donations/agdq2018?page="
    dataset = np.zeros( (30000, 2), dtype=object )
    for i in range(1, 893):
        list_req = Request(base_url + str(i), headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(list_req) as u:
            soup = BeautifulSoup(u, "lxml")

        # Finding all <tr> tags
        trs = soup.find_all('tr')

        # Setup
        donation_urls = []

        # Getting urls to all donations with commments on current page
        counter = 0
        for tr in trs:
            tds = tr.find_all('td')
            if(len(tds) == 4): 
                if(str(tds[3].string).strip() == "Yes"):
                    dataset[counter, 1] = str(tds[2].text).strip()[1:]
                    counter += 1
                    donation_urls.append("https://gamesdonequick.com" + tds[2].a['href'])

        # Getting donation comment from each url
        counter = 0
        for url in donation_urls:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req) as u:
            # with open("test_donation.html") as fp:
                donation_soup = BeautifulSoup(u, "lxml")
                comment = str(donation_soup.td.text).strip()
                dataset[counter, 0] = comment
                print(comment)
                counter += 1
            # pay respects
            time.sleep(3)

    clean_dataset = dataset[~np.all(dataset == 0, axis=1)]
    np.savetxt("dataset.txt", clean_dataset, delimiter=',', fmt='%s, %s')

scrape_donations()