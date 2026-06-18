from core.game_loop import Game
from core.save_system import load_game, delete_save, save_info

# sistema de menu inicial
def _menu_inicial() -> str:
    print("=" * 45)
    print(" TERMINAL DUCK PET GAME ")
    print("=" * 45)
    print()
    print(save_info())
    print()

    data = load_game()
    if data:
        print("  O que deseja fazer?")
        print("  [1] Continuar jogo salvo")
        print("  [2] Novo jogo (apaga o save atual)")
        print("  [0] Sair")
        opcao = input("\n  Escolha: ").strip()
        if opcao == "1":
            return "continuar"
        elif opcao == "2":
            confirmacao = input(
                " Tem certeza? O save atual será APAGADO. (s/n): "
            ).strip().lower()
            if confirmacao == "s":
                delete_save()
                return "novo"
            return _menu_inicial() 
        else:
            return "sair"
    else:
        print("  [1] Começar novo jogo")
        print("  [0] Sair")
        opcao = input("\n  Escolha: ").strip()
        return "novo" if opcao == "1" else "sair"

# sistema de criacao de novo jogo
def _criar_novo_jogo() -> Game:
    print()
    nome = input("  Como vai se chamar seu pato? ").strip()
    if not nome:
        nome = "Duckinho"
    game = Game(duck_name=nome, starting_coins=100)
    print(f"\n  Bem-vindo, {nome}! Que a aventura comece. 🥚\n")
    return game

# sistema principal de execucao
def main():
    decisao = _menu_inicial()

    if decisao == "sair":
        print("\n Até logo! ")
        return

    if decisao == "continuar":
        game = Game()
        data = load_game()
        game.carregar(data)
        print(f"\n Jogo carregado! Continuando com {game.duck.name}...\n")
    else:
        game = _criar_novo_jogo()
        
    game.rodar()

if __name__ == "__main__":
    main()