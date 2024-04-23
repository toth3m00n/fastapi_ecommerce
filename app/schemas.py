from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int # Количество товара в наличии,
    category: int


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None
