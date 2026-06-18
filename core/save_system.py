import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# sistema de configuracao de pasta segura
def _get_save_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    save_dir = base / "DuckPetGame"
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir

# variaveis globais de arquivo
SAVE_FILE = _get_save_dir() / "save.json"
BACKUP_FILE = _get_save_dir() / "save_backup.json"

# sistema de salvar os dados no json
def save_game(duck, wallet, turno: int, filhote=None) -> None:
    if SAVE_FILE.exists():
        try:
            SAVE_FILE.replace(BACKUP_FILE)
        except Exception:
            pass

    data = {
        "versao": "1.1",
        "salvo_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "turno": turno,
        "moedas": wallet.coins,
        "pato": {
            "nome": duck.name,
            "fome": duck._hunger,
            "sede": duck._thirst,
            "estresse": duck._stress,
            "alcool": duck._alcohol,
            "doente": duck._is_sick,
            "fumante": duck._is_smoker,
            "alcoolatra": duck._is_alcoholic,
        },
        "filhote": None if filhote is None else {
            "nome": filhote.name,
            "fome": filhote._hunger,
            "sede": filhote._thirst,
            "estresse": filhote._stress,
            "doente": filhote._is_sick,
        },
    }

    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n Jogo salvo em: {SAVE_FILE}")
    except Exception as e:
        print(f"\n Erro ao salvar: {e}")

# sistema de leitura e carregamento do save
def load_game() -> Optional[dict]:
    for arquivo in (SAVE_FILE, BACKUP_FILE):
        if not arquivo.exists():
            continue
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                data = json.load(f)
            if arquivo == BACKUP_FILE:
                print(" Save principal corrompido. Carregando backup...")
            return data
        except (json.JSONDecodeError, KeyError):
            continue

    return None

# sistema de exclusao de save
def delete_save() -> bool:
    apagou = False
    for arquivo in (SAVE_FILE, BACKUP_FILE):
        if arquivo.exists():
            arquivo.unlink()
            apagou = True
    return apagou

# sistema de checagem
def save_exists() -> bool:
    return SAVE_FILE.exists() or BACKUP_FILE.exists()

# sistema de texto de informacoes do save
def save_info() -> str:
    data = load_game()
    if data is None:
        return " Nenhum save encontrado. Comecando um novo jogo!"
    info = (
        f" Save encontrado!\n"
        f" Pato: {data['pato']['nome']}  | "
        f"Turno: {data['turno']}  | "
        f"Moedas: {data['moedas']}  | "
        f"Salvo em: {data['salvo_em']}"
    )
    filhote = data.get("filhote")
    if filhote:
        info += f"\n Filhote: {filhote['nome']}"
    return info