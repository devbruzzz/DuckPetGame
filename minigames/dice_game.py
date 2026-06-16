import random

from core.store import Store, Wallet
from minigames.car_racing import CarRacing
from minigames.dice_game import DiceGame
from models.duck import DuckDad
from ui.display import (
    exibir_status,
    exibir_menu_principal,
    exibir_loja,
    mensagem_evento,
    tela_game_over,
)


class Game:
    def __init__(self, duck_name: str = "Pato", starting_coins: int = 100):
        self.duck = DuckDad(duck_name)
        self.wallet = Wallet(starting_coins)
        self.store = Store.default()
        self.turno = 0
        self.rodando = True

    # ── helpers ──────────────────────────────────────────────

    def status_text(self) -> str:
        return (
            f"=== Status do jogo ===\n"
            f"Nome: {self.duck.name}\n"
            f"Saldo: {self.wallet}\n"
            f"Fome: {self.duck.hunger}\n"
            f"Sede: {self.duck.thirst}\n"
            f"Estresse: {self.duck.stress}\n"
            f"Vontade de beber: {self.duck.alcohol}\n"
            f"Doente: {'Sim' if self.duck.is_sick else 'Nao'}"
        )

    def shop_text(self) -> str:
        return "\n".join(self.store.list_items())

    def buy(self, item_id: int) -> str:
        return self.store.purchase(item_id, self.wallet, self.duck)

    def play_race(self) -> str:
        message, reward = CarRacing().play()
        self.wallet.earn(reward)
        self.duck.pass_time()
        return f"{message}\nVoce ganhou {reward} moedas e agora tem {self.wallet}."

    # ── ações do menu ─────────────────────────────────────────

    def _acao_loja(self):
        while True:
            op = exibir_loja(self.shop_text())
            if op == "0":
                break
            try:
                item_id = int(op)
                resultado = self.buy(item_id)
                mensagem_evento(resultado)
            except ValueError:
                mensagem_evento("ID inválido.")

    def _acao_corrida(self):
        msg, reward = CarRacing().play()
        self.wallet.earn(reward)
        mensagem_evento(f"{msg}\n  +{reward} moedas  |  total: {self.wallet}")

    def _acao_dados(self):
        msg, _ = DiceGame().play(self.wallet)
        mensagem_evento(msg)

    def _acao_conversar(self):
        frases_normais = [
            "QUACK! (oi, oi, oi!)",
            "quack... (tô entediado)",
            "QUACK QUACK! (me dá biscoito!)",
            "quack~ (gostei dessa conversa)",
        ]
        if self.duck.hunger >= 70:
            frase = "QUACK QUACK!! (COM FOME!! me alimenta!!)"
        elif self.duck.stress >= 70:
            frase = "quack... (muito estressado, preciso relaxar)"
        elif self.duck.alcohol >= 70:
            frase = "quaaaaack... (tô em crise, preciso da bebida)"
        elif self.duck.is_sick:
            frase = "quack... *tosse* (tô doente, leva no vet)"
        else:
            frase = random.choice(frases_normais)

        mensagem_evento(f"{self.duck.name} diz: {frase}")
        # conversar reduz estresse levemente
        self.duck._stress = max(0, self.duck._stress - 5)

    # ── verificações de fim de jogo ───────────────────────────

    def _verificar_game_over(self) -> bool:
        if self.duck.hunger >= 100 and self.duck.stress >= 100:
            return True
        if self.duck.hunger >= 100 and self.duck.thirst >= 100:
            return True
        return False

    # ── LOOP PRINCIPAL ────────────────────────────────────────

    def rodar(self):
        while self.rodando:
            self.turno += 1

            # 1. Exibe estado atual
            exibir_status(self.duck, self.wallet, self.turno)

            # 2. Verifica game over
            if self._verificar_game_over():
                tela_game_over(self.duck, self.turno)
                self.rodando = False
                break

            # 3. Lê ação do jogador
            opcao = exibir_menu_principal()

            # 4. Executa ação
            if opcao == "1":
                self._acao_loja()
            elif opcao == "2":
                self._acao_corrida()
            elif opcao == "3":
                self._acao_dados()
            elif opcao == "4":
                self._acao_conversar()
            elif opcao == "5":
                mensagem_evento("O tempo passou...")
            elif opcao == "0":
                print(f"\n  Até logo! {self.duck.name} vai sentir sua falta. 🦆")
                self.rodando = False
                break
            else:
                mensagem_evento("Opção inválida. O pato te olhou torto.")

            # 5. Passa o tempo — atributos se degradam a cada turno
            self.duck.pass_time()