from random import shuffle

NUMEROS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
PALOS = ('♠', '♥', '♦', '♣')
ROJO, NEGRO = "\033[31m", "\033[0m"
CANT_CARTAS_ROBADAS = 3
JUGADOR1, JUGADOR2 = "Jugador 1", "Jugador 2"

def generar_cartas():
    """Genera una baraja de cartas con todos los números y palos disponibles."""
    return [(num, palo) for num in NUMEROS for palo in PALOS]

def barajar_mazo(mazo):
    """Baraja el mazo de cartas in-place."""
    return shuffle(mazo)

def generar_mazo_jugador(mazo, tamanio):
    """Genera y devuelve un mazo para un jugador"""
    mazo_jugador = []
    for _ in range(tamanio):
        mazo_jugador.append(mazo.pop(0))
    
    return mazo_jugador

def dibujar_carta(carta_jug_1, carta_jug_2):
    """Muestra por consola las cartas jugadas por ambos jugadores en formato gráfico."""
    print("- J1 -  - J2 -")
    print(" ______    ______")
    print(f"|{carta_jug_1[0]:2>}    |   |{carta_jug_2[0]:>2}   |")
    print(f"| {carta_jug_1[1]:>2}   |  |  {carta_jug_2[1]:>2}  |")
    print(f"|____{carta_jug_1[0]:>2}|  |____{carta_jug_2[0]:>2}|")

def mostrar_carta_jugador(cartas_actuales_jugador):
    """Imprime las cartas actuales del jugador sin revelar el contenido exacto."""
    for tupla in cartas_actuales_jugador:
        print(str(tupla[0]) + tupla[1], end=" ")

def sacar_carta(baraja):
    """Extrae y devuelve la primera carta del mazo."""
    return baraja.pop(0)

def comprobar_ganador_ronda(carta_1, carta_2):
    """Devuelve 0 si gana el jugador 1, o 1 si gana el jugador 2, comparando los valores numéricos de las cartas."""
    return 0 if carta_1[0] > carta_2[0] else 1

def jugar():
    """Inicia y ejecuta el juego completo entre dos jugadores, mostrando las estadísticas al final."""
    baraja = generar_cartas()
    cant_cartas_baraja = len(baraja)
    barajar_mazo(baraja)
    tamanio_mazo = len(baraja) // 2;
    cartas_jugador_1 = generar_mazo_jugador(baraja, tamanio_mazo)
    cartas_jugador_2 = generar_mazo_jugador(baraja, tamanio_mazo)

    rondas = 0
    win_jug_1 = 0
    win_jug_2 = 0

    while len(cartas_jugador_1) > 1 and len(cartas_jugador_2) > 1:
        rondas += 1
        print(f"--- Ronda {rondas} ---")
        print(f"Mazo del jugador 1 oculto ({len(cartas_jugador_1)}): ", end="")
        mostrar_carta_jugador(cartas_jugador_1)
        print()
        print(f"Mazo del jugador 2 oculto ({len(cartas_jugador_2)}): ", end="")
        mostrar_carta_jugador(cartas_jugador_2)
        print()

        cant_cartas = 1
        hay_empate = True
        cartas_en_juego = []
        
        while hay_empate:
            
            #Si le queda una carta pierde, ya que al robar se quedaría sin ellla
            if len(cartas_jugador_1) > 1 or len(cartas_jugador_2) > 1:
                carta_jugador_1 = sacar_carta(cartas_jugador_1)
                carta_jugador_2 = sacar_carta(cartas_jugador_2)

                cartas_en_juego.append(carta_jugador_1)
                cartas_en_juego.append(carta_jugador_2)

                dibujar_carta(carta_jugador_1, carta_jugador_2)

                #Se comprueba que las cartas son del mismo numero para poder quitar 3 cartas a cada jugador
                if carta_jugador_1[0] == carta_jugador_2[0]:
                    for _ in range(CANT_CARTAS_ROBADAS):
                        if len(cartas_jugador_1) >= 3:
                            cartas_en_juego.append(sacar_carta(cartas_jugador_1))
                        else:
                            cartas_jugador_1 = []
                            cant_cartas = 0

                        if len(cartas_jugador_2) >= 3:
                            cartas_en_juego.append(sacar_carta(cartas_jugador_2))
                        else:
                            cartas_jugador_2 = []
                            cant_cartas = 0
                    
                    if cant_cartas != 0:
                        continue
                
                #Al conocer si hay algún ganador, le añadiremos a su mazo todas las cartas jugadas
                jugador_ganador = comprobar_ganador_ronda(carta_jugador_1, carta_jugador_2)
                input()
                if jugador_ganador == 0 or jugador_ganador == 1 or cant_cartas != 0:
                    hay_empate = False

                if not hay_empate:
                    for x in range(len(cartas_en_juego)):
                        if jugador_ganador == 0:
                            cartas_jugador_1.append(cartas_en_juego[x])
                            ganador = JUGADOR1
                            win_jug_1 += 1
                        else:
                            cartas_jugador_2.append(cartas_en_juego[x])
                            ganador = JUGADOR2
                            win_jug_2 += 1

                    print(f"¡{ganador} gana la ronda!\n")
            
    print(f"{JUGADOR2 if len(cartas_jugador_1) == 0 else JUGADOR1} ha ganado el juego!\n")

    print("Estadísticas")
    print("------------")
    print(f"{JUGADOR1}: {win_jug_1} victorias")
    print(f"{JUGADOR1}: {win_jug_2} victorias")
    print(f"Número de rondas jugadas: {rondas}")
    print(f"Porcentaje de cartas en el mazo del {JUGADOR1}: {(len(cartas_jugador_1) * 100 / cant_cartas_baraja):.2}%")
    print(f"Porcentaje de cartas en el mazo del {JUGADOR2}: {(len(cartas_jugador_2) * 100 / cant_cartas_baraja):.2}%")
            
if __name__ == '__main__':
    jugar()

    