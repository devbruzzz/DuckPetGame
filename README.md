# DuckPetGame
## Como jogar

1. Execute o jogo:

```bash
python main.py

```

2. No terminal interativo, crie o jogo e confira o status:

```python
from core.game_loop import Game

game = Game("Duckinho", starting_coins=100)
# a interface visual é exibida automaticamente ao rodar o game.rodar()

```

3. Ver a loja disponível:

```python
# a loja é exibida automaticamente ao selecionar a opção 1 no menu

```

4. Comprar um item:

```python
# a compra é feita selecionando o ID do item dentro do menu da loja

```

5. Jogar a corrida para ganhar moedas:

```python
# o minigame é acessado selecionando a opção 2 no menu principal

```

## Itens da loja

* Racao nutritiva: reduz fome e deixa o pato mais feliz.
* Garrafa de agua: reduz sede.
* Brinquedo relaxante: diminui estresse.
* Cura do veterinario: cura o pato quando ele fica doente.
* Bebida especial: reduz a vontade de beber.
* Maco de cigarro: diminui o estresse rapidamente.

## Economia

* O jogador começa com moedas no Wallet.
* Cada compra gasta moedas.
* Os minigames recompensam moedas conforme o desempenho.

## Arquivos importantes

* `main.py` – ponto de entrada do jogo.
* `core/store.py` – loja, itens e carteira.
* `core/game_loop.py` – lógica principal do jogo.
* `models/duck.py` – modelo de status do pato.
* `minigames/car_racing.py` – minigame que gera moedas.
* `ui/display.py` – interface visual.