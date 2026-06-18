import random

from core.events import EventManager
from core.save_system import save_game, load_game, delete_save, save_info
from core.store import Store, Wallet

from minigames.car_racing import CarRacing
from minigames.dice_game import DiceGame
from minigames.hangman_game import HangmanGame

from models.duck import DuckDad, DuckSon

from ui.display import (
    exibir_status,
    exibir_menu_principal,
    exibir_loja,
    mensagem_evento,
    tela_game_over,
)

class Game:
    # sistema de inicializacao do jogo
    def __init__(self, duck_name: str = "Pato", starting_coins: int = 100):
        self.duck = DuckDad(duck_name)
        self.filhote = None
        self.wallet = Wallet(starting_coins)
        self.store = Store.default()
        self.event_manager = EventManager()
        self.turno = 0
        self.rodando = True

    # sistema de salvamento
    def salvar(self) -> None:
        save_game(self.duck, self.wallet, self.turno, self.filhote)

    # sistema de carregamento
    def carregar(self, data: dict) -> None:
        pato_data = data["pato"]
        self.duck.name        = pato_data["nome"]
        self.duck._hunger     = pato_data["fome"]
        self.duck._thirst     = pato_data["sede"]
        self.duck._stress     = pato_data["estresse"]
        self.duck._alcohol    = pato_data["alcool"]
        self.duck._is_sick    = pato_data["doente"]
        self.duck._is_smoker  = pato_data["fumante"]
        self.duck._is_alcoholic = pato_data["alcoolatra"]
        self.wallet.coins     = data["moedas"]
        self.turno            = data["turno"]

        filhote_data = data.get("filhote")
        if filhote_data:
            self.filhote = DuckSon(filhote_data["nome"])
            self.filhote._hunger  = filhote_data["fome"]
            self.filhote._thirst  = filhote_data["sede"]
            self.filhote._stress  = filhote_data["estresse"]
            self.filhote._is_sick = filhote_data["doente"]
        else:
            self.filhote = None

    # acao basica de compra
    def buy(self, item_id: int) -> str:
        return self.store.purchase(item_id, self.wallet, self.duck)

    # acao de abrir a loja interativa
    def _acao_loja(self):
        while True:
            texto_loja = "\n".join(self.store.list_items())
            op = exibir_loja(texto_loja)
            
            if op == "0":
                break
            try:
                item_id = int(op)
            except ValueError:
                mensagem_evento("ID inválido.")
                continue

            item = self.store.find_item(item_id)
            if item is None:
                mensagem_evento("Produto não encontrado.")
                continue

            # se houver filhote, pergunta em qual dos dois usar o item
            alvo = self.duck
            if self.filhote is not None:
                escolha = input(
                    f"  Usar em quem? [1] {self.duck.name}  [2] {self.filhote.name} (filhote): "
                ).strip()
                if escolha == "2":
                    alvo = self.filhote

            # filhote nao pode usar itens de vicio (cigarro/alcool)
            if isinstance(alvo, DuckSon) and item.effect in ("smoke", "alcohol"):
                mensagem_evento(f"{alvo.name} é um filhote e não pode usar esse item.")
                continue

            resultado = self.store.purchase(item_id, self.wallet, alvo)
            mensagem_evento(resultado)

    # acao do minigame de corrida
    def _acao_corrida(self):
        msg, reward = CarRacing().play()
        self.wallet.earn(reward)
        mensagem_evento(f"{msg}\n  +{reward} moedas  |  total: {self.wallet}")

    # acao do minigame de forca
    def _acao_forca(self):
        msg, reward = HangmanGame().play()
        self.wallet.earn(reward)
        mensagem_evento(f"{msg}\n  +{reward} moedas  |  total: {self.wallet}")

    # acao do minigame de dados
    def _acao_dados(self):
        msg, _ = DiceGame().play(self.wallet)
        mensagem_evento(msg)

    # acao de conversar e interagir
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
        self.duck._stress = max(0, self.duck._stress - 5)

    # acao de mudanca de nome
    def _acao_mudar_nome(self):
        print("\n" + "="*44)
        novo_nome = input("  Digite o novo nome do pato: ").strip()
        if novo_nome:
            msg = self.duck.change_name(novo_nome)
            mensagem_evento(msg)
        else:
            mensagem_evento("Nome inválido.")

    # acao de criar um filho
    def _acao_reproduzir(self):
        print("\n" + "="*44)

        if self.filhote is not None:
            mensagem_evento(
                f"{self.duck.name} já tem um filhote, {self.filhote.name}.\n"
                f"  Cuide bem dele antes de pensar em outro!"
            )
            return

        print(f"  Um filhote vai nascer e ficar ao lado de {self.duck.name}.")
        confirmacao = input("  Tem certeza que deseja continuar? (s/n): ").strip().lower()
        if confirmacao == "s":
            nome_filhote = input("  Qual sera o nome do filhote? ").strip()
            if not nome_filhote:
                nome_filhote = "Duckinho Jr"

            self.filhote = self.duck.reproduce(nome_filhote)
            mensagem_evento(
                f" Um ovo chocou! Bem-vindo, {self.filhote.name}!\n"
                f"  Agora sao 2 patos para cuidar."
            )

    # sistema de morte do pato
    def _verificar_game_over(self) -> bool:
        if self.duck.hunger >= 100 and self.duck.stress >= 100:
            return True
        if self.duck.hunger >= 100 and self.duck.thirst >= 100:
            return True
        if self.filhote is not None:
            if self.filhote.hunger >= 100 and self.filhote.stress >= 100:
                return True
            if self.filhote.hunger >= 100 and self.filhote.thirst >= 100:
                return True
        return False

    # loop central do jogo
    def rodar(self):
        while self.rodando:
            self.turno += 1
            exibir_status(self.duck, self.wallet, self.turno, self.filhote)

            # verifica game over
            if self._verificar_game_over():
                tela_game_over(self.duck, self.turno)
                # apaga o save ao perder
                delete_save()
                self.rodando = False
                break

            opcao = exibir_menu_principal()

            if opcao == "1":
                self._acao_loja()
            elif opcao == "2":
                self._acao_corrida()
            elif opcao == "3":
                self._acao_dados()
            elif opcao == "4":
                self._acao_forca()
            elif opcao == "5":
                self._acao_conversar()
            elif opcao == "6":
                mensagem_evento("O tempo passou...")
            elif opcao == "7":
                self._acao_mudar_nome()
            elif opcao == "8":
                self._acao_reproduzir()
            elif opcao == "0":
                self.salvar()
                print(f"\n  Ate logo! {self.duck.name} vai sentir sua falta. 🦆")
                self.rodando = False
                break
            else:
                mensagem_evento("Opção inválida. O pato te encarou em silencio.")

            # sorteio de imprevistos
            mensagem = self.event_manager.trigger_event(self.duck, self.wallet)
            
            if mensagem:
                mensagem_evento(mensagem)

            self.salvar()
            self.duck.pass_time()
            if self.filhote is not None:
                self.filhote.pass_time()