from interface_class import *
from helper_class import *
from proxy_interface import *
import cloudscraper
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm as sqlorm

class MALL():

    def __init__(self):
        self.helper = Helper()
        self.proxy_filename = "data.json"
        self.all_proxies = self.helper.read_json_file(
            self.proxy_filename)["proxies"]
        self.Shopping_links =[]
        self.City_links =[]
        self.shop =[]

        with open ('done.json','r',encoding='utf-8') as input:
            self.done = json.load(input)

    def getProxy(self):

        proxy = random.choice(self.all_proxies)

        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'

        return {"https": proxyHandler, "http": proxyHandler}
    
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

    def get_mall_States(self, link):
        try:
            scraper = cloudscraper.create_scraper()
            print(link)
            response = scraper.get(link,proxies=self.getProxy())
            print(response.status_code)
            if 'Shopping' in response.text:
                soup = BeautifulSoup(response.content,'lxml')
                urls = soup.find_all('a',{'class':'list-link'})
                
                for url in urls:
                    self.Shopping_links.append(self.helper.get_url_from_tag(url))
                time.sleep(5)
                print(len(list(set(self.Shopping_links))))
                with open ('State.json','w') as json_file:
                    json.dump(self.Shopping_links,json_file,indent=4)
            else:
                print(f"No 'Shopping' found on the page {link}")
                self.get_mall_States(link)
        except Exception as e:
            print(link, e)
            self.get_mall_States(link)

    def get_mall_city(self, links):
        try:
            scraper = cloudscraper.create_scraper()
            print(links)
            response = scraper.get(links, proxies=self.getProxy())

            if 'Shopping' in response.text:
                soup = BeautifulSoup(response.text, 'html.parser')
                divs = soup.find('div', {'class': "state-list-wrap"})
                urls = divs.find_all('a', {'class': "list-link"})
                for url in urls:
                    self.City_links.append(url['href'])
                time.sleep(5)
                print(len(list(set(self.City_links))))
                with open ('City.json','w') as json_file:
                    json.dump(self.City_links,json_file,indent=4)
            else:
                print(f"No 'Shopping' found on the page {links}")
                self.get_mall_city(links)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.get_mall_city(links)

    def get_shop(self,link):
        proxies = self.getProxy()
        try:
            scraper = cloudscraper.create_scraper()
            print(link)
            response = scraper.get(link,proxies=proxies)

            if 'Shopping' in response.text:
                soup = BeautifulSoup(response.text, 'html.parser')
                urls = soup.find_all('li',{'class':'store-list-item'})
                for url in urls:
                    self.shop.append(self.helper.get_url_from_tag(url.find('a', {'class': 'link-cover'})))
                time.sleep(3)
                print(len(list(set(self.shop))))
                with open ('Shop.json','w') as json_file:
                    json.dump(self.shop,json_file,indent=4)
            else:
                print(f"No 'Shopping' found on the page {link}")
                self.get_shop(link)
        except Exception as e:
            print(e)
            self.get_shop(link)

    def get_data(self,link_url):
        proxies = self.getProxy()
        try:
            if link_url not in self.done:
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

                    
                scraper_instance = cloudscraper.create_scraper()
                print(link_url)
                
                response = scraper_instance.get(link_url, proxies=proxies)

                if 'Shopping' in response.text:
                    soup = BeautifulSoup(response.content, 'lxml')

                    scraper['URL'] = link_url

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
                    
                else:
                    print(f"No 'Shopping' found on the page {link_url}")
                    self.get_data(link_url)
            else:
                print("skuipping Shop Url...")
            with open ('done.json','w') as json_file:
                json.dump(link_url,json_file,indent=4)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.get_data(link_url)

    def run_multiThread(self, function, max_workers, args):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(function, args)

    def runner(self):
        self.get_mall_States('https://www.hoursguide.com/mall/index/')
        print("*"*50)
        self.run_multiThread(
            self.get_mall_city,
            5,
            self.Shopping_links
        )
        print("*"*50)
        self.run_multiThread(
            self.get_shop,
            15,
            self.City_links
        )
        print("*"*50)
        self.run_multiThread(
            self.get_data,
            20,
            self.shop
        )

if __name__ == "__main__":
    main = MALL()
    main.runner()