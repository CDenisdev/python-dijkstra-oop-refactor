# mapa.py
from typing import List, Tuple  #para anotar tipos list, tuple
import heapq    # cola de prioridad para dijkstra
import math     #usamos math.inf en als comparaciones de costo 

# Constantes del terreno (Mapa)
LIBRE = 0
EDIFICIO = 1
AGUA = 2
BLOQ = 3
EMOJI_INICIO = "🚦"
EMOJI_DESTINO = "🏁"
EMOJI_RUTA = "⭐"

# Para mostrar el mapa con estos emojis
EMOJIS = {
    LIBRE: "⬜",
    EDIFICIO: "🏢",
    AGUA: "💧",
    BLOQ: "⛔"
}

# Damos los valores a las celdas para Dijkstra
COSTO_CELDA = {
    LIBRE: 1,
    AGUA: 3,
    EDIFICIO: None,
    BLOQ: None
}

# ============================================================================
#  -------------------------CLASE MAPA-----------------------------------------------
# se defina el tamaño del mapa, definimos limites, inicio, destino, ubicar obstaculos
# limpiar celda, y render que es para mostrar el mapa en consola
# ============================================================================

class Mapa: # Modelo del mundo donde se calculan las rutas
    def __init__(self, alto: int, ancho: int): #El constructor filtra valores no validos e inicializa en un 10x10
        if alto <= 0 or ancho <= 0:
            print("Tamaño inválido, se usará 10x10 por defecto.")
            alto, ancho = 10, 10
        self.alto = alto
        self.ancho = ancho
        self.matriz = [[LIBRE for _ in range(ancho)] for _ in range(alto)]
        self.inicio = None
        self.destino = None

    def dentro_limites(self, f: int, c: int) -> bool: # Comprueba limite de mapas
        return 0 <= f < self.alto and 0 <= c < self.ancho

    def definir_inicio(self, f: int, c: int):
        if not self.dentro_limites(f, c):
            print("El inicio esta fuera del mapa.")
            return 
        if self.matriz[f][c] != LIBRE:
            print ("El inicio no puede estar en un obstaculo")
            return
        self.inicio = (f,c)
        print(f"Inicio definido en ({f}, {c})")

    def definir_destino(self, f: int, c: int):
        if not self.dentro_limites(f, c):
            print("El destino esta fuera del mapa")
            return
        if self.matriz[f][c] != LIBRE:
            print ("El destino no puede estar sobre un obstaculo")
            return
        self.destino = (f,c)
        print (f"Destino esta definido en ({f}, {c})")

    def agregar_obstaculo(self, tipo: int, f: int, c: int):
        if tipo not in (EDIFICIO, AGUA, BLOQ):
            print ("Tipo de obstaculo invalido (usa 1=EDIFICIO, 2=AGUA, 3=BLOQ).")
            return 
        if not self.dentro_limites(f, c):
            print("Coordenadas fuera del mapa.")
            return
        if self.inicio == (f, c) or self.destino == (f, c):
            print("No puedes poner un obstaculo sobre inicio o destino")
            return
        self.matriz[f][c] = tipo
        print (F"Obstaculo agregado en ({f}, {c})")

    def limpiar_celda(self, f: int, c: int):

        if not self.dentro_limites(f, c):
            print("Coordenadas fuera del mapa")
            return
        self.matriz[f][c] = LIBRE
        print(f"Celda limpiada en ({f}, {c})")


    def render(self, ruta: List[Tuple[int, int]] | None = None) -> str:
        ruta_set = set(ruta) if ruta else set()
        lineas = []

        for f in range (self.alto):
            piezas = []
            for c in range(self.ancho):
                simbolo = EMOJIS[self.matriz[f][c]]

                if (f, c) in ruta_set:
                    simbolo = EMOJI_RUTA
                
                if self.inicio == (f, c):
                    simbolo = EMOJI_INICIO
                if self.destino == (f, c):
                    simbolo = EMOJI_DESTINO

                piezas.append(simbolo)
            lineas.append("".join(piezas))
        return "\n".join(lineas)

# ============================================================================
# CLASE RUTA
# Ruta es un objero contenedor: guarda el camino y el costo que tuvo que recorrer
# ============================================================================
class Ruta:
    def __init__(self, pasos: List[Tuple[int, int]], costo_total: float | int): 
        self.pasos = pasos
        self.costo_total = costo_total

    # Len devuelve el numero de pasos 
    def __len__(self):
        return len(self.pasos)
    
    # iter permite iterar la ruta con for
    def __iter__(self):
        return iter(self.pasos)
    
    # sstr para imprimir la ruta 
    def __str__(self):
        return f"Ruta de {len(self)} pasos, costo total = {self.costo_total}"
    
    # decuelve la misma ruta alreves (opcional) por si quiera agregar una funcion para reconstruir la ruta de atras hacia adelante
    def invertir(self):
        return Ruta(list(reversed(self.pasos)), self.costo_total)

# ============================================================================
# ------------------------CLASE DIJKSTRA--------------------------------------
# Esta clase encapsula todo el algoritmo de Dijkstra,
# que busca el camino más barato entre dos puntos de un grafo —
# en este caso, el grafo es mi mapa.
# ============================================================================
class Dijkstra:
    def __init__(self):
        self.direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def calcular_ruta(self, mapa : Mapa ):
        if mapa.inicio is None or mapa.destino is None:
            print("Define inicio y destino primero")
            return None
        
        si, sj = mapa.inicio
        gi, gj = mapa.destino

        dist = { (si, sj): 0}
        padres ={}
        heap = [(0, (si, sj))]

        while heap:
            costo_actual, (i, j) = heapq.heappop(heap)

            if (i, j) == (gi ,gj):
                pasos = self.reconstruir_ruta(padres, (si, sj), (gi, gj))
                return Ruta(pasos, costo_actual)
            
            if costo_actual > dist.get((i ,j), math.inf):
                continue
            for di, dj in self.direcciones:
                ni, nj = i + di, j + dj

                if not mapa.dentro_limites(ni, nj):
                    continue

                costo_celda = COSTO_CELDA.get(mapa.matriz[ni][nj], None)
                if costo_celda is None:
                    continue
                
                nuevo_costo = costo_actual + costo_celda

                if nuevo_costo < dist.get((ni, nj), math.inf):
                    dist[(ni, nj)] = nuevo_costo
                    padres[(ni, nj)] = (i, j)
                    heapq.heappush(heap, (nuevo_costo, (ni, nj)))
        
        print ("No hay ruta posible")
        return None
    
    def reconstruir_ruta(self, padres, inicio, destino):
        ruta = []
        actual = destino
        while actual != inicio:
            ruta.append(actual)
            actual = padres[actual]
        ruta.append(inicio)
        ruta.reverse()
        return ruta

# ============================================================================
# -----------------CLASE CALCULADORA DE RUTAS---------------------------------
# Coordina todo el proceso de calculo, su funcion es conectar las piezas y 
# mostrar el resultado final al usuario. Aca vemos polimorfismo
# ============================================================================
class CalculadoraDeRutas:
    def __init__(self, mapa: Mapa, algoritmo: Dijkstra):
        self.mapa = mapa
        self.algoritmo = algoritmo

    def calcular_y_mostrar(self):
        ruta = self.algoritmo.calcular_ruta(self.mapa)
        if ruta is None:
            print("No hay ruta encontrada.")
        else:
            print(f"\nRuta encontrada con costo total {ruta.costo_total}:")
            print(self.mapa.render(ruta.pasos))

# ============================================================================
# CLASE APP
# Interfaz que ve el usuario
# ============================================================================
class App:
    def __init__(self):
        self.mapa = None
        self.calculadora = None

    def run(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Crear mapa personalizado")
            print("2. Usar mapa por defecto (10x10)")
            print("3. Definir inicio 🚦")
            print("4. Definir destino 🏁")
            print("5. Agregar obstáculo (🏢, 💧, ⛔)")
            print("6. Limpiar celda ⬜")
            print("7. Mostrar mapa")
            print("8. Calcular ruta ⭐ con Dijkstra")
            print("9. Salir")

            opcion = input("Elige una opción: ")

            if opcion == "1":
                self.crear_mapa_personalizado()
            elif opcion == "2":
                self.mapa = Mapa(10, 10)
                self.calculadora = CalculadoraDeRutas(self.mapa, Dijkstra())
                print("Mapa por defecto creado.")
            elif opcion == "3":
                self.definir_inicio()
            elif opcion == "4":
                self.definir_destino()
            elif opcion == "5":
                self.agregar_obstaculo()
            elif opcion == "6":
                self.limpiar_celda()
            elif opcion == "7":
                self.mostrar_mapa()
            elif opcion == "8":
                self.calcular_ruta()
            elif opcion == "9":
                print("Saliendo del programa...")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")

    # === MÉTODOS DE MENÚ ===

    def crear_mapa_personalizado(self):
        alto = int(input("Número de filas: "))
        ancho = int(input("Número de columnas: "))
        self.mapa = Mapa(alto, ancho)
        self.calculadora = CalculadoraDeRutas(self.mapa, Dijkstra())
        print("Mapa creado.")

    def definir_inicio(self):
        if self.mapa is None:
            print("Primero crea un mapa.")
            return
        f = int(input("Fila de inicio: "))
        c = int(input("Columna de inicio: "))
        self.mapa.definir_inicio(f, c)

    def definir_destino(self):
        if self.mapa is None:
            print("Primero crea un mapa.")
            return
        f = int(input("Fila de destino: "))
        c = int(input("Columna de destino: "))
        self.mapa.definir_destino(f, c)

    def agregar_obstaculo(self):
        if self.mapa is None:
            print("Primero crea un mapa.")
            return
        print("Tipos: 1=🏢 Edificio, 2=💧 Agua, 3=⛔ Bloqueado")
        t = int(input("Tipo: "))
        f = int(input("Fila: "))
        c = int(input("Columna: "))
        self.mapa.agregar_obstaculo(t, f, c)

    def limpiar_celda(self):
        if self.mapa is None:
            print("Primero crea un mapa.")
            return
        f = int(input("Fila: "))
        c = int(input("Columna: "))
        self.mapa.limpiar_celda(f, c)

    def mostrar_mapa(self):
        if self.mapa is None:
            print("Primero crea un mapa.")
            return
        print("\nMapa actual:")
        print(self.mapa.render())

    def calcular_ruta(self):
        if self.calculadora is None:
            print("Primero crea un mapa.")
            return
        self.calculadora.calcular_y_mostrar()



if __name__ == "__main__":
    print("=== CALCULADORA DE RUTAS - VERSIÓN OOP ===")
    app = App()
    app.run()