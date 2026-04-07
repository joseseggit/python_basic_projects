from tabulate import tabulate

def main():
    tablero = dict(zip(["a1", "b1", "c1", "a2", "b2", "c2", "a3", "b3", "c3"],["","","","","","","","","",]))
    ronda = 1
    while True:
        imprimir_tablero(tablero)
        #Primer jugador
        user_choice(tablero, "X")
        imprimir_tablero(tablero)
        ronda += 1
        #Comprobación de si se ha ganado
        if win_cond(tablero, "X"):
            print("Gana X")
            break
        if ronda >= 9:
            print("EMPATE!")
            break
        #Segundo jugador
        user_choice(tablero, "O")
        #Comprobación de si se ha ganado
        if win_cond(tablero, "O"):
            imprimir_tablero(tablero)
            print("Gana O")
            break
        ronda += 1

def user_choice(tablero, simbolo):
    while True:
        u1_choice = input("Selecciona una casilla para poner " + simbolo + " ")
        if u1_choice in tablero.keys() and tablero[u1_choice] == "":
            tablero[u1_choice] = simbolo
            break
        else:
            print("Opción no válida. Vuelve a intentarlo.")

def imprimir_tablero(tablero):
    filas = [
        [tablero["a1"], tablero["b1"], tablero["c1"]],
        [tablero["a2"], tablero["b2"], tablero["c2"]],
        [tablero["a3"], tablero["b3"], tablero["c3"]],
    ]
    print(tabulate(filas, headers=["a","b","c"], showindex=[1,2,3], tablefmt="grid"))

def comp_filas(tablero, inicio, simbolo):
    count = 0
    indic = list(tablero.keys()).index(inicio)
    for _ in range(3):
        if tablero[list(tablero.keys())[indic + _]] == simbolo:
            count += 1
        else:
            return False
    return True

def comp_columnas(tablero, inicio, simbolo):
    count = 0
    indic = list(tablero.keys()).index(inicio)
    for _ in range(3):
        if tablero[list(tablero.keys())[indic + (3*_)]] == simbolo:
            count += 1
        else:
            return False
    return True

def comp_oblicuas(tablero, inicio, simbolo):
    list1 = []
    if inicio == "a1":
        list1 = ["a1", "b2", "c3"]
    else:
        list1 = ["a3", "b2", "c1"]
    return tablero[list1[0]] == tablero[list1[1]] == tablero[list1[2]] == simbolo

def win_cond(tablero, simbolo):
    entradas_f = ["a1","a2","a3"]   
    entradas_c = ["a1", "b1", "c1"]
    entradas_o = ["a1", "c1"]
    for _ in entradas_f:
        cond = comp_filas(tablero, _, simbolo)
        if cond:
            return cond
    for _ in entradas_c:
        cond = comp_columnas(tablero, _, simbolo)
        if cond:
            return cond
    for _ in entradas_o:
        cond = comp_oblicuas(tablero,_, simbolo)
        if cond:
            return cond
    return cond

if __name__ == "__main__":
    main()
