from app.db import engine
from app.models import Base


try:
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы")
except Exception as e:
    print("Не получилось создать таблицы")
    raise e
