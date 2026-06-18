import os

LARGURA_TELA = 44

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# funcoes auxiliares de interface
def _linha(caractere="="):
    return caractere * LARGURA_TELA

def _cabecalho(titulo):
    print(_linha())
    print(f"  {titulo}")
    print(_linha())

def barra_progresso(valor, maximo=100, tamanho=20):
    valor = max(0, min(valor, maximo))
    preenchido = int((valor / maximo) * tamanho)
    vazio = tamanho - preenchido
    return f"[{'█' * preenchido}{'░' * vazio}] {valor}/{maximo}"

def _linha_status(rotulo, valor):
    return f"  {rotulo:<18}{barra_progresso(valor)}"

# artes do pato em ascii
_PATO_FELIZ = r"""
      __
    <(^ )_    ♪
     ( ._> /
      `---'
"""

_PATO_NORMAL = r"""
      __
    <(o )_
     ( ._> /
      `---'
"""

_PATO_COM_FOME = r"""
      __
    <(o )_    barriga roncando
     ( ._> /
      `---'
"""

_PATO_ESTRESSADO = r"""
      __
    <(>~<)__
     ( ._> /
      `---'
"""

_PATO_DOENTE = r"""
      __
    <(x )_    
     ( ._> /
      `---'
"""

_PATO_FUMANDO_BEBENDO = r"""
      __
    <(o )_    cigarro na asa
     ( ._> /  copo de bebida do lado
      `---'
"""

# sistema de desenho do pato baseado nos status
def desenhar_pato(duck):
    if duck.is_sick:
        return _PATO_DOENTE
    if duck.stress >= 70 and duck.alcohol >= 70:
        return _PATO_FUMANDO_BEBENDO
    if duck.stress >= 70:
        return _PATO_ESTRESSADO
    if duck.hunger >= 70 or duck.thirst >= 70:
        return _PATO_COM_FOME
    if duck.hunger <= 20 and duck.thirst <= 20 and duck.stress <= 20:
        return _PATO_FELIZ
    return _PATO_NORMAL

# sistema de exibicao de status
def exibir_status(duck, wallet, turno):
    limpar_tela()
    _cabecalho(f" TERMINAL DUCK  -  Turno {turno}")
    print(desenhar_pato(duck))
    print(f"  Nome:  {duck.name}")
    print(f"  Saldo: {wallet}")
    print()
    print(_linha_status("Fome:", duck.hunger))
    print(_linha_status("Sede:", duck.thirst))
    print(_linha_status("Estresse:", duck.stress))
    print(_linha_status("Vontade de beber:", duck.alcohol))
    print()
    
    # mensagens de status
    if duck.hunger == 0:
        print(f"  {duck.name} esta de barriga cheia!")
    elif duck.hunger >= 85:
        print(f"  {duck.name} esta com muita fome. Alimente ele agora!")

    if duck.thirst == 0:
        print(f"  {duck.name} esta totalmente hidratado!")
    elif duck.thirst >= 85:
        print(f"  {duck.name} esta com sede. De agua para ele!")

    if duck.stress == 0:
        print(f"  {duck.name} esta totalmente relaxado!")
    elif duck.stress >= 85:
        print(f"  {duck.name} esta muito estressado. Ajude ele a relaxar!")

    if duck.alcohol == 0:
        print(f"  A vontade de beber alcool de {duck.name} esta saciada!")
    elif duck.alcohol >= 85:
        print(f"  {duck.name} esta em crise de abstinencia! De alcool para ele!")
    
    if duck.is_sick:
        print()
        print("   O pato esta doente! Leve-o ao veterinario na loja.")
        
    print()
    print(_linha())

# sistema do menu principal
def exibir_menu_principal():
    print()
    print("  O que voce quer fazer?")
    print("  1. Ir a loja")
    print("  2. Jogar corrida de carros (ganhar moedas)")
    print("  3. Jogar dados (apostar moedas)")
    print("  4. Jogar forca do pato (ganhar moedas)")
    print("  5. Conversar com o pato")
    print("  6. Deixar o tempo passar")
    print("  7. Trocar o nome do pato")
    print("  8. Ter um filhote (Aposentar o atual)")
    print("  0. Sair do jogo")
    print()
    return input("  Escolha uma opcao: ").strip()

# sistema da loja visual
def exibir_loja(texto_loja):
    limpar_tela()
    _cabecalho(" LOJA DO PATO")
    print()
    print(texto_loja)
    print()
    print("  0. Voltar ao menu principal")
    print()
    return input("  Digite o ID do item que deseja comprar: ").strip()

# sistema de popup de mensagens
def mensagem_evento(mensagem):
    print()
    print(_linha("-"))
    for linha_texto in str(mensagem).split("\n"):
        print(f"  {linha_texto}")
    print(_linha("-"))
    input("\n  Pressione ENTER para continuar...")

# sistema da tela de derrota
def tela_game_over(duck, turno):
    limpar_tela()
    _cabecalho("GAME OVER")
    print(desenhar_pato(duck))
    print(f"  {duck.name} nao aguentou mais o descuido...")
    print(f"  O jogo durou {turno} turno(s).")
    print()
    print(_linha())
    input("\n  Pressione ENTER para sair...")