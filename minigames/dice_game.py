import random
import time


class DiceGame:
    def __init__(self):
        self.aposta_minima = 10

    def play(self, wallet) -> tuple[str, int]:
        """
        Retorna (mensagem, ganho_liquido).
        ganho_liquido positivo = ganhou, negativo = perdeu, 0 = empate.
        """
        if wallet.coins < self.aposta_minima:
            return f"Você não tem moedas suficientes. (mínimo {self.aposta_minima})", 0

        print(f"\n  🎲 JOGO DE DADOS  |  Saldo: {wallet}")
        print(f"  Aposte um valor (mínimo {self.aposta_minima}):")
        try:
            aposta = int(input("  Aposta: ").strip())
        except ValueError:
            return "Valor inválido.", 0

        if aposta < self.aposta_minima:
            return f"Aposta mínima é {self.aposta_minima} moedas.", 0
        if not wallet.can_buy(aposta):
            return "Saldo insuficiente para essa aposta.", 0

        dado_jogador = random.randint(1, 6)
        dado_pato    = random.randint(1, 6)

        print(f"\n  Você tirou:  {dado_jogador} 🎲")
        time.sleep(0.6)
        print(f"  O pato tirou: {dado_pato} 🎲")
        time.sleep(0.8)

        if dado_jogador > dado_pato:
            wallet.earn(aposta)
            return f"Você venceu! +{aposta} moedas. Total: {wallet}", aposta
        elif dado_pato > dado_jogador:
            wallet.spend(aposta)
            return f"O pato venceu... -{aposta} moedas. Total: {wallet}", -aposta
        else:
            return "Empate! Ninguém ganhou nada.", 0