from product_manager.models import Product
from product_manager.repositories.repository import ProductRepository
from product_manager.validators.product_validator import ProductValidator

class ProductCreator:
    def __init__(self, repository: ProductRepository, validator: ProductValidator):
        self.repository = repository
        self.validator = validator

    def create(self, name: str, description: str, price: float, category: str) -> Product:
        self.validator.validate(name, price)
        product = Product(name=name, description=description, price=price, category=category)
        return self.repository.add(product)