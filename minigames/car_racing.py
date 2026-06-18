import random

class CarRacing:
    # sistema de configuracao de pistas
    def __init__(self):
        self.track_names = [
            "Pista do Parque",
            "Circuito do Lago",
            "Rua da Favela",
            "Autódromo do Pato"
        ]

    # sistema principal de jogatina
    def play(self) -> tuple[str, int]:
        track = random.choice(self.track_names)
        performance = random.randint(1, 100)

        if performance >= 85:
            reward = 40
            message = (
                f"Você correu na {track} e venceu com estilo!"
                "\nRecompensa: +40 moedas."
            )
        elif performance >= 60:
            reward = 25
            message = (
                f"Voce terminou a corrida na {track} em segundo lugar."
                "\nRecompensa: +25 moedas."
            )
        elif performance >= 35:
            reward = 15
            message = (
                f"Voce completou a corrida na {track}. Não foi fácil, mas valeu."
                "\nRecompensa: +15 moedas."
            )
        else:
            reward = 5
            message = (
                f"A corrida na {track} foi dificil, mas voce chegou ao fim."
                "\nRecompensa: +5 moedas."
            )

        return message, reward