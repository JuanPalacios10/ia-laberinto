import pygame
import sys

import tkinter as tk
from tkinter import font

class EditorLaberinto:
    def __init__(self):
        # Configuración inicial
        self.ROWS, self.COLS = self.pedir_dimensiones()
        self.WIDTH, self.HEIGHT = 600, 600
        
        self.CELL_WIDTH = self.WIDTH // self.COLS
        self.CELL_HEIGHT = self.HEIGHT // self.ROWS
        self.CELL_SIZE = min(self.CELL_WIDTH, self.CELL_HEIGHT)  # Para que sea cuadrada

        # Colores
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (120, 120, 120)  # X

        # Inicializar pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT + 50))
        pygame.display.set_caption("Editor de Laberinto")
        self.font = pygame.font.SysFont("Arial", 20)

        # Herramientas disponibles
        self.TOOLS = ["empty", "raton", "queso", "X", "C", "R", "L", "U", "D"]
        self.current_tool = "raton"

        # Mapa visual inicial
        self.editor_grid = [[" " for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.raton_pos = None
        self.queso_pos = None

        # Ratón y queso
        self.raton_img = pygame.image.load("assets/mouse.png")
        self.queso_img = pygame.image.load("assets/cheese.png")
        self.gato_img = pygame.image.load("assets/cat.png")

        self.raton_img = pygame.transform.scale(self.raton_img, (self.CELL_SIZE, self.CELL_SIZE))
        self.queso_img = pygame.transform.scale(self.queso_img, (self.CELL_SIZE, self.CELL_SIZE))
        self.gato_img = pygame.transform.scale(self.gato_img, (self.CELL_SIZE, self.CELL_SIZE))

    def pedir_dimensiones(self):
        def aceptar():
            nonlocal filas, columnas
            try:
                filas = int(entry_filas.get())
                columnas = int(entry_columnas.get())
                if filas <= 0 or columnas <= 0:
                    raise ValueError
                ventana.destroy()
            except ValueError:
                label_error.config(text="Introduce números válidos (mayores que 0)")

        filas = columnas = 0
        ventana = tk.Tk()
        ventana.title("Tamaño del laberinto")
        ventana.resizable(False, False)

        # Crear los widgets
        fuente = font.Font(size=10)
        tk.Label(ventana, text="Número de filas:", font=fuente).grid(row=0, column=0, padx=15, pady=10, sticky="e")
        entry_filas = tk.Entry(ventana, font=fuente, width=10)
        entry_filas.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ventana, text="Número de columnas:", font=fuente).grid(row=1, column=0, padx=15, pady=10, sticky="e")
        entry_columnas = tk.Entry(ventana, font=fuente, width=10)
        entry_columnas.grid(row=1, column=1, padx=10, pady=10)

        label_error = tk.Label(ventana, text="", fg="red", font=fuente)
        label_error.grid(row=2, column=0, columnspan=2, pady=(0, 5))

        boton = tk.Button(ventana, text="Aceptar", command=aceptar, bg="#4CAF50", fg="white", font=fuente, width=12)
        boton.grid(row=3, column=0, columnspan=2, pady=10)

        # Centrado de la ventana
        ventana.update_idletasks()
        ancho_ventana = ventana.winfo_width()
        alto_ventana = ventana.winfo_height()
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        ventana.mainloop()
        return filas, columnas

    def draw_grid(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell = self.editor_grid[row][col]
                rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)

                if "X" in cell:
                    pygame.draw.rect(self.screen, self.DARK_GRAY, rect)
                else:
                    pygame.draw.rect(self.screen, self.WHITE, rect)

                pygame.draw.rect(self.screen, self.GRAY, rect, 1)

                # Dibujar elementos de la celda
                for element in cell:
                    if element == "C":
                        self.screen.blit(self.gato_img, rect.topleft)
                    elif element == "G":
                        self.screen.blit(self.queso_img, rect.topleft)
                    elif element == "R":
                        pygame.draw.line(self.screen, self.BLACK, rect.topright, rect.bottomright, 8)
                    elif element == "L":
                        pygame.draw.line(self.screen, self.BLACK, rect.topleft, rect.bottomleft, 4)
                    elif element == "U":
                        pygame.draw.line(self.screen, self.BLACK, rect.topleft, rect.topright, 4)
                    elif element == "D":
                        pygame.draw.line(self.screen, self.BLACK, rect.bottomleft, rect.bottomright, 8)

        if self.raton_pos:     # Dibujar el ratón al final para que esté encima de todo
            row, col = self.raton_pos
            if 0 <= row < self.ROWS and 0 <= col < self.COLS:
                rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                self.screen.blit(self.raton_img, rect.topleft)

    def draw_ui(self):
        """Dibuja la interfaz de usuario en la parte inferior"""
        pygame.draw.rect(self.screen, self.WHITE, (0, self.HEIGHT, self.WIDTH, 50))
        label = self.font.render(f"Herramienta actual: {self.current_tool}", True, self.BLACK)
        self.screen.blit(label, (10, self.HEIGHT + 10))

    def set_cell(self, row, col):
        """Modifica el contenido de una celda según la herramienta actual"""
        # Validación de límites
        if not (0 <= row < self.ROWS and 0 <= col < self.COLS):
            print("Error: Intento de modificar celda fuera de los límites.")
            return

        current = self.editor_grid[row][col]
        current_element_count = len(current.strip()) # Cuenta los elementos existentes

        if self.current_tool == "raton":
            if "X" in current or "C" in current:
                print("No se puede colocar el ratón sobre 'X' o 'C'.")
                return
            self.raton_pos = (row, col)

        elif self.current_tool == "queso": 
            if "X" in current or "C" in current:
                print("No se puede colocar el queso sobre 'X', 'C'.")
                return
            if "G" not in current and current_element_count >= 4:
                print(f"Límite de 4 elementos alcanzado en [{row},{col}]. No se puede añadir Queso ('G').")
                return
            if self.queso_pos:
                q_row, q_col = self.queso_pos
                if 0 <= q_row < self.ROWS and 0 <= q_col < self.COLS:
                    old_cell_content = self.editor_grid[q_row][q_col].replace("G", "")
                    self.editor_grid[q_row][q_col] = old_cell_content if old_cell_content.strip() else " " 
            if "G" not in current:
                self.editor_grid[row][col] = "G" if current == " " else current + "G"
            self.queso_pos = (row, col)

        elif self.current_tool == "empty":
            if (row, col) == self.raton_pos:
                self.raton_pos = None
            if (row, col) == self.queso_pos:
                self.queso_pos = None
            self.editor_grid[row][col] = " "

        elif self.current_tool == "X": 
            if (row, col) == self.raton_pos or (row, col) == self.queso_pos or "C" in current:
                print("No se puede colocar 'X' sobre Ratón, Queso o Gato.")
                return
            self.editor_grid[row][col] += "X"

        elif self.current_tool == "C": # Gato
            if "X" in current or "G" in current or (row, col) == self.raton_pos:
                print("No se puede colocar 'C' sobre 'X', Queso ('G') o Ratón.")
                return
            if "C" not in current and current_element_count >= 4:
                print(f"Límite de 4 elementos alcanzado en [{row},{col}]. No se puede añadir Gato ('C').")
                return
            if "C" not in current:
                self.editor_grid[row][col] = "C" if current == " " else current + "C"

        elif self.current_tool in ["R", "L", "U", "D"]:
            if self.current_tool not in current and current_element_count >= 4:
                print(f"Límite de 4 elementos alcanzado en [{row},{col}]. No se puede añadir Pared ('{self.current_tool}').")
                return
            if self.current_tool not in current:
                self.editor_grid[row][col] = self.current_tool if current == " " else current + self.current_tool

    def get_final_map_data(self):
        if self.raton_pos is None:
            print("ERROR: El Ratón (posición inicial) no ha sido colocado en el mapa.")
            return None, None
        if self.queso_pos is None:
            print("ERROR: El Queso (objetivo) no ha sido colocado en el mapa.")
            return None, None
        
        final_grid = [row[:] for row in self.editor_grid]
        
        print("\n--- Mapa Final Generado ---")
        print("Grid:")
        # Imprimimos cada fila con una coma al final
        for i, r in enumerate(final_grid):
            row_str = str(r)
            if i < len(final_grid) - 1:  # Todas las filas excepto la última llevan coma
                row_str += ','
            print(row_str)
        print("Posición Inicial Queso:", self.queso_pos)
        print("Posición Inicial Raton", self.raton_pos)
        print("-------------------------\n")

        return final_grid, self.queso_pos, self.raton_pos

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_ui()
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if y < self.HEIGHT:
                        row = y // self.CELL_SIZE
                        col = x // self.CELL_SIZE
                        if event.button == 1:
                            self.set_cell(row, col)
                        elif event.button == 3:
                            self.editor_grid[row][col] = " "

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.current_tool = "raton"
                    elif event.key == pygame.K_2:
                        self.current_tool = "queso"
                    elif event.key == pygame.K_3:
                        self.current_tool = "X"
                    elif event.key == pygame.K_4:
                        self.current_tool = "C"

                    elif event.unicode.lower() == 'r':
                        self.current_tool = "R"
                    elif event.unicode.lower() == 'd':
                        self.current_tool = "D"
                    elif event.unicode.lower() == 'l':
                        self.current_tool = "L"
                    elif event.unicode.lower() == 'u':
                        self.current_tool = "U"

                    elif event.key == pygame.K_0:
                        self.current_tool = "empty"

                    elif event.key == pygame.K_s:
                        final_map, start_pos, agent_position = self.get_final_map_data()
                        if final_map and start_pos and agent_position:
                            print("¡Mapa exportado a consola!")
                            return final_map, start_pos, agent_position
                        else:
                            print("Exportación fallida: Revisa que el ratón y el queso estén colocados.")
                            

# if __name__ == "__main__":
#     editor = EditorLaberinto()
#     editor.run()