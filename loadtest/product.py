import copy
import random
from typing import Any

from faker import Faker

PRODUCT_TYPES = ["Điện thoại", "Tai nghe", "Ốp lưng", "Sạc dự phòng", "Cáp sạc", "Loa"]
BRANDS = ["Sao Mai", "Hồng Hà", "Phương Nam", "Đại Việt", "Thiên Long"]
COLORS = ["Đỏ", "Xanh", "Đen", "Trắng", "Vàng", "Hồng"]
SIZES = ["S", "M", "L", "XL"]
UNITS = ["PCS", "BOX", "SET", "PACK"]
ASSET_TYPES = ["Single", "Bundle"]
CATEGORIES = {
    "CAT01": "Điện thoại",
    "CAT02": "Phụ kiện",
    "CAT03": "Âm thanh",
    "CAT04": "Khuyến mãi",
}

MUTABLE_FIELDS = ["color", "size", "productName", "description", "isActive"]

Product = dict[str, Any]


class ProductFaker:
    def __init__(self, seed: int) -> None:
        self.fake = Faker("vi_VN")
        self.fake.seed_instance(seed)  # same seed -> same data on every run
        self.random = random.Random(seed)
        self.products: dict[str, Product] = {}
        self._next_product_id = 1

    def new_product(self) -> Product:
        sku = self.fake.unique.bothify("SKU-#####")
        product: Product = {
            "productId": self._next_product_id,
            "sku": sku,
            "partnerSKU": f"P-{sku.removeprefix('SKU-')}",
            "productName": self._product_name(),
            "assetType": self.random.choice(ASSET_TYPES),
            "color": self.random.choice(COLORS),
            "size": self.random.choice(SIZES),
            "description": self.fake.sentence(nb_words=8),
            "isActive": True,
            "hasSerial": self.random.random() < 0.2,
            "hasExpiration": self.random.random() < 0.1,
            "units": self.random.sample(UNITS, k=self.random.randint(1, 2)),
            "categories": [
                {"categoryCode": code, "categoryName": CATEGORIES[code]}
                for code in self.random.sample(
                    list(CATEGORIES), k=self.random.randint(1, 2)
                )
            ],
        }
        self._next_product_id += 1
        self.products[sku] = product
        return copy.deepcopy(product)

    def _product_name(self) -> str:
        return (
            f"{self.random.choice(PRODUCT_TYPES)} {self.random.choice(BRANDS)} "
            f"{self.random.randint(1, 999)}"
        )
