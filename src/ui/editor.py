from typing import Optional
import pygame
import sys
import tkinter as tk
from tkinter import font
from ui.config_ui import Colors, Images, Tools, Window
from constants.maze_options import option_to_string, string_to_option
from ui.elements import ElementFactory


def create_window():
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
    tk.Label(ventana, text="Número de filas:", font=fuente).grid(
        row=0, column=0, padx=15, pady=10, sticky="e"
    )
    entry_filas = tk.Entry(ventana, font=fuente, width=10)
    entry_filas.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana, text="Número de columnas:", font=fuente).grid(
        row=1, column=0, padx=15, pady=10, sticky="e"
    )
    entry_columnas = tk.Entry(ventana, font=fuente, width=10)
    entry_columnas.grid(row=1, column=1, padx=10, pady=10)

    label_error = tk.Label(ventana, text="", fg="red", font=fuente)
    label_error.grid(row=2, column=0, columnspan=2, pady=(0, 5))

    boton = tk.Button(
        ventana,
        text="Aceptar",
        command=aceptar,
        bg="#4CAF50",
        fg="white",
        font=fuente,
        width=12,
    )
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

    width: int = 600
    height: int = 600

    return Window(filas, columnas, width, height)


class ConfigMaze:
    def __init__(self, window: Window):
        # Configuración inicial
        self.__window = window
        self.__cell_width = self.__window.width // self.__window.cols
        self.__cell_height = self.__window.height // self.__window.rows
        self.__cell_size = min(self.__cell_width, self.__cell_height)

        # Inicializar pygame
        pygame.init()
        self.__screen = pygame.display.set_mode(
            (self.__window.width, self.__window.height + 50)
        )
        pygame.display.set_caption("Editor de Laberinto")
        self.font = pygame.font.SysFont("Arial", 20)

        # Herramientas disponibles
        self.current_tool = Tools.MOUSE.value

        # Mapa visual inicial
        self.editor_grid = [
            [" " for _ in range(self.__window.cols)] for _ in range(self.__window.rows)
        ]
        self.raton_pos = None
        self.queso_pos = None

        # Ratón y queso
        Images.set_scale(self.__cell_size)

    def __draw_element(self, cell: str, rect: pygame.Rect) -> None:
        for element in cell:
            if element == option_to_string("OBSTACLE") or element == option_to_string(
                "FREE"
            ):
                continue

            tool = string_to_option(element)

            if tool is None:
                return None

            ElementFactory.get_element(Tools[tool]).draw(self.__screen, rect)

    def draw_grid(self):
        for row in range(self.__window.rows):
            for col in range(self.__window.cols):
                cell = self.editor_grid[row][col]
                rect = pygame.Rect(
                    col * self.__cell_size,
                    row * self.__cell_size,
                    self.__cell_size,
                    self.__cell_size,
                )

                if option_to_string("OBSTACLE") in cell:
                    ElementFactory.get_element(Tools.OBSTACLE).draw(self.__screen, rect)
                else:
                    pygame.draw.rect(self.__screen, Colors.free, rect)

                pygame.draw.rect(self.__screen, Colors.division, rect, 1)
                self.__draw_element(cell, rect)

                # Dibujar elementos de la celda
                # for element in cell:
                #     if element == "C":
                #         self.screen.blit(self.gato_img, rect.topleft)
                #     elif element == "G":
                #         self.screen.blit(self.queso_img, rect.topleft)
                #     elif element == "R":
                #         pygame.draw.line(
                #             self.screen,
                #             self.__colors.wall,
                #             rect.topright,
                #             rect.bottomright,
                #             8,
                #         )
                #     elif element == "L":
                #         pygame.draw.line(
                #             self.screen,
                #             self.__colors.wall,
                #             rect.topleft,
                #             rect.bottomleft,
                #             4,
                #         )
                #     elif element == "U":
                #         pygame.draw.line(
                #             self.screen,
                #             self.__colors.wall,
                #             rect.topleft,
                #             rect.topright,
                #             4,
                #         )
                #     elif element == "D":
                #         pygame.draw.line(
                #             self.screen,
                #             self.__colors.wall,
                #             rect.bottomleft,
                #             rect.bottomright,
                #             8,
                #         )

        if self.raton_pos:  # Dibujar el ratón al final para que esté encima de todo
            row, col = self.raton_pos

            if not 0 <= row < self.__window.rows or not 0 <= col < self.__window.cols:
                return

            rect = pygame.Rect(
                col * self.__cell_size,
                row * self.__cell_size,
                self.__cell_size,
                self.__cell_size,
            )

            ElementFactory.get_element(Tools.MOUSE).draw(self.__screen, rect)

    def draw_ui(self):
        """Dibuja la interfaz de usuario en la parte inferior"""
        pygame.draw.rect(
            self.__screen,
            (255, 255, 255),
            (0, self.__window.height, self.__window.width, 50),
        )
        label = self.font.render(
            f"Herramienta actual: {self.current_tool}", True, (0, 0, 0)
        )
        self.__screen.blit(label, (10, self.__window.height + 10))

    def set_mouse_fix(self, target: str, valid_elements: list[Tools]) -> Optional[str]:
        count: int = 0
        message: str = f"No se puede colocar el {self.current_tool} sobre un"

        for element in valid_elements:
            if option_to_string(element.name) in target:
                message += f" {element.value.lower()}"
                count += 1

        if count == 0:
            return None

        return message

    def set_cell(self, row, col):
        """Modifica el contenido de una celda según la herramienta actual"""
        # Validación de límites
        if not 0 <= row < self.__window.rows or not 0 <= col < self.__window.cols:
            print("Error: Intento de modificar celda fuera de los límites.")
            return

        current = self.editor_grid[row][col]
        current_element_count = len(current.strip())  # Cuenta los elementos existentes

        if self.current_tool == Tools.MOUSE.value:
            if "X" in current or "C" in current:
                print("No se puede colocar el ratón sobre 'X' o 'C'.")
                return
            
            self.raton_pos = (row, col)

        elif self.current_tool == "queso":
            if "X" in current or "C" in current:
                print("No se puede colocar el queso sobre 'X', 'C'.")
                return
            if "G" not in current and current_element_count >= 4:
                print(
                    f"Límite de 4 elementos alcanzado en [{row},{col}]. No se puede añadir Queso ('G')."
                )
                return
            if self.queso_pos:
                q_row, q_col = self.queso_pos
                if 0 <= q_row < self.__window.rows and 0 <= q_col < self.__window.cols:
                    old_cell_content = self.editor_grid[q_row][q_col].replace("G", "")
                    self.editor_grid[q_row][q_col] = (
                        old_cell_content if old_cell_content.strip() else " "
                    )
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
            if (
                (row, col) == self.raton_pos
                or (row, col) == self.queso_pos
                or "C" in current
            ):
                print("No se puede colocar 'X' sobre Ratón, Queso o Gato.")
                return
            self.editor_grid[row][col] += "X"

        elif self.current_tool == "C":  # Gato
            if "X" in current or "G" in current or (row, col) == self.raton_pos:
                print("No se puede colocar 'C' sobre 'X', Queso ('G') o Ratón.")
                return
            if "C" not in current and current_element_count >= 4:
                print(
                    f"Límite de 4 elementos alcanzado en [{row},{col}]. No se puede añadir Gato ('C')."
                )
                return
            if "C" not in current:
                self.editor_grid[row][col] = "C" if current == " " else current + "C"

        elif self.current_tool in ["R", "L", "U", "D"]:
            if self.current_tool not in current and current_element_count >= 4:
                print(
                    f"Límite de 4 elementos alcanzado en [{row},{col}]. No se puede añadir Pared ('{self.current_tool}')."
                )
                return
            if self.current_tool not in current:
                self.editor_grid[row][col] = (
                    self.current_tool if current == " " else current + self.current_tool
                )

    # def get_final_map_data(self):
    #     """Obtiene los datos finales del mapa para exportar"""
    #     if self.raton_pos is None:
    #         print("ERROR: El Ratón (posición inicial) no ha sido colocado en el mapa.")
    #         return None, None
    #     if self.queso_pos is None:
    #         print("ERROR: El Queso (objetivo) no ha sido colocado en el mapa.")
    #         return None, None

    #     # Retorna una copia profunda para evitar modificaciones externas accidentales
    #     final_grid = [row[:] for row in self.editor_grid]
    #     final_raton_pos = self.raton_pos

    #     print("\n--- Mapa Final Generado ---")
    #     print("Grid:")
    #     for r in final_grid:
    #         print(r)
    #     print("Posición Inicial Ratón:", final_raton_pos)
    #     print("Posición Queso:", self.queso_pos)
    #     print("-------------------------\n")

    #     return final_grid, self.queso_pos, final_raton_pos

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
        self.__running = True

        while self.__running:
            self.render()
            clock.tick(60)
            self.event_pygame()
            
    def event_pygame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_event(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_event(event)
                
    def render(self):
        self.__screen.fill((255, 255, 255))
        self.draw_grid()
        self.draw_ui()
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

    def handle_mouse_event(self, event):
        x, y = pygame.mouse.get_pos()
        if y < self.__window.height:
            row = y // self.__cell_size
            col = x // self.__cell_size
            if event.button == 1:
                self.set_cell(row, col)
            elif event.button == 3:
                self.editor_grid[row][col] = " "

    def handle_key_event(self, event):

        key = event.key
        unicode = event.unicode.lower()

        tool_keys = {
            pygame.K_1: Tools.MOUSE.value,
            pygame.K_2: "queso",
            pygame.K_3: "X",
            pygame.K_4: "C",
            pygame.K_0: "empty",
            ord("r"): "R",
            ord("d"): "D",
            ord("l"): "L",
            ord("u"): "U",
        }

        if key in tool_keys:
            self.current_tool = tool_keys[key]
        elif unicode in ['r', 'd', 'l', 'u']:
            self.current_tool = unicode.upper()
        elif key == pygame.K_s:
            self.__running = False
        

    def export_map(self):
        final_map, goal_position ,agent_position, = self.get_final_map_data()
        if final_map and goal_position and agent_position:
            print("¡Mapa exportado a consola!")
            return final_map, goal_position, agent_position
        else:
            print(
                "Exportación fallida: Revisa que el ratón y el queso estén colocados."
            )
