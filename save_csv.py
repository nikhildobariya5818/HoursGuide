from interface_class import *
from helper_class import *
from proxy_interface import *
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm as sqlorm
import pandas as pd


class ExportData():


    def export_csv(self,filename):

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

        shop = session.query(Read).all()

        shop = [record.__dict__ for record in shop]

        session.close()


        pd.DataFrame(shop).to_csv(filename)

        print(shop)


if __name__ == "__main__":
    d = ExportData()
    d.export_csv("tempOutput.csv")