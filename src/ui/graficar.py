import pygame
import sys
from controller.controller import Controller
from ui.config_ui import Colors, Images, Tools
from constants.maze_options import option_to_string, string_to_option
from ui.elements import ElementFactory


class GraphMaze:
    def __init__(self, grid: list[list[str]], raton_pos: tuple[int, int]):
        # Configuración inicial
        self.ROWS = len(grid)
        self.COLS = len(grid[0]) if self.ROWS > 0 else 0
        self.WIDTH, self.HEIGHT = 600, 600

        self.UI_HEIGHT = 4 * 20 + 10  # 3 líneas de 20px + algo de margen
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT + self.UI_HEIGHT)
        )

        self.CELL_WIDTH = self.WIDTH // self.COLS
        self.CELL_HEIGHT = self.HEIGHT // self.ROWS
        self.CELL_SIZE = min(self.CELL_WIDTH, self.CELL_HEIGHT)  # Para que sea cuadrada

        # Inicializar pygame
        pygame.init()
        pygame.display.set_caption("Visualizador de Laberinto")
        self.font = pygame.font.SysFont("Arial", 20)

        # Mapa y posición del ratón
        self.grid = grid
        self.raton_pos = raton_pos

        Images.set_scale(self.CELL_SIZE)

    def __draw_element(self, cell: str, rect: pygame.Rect) -> None:
        for element in cell:
            if element == option_to_string("OBSTACLE") or element == option_to_string(
                "FREE"
            ):
                continue

            tool = string_to_option(element)

            if tool is None:
                return None

            ElementFactory.get_element(Tools[tool]).draw(self.screen, rect)

    def draw_grid(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell = self.grid[row][col]
                rect = pygame.Rect(
                    col * self.CELL_SIZE,
                    row * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE,
                )

                if option_to_string("OBSTACLE") in cell:
                    ElementFactory.get_element(Tools.OBSTACLE).draw(self.screen, rect)
                else:
                    ElementFactory.get_element(Tools.FREE).draw(self.screen, rect)

                pygame.draw.rect(self.screen, Colors.division, rect, 1)
                self.__draw_element(cell, rect)

        if self.raton_pos:  # Dibujar el ratón al final para que esté encima de todo
            row, col = self.raton_pos

            if not 0 <= row < self.ROWS or not 0 <= col < self.COLS:
                return

            rect = pygame.Rect(
                col * self.CELL_SIZE,
                row * self.CELL_SIZE,
                self.CELL_SIZE,
                self.CELL_SIZE,
            )

            ElementFactory.get_element(Tools.MOUSE).draw(self.screen, rect)

    def update_position(self, new_pos):
        if 0 <= new_pos[0] < self.ROWS and 0 <= new_pos[1] < self.COLS:
            self.raton_pos = new_pos
            return True
        return False

    def draw_ui(self, controller: Controller):
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, self.HEIGHT, self.WIDTH, self.UI_HEIGHT),
        )

        line_spacing = 20  # Espacio entre líneas
        x, y = 10, self.HEIGHT + 5

        # Línea 1
        label1 = self.font.render(
            f"Búsqueda actual: {controller.get_state()['search_name']}", True, (0, 0, 0)
        )
        self.screen.blit(label1, (x, y))

        # Línea 2
        label2 = self.font.render(
            f"Cantidad de movimientos: {controller.get_state()['step']}",
            True,
            (0, 0, 0),
        )
        self.screen.blit(label2, (x, y + line_spacing))

        # Línea 3
        label3 = self.font.render(
            f"Posición del ratón: {self.raton_pos}", True, (0, 0, 0)
        )
        self.screen.blit(label3, (x, y + 2 * line_spacing))

        # Línea 3
        if self.raton_pos == controller.get_state()["goal_position"]:
            label3 = self.font.render("Ahora puedes descansar!!!", True, (0, 0, 0))
            self.screen.blit(label3, (x, y + 3 * line_spacing))

    def run(self, controller: Controller):
        clock = pygame.time.Clock()

        while controller.is_running():
            self.event_pygame(controller)

            # Se obtiene el nuevo estado del laberinto
            state = controller.get_state()
            self.grid = state["maze"].get_map()
            self.update_position(state["agent_position"])

            self.render(controller)
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def event_pygame(self, controller: Controller):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                controller.set_running(False)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_event(event, controller)

    def handle_key_event(self, event, controller: Controller):
        if event.key == pygame.K_ESCAPE:
            controller.set_running(False)
        elif event.key == pygame.K_SPACE:
            controller.update()

    def render(self, controller: Controller):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.draw_ui(controller)
        pygame.display.flip()
