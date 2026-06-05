class DuckDad:
    def __init__(self, name):
        self.name = name
        self._hunger = 0
        self._thirst = 0
        self._stress = 0
        self._alcohol = 0
        self._is_sick = False
        self._is_smoker = True
        self._is_alcoholic = True

    # limites para não passar de 0 e 100
    def _check_limits(self):
        if self._hunger >= 100: 
            self._hunger = 100
            self._is_sick = True
        elif self._hunger < 0: 
            self._hunger = 0
            
        if self._thirst >= 100: 
            self._thirst = 100
            self._is_sick = True
        elif self._thirst < 0: 
            self._thirst = 0
        
        if self._stress >= 100: 
            self._stress = 100
            self._is_sick = True
        elif self._stress < 0: 
            self._stress = 0
        
        if self._alcohol >= 100: 
            self._alcohol = 100
            self._is_sick = True
        elif self._alcohol < 0: 
            self._alcohol = 0

        # mensagens de status
        if self._hunger == 0:
            print(f"{self.name} está de barriga cheia!")
        elif self._hunger >= 85:
            print(f"{self.name} está com muita fome. Alimente ele agora!")

        if self._thirst == 0:
            print(f"{self.name} está totalmente hidratado!")
        elif self._thirst >= 85:
            print(f"{self.name} está com sede. Dê água para ele!")

        if self._stress == 0:
            print(f"{self.name} está totalmente relaxado!")
        elif self._stress >= 85:
            print(f"{self.name} está muito estressado. Ajude ele a relaxar!")

        if self._alcohol == 0:
            print(f"A vontade de beber álcool de {self.name} está saciada!")
        elif self._alcohol >= 85:
            print(f"{self.name} está em crise de abstinência! Dê álcool para ele!")
    
    # sistema de fome
    def feed(self, food_value):
        if food_value <= 0:
            return "Valor inválido."
            
        if self._hunger < 10:
            return f"{self.name} não quer comer agora."
        else:
            self._hunger -= food_value
            self._check_limits()
            return f"{self.name} comeu!"
    
    # sistema de sede
    def drink(self, water_value):
        if water_value <= 0:
            return "Valor inválido."
            
        if self._thirst < 10:
            return f"{self.name} não quer beber agora."
        else:
            self._thirst -= water_value
            self._check_limits()
            return f"{self.name} bebeu!"

    # sistema de estresse
    def smoking(self, smoking_value):
        if smoking_value <= 0:
            return "Valor inválido."
            
        if not self._is_smoker:
            self._is_smoker = True
            self._stress -= smoking_value
            self._check_limits()
            return f"{self.name} fumou pela primeira vez."
            
        if self._stress < 10:
            return f"{self.name} não está estressado."
        else:
            self._stress -= smoking_value
            self._check_limits()
            return f"{self.name} fumou e está menos estressado!"
    
    # sistema de alcool
    def drinking_alcohol(self, alcohol_value):
        if alcohol_value <= 0:
            return "Valor inválido."
            
        if not self._is_alcoholic:
            self._is_alcoholic = True
            self._alcohol -= alcohol_value
            self._check_limits()
            return f"{self.name} bebeu pela primeira vez."
            
        if self._alcohol < 10:
            return f"{self.name} não quer beber agora."
        else:
            self._alcohol -= alcohol_value
            self._check_limits()
            return f"{self.name} bebeu álcool!"

    # sistema de brincadeira
    def play(self):
        self._hunger += 15
        self._thirst += 15
        self._stress -= 20
        self._alcohol -= 10
        self._check_limits()
        return f"{self.name} brincou!"

    # sistema de passar o tempo
    def pass_time(self):
        self._hunger += 5
        self._thirst += 5
        self._stress += 15
        
        if self._is_alcoholic:
            if self._stress > 50:
                self._alcohol += 20
            else:
                self._alcohol += 5
            
        self._check_limits()

    # sistema de cura
    def heal(self):
        if self._is_sick:
            self._is_sick = False
            self._hunger -= 30
            self._thirst -= 30
            self._stress -= 30
            self._alcohol -= 30
            self._check_limits()
            return f"{self.name} tomou o remédio e está curado!"
        else:
            return f"{self.name} não está doente."

    # sistema de mudança de nome
    def change_name(self, new_name):
        self.name = new_name
        return f"Nome alterado para {self.name}!"

# sistema de reprodução
class DuckSon(DuckDad):
    def __init__(self, name):
        super().__init__(name)
        self._is_smoker = False
        self._is_alcoholic = False

    def reproduce(self, baby_name):
        return DuckSon(baby_name)