# Práctica 3: Uso de la Herramienta JFLAP para Convertir Autómatas Finitos Deterministas a Expresiones Regulares y Extensión de Software para simular Autómatas No Deterministas, AFN con Transiciones Lambda y Minimización de AFD

Este proyecto es una aplicación integral desarrollada en **Python** utilizando el framework **Flet** para la interfaz gráfica. [cite_start]Su objetivo es profundizar en la relación entre los autómatas finitos y las expresiones regulares, además de proporcionar herramientas de simulación y minimización de autómatas[cite: 10].

## 👥 Datos del Equipo
* **Romero Martínez Diego Enrique** | Boleta: 2025630526
* **Barrera Guerrero José Emanuel** | Boleta: 2025630497
* **Grupo:** 4CM4
* **Profesor:** Gabriel Hurtado Avilés


## 🚀 Funcionalidades

La aplicación se divide en tres módulos principales accessibles mediante pestañas:

1.  **Subcadenas, Prefijos y Sufijos:** Cálculo y visualización de todas las combinaciones posibles de una cadena dada, con opción de exportación a `.txt`.
2.  **Cerraduras de Kleene y Positiva:** Generación de lenguajes basados en un alfabeto específico y una longitud máxima configurada por el usuario.
3.  **Autómatas y Minimización:**
    * **Simulación AFN-λ:** Procesamiento paso a paso de cadenas, visualizando el conjunto de estados activos y calculando la λ-clausura en cada transición.
    * **Minimización de AFD:** Implementación del **Algoritmo de Hopcroft** para reducir autómatas a su mínima expresión equivalente, eliminando estados inaccesibles y fusionando estados equivalentes.

## 🛠️ Requisitos e Instalación

[cite_start]Para ejecutar este programa en un entorno **Linux**, sigue estos pasos[cite: 131]:

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-de-tu-repositorio>
    cd <nombre-de-la-carpeta>
    ```

2.  **Instalar dependencias:**
    Se recomienda el uso de un entorno virtual para evitar conflictos:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install flet
    ```

## 🖥️ Ejecución

Una vez instaladas las dependencias, inicia la aplicación con el siguiente comando:

```bash
python3 main.py
