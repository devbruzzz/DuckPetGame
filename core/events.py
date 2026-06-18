import random
from typing import Optional

class EventManager:
    def __init__(self):
        pass

    # sistema de sorteio de evento
    def trigger_event(self, duck, wallet) -> Optional[str]:
        # 25% de chance de ocorrer um evento
        if random.randint(1, 100) > 25:
            return None

        events = [
            self.find_food,
            self.find_water,
            self.bad_night,
            self.party,
            self.rain,
            self.get_sick,
            self.win_money,
            self.lonely_day
        ]

        event = random.choice(events)
        return event(duck, wallet)

    # -------------------------
    # EVENTOS
    # -------------------------

    # evento de achar comida
    def find_food(self, duck, wallet):
        duck._hunger = max(0, duck._hunger - 15)
        duck._check_limits()
        return f"🍞 {duck.name} encontrou comida na rua! (-15 fome)"

    # evento de achar agua
    def find_water(self, duck, wallet):
        duck._thirst = max(0, duck._thirst - 15)
        duck._check_limits()
        return f"🚰 {duck.name} encontrou uma poca de agua. (-15 sede)"

    # evento de insonia
    def bad_night(self, duck, wallet):
        duck._stress = min(100, duck._stress + 20)
        duck._check_limits()
        return f"🌙 {duck.name} teve uma noite ruim. (+20 estresse)"

    # evento de festa
    def party(self, duck, wallet):
        duck._stress = max(0, duck._stress - 20)
        duck._alcohol = min(100, duck._alcohol + 10)
        duck._check_limits()
        return f"🎉 {duck.name} foi para uma festa! (-20 estresse, +10 abstinencia)"

    # evento de chuva
    def rain(self, duck, wallet):
        duck._thirst = max(0, duck._thirst - 10)
        duck._stress = max(0, duck._stress - 10)
        duck._check_limits()
        return f"🌧️ Um dia chuvoso deixou {duck.name} relaxado."

    # evento de doenca surpresa
    def get_sick(self, duck, wallet):
        if duck._hunger > 70 or duck._thirst > 70:
            duck._is_sick = True
            return f"🤒 {duck.name} ficou doente por falta de cuidados!"
        return None

    # evento de achar dinheiro
    def win_money(self, duck, wallet):
        achadas = random.randint(10, 30)
        wallet.earn(achadas)
        return f"💰 {duck.name} encontrou {achadas} moedas perdidas!"

    # evento de solidao
    def lonely_day(self, duck, wallet):
        duck._stress = min(100, duck._stress + 15)
        duck._check_limits()
        return f"😔 {duck.name} passou o dia sozinho. (+15 estresse)"