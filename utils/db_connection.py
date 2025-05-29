from sqlalchemy import create_engine,Column,Integer,String,delete
from sqlalchemy.orm import sessionmaker, declarative_base


database_url = "mysql+mysqlconnector://root:shreya123@localhost/log_analyze_report_generate"



engine = create_engine(database_url)
Session = sessionmaker(bind = engine)
session = Session()

base = declarative_base()
class Error(base):
    __tablename__="Error"
    
    log_file = Column(String(100),primary_key = True) 
    #import pdb;pdb.set_trace()
    log_count = Column(Integer)

   
class Info(base):
    __tablename__="Info"
    
    log_file = Column(String(100),primary_key = True) 
    log_count = Column(Integer)

  
class Warning(base):
    __tablename__="Warning"
   
    log_file = Column(String(100),primary_key = True) 
    log_count = Column(Integer)

 
base.metadata.create_all(engine)

session.query(Error).delete()
session.query(Info).delete()
session.query(Warning).delete()
def add_into_db(file_name,log_types):
    
    #------------
    error = Error(log_file=file_name, log_count = log_types['error'])
    info = Info(log_file = file_name, log_count = log_types['info'])
    warning = Warning(log_file = file_name, log_count = log_types['warning'])
#------------------
    

#---------------------------

    session.add(error)
    session.add(info)
    session.add(warning)


    session.commit()




