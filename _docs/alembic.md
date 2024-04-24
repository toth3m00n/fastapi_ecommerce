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

--- 

### Асинхронный alembic

1. Среда ```alembic init -t async app/migrations```
2. создание миграций ```alembic revision --autogenerate -m "Initial migration"```
3. применение миграций ```alembic upgrade head```

--- 

#### Наполнение БД

```angular2html
INSERT INTO public.category (id, name, slug, is_active, parent_id) VALUES (1, 'Apple', 'apple', true, null);
INSERT INTO public.category (id, name, slug, is_active, parent_id) VALUES (2, 'Смартфоны', 'smartfony', true, 1);
INSERT INTO public.category (id, name, slug, is_active, parent_id) VALUES (3, 'Ноутбуки', 'noutbuki', true, 1);
INSERT INTO public.category (id, name, slug, is_active, parent_id) VALUES (4, 'Планшеты', 'planshety', true, 1);
INSERT INTO public.category (id, name, slug, is_active, parent_id) VALUES (5, 'Asus', 'asus', true, null);
```

```angular2html
INSERT INTO public.product (id, name, slug, description, price, image_url, stock, category_id, rating, is_active) VALUES (1, 'IPhone 15', 'iphone-15', 'string', 100000, 'string', 10, 2, 0, true);
INSERT INTO public.product (id, name, slug, description, price, image_url, stock, category_id, rating, is_active) VALUES (2, 'IPhone 14', 'iphone-14', 'string', 80000, 'string', 15, 2, 0, true);
INSERT INTO public.product (id, name, slug, description, price, image_url, stock, category_id, rating, is_active) VALUES (3, 'IPhone 13', 'iphone-13', 'string', 72000, 'string', 5, 2, 0, true);
INSERT INTO public.product (id, name, slug, description, price, image_url, stock, category_id, rating, is_active) VALUES (4, 'IPhone 12', 'iphone-12', 'string', 65000, 'string', 2, 2, 0, true);
INSERT INTO public.product (id, name, slug, description, price, image_url, stock, category_id, rating, is_active) VALUES (5, 'MacBook Air', 'macbook-air', 'string', 90000, 'string', 8, 3, 0, true);
INSERT INTO public.product (id, name, slug, description, price, image_url, stock, category_id, rating, is_active) VALUES (6, 'MacBook Pro', 'macbook-pro', 'string', 140000, 'string', 11, 3, 0, true);
INSERT INTO public.product (id, name, slug, description, price, image_url, stock, category_id, rating, is_active) VALUES (7, 'iPad (9th Gen)', 'ipad-9th-gen', 'string', 35000, 'string', 30, 4, 0, true);
INSERT INTO public.product (id, name, slug, description, price, image_url, stock, category_id, rating, is_active) VALUES (8, 'iPad (10th Gen)', 'ipad-10th-gen', 'string', 52000, 'string', 20, 4, 0, true);
```