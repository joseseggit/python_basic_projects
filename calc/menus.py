import funciones

def main():
    calculadora()

def calculadora():
    while True:
        mostrar_menu()
        opciones  = ["+","-","*","/","^","v","|","x"]
        opc = obtener_opcion(opciones)
        if opc != "x":
            mensajes_explicativos(opc)
            nums = obtener_numeros()
            try:
                resultado = realizar_operacion(nums,opc)
                if resultado != None:
                    print(f"\033[32mEl resultado de la operación '{opc}' es {resultado}\033[0m")
            except TypeError:
                print("\033[31mDebes introducir al menos un operando\033[0m")
        else:
            conf = input("\033[31m¿Está seguro de que quiere salir? (s/n) \033[0m")
            if conf == "s":
                break

def mostrar_menu():
    print("-------------- Bienvenido a la calculadora JS! --------------")
    print("-------------- Las operaciones disponibles son; -------------")
    print("- Suma (+): Suma una lista de números -----------------------")
    print("- Resta (-): Resta una lista de números ---------------------")
    print("- Producto (*): Multiplica una lista de números -------------")
    print("- División (/): Divide una lista de números -----------------")
    print("- Potencia (^): Eleva un número a otro ----------------------")
    print("- Raiz (v): Raíz n-ésima de un número -----------------------")
    print("- Valor Absoluto (|): Valor absoluto de un número -----------")
    print("- Salir (x): Terminar la sesión -----------------------------")

def obtener_opcion(opciones):
    opc = ""
    while True:
        print("--------------------- ¿Qué quiere hacer? --------------------")
        opc = input()
        if opc not in opciones:
            print("\033[31m------------------- Operación no permitida ------------------\033[0m\n")
        else:
            break
    return opc

def obtener_numeros():
    nums = []
    while True:
        n1 = input("Introduzca un operando. Introduzca un carácter para interrumpir. ")
        try:
            n1 = float(n1)
            nums.append(n1)
        except ValueError:
            break
    if nums == []:
        return None
    return nums

def realizar_operacion(nums, opc):
    match opc:
        case "+":
            return funciones.sumar(nums)
        case "-":
            return funciones.restar(nums)
        case "*":
            return funciones.multiplicar(nums)
        case "/":
            return funciones.dividir(nums)
        case "^":
            return funciones.potencia(nums)
        case "v":
            return funciones.root(nums)
        case "|":
            return funciones.absoluto(nums)

def mensajes_explicativos(opc):
    match opc:
        case "-":
            print("\033[31mPrimer operando menos el resto de operandos\033[0m")
        case "/":
            print("\033[31mPrimer operando será dividido por el resto de operandos.\033[0m")
        case "^":
            print("\033[31mPrimer operando elevado al segundo. No se permiten más de dos operandos.\033[0m")
        case "v":
            print("\033[31mRaíz del orden del segundo operando sobre el primer operando. No se permiten más de dos operandos.\033[0m")
        case "|":
            print("\033[31mNo se permite más de un operando.\033[0m")



if __name__ == "__main__":
    main()
