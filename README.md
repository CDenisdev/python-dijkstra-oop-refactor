# 🗺️ Calculadora de Rutas OOP con Algoritmo de Dijkstra

Este proyecto es una aplicación de consola en Python que calcula la ruta de costo mínimo en un mapa de grilla con terrenos variables (obstáculos y "terrenos difíciles" como el agua).

Este fue un reto de dos partes:
1.  **Implementación Inicial:** Construir una calculadora de rutas funcional usando el **Algoritmo de Dijkstra** (ver `calculadora_de_rutas.py`).
2.  **Refactorización a OOP:** Re-arquitecturar el script procedural a un diseño de **Programación Orientada a Objetos (OOP)** limpio, extensible y mantenible (ver `Calculadoraderutas2.py`).

---

## 🛠️ Arquitectura y Conceptos Técnicos (Versión OOP)

El objetivo principal fue aplicar principios de diseño de software para crear un sistema robusto.

* **Programación Orientada a Objetos (OOP):** El código está completamente encapsulado en clases (`Mapa`, `Celda`, `CalculadoraDeRutas`, `AplicacionPathfinding`).
* **Principios SOLID:**
    * **S - Responsabilidad Única:** Cada clase tiene un solo propósito (el `Mapa` gestiona el estado, `CalculadoraDijkstra` solo calcula, `AplicacionPathfinding` solo maneja la UI).
    * **O - Abierto/Cerrado:** El sistema es extensible. Gracias a la Clase Base Abstracta (`AlgoritmoBusqueda`), se podría añadir un nuevo algoritmo (como A*) sin modificar el `CalculadoraDeRutas`.
* **Patrón de Diseño Strategy:** Se utilizó una clase abstracta (`AlgoritmoBusqueda`) para definir una "estrategia" de búsqueda, permitiendo que la clase principal (`CalculadoraDeRutas`) opere con cualquier algoritmo que implemente esa interfaz.
* **Patrón de Diseño Facade:** La clase `CalculadoraDeRutas` actúa como una "fachada" (Facade), simplificando la lógica compleja de interactuar con el mapa y el algoritmo para el cliente (la `AplicacionPathfinding`).
* **Algoritmo de Dijkstra:** Implementado desde cero usando un **`heapq` (cola de prioridad)** para una eficiencia óptima ($O((E+V) \log V)$) en la búsqueda del camino más corto en un grafo ponderado.

---

## ✨ Funcionalidades

* Creación de mapas de tamaño dinámico.
* Añadir/quitar obstáculos con diferentes costos (🏢 Edificio, 💧 Agua, ⛔ Bloqueado).
* Definir puntos de inicio (🚦) y destino (🏁).
* Visualización en consola de la ruta óptima (⭐) y el costo total.

---

