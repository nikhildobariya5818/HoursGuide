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

class STATES():
    
    def __init__(self):
        self.interface = INTERFACING()
        self.urls = []
        self.shopping = []
        self.read_Shopping_url()
        self.helper = Helper()
        self.proxy_filename = "data.json"
        self.all_proxies = self.helper.read_json_file(
            self.proxy_filename)["proxies"]
        
    def getProxy(self):

        proxy = random.choice(self.all_proxies)

        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'

        return {"https": proxyHandler, "http": proxyHandler}
    
    def read_State_url(self):
        Base = sqlorm.declarative_base()

        class Read(Base):
            __tablename__ = 'State'  ############
            id = Column(Integer, primary_key=True)
            State_Url = Column(String)
            Shopping_url = Column(String)

        engine = create_engine("sqlite:///Source.db")
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        shopping_records = session.query(Read.Shopping_url).all()
        print(len(shopping_records))    ##########
        self.shopping = [record[0] for record in shopping_records]

        session.close()

        print(f"Number of shopping URLs: {len(self.shopping)}")

    def read_Shopping_url(self):
        Base = sqlorm.declarative_base()

        class Read(Base):
            __tablename__ = 'Shopping'
            id = Column(Integer, primary_key=True)
            Shopping_Url = Column(String)
            page_url = Column(String)

        engine = create_engine("sqlite:///Source.db")
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        urls_records = list(session.query(Read.Shopping_Url).all())
        self.urls = [record[0] for record in urls_records]
        print(len(self.urls))

    def save_to_database(self, url, Shooping):
        engine = create_engine("sqlite:///Source.db")
        Base = sqlorm.declarative_base()

        class User(Base):
            __tablename__ = 'State'
            id = Column(Integer, primary_key=True)
            State_Url = Column(String)
            Shopping_url = Column(String)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_user = User(State_Url=url, Shopping_url=Shooping)
        session.add(new_user)
        session.commit()

        session.close()

    def get_state_listing(self):
        # for i in self.urls:
        #     self.runner(i[0])

        self.read_State_url()               #######################
        # x= set(self.urls)
        # y = set(self.shopping)

        # self.helper.write_json_file(self.urls,"urls")
        # self.helper.write_json_file(self.shopping,"shopping")

        # print(len(x),len(y))
        urls = list(set(self.urls)-set(self.shopping))
        print((urls))

        # input()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.runner,urls)


    def runner(self, link):
        self.read_State_url()

        try:
            proxies = self.getProxy()
            scraper = cloudscraper.create_scraper()
            States_link = []
            link_url = link

            # if link_url not in self.shopping:
            response = scraper.get(link_url,proxies=proxies)
            print(response.status_code)
            print(link)
            
            if 'Shopping' in response.text:
                soup = BeautifulSoup(response.content,'lxml')
                urls = soup.find_all('a',{'class':'state-link'})
                for url in urls:
                    States_link.append(self.helper.get_url_from_tag(url))
                time.sleep(5)
                print(len(list(set(States_link))))
                for links in States_link:
                    self.save_to_database(links, link_url)
                # gc.collect()
            else:
                print("No 'Shopping' found on this page.")
            # else:
            #     print(f"Skipping {link_url} because it's already scraped.")
        except Exception as e:
            print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    hourse = STATES()
    hourse.get_state_listing()
