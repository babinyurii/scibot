from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///pubmed_search.db', echo = True)
Base = declarative_base()
 

class PubMedSearch(Base):
    __tablename__ = "search_config"
 
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    query_words = Column(String)  
    email = Column(String(256), unique=True)
    schedule_interval = Column(String(256))
    # add schedule time
 
    
    def __init__(self, user_id, query_words):
        self.user_id = user_id
        self.query_words = query_words    

Base.metadata.create_all(engine)


#############################
# db methods
############################
def add_query(user, query):
    with Session(engine) as session:
        query_record = PubMedSearch(user_id=user, query_words=query)
        session.add(query_record)
        session.commit()
     

def get_query(user):
    with Session(engine) as session:
        search_query = session.query(PubMedSearch).filter_by(user_id=user).first()
        return search_query.query_words


def edit_email(email, user):
    with Session(engine) as session:
        user_record = session.query(PubMedSearch).filter_by(user_id=user).first()
        user_record.email = email
        session.commit()

def edit_schedule_interval(schedule_interval, user):
    with Session(engine) as session:
        user_record = session.query(PubMedSearch).filter_by(user_id=user).first()
        user_record.schedule_interval = schedule_interval
        session.commit()


