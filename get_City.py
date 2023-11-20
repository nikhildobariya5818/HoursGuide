import json
from interface_class import *
from helper_class import *
from proxy_interface import *
from itertools import count
import cloudscraper
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm as sqlorm
import gc

class CITY():

    def __init__(self):
        self.interface = INTERFACING()
        self.read_State_url()
        self.helper = Helper()
        self.proxy_filename = "data.json"
        self.all_proxies = self.helper.read_json_file(
            self.proxy_filename)["proxies"]

    def getProxy(self):

        proxy = random.choice(self.all_proxies)

        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'

        return {"https": proxyHandler, "http": proxyHandler}
    
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

        State_records = session.query(Read.State_url).all()
        print(len(State_records))
        self.State = [record[0] for record in State_records]

        session.close()

        print(f"Number of State URLs: {len(self.State)}")

    def read_State_url(self):
        Base = sqlorm.declarative_base()

        class Read(Base):
            __tablename__ = 'State'
            id = Column(Integer, primary_key=True)
            State_Url = Column(String)
            Shooping_url = Column(String)

        engine = create_engine("sqlite:///Source.db")
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        urls_records = list(session.query(Read.State_Url).all())
        self.urls = [record[0] for record in urls_records]
        print(len(self.urls))

    def save_to_database(self, url, State):
        engine = create_engine("sqlite:///Source.db")
        Base = sqlorm.declarative_base()

        class User(Base):
            __tablename__ = 'City'

            id = Column(Integer, primary_key=True)
            City_url = Column(String)
            State_url = Column(String)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_user = User(City_url=url, State_url=State)
        session.add(new_user)
        session.commit()

        session.close()

    def get_city_listing(self):
        # for i in self.urls:
        #     self.runner(i)
        self.read_City_url()
        urls = list(set(self.urls) - set(self.State))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.runner, urls)

    def runner(self, link,count=1):
        self.read_City_url()
        if count >10:
            return
        count += 1
        try:
            proxies = self.getProxy()
            # link_url = link[0]
            City_links = []
            # if link_url not in self.State:


            scraper = cloudscraper.create_scraper()
            print(link)
            response = scraper.get(link,proxies=proxies)

            if 'Shopping' in response.text:
                soup = BeautifulSoup(response.text, 'html.parser')
                divs = soup.find('div',{'class':"state-list-wrap"})
                urls = divs.find_all('a',{'class':"list-link"})
                for url in urls:
                    City_links.append(url['href'])
                time.sleep(5)
                print(len(list(set(City_links))))
                for city_link in City_links:
                    self.save_to_database(city_link, link)
                # gc.collect()
            else:
                print(f"No 'Shopping' found on the page {link}")
                self.runner(link,count)
            # else:
            #     print(f"Skipping {link_url} because it's already scraped.")
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.runner(link,count)


if __name__ == "__main__":
    hourse = CITY()
    hourse.get_city_listing()
