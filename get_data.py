import requests
from bs4 import BeautifulSoup
from interface_class import *
from helper_class import *
from proxy_interface import *
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm as sqlorm
import cloudscraper,gc

class DATA():

    def __init__(self):
        self.helper = Helper()
        self.read_Shop_url()
        self.proxy_filename = "data.json"
        self.all_proxies = self.helper.read_json_file(
            self.proxy_filename)["proxies"]

    def getProxy(self):

        proxy = random.choice(self.all_proxies)

        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'

        return {"https": proxyHandler, "http": proxyHandler}
    
    def read_Output_url(self):
            Base = sqlorm.declarative_base()

            class Read(Base):
                __tablename__ = 'Output'

                id = Column(Integer, primary_key=True)
                Shop_url = Column(String)
                store_name = Column(String)
                address = Column(String)
                telephone = Column(String)
                website = Column(String)
                hours = Column(String)
                contact_email = Column(String)  
                details = Column(String)  
                mall_name = Column(String)  
                brand_name = Column(String)  
                state_name = Column(String)
                city_name = Column(String)

            engine = create_engine("sqlite:///Source.db")
            Base.metadata.create_all(engine)

            Session = sessionmaker(bind=engine)
            session = Session()

            shop = session.query(Read.Shop_url).all()
            print(len(shop))
            self.shop = [record[0] for record in shop]

            session.close()

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

        urls_records = list(session.query(Read.Shop_url).all())
        self.urls = [record[0] for record in urls_records]
        print(len(self.urls))

    def save_to_database(self, scraper):
        engine = create_engine("sqlite:///Source.db")
        Base = sqlorm.declarative_base()
        # print("*"*50,scraper)
        class Shop(Base):
            __tablename__ = 'Output'

            id = Column(Integer, primary_key=True)
            Shop_url = Column(String)
            store_name = Column(String)
            address = Column(String)
            telephone = Column(String)
            website = Column(String)
            hours = Column(String)
            contact_email = Column(String)  
            details = Column(String)  
            mall_name = Column(String)  
            brand_name = Column(String)  
            state_name = Column(String)
            city_name = Column(String)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_shop = Shop(
            Shop_url=scraper['URL'],
            store_name=scraper['store_name'],
            address=scraper['address'],
            telephone=scraper['telephone'],
            website=scraper['website'],
            hours=scraper['hours'],
            contact_email=scraper['contact_email'],
            details=scraper['details'],
            mall_name=scraper['mall_name'],
            brand_name=scraper['brand_name'],
            state_name=scraper['state_name'],
            city_name=scraper['city_name']
        )

        session.add(new_shop)
        session.commit()

        session.close()

    def get_data(self):
        # for i in self.urls:
        #     self.runner(i)
        self.read_Output_url()
        urls = list(set(self.urls) - set(self.shop))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.runner, urls)

    def runner(self, link):
        self.read_Output_url()
        proxies = self.getProxy()
        try:
            # link_url = link[0]
            scraper = { 
                "URL": "",
                "store_name": "",
                "address": "",
                "telephone": "",
                "website": "",
                "hours": "",
                "contact_email": "",
                "details": "",
                "mall_name": "",
                "brand_name": "",
                "state_name": "",
                "city_name": ""
            }

            # if link_url not in self.shop:
            scraper_instance = cloudscraper.create_scraper()
            print(link)
            response = scraper_instance.get(link, proxies=proxies)
            print(response.status_code)
            if 'Shopping' in response.text:
                soup = BeautifulSoup(response.content, 'lxml')

                scraper['URL'] = link

                try:
                    scraper['store_name'] = self.helper.get_text_from_tag(soup.find('b', {'itemprop': 'name'}))
                except:
                    scraper['store_name'] = ''

                try:
                    scraper['address'] = self.helper.get_text_from_tag(
                        soup.find('li', {'itemprop': 'address'}).find('div', {'class': 'brand-desc-r'}))
                except:
                    scraper['address'] = ''

                try:
                    scraper['telephone'] = self.helper.get_text_from_tag(
                        soup.find('li', {'itemprop': 'telephone'}).find('div', {'class': 'brand-desc-r'}))
                except:
                    scraper['telephone'] = ''

                try:
                    scraper['website'] = self.helper.get_text_from_tag(
                        soup.find('div', {'class': 'store_web'}).find('div', {'class': 'store-detail-l'}))
                except:
                    scraper['website'] = ''

                try:
                    hours_data = []
                    hours_element = soup.find('ul', {"class": "hour-list-wrap"}).find_all('li', {"class": "hour-item"})
                    for hours in hours_element:
                        hours_data.append(hours.text)
                    scraper['hours'] = ' \n'.join(hours_data)
                except:
                    scraper['hours'] = ''

                try:
                    scraper['city_name'] = self.helper.get_text_from_tag(soup.find_all('span', {"class": "breadcrumb-wrap"})[2])
                except:
                    scraper['city_name'] = ''

                try:
                    scraper['state_name'] = self.helper.get_text_from_tag(soup.find_all('span', {"class": "breadcrumb-wrap"})[3])
                except:
                    scraper['state_name'] = ''

                self.save_to_database(scraper)
                # gc.collect()
            else:
                print(f"No 'Shopping' found on the page {link}")
                self.runner(link)
            # else:
            #     print(f"Skipping {link_url} because it's already scraped.")
            # print(scraper)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.runner(link)

if __name__ == "__main__":
    d = DATA()
    d.get_data()

 