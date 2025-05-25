"""
Universidad del valle de Guatemala
Curso: Teoría de la probabilidades
Profesor: Ing. Paulo Vladimir
Grupo: 1


Simulación del problema de las 10 puertas utilizando Cadenas de Markov
Este código simula el famoso problema de las 10 puertas, donde un presentador revela 8 puertas sin premio
y el jugador debe decidir si cambiar su elección inicial o no.


Objetivo:
El objetivo es comparar las probabilidades de ganar al cambiar o no cambiar la puerta elegida.
 
# """

import numpy as np
import random

class CadenaMarkov10Puertas:
    def __init__(self):
        # Estados: 0=Inicial, 1=Revelación, 2=Decisión, 3=Ganar, 4=Perder
        self.estados = ['Inicial', 'Revelación', 'Decisión', 'Ganar', 'Perder']
        self.estado_actual = 0
        self.puerta_premio = None
        self.puerta_elegida = None
        self.puerta_alternativa = None
        
    def simular_juego(self, cambiar=False):
        # Reiniciar el juego
        self.estado_actual = 0
        self.puerta_premio = random.randint(0, 9)
        
        # Estado 0 -> 1: Selección inicial
        self.puerta_elegida = random.randint(0, 9)
        self.estado_actual = 1
        
        # Estado 1 -> 2: Presentador abre 8 puertas
        puertas_disponibles = [i for i in range(10) if i != self.puerta_elegida and i != self.puerta_premio]
        if self.puerta_elegida == self.puerta_premio:
            # Si eligió la correcta, el presentador deja cualquier otra puerta
            self.puerta_alternativa = random.choice(puertas_disponibles)
        else:
            # Si eligió incorrecta, el presentador deja la puerta con el premio
            self.puerta_alternativa = self.puerta_premio
        self.estado_actual = 2
        
        # Estado 2 -> 3 o 4: Decisión final
        if cambiar:
            self.puerta_elegida = self.puerta_alternativa
        
        if self.puerta_elegida == self.puerta_premio:
            self.estado_actual = 3  # Ganar
            return 1
        else:
            self.estado_actual = 4  # Perder
            return 0
    
    def calcular_probabilidades(self, n_simulaciones=10000):
        # Estrategia 1: Nunca cambiar
        victorias_sin_cambiar = sum(self.simular_juego(cambiar=False) for _ in range(n_simulaciones))
        prob_ganar_sin_cambiar = victorias_sin_cambiar / n_simulaciones
        
        # Estrategia 2: Siempre cambiar
        victorias_cambiando = sum(self.simular_juego(cambiar=True) for _ in range(n_simulaciones))
        prob_ganar_cambiando = victorias_cambiando / n_simulaciones
        
        return prob_ganar_sin_cambiar, prob_ganar_cambiando

# Ejecutar simulación
print("=== SIMULACIÓN CON CADENAS DE MARKOV ===\n")
cadena = CadenaMarkov10Puertas()
prob_sin_cambiar, prob_cambiando = cadena.calcular_probabilidades(10000)

print(f"Estrategia: NUNCA CAMBIAR")
print(f"  - Probabilidad de GANAR: {prob_sin_cambiar:.4f} ≈ {prob_sin_cambiar:.1%}")
print(f"  - Probabilidad de PERDER: {1-prob_sin_cambiar:.4f} ≈ {(1-prob_sin_cambiar):.1%}")
print(f"  - Valor teórico esperado: 1/10 = 0.1000 (10%)\n")

print(f"Estrategia: SIEMPRE CAMBIAR")
print(f"  - Probabilidad de GANAR: {prob_cambiando:.4f} ≈ {prob_cambiando:.1%}")
print(f"  - Probabilidad de PERDER: {1-prob_cambiando:.4f} ≈ {(1-prob_cambiando):.1%}")
print(f"  - Valor teórico esperado: 9/10 = 0.9000 (90%)\n")

print("CONCLUSIÓN: ¡Es mucho mejor CAMBIAR de puerta!")
print(f"Cambiar aumenta la probabilidad de ganar de {prob_sin_cambiar:.1%} a {prob_cambiando:.1%}")