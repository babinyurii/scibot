from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
 
engine = create_engine('sqlite:///pubmed_search.db', echo = True)
Base = declarative_base()
 

class PubMedSearch(Base):
    __tablename__ = "search_config"
 
    id = Column(Integer, primary_key=True)
    query_words = Column(String)  
 
    
    def __init__(self, name):
        self.name = name    

Base.metadata.create_all(engine)