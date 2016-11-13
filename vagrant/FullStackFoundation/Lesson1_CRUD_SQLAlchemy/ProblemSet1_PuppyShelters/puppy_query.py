from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy
import datetime

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# 1. Query all of the puppies and return the results in ascending alphabetical order
def query1():
    puppies = session.query(Puppy.name, Puppy.id).order_by(Puppy.name.asc()).all()
    for puppy in puppies:
        print('{name}, {id}'.format(name=puppy.name, id=puppy.id))


# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
def query2():
    sixMonthsAgo = datetime.date.today() - datetime.timedelta(days=180)
    puppies = session.query(Puppy)\
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)\
        .order_by(Puppy.dateOfBirth.desc()).all()
    for puppy in puppies:
        print('{name}, {dob}'.format(name=puppy.name, dob=puppy.dateOfBirth))


# 3. Query all puppies by ascending weight
def query3():
    puppies = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()
    for puppy in puppies:
        print('{name}, {weight}'.format(name=puppy.name, weight=puppy.weight))


# 4. Query all puppies grouped by the shelter in which they are staying
def query4():
    result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for item in result:
        print item[0].id, item[0].name, item[1]


if __name__ == '__main__':
    # query1()
    # query2()
    # query3()
    query4()
