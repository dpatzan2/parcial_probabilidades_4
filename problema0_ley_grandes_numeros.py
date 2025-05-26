"""
Universidad del valle de Guatemala
Curso: Teoría de la probabilidades
Profesor: Ing. Paulo Vladimir
Grupo: 1


Simulación del problema de las 10 puertas utilizando la Ley de los Grandes Números
Este código simula el famoso problema de las 10 puertas, donde un presentador revela 8 puertas sin premio
y el jugador debe decidir si cambiar su elección inicial o no.


Objetivo:
El objetivo es comparar las probabilidades de ganar al cambiar o no cambiar la puerta elegida.

# """

import numpy as np
import matplotlib.pyplot as plt
import random

class LeyGrandesNumeros10Puertas:
    def __init__(self):
        self.resultados_sin_cambiar = []
        self.resultados_cambiando = []
        
    def jugar_una_vez(self, cambiar=False):
        puerta_premio = random.randint(0, 9)
        puerta_elegida = random.randint(0, 9)
        
        # El presentador abre 8 puertas sin premio
        if puerta_elegida == puerta_premio:
            # Si eligió correctamente, queda cualquier otra puerta
            puertas_restantes = [i for i in range(10) if i != puerta_elegida]
            puerta_alternativa = random.choice(puertas_restantes)
        else:
            # Si eligió incorrectamente, queda la puerta con el premio
            puerta_alternativa = puerta_premio
        
        # Decisión final
        if cambiar:
            puerta_final = puerta_alternativa
        else:
            puerta_final = puerta_elegida
            
        return 1 if puerta_final == puerta_premio else 0
    
    def simular_convergencia(self, n_max=10000):
        promedios_sin_cambiar = []
        promedios_cambiando = []
        numeros_juegos = []
        
        for n in range(1, n_max + 1):
            # Jugar una vez más con cada estrategia
            self.resultados_sin_cambiar.append(self.jugar_una_vez(cambiar=False))
            self.resultados_cambiando.append(self.jugar_una_vez(cambiar=True))
            
            # Calcular promedios acumulados cada 100 juegos
            if n % 100 == 0:
                promedio_sin_cambiar = np.mean(self.resultados_sin_cambiar)
                promedio_cambiando = np.mean(self.resultados_cambiando)
                
                promedios_sin_cambiar.append(promedio_sin_cambiar)
                promedios_cambiando.append(promedio_cambiando)
                numeros_juegos.append(n)
        
        return numeros_juegos, promedios_sin_cambiar, promedios_cambiando
    
    def graficar_convergencia(self, numeros_juegos, promedios_sin_cambiar, promedios_cambiando):
        plt.figure(figsize=(12, 8))
        
        # Graficar las convergencias
        plt.plot(numeros_juegos, promedios_sin_cambiar, 'b-', linewidth=2, 
                label='Nunca cambiar (converge a 1/10)', alpha=0.8)
        plt.plot(numeros_juegos, promedios_cambiando, 'r-', linewidth=2, 
                label='Siempre cambiar (converge a 9/10)', alpha=0.8)
        
        # Líneas de referencia teóricas
        plt.axhline(y=0.1, color='blue', linestyle='--', alpha=0.5, 
                   label='Valor teórico sin cambiar = 0.1')
        plt.axhline(y=0.9, color='red', linestyle='--', alpha=0.5, 
                   label='Valor teórico cambiando = 0.9')
        
        # Configuración del gráfico
        plt.xlabel('Número de juegos', fontsize=12)
        plt.ylabel('Proporción de victorias', fontsize=12)
        plt.title('Ley de los Grandes Números - Problema de las 10 Puertas', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend(loc='right', fontsize=10)
        plt.ylim(0, 1)
        
        # Añadir anotaciones
        plt.text(numeros_juegos[-1]*0.7, 0.15, 
                f'Sin cambiar: {promedios_sin_cambiar[-1]:.3f}', 
                fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        plt.text(numeros_juegos[-1]*0.7, 0.85, 
                f'Cambiando: {promedios_cambiando[-1]:.3f}', 
                fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        
        plt.tight_layout()
        plt.show()

# Ejecutar simulación
print("=== LEY DE LOS GRANDES NÚMEROS ===\n")
print("Simulando 1,000,000 juegos para cada estrategia...")

lgn = LeyGrandesNumeros10Puertas()
numeros, promedios_no_cambiar, promedios_cambiar = lgn.simular_convergencia(1000000)

print(f"\nResultados finales después de 1,000,000 juegos:")
print(f"  - Sin cambiar: {promedios_no_cambiar[-1]:.4f} (teórico: 0.1000)")
print(f"  - Cambiando: {promedios_cambiar[-1]:.4f} (teórico: 0.9000)")

print(f"\nDiferencia con valores teóricos:")
print(f"  - Sin cambiar: {abs(promedios_no_cambiar[-1] - 0.1):.4f}")
print(f"  - Cambiando: {abs(promedios_cambiar[-1] - 0.9):.4f}")

print("\nLa Ley de los Grandes Números confirma que las frecuencias relativas")
print("convergen a las probabilidades teóricas cuando n → ∞")

# Graficar la convergencia
lgn.graficar_convergencia(numeros, promedios_no_cambiar, promedios_cambiar)