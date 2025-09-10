from typing import List, Optional
from product_manager.models import Product
from product_manager.interfaces.product_repositories import IProductRepository

class ProductRepository(IProductRepository):
    def __init__(self):
        self._products: dict[int, Product] = {}
        self._next_id = 1

    def add(self, product: Product) -> Product:
        product.id = self._next_id
        self._products[self._next_id] = product
        self._next_id += 1
        return product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    def get_all(self) -> List[Product]:
        return list(self._products.values())

    def update(self, product: Product) -> bool:
        if product.id in self._products:
            self._products[product.id] = product
            return True
        return False

    def delete(self, product_id: int) -> bool:
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False