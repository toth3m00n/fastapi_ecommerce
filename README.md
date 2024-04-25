## FastApi Project

### Stack:

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SqlAlchemy-%2307405e.svg?&style=for-the-badge&logo=SqlAlchemy&logoColor=white")
![Alembic](https://img.shields.io/badge/Alembic-%23075e.svg?&style=for-the-badge&logo=Alembic&logoColor=white")
![Pydantic](https://img.shields.io/badge/Pydantic-%23e75e.svg?&style=for-the-badge&logo=Alembic&logoColor=white")

### About:

ecommerce shop

### Notes:

## Start

```
uvicorn app.main:app --reload [--port 8000] 
```
[you can change or skip]

+ Start database in docker + adminer
```angular2html
docker-compose up 
```
access to **adminer** you may get in url:
```angular2html
http://localhost:8080/
```
---

#### Fill db

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

---

#### Alembic

you can get access to info in the path
_docs/alembic.md

--- 

### Models: 

+ Product
+ Category
+ User

--- 

### Documentation

go to

```/docs```


---
### Common APIs

Api for
+ Delete
+ Create
+ Update
+ Get

---

also 
#### aouth2 system

---

**Roles**

- Admin (can do anything)
- Supplier (can add and update Product)
- Customer (can see product and category)