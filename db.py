from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
 
engine = create_engine('sqlite:///pubmed_search.db', echo = True)
Base = declarative_base()
 

class PubMedSearch(Base):
    __tablename__ = "search_config"
 
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    query_words = Column(String)  
    # add schedule time
 
    
    def __init__(self, user_id, query_words):
        self.user_id = user_id
        self.query_words = query_words    

Base.metadata.create_all(engine)