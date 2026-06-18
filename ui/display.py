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

# artes do filhote em ascii (visual proprio, mais simples que o pato adulto)
_FILHOTE_FELIZ = r"""
      __
    <(^ )_    ♪
     (_ ->/
"""

_FILHOTE_NORMAL = r"""
      __
    <(o )_
     (_ ->/
"""

_FILHOTE_COM_FOME = r"""
      __
    <(o )_    barriga roncando
     (_ ->/
"""

_FILHOTE_ESTRESSADO = r"""
      __
    <(>~)__
     (_ ->/
"""

_FILHOTE_DOENTE = r"""
      __
    <(x )_
     (_ ->/
"""

# sistema de desenho do filhote baseado nos status (filhote nunca fica em
# estado de fumando/bebendo pois ele nao pode se viciar)
def desenhar_filhote(filhote):
    if filhote.is_sick:
        return _FILHOTE_DOENTE
    if filhote.stress >= 70:
        return _FILHOTE_ESTRESSADO
    if filhote.hunger >= 70 or filhote.thirst >= 70:
        return _FILHOTE_COM_FOME
    if filhote.hunger <= 20 and filhote.thirst <= 20 and filhote.stress <= 20:
        return _FILHOTE_FELIZ
    return _FILHOTE_NORMAL

# junta duas artes ascii lado a lado (usado para mostrar pato + filhote)
def _lado_a_lado(arte_esquerda, arte_direita, espaco=4):
    linhas_esq = arte_esquerda.strip("\n").split("\n")
    linhas_dir = arte_direita.strip("\n").split("\n")
    altura = max(len(linhas_esq), len(linhas_dir))
    linhas_esq += [""] * (altura - len(linhas_esq))
    linhas_dir += [""] * (altura - len(linhas_dir))
    largura_esq = max((len(l) for l in linhas_esq), default=0)

    resultado = []
    for esq, dir in zip(linhas_esq, linhas_dir):
        resultado.append(f"{esq.ljust(largura_esq)}{' ' * espaco}{dir}")
    return "\n".join(resultado)

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
def exibir_status(duck, wallet, turno, filhote=None):
    limpar_tela()
    _cabecalho(f" TERMINAL DUCK  -  Turno {turno}")

    if filhote is not None:
        print(_lado_a_lado(desenhar_pato(duck), desenhar_filhote(filhote)))
        print(f"  Nome:  {duck.name}" + " " * 10 + f"Filhote: {filhote.name}")
    else:
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
        print(f"  {duck.name} está de barriga cheia!")
    elif duck.hunger >= 85:
        print(f"  {duck.name} está com muita fome. Alimente ele agora!")

    if duck.thirst == 0:
        print(f"  {duck.name} está totalmente hidratado!")
    elif duck.thirst >= 85:
        print(f"  {duck.name} está com sede. De agua para ele!")

    if duck.stress == 0:
        print(f"  {duck.name} está totalmente relaxado!")
    elif duck.stress >= 85:
        print(f"  {duck.name} está muito estressado. Ajude ele a relaxar!")

    if duck.alcohol == 0:
        print(f"  A vontade de beber álcool de {duck.name} está saciada!")
    elif duck.alcohol >= 85:
        print(f"  {duck.name} está em crise de abstinencia! De álcool para ele!")
    
    if duck.is_sick:
        print()
        print("   O pato está doente! Leve-o ao veterinario na loja.")

    # status do filhote (sem barra de alcool, pois ele nao pode se viciar)
    if filhote is not None:
        print()
        print(_linha("-"))
        print(f"  Status de {filhote.name} (filhote):")
        print(_linha_status("Fome:", filhote.hunger))
        print(_linha_status("Sede:", filhote.thirst))
        print(_linha_status("Estresse:", filhote.stress))
        print()

        if filhote.hunger >= 85:
            print(f"  {filhote.name} está com muita fome. Alimente ele agora!")
        if filhote.thirst >= 85:
            print(f"  {filhote.name} está com sede. De agua para ele!")
        if filhote.stress >= 85:
            print(f"  {filhote.name} está muito estressado. Ajude ele a relaxar!")
        if filhote.is_sick:
            print(f"   {filhote.name} está doente! Leve-o ao veterinario na loja.")
        
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
    print("  8. Ter um filhote")
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
    print(f"  {duck.name} não aguentou mais o descuido...")
    print(f"  O jogo durou {turno} turno(s).")
    print()
    print(_linha())
    input("\n  Pressione ENTER para sair...")