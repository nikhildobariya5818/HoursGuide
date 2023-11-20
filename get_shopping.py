import json
from interface_class import *
from helper_class import *
from proxy_interface import *
from itertools import count
import cloudscraper,gc
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm as sqlorm

class SHOPPING():

    def __init__(self, type):
        self.listing = []
        self.indexes = []
        self.read_index_url()
        self.type = type
        self.create_listings()
        self.interface = INTERFACING()
        self.helper = Helper()
        self.proxy_filename = "data.json"
        self.all_proxies = self.helper.read_json_file(
            self.proxy_filename)["proxies"]
    
    def getProxy(self):

        proxy = random.choice(self.all_proxies)

        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'

        return {"https": proxyHandler, "http": proxyHandler}
    
    def create_listings(self):
        alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1"]
        for i in alpha:
            listing = f"https://www.hoursguide.com/brands/{self.type}/index/{i}"
            if listing not in self.indexes:
                self.listing.append(listing)

    def read_index_url(self):
        Base = sqlorm.declarative_base()

        class Read(Base):
            __tablename__ = 'Index'
            id = Column(Integer, primary_key=True)
            Index_Url = Column(String)
            type = Column(String)

        engine = create_engine("sqlite:///Source.db")
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        index_records = session.query(Read.Index_Url).all()
        print(len(index_records))
        self.indexes = [record[0] for record in index_records]

        session.close()

        print(f"Number of Index URLs: {len(self.indexes)}")

    def save_to_database(self, url, page_url):
        engine = create_engine("sqlite:///Source.db")
        Base = sqlorm.declarative_base()

        class User(Base):
            __tablename__ = 'Shopping'

            id = Column(Integer, primary_key=True)
            Shopping_Url = Column(String)
            page_url = Column(String)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_user = User(Shopping_Url=url, page_url=page_url)
        session.add(new_user)
        session.commit()

        session.close()

    def save_index_to_database(self, Index_Url):
        engine = create_engine("sqlite:///Source.db")
        Base = sqlorm.declarative_base()

        class User(Base):
            __tablename__ = 'Index'

            id = Column(Integer, primary_key=True)
            Index_Url = Column(String)
            type = Column(String)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_user = User(Index_Url=Index_Url, type=self.type)
        session.add(new_user)
        session.commit()

        session.close()

    def runner(self, link):
        try:
            scraper = cloudscraper.create_scraper()

            Shopping_links = []
            for i in count():
                page_url = f'{link}/p/{i + 1}/'
                print(page_url)
                while True:
                    response = scraper.get(page_url,proxies=self.getProxy())
                    print(response.status_code)
                    if 'Shopping' in response.text:
                        soup = BeautifulSoup(response.content,'lxml')
                        urls = soup.find_all('a',{'class':'list-link'})
                        
                        for url in urls:
                            Shopping_links.append(self.helper.get_url_from_tag(url))
                        time.sleep(5)
                        print(len(list(set(Shopping_links))))
                        break

                    print('Retrying ...')
                
                if not urls:
                    break

            self.save_index_to_database(link)

            for link in list(set(Shopping_links)):
                self.save_to_database(link, page_url)
            # gc.collect()


        except Exception as e:
            print(link, e)
            self.runner(link)

    def get_shopping_listing(self):
        # for link in self.listing:
        #     self.runner(link)
         with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.runner, self.listing)


if __name__ == "__main__":
    obj = SHOPPING("banks")
    obj.get_shopping_listing()
