from typing import Optional
from product_manager.models import Product
from product_manager.repositories.repository import ProductRepository
from product_manager.validators.product_validator import ProductValidator

class ProductUpdater:
    def __init__(self, repository: ProductRepository, validator: ProductValidator):
        self.repository = repository
        self.validator = validator

    def update(self, product_id: int, name: str, description: str, price: float, category: str) -> Product:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError("Produit non trouvé.")

        self.validator.validate(name, price)

        product.name = name
        product.description = description
        product.price = price
        product.category = category
        self.repository.update(product)
        return product