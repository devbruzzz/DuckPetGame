from dataclasses import dataclass
from typing import List, Optional

from models.duck import DuckDad

@dataclass
class ShopItem:
    id: int
    name: str
    price: int
    description: str
    effect: str
    value: int = 0

# sistema de carteira e economia
class Wallet:
    def __init__(self, coins: int = 100):
        self.coins = max(0, coins)

    def can_buy(self, price: int) -> bool:
        return price <= self.coins

    def spend(self, price: int) -> bool:
        if price <= 0 or not self.can_buy(price):
            return False
        self.coins -= price
        return True

    def earn(self, amount: int) -> None:
        if amount > 0:
            self.coins += amount

    def __str__(self) -> str:
        return f"{self.coins} moedas"

# classe principal da loja
class Store:
    def __init__(self, items: Optional[List[ShopItem]] = None):
        self.items = items or []

    # configuracao dos itens padrao da loja
    @staticmethod
    def default() -> "Store":
        items = [
            ShopItem(
                id=1,
                name="Ração nutritiva",
                price=20,
                description="Reduz a fome e mantém o pato feliz.",
                effect="feed",
                value=30,
            ),
            ShopItem(
                id=2,
                name="Garrafa de água",
                price=15,
                description="Acaba com a sede e recupera energia.",
                effect="drink",
                value=30,
            ),
            ShopItem(
                id=3,
                name="Passeio de skate",
                price=25,
                description="O pato se diverte e o estresse diminui.",
                effect="relax",
            ),
            ShopItem(
                id=4,
                name="Cura do veterinário",
                price=40,
                description="Resolve problemas de saude e coloca o pato em forma.",
                effect="heal",
            ),
            ShopItem(
                id=5,
                name="Bebida especial",
                price=30,
                description="Alivia a abstinência e reduz a vontade de beber.",
                effect="alcohol",
                value=20,
            ),
            ShopItem(
                id=6, 
                name="Maço de cigarro", 
                price=15, 
                description="Diminui o estresse rapidamente.", 
                effect="smoke", 
                value=25
            ),
        ]
        return Store(items)

    # sistema de formatacao da prateleira
    def list_items(self) -> List[str]:
        lines = []
        for item in self.items:
            lines.append(
                f"{item.id}. {item.name} - {item.price} moedas\n   {item.description}"
            )
        return lines

    # sistema de busca de item
    def find_item(self, item_id: int) -> Optional[ShopItem]:
        return next((item for item in self.items if item.id == item_id), None)

    # sistema de processamento de compra
    def purchase(self, item_id: int, wallet: Wallet, duck: DuckDad) -> str:
        item = self.find_item(item_id)
        if item is None:
            return "Produto nao encontrado."

        if not wallet.can_buy(item.price):
            return "Saldo insuficiente."

        wallet.spend(item.price)
        return self.apply_item(item, duck)

    # sistema de aplicacao do efeito do item no pato
    def apply_item(self, item: ShopItem, duck: DuckDad) -> str:
        if item.effect == "feed":
            return duck.feed(item.value)
        if item.effect == "drink":
            return duck.drink(item.value)
        if item.effect == "relax":
            return duck.play()
        if item.effect == "heal":
            return duck.heal()
        if item.effect == "alcohol":
            return duck.drinking_alcohol(item.value)
        if item.effect == "smoke":
            return duck.smoking(item.value)
        return "O item foi comprado, mas nada aconteceu."