import json
from interface_class import *
from helper_class import *
from proxy_interface import *
from itertools import count
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm as sqlorm
import cloudscraper,gc


class SHOP():

    def __init__(self):
        self.read_City_url()
        self.helper = Helper()
        self.proxy_filename = "data.json"
        self.all_proxies = self.helper.read_json_file(
            self.proxy_filename)["proxies"]
        
    def getProxy(self):

        proxy = random.choice(self.all_proxies)

        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'

        return {"https": proxyHandler, "http": proxyHandler}
    
    def read_Shop_url(self):
        Base = sqlorm.declarative_base()

        class Read(Base):
            __tablename__ = 'Shop'
            id = Column(Integer, primary_key=True)
            Shop_url = Column(String)
            City_url = Column(String)

        engine = create_engine("sqlite:///Source.db")
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        City_records = session.query(Read.City_url).all()
        # print(len(City_records))
        self.City = [record[0] for record in City_records]

        session.close()

    def read_City_url(self):
        Base = sqlorm.declarative_base()
        
        class Read(Base):
            __tablename__ = 'City'
            id = Column(Integer, primary_key=True)
            City_url = Column(String)
            State_url = Column(String)

        engine = create_engine("sqlite:///Source.db")
        Base.metadata.create_all(engine) 

        Session = sessionmaker(bind=engine)
        session = Session()

        urls_records = list(session.query(Read.City_url).all())
        self.urls = [record[0] for record in urls_records]
        print(len(self.urls))

    def save_to_database(self,url,Shop):
        engine = create_engine("sqlite:///Source.db")  
        Base = sqlorm.declarative_base()

        class User(Base):
            __tablename__ = 'Shop'
            
            id = Column(Integer, primary_key=True)
            Shop_url = Column(String)
            City_url = Column(String)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_user = User(Shop_url=url,City_url=Shop)
        session.add(new_user)
        session.commit()

        session.close()

    def get_shop_listing(self):
        # for i in self.urls:
        #     self.runner(i)
        self.read_Shop_url()
        urls = list(set(self.urls) - set(self.City))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.runner, urls)

    def runner(self,link,count=1):
        self.read_Shop_url()
        if count >10:
            return
        count += 1
        
        try:
            proxies = self.getProxy()
            # link_url = link[0]
            Shop_link = [] 
            # if link_url not in self.City:

            scraper = cloudscraper.create_scraper()
            print(link)
            response = scraper.get(link,proxies=proxies)

            if 'Shopping' in response.text:
                soup = BeautifulSoup(response.text, 'html.parser')
                urls = soup.find_all('li',{'class':'store-list-item'})
                for url in urls:
                    Shop_link.append(self.helper.get_url_from_tag(url.find('a', {'class': 'link-cover'})))
                time.sleep(3)
                print(len(list(set(Shop_link))))
                for shop in Shop_link:
                    self.save_to_database(shop, link)
                # gc.collect()
            else:
                print(f"No 'Shopping' found on the page {link}")
                self.runner(link,count)
            # else:
            #     print(f"Skipping {link_url} because it's already scraped.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.runner(link,count)


if __name__ == "__main__":
    hourse = SHOP()
    hourse.get_shop_listing()