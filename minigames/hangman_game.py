import random

class HangmanGame:
    def __init__(self):
        # palavras do jogo
        self.words = [
            "PATO", "LAGO", "CHAPEU", "QUACK", 
            "BICO", "PAVAO", "RACAO", "MOEDA", 
            "VETERINARIO", "BRINQUEDO", "CARRO", 
            "DADO", "LOJA", "MINIGAME", "ANIMAL",
        ]
        self.max_errors = 6
        self.reward = 30

    # sistema principal de adivinhacao
    def play(self) -> tuple[str, int]:
        word = random.choice(self.words)
        guessed_letters = set()
        errors = 0

        print("\n" + "="*35)
        print("JOGO DA FORCA DO PATO")
        print("="*35)
        print(f" Dica: Palavras do universo do jogo!\n Recompensa: {self.reward} moedas.")

        while errors < self.max_errors:
            display_word = "".join(
                [letter if letter in guessed_letters else "_" for letter in word]
            )
            
            print(f"\n  Palavra: {' '.join(display_word)}")
            print(f"  Erros: {errors}/{self.max_errors} | Letras usadas: {', '.join(sorted(guessed_letters))}")
            
            if "_" not in display_word:
                return f"\n Parabens! Voce venceu! A palavra era '{word}'.", self.reward

            guess = input("\n  Chute uma letra: ").strip().upper()

            if not guess or len(guess) != 1 or not guess.isalpha():
                print("  [!] Digite apenas uma letra valida.")
                continue

            if guess in guessed_letters:
                print("  [!] Voce ja tentou essa letra!")
                continue

            guessed_letters.add(guess)

            if guess in word:
                print("  [v] Acertou a letra!")
            else:
                print("  [x] Errou a letra...")
                errors += 1

        return f"\n[!] Voce atingiu o limite de erros! A palavra correta era '{word}'.", 0