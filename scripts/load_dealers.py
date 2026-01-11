import json 

from app.db import Session
from app.models import Dealer

session = Session()

with open('dealers.json', encoding='utf-8') as f:
    dealers_data = json.load(f)

for data in dealers_data:
    dealer = Dealer(
        name=data['Name'],
        city=data['City'],
        address=data['Address'],
        area=data['Area'],
        rating=data['Rating']
    )
    session.add(dealer)

try:
    session.commit()
    print('Диллеры загружены')
except:
    print('Не получилось загрузить диллеров')
finally:
    session.close()
