import datetime
import json
import sqlalchemy
from sqlalchemy.orm import  sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = "postgresql://postgres:gearsofwar2@localhost:5432/test"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/test_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

print ('Выберите тип поиска 1 - по id издателя , 2 - по названию:')
couse = int(input())
if couse == 1 :
    print ('Введите id издателя:')
    couse = int(input())
    q =  session.query(Book).with_entities(Book.title, Shop.name, Sale.price, Sale.date_sale)\
        .join(Publisher, Publisher.id == Book.id_publisher)\
        .join(Stock, Stock.id_book == Book.id)\
        .join(Shop, Shop.id == Stock.id_shop)\
        .join(Sale, Sale.id_stock == Stock.id).filter(Publisher.id == couse).all()
    for s in q :
        formatted_datetime = s[3].strftime("%d-%m-%Y")
        print (f'{s[0]}|{s[1]}|{s[2]}|{formatted_datetime}')
else:
    print ('Введите название:')
    couse = f'%{input()}%'
    q =  session.query(Book).with_entities(Book.title, Shop.name, Sale.price, Sale.date_sale)\
        .join(Publisher, Publisher.id == Book.id_publisher)\
        .join(Stock, Stock.id_book == Book.id)\
        .join(Shop, Shop.id == Stock.id_shop)\
        .join(Sale, Sale.id_stock == Stock.id).filter(Publisher.name.ilike(couse)).all()
    for s in q :
        formatted_datetime = s[3].strftime("%d-%m-%Y")
        print (f'{s[0]}|{s[1]}|{s[2]}|{formatted_datetime}')