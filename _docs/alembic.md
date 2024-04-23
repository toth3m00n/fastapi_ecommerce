### Настройка alembic

+ Сначала надо создать окружение

```alembic init app/migrations```

---

1. заходим в ```alembic.ini``` и находим **sqlalchemy.url**
вставляем свой url. В моем случае это ```sqlalchemy.url =sqlite:///ecommerce.db```

2. далее идем в ```env.py``` и устанавливаем ```target_metadata = Base.metadata```
где **Base** это наша базовая модель для SQLAlchemy, от которой 
мы наследовались

3. не забываем делать перед пунктом 2 
```
from app.models.category import Category
from app.models.products import Product
```
импорт своих моделей, чтобы их было видно еще до настройки alembic


---
### Миграции

+ ``` alembic revision --autogenerate -m "Initial migration" ``` -
инициализация миграции

+ ```alembic upgrade head``` - выполнение миграции

---

#### Перечень возможных комманд

+ ```alembic upgrade +2``` две версии включая текущую для апгрейда
+ ```alembic downgrade -1``` на предыдущую для даунгрейда
+ ```alembic current``` получить информацию о текущей версии
+ ```alembic history``` --verbose история миграций
+ ```alembic downgrade``` base даунгрейд в самое начало
+ ```alembic upgrade head``` апгрейд до самого конца