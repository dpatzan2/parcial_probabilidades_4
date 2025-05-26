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


def calcular_probabilidades_teoricas(p):
    # Matriz de transición completa P (5x5)
    P = np.array([
        [0, 1, 0,   0,   0],
        [0, 0, 1,   0,   0],
        [0, 0, 0,   p, 1-p],
        [0, 0, 0,   1,   0],
        [0, 0, 0,   0,   1]
    ])

    # Extraer las submatrices Q (transitorios) y R (a absorbentes)
    Q = P[:3, :3]  # Estados E1, E2, E3
    R = P[:3, 3:]  # Transiciones desde E1, E2, E3 hacia E4 y E5

    # Matriz fundamental: N = (I - Q)^-1
    I = np.eye(Q.shape[0])
    N = np.linalg.inv(I - Q)

    # Matriz de absorción: B = N @ R
    B = N @ R

    # Mostrar probabilidades desde E1
    print(f"\nProbabilidad de ganar desde E1: {B[0, 0]:.4f}")
    print(f"Probabilidad de perder desde E1: {B[0, 1]:.4f}")

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
print("=== RESULTADOS TEÓRICOS CON CADENAS DE MARKOV ===\n")
# Estrategia: no cambiar (p = 0.1)
print("Estrategia: NO cambiar de puerta (p = 0.1)")
calcular_probabilidades_teoricas(p=0.1)

# Estrategia: siempre cambiar (p = 0.9)
print("\nEstrategia: CAMBIAR de puerta (p = 0.9)")
calcular_probabilidades_teoricas(p=0.9)

print("\n=== SIMULACIÓN CON CADENAS DE MARKOV ===\n")
cadena = CadenaMarkov10Puertas()
prob_sin_cambiar, prob_cambiando = cadena.calcular_probabilidades(1000000)

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