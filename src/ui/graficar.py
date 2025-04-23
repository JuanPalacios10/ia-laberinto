import pygame
import sys
from controller.controller import Controller

class GraficarLaberinto:
    def __init__(self, grid: list[list[str]], raton_pos: tuple[int,int]):
        
        # Configuración inicial
        self.ROWS = len(grid)
        self.COLS = len(grid[0]) if self.ROWS > 0 else 0
        self.WIDTH, self.HEIGHT = 600, 600
        
        self.CELL_WIDTH = self.WIDTH // self.COLS
        self.CELL_HEIGHT = self.HEIGHT // self.ROWS
        self.CELL_SIZE = min(self.CELL_WIDTH, self.CELL_HEIGHT)  # Para que sea cuadrada

        # Colores (los mismos que en el editor para consistencia)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (120, 120, 120)  # Para paredes 'X'
        self.RED = (255, 0, 0)  # Para resaltar el ratón

        # Inicializar pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Visualizador de Laberinto")
        self.font = pygame.font.SysFont("Arial", 20)

        # Mapa y posición del ratón
        self.grid = grid
        self.raton_pos = raton_pos
        self.current_pos = raton_pos  # Posición actual del ratón (puede moverse)

        # Cargar imágenes (asegúrate de tener estas imágenes en la carpeta assets)
        try:
            self.raton_img = pygame.image.load("assets/mouse.png")
            self.queso_img = pygame.image.load("assets/cheese.png")
            self.gato_img = pygame.image.load("assets/cat.png")
            
            self.raton_img = pygame.transform.scale(self.raton_img, (self.CELL_SIZE, self.CELL_SIZE))
            self.queso_img = pygame.transform.scale(self.queso_img, (self.CELL_SIZE, self.CELL_SIZE))
            self.gato_img = pygame.transform.scale(self.gato_img, (self.CELL_SIZE, self.CELL_SIZE))
        except:
            print("Advertencia: No se pudieron cargar las imágenes. Usando formas geométricas.")
            self.raton_img = None
            self.queso_img = None
            self.gato_img = None

    def draw_grid(self):
        """Dibuja el laberinto completo"""
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell = self.grid[row][col]
                rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, 
                                  self.CELL_SIZE, self.CELL_SIZE)

                # Dibujar fondo de la celda
                if "X" in cell:
                    pygame.draw.rect(self.screen, self.DARK_GRAY, rect)
                else:
                    pygame.draw.rect(self.screen, self.WHITE, rect)

                pygame.draw.rect(self.screen, self.GRAY, rect, 1)  # Borde

                # Dibujar elementos de la celda
                for element in cell:
                    if element == "C":  # Gato
                        if self.gato_img:
                            self.screen.blit(self.gato_img, rect.topleft)
                        else:
                            pygame.draw.circle(self.screen, self.BLACK, rect.center, self.CELL_SIZE//3)
                    elif element == "G":  # Queso
                        if self.queso_img:
                            self.screen.blit(self.queso_img, rect.topleft)
                        else:
                            pygame.draw.polygon(self.screen, (255, 255, 0), [
                                (rect.left + rect.width//2, rect.top),
                                (rect.right, rect.top + rect.height//2),
                                (rect.left + rect.width//2, rect.bottom),
                                (rect.left, rect.top + rect.height//2)
                            ])
                    elif element == "R":  # Pared derecha
                        pygame.draw.line(self.screen, self.BLACK, rect.topright, rect.bottomright, 8)
                    elif element == "L":  # Pared izquierda
                        pygame.draw.line(self.screen, self.BLACK, rect.topleft, rect.bottomleft, 4)
                    elif element == "U":  # Pared arriba
                        pygame.draw.line(self.screen, self.BLACK, rect.topleft, rect.topright, 4)
                    elif element == "D":  # Pared abajo
                        pygame.draw.line(self.screen, self.BLACK, rect.bottomleft, rect.bottomright, 8)

        # Dibujar posición actual del ratón
        if self.current_pos:
            row, col = self.current_pos
            if 0 <= row < self.ROWS and 0 <= col < self.COLS:
                rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, 
                                 self.CELL_SIZE, self.CELL_SIZE)
                if self.raton_img:
                    self.screen.blit(self.raton_img, rect.topleft)
                else:
                    pygame.draw.circle(self.screen, self.RED, rect.center, self.CELL_SIZE//3)

    def update_position(self, new_pos):
        """Actualiza la posición del ratón"""
        if 0 <= new_pos[0] < self.ROWS and 0 <= new_pos[1] < self.COLS:
            self.current_pos = new_pos
            return True
        return False
    

    def run(self, controller: Controller):
        clock = pygame.time.Clock()

        while controller.is_running():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    controller.set_running(False)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        controller.set_running(False)
                    elif event.key == pygame.K_SPACE:
                        controller.update()
            
            # Se obtiene el nuevo estado del laberinto 
            state = controller.get_state()
            self.grid = state["maze"].get_map() 
            self.update_position(state["agent_position"])  
            
            self.screen.fill(self.WHITE)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()
