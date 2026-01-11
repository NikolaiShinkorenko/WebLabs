import json
import random

from app.db import Session
from app.models import Car, Dealer

session = Session()

dealers = session.query(Dealer).all()

if not dealers:
    raise Exception('Нет дилеров в БД')

with open('cars.json', encoding='utf-8') as f:
    cars_data = json.load(f)['cars']

for data in cars_data:
    dealer = random.choice(dealers)

    car = Car(
        firm=data['firm'],
        model=data['model'],
        year=data['year'],
        power=data['power'],
        color=data['color'],
        price=data['price'],
        dealer_id=dealer.id,
    )
    session.add(car)

try:
    session.commit()
    print('Автомобили загружены')
except:
    print('Не получилось загрузить автомобили')
finally:
    session.close()
