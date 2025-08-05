from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import json


engine = create_engine('sqlite:///pubmed_search.db', echo = True)
Base = declarative_base()
 

class PubMedSearch(Base):
    __tablename__ = "search_config"
 
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    query_words = Column(String)  
    email = Column(String(256), unique=True)
    schedule_interval = Column(String(256)) 
    
    def __init__(self, user_id, email, query_words, schedule_interval):
        self.user_id = user_id
        self.query_words = query_words   
        self.email = email
        self.schedule_interval = schedule_interval

Base.metadata.create_all(engine)


#############################
# db methods
############################

def check_record_exists(user):
    with Session(engine) as session:
        return session.query(PubMedSearch).filter_by(user_id=user).first()


def create_query(user, user_query):
    with Session(engine) as session:
        query_record = PubMedSearch(user_id=user, 
                                    query_words=user_query['keywords'],
                                    email=user_query['email'],
                                    schedule_interval=user_query['interval'])
                                   
        session.add(query_record)
        session.commit()
     

def get_record_keywords(user):
    with Session(engine) as session:
        search_query = session.query(PubMedSearch).filter_by(user_id=user).first()
        return search_query.query_words

def get_record_email(user):
    with Session(engine) as session:
        search_query = session.query(PubMedSearch).filter_by(user_id=user).first()
        return search_query.email

def get_record_schedule_interval(user):
    with Session(engine) as session:
        search_query = session.query(PubMedSearch).filter_by(user_id=user).first()
        return search_query.schedule_interval


def update_email(user, email):
    with Session(engine) as session:
        user_record = session.query(PubMedSearch).filter_by(user_id=user).first()
        user_record.email = email
        session.commit()

def update_schedule_interval(schedule_interval, user):
    with Session(engine) as session:
        user_record = session.query(PubMedSearch).filter_by(user_id=user).first()
        user_record.schedule_interval = schedule_interval
        session.commit()

def update_keywords(user, query_words):
    with Session(engine) as session:
        user_record = session.query(PubMedSearch).filter_by(user_id=user).first()
        json_string = json.dumps(query_words)

        user_record.query_words = json_string
        session.commit()

def get_records_by_schedule_interval(schedule_interval):
    with Session(engine) as session:
        records = session.query(PubMedSearch).filter_by(schedule_interval=schedule_interval).all()
    return records
    


