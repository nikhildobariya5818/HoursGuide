from get_shopping import *
from get_states import *
from get_City import *
from get_shop import *
from get_data import *
from save_csv import ExportData
import sqlite3
from interface_class import *
sys.setrecursionlimit(5000)

def clear_DB():
    conn = sqlite3.connect("Source.db")

    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"Dropping table: {table_name}")
        try:
            cursor.execute(f"DROP TABLE IF EXISTS \"{table_name}\";")
        except sqlite3.Error as e:
            print(f"Error dropping table {table_name}: {e}")

    conn.commit()
    conn.close()

class MAIN():

    def __init__(self, type):
        self.interface = INTERFACING()
        self.type = type

    def get_entity_indexes(self):
        try:
            self.shopping = SHOPPING(self.type)
            print("1. Get the Shopping Listing:")
            self.shopping.get_shopping_listing()
            self.interface.kill_chrome()
            self.interface.delete_temp()
        except Exception as e:
            print(e)
            self.get_entity_indexes()

    def get_states(self):
        try:
            self.state = STATES()
            print("2. Get the State Listing:")
            self.state.get_state_listing()
            self.interface.kill_chrome()
            self.interface.delete_temp()
        except Exception as e:
            print(e)
            self.get_states()
        
    def get_cities(self):
        try:
            self.city = CITY()
            print("3. Get the City Listing:")
            self.city.get_city_listing()
            self.interface.kill_chrome()
            self.interface.delete_temp()
        except Exception as e:
            print(e)
            self.get_cities()
        
    def get_shops(self):
        try:
            self.shop = SHOP()
            print("4. Get the Shop Listing:")
            self.shop.get_shop_listing()
            self.interface.kill_chrome()
            self.interface.delete_temp()
        except Exception as e:
            print(e)
            self.get_shops()

    def get_data(self):
        try:
            self.data = DATA()
            print("5. Get the Data:")
            self.data.get_data()
            self.interface.kill_chrome()
            self.interface.delete_temp()
        except Exception as e:
            print(e)
            self.get_data()        

    def execute_all(self):
        print("Executing all functions:")

        self.get_entity_indexes()

        self.get_states()

        self.get_cities()

        self.get_shops()

        self.get_data() 

        self.exporter = ExportData()
        print("6. Writing Csv:")

        csv_file_name = self.type.replace("-", "_") + 'Output.csv'
        self.exporter.export_csv(csv_file_name)
        # clear_DB()

    def execute_mall(self):
        self.get_entity_indexes()




if __name__ == "__main__":
    print("1. Scrap Data")
    print("2. Clear Database")
    option = input("Enter number: ")
    match int(option):
        case 1:
            print("1. Accessories")
            print("2. Apparel")
            print("3. Arts & Crafts")
            print("4. Automotive")
            print("5. Banks")
            print("6. Beauty & Health")
            print("7. Bookstores")
            print("8. Dental & Hospital")
            print("9. Drug Stores")
            print("10. Electronics")
            print("11. Entertainment")
            print("12. Express & Transport")
            print("13. Gas Station")
            print("14. Grocery & Market")
            print("15. Hair Salons")
            print("16. Home & Garden")
            print("17. Insurance & Finance")
            print("18. Other Services")
            print("19. Outlets")
            print("20. Pets")
            print("21. Printing")
            print("22. Real Estate")
            print("23. Shoes")
            print("24. Shopping")
            print("25. Sports")
            print("26. Toys & Gifts")
            print("27. Travel & Lodging")
            option = input("Enter number according to type: ")
            match int(option):
                case 1:
                    Scraper = MAIN(type="accessories")
                    Scraper.execute_all()
                case 2:
                    Scraper = MAIN(type="apparel")
                    Scraper.execute_all()
                case 3:
                    Scraper = MAIN(type="arts-and-crafts")
                    Scraper.execute_all()
                case 4:
                    Scraper = MAIN(type="automotive")
                    Scraper.execute_all()
                case 5:
                    Scraper = MAIN(type="banks")
                    Scraper.execute_all()
                case 6:
                    Scraper = MAIN(type="beauty-and-health")
                    Scraper.execute_all()
                case 7:
                    Scraper = MAIN(type="bookstores")
                    Scraper.execute_all()
                case 8:
                    Scraper = MAIN(type="dental-and-hospital")
                    Scraper.execute_all()
                case 9:
                    Scraper = MAIN(type="drug-stores")
                    Scraper.execute_all()
                case 10:
                    Scraper = MAIN(type="electronics")
                    Scraper.execute_all()
                case 11:
                    Scraper = MAIN(type="entertainment")
                    Scraper.execute_all()
                case 12:
                    Scraper = MAIN(type="express-and-transport")
                    Scraper.execute_all()
                case 13:
                    Scraper = MAIN(type="gas-station")
                    Scraper.execute_all()
                case 14:
                    Scraper = MAIN(type="grocery-and-market")
                    Scraper.execute_all()
                case 15:
                    Scraper = MAIN(type="hair-salons")
                    Scraper.execute_all()
                case 16:
                    Scraper = MAIN(type="home-and-garden")
                    Scraper.execute_all()
                case 17:
                    Scraper = MAIN(type="insurance-and-finance")
                    Scraper.execute_all()
                case 18:
                    Scraper = MAIN(type="other-services")
                    Scraper.execute_all()
                case 19:
                    Scraper = MAIN(type="outlets")
                    Scraper.execute_all()
                case 20:
                    Scraper = MAIN(type="pets")
                    Scraper.execute_all()
                case 21:
                    Scraper = MAIN(type="printing")
                    Scraper.execute_all()
                case 22:
                    Scraper = MAIN(type="real-estate")
                    Scraper.execute_all()
                case 23:
                    Scraper = MAIN(type="shoes")
                    Scraper.execute_all()
                case 24:
                    Scraper = MAIN(type="shopping")
                    Scraper.execute_all()
                case 25:
                    Scraper = MAIN(type="sports")
                    Scraper.execute_all()
                case 26:
                    Scraper = MAIN(type="toys-and-gifts")
                    Scraper.execute_all()
                case 27:
                    Scraper = MAIN(type="travel-and-lodging")
                    Scraper.execute_all()
                case 28:
                    Scraper = MAIN(type="mall")
                    Scraper.execute_mall()
                case _:
                    print("Something went wrong")

        case 2:
            clear_DB()
        case _:
            print("Something went wrong")