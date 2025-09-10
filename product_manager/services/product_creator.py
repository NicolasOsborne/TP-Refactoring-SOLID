from product_manager.models.product_model import Product
from product_manager.validators.product_validator import ProductValidator
from product_manager.interfaces.product_repositories import IProductWriter

class ProductCreator:
    def __init__(self, repository: IProductWriter, validator: ProductValidator):
        self.repository = repository
        self.validator = validator

    def create(self, name: str, description: str, price: float, category: str) -> Product:
        self.validator.validate(name, price)
        product = Product(name=name, description=description, price=price, category=category)
        return self.repository.add(product)