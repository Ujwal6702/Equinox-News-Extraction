import random
import threading
import requests
from bs4 import BeautifulSoup
import time
from datetime import date
import pandas as pd



def googleNews(Text):
    """

    This function takes a string as input and
    returns a pandas dataframe with columns: text, link, publish_date, scraped_date, title 
    extracted from google search results.
    
    """
    try:

        print("Google")
        print(f"Search Text: {Text}")
        url = f"https://www.google.com/search?q={"+".join(Text.split(" "))}&tbm=nws&source=lnt&tbs=qdr:d&sa=X"
        website = "https://www.google.com"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        try:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')  
        except:
            print("Google not working")
            err = "Error in Module "
            return
        
        links=[]
        titles=[]
        texts=[]
        page_number=0
        try:
            while True:
                page_number+=1
                print(f"page number: {page_number}")
                articles = soup.find_all("div", class_="SoaBEf")
                print(f"total number of articles in this page: {len(articles)}")
                for article in articles:
                    a=article.find("a")["href"]
                    b=article.find("div", class_="n0jPhd ynAwRc MBeuO nDgy9d").text
                    c=article.find("div", class_="GI74Re nDgy9d").text
                    if a and b:
                        links.append(a)
                        titles.append(b)
                        texts.append(c)
                
                next_page = soup.find("a", id="pnnext")["href"]
                time.sleep(round(random.uniform(0.5, 1), 2))
                if next_page:
                    page = requests.get(website+str(next_page), headers=headers)
                    soup = BeautifulSoup(page.content, 'html.parser')
                else:
                    break
        except:
            if len(links)==0:
                        print("Google not working")
                        return
        
        final_links = []
        title, text, pub_date, scraped_date = [], [], [], []
        today = date.today()
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=5, pool_maxsize=5)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        def getartciles(link, a, b):
                today=date.today()
                final_links.append(link)
                title.append(a)
                text.append(b)
                scraped_date.append(str(today))
                pub_date.append(str(today))

        
        thread_list=[]
        length=len(links)
        for i in range(length):
            thread_list.append(threading.Thread(target=getartciles, args=(links[i],titles[i], texts[i], )))
        
        for thread in thread_list:
            thread.start()
        
        for thread in thread_list:
            thread.join()
        
        session.close()
        df = pd.DataFrame({"text": text, "link": final_links,
                            "publish_date": pub_date, "scraped_date": scraped_date, "title": title})
        
        df = df.drop_duplicates(subset=["link"])
        
        return df
    
    except:
        print("Google not working")

if __name__ == "__main__":
    print(googleNews("Space Research"))