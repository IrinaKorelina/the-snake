import pygame
from random import randint


# --- Константы ---
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20


# --- Классы ---
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализирует базовый игровой объект в центре экрана."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = (0, 0, 0)

    def draw(self, surface):
        """Отрисовывает объект на поверхности. Должен быть переопределён в наследниках."""
        pass


class Apple(GameObject):
    """Класс яблока — целевого объекта в игре «Змейка»."""

    def __init__(self):
        """Создаёт яблоко, задаёт его цвет и размещает в случайной точке поля."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Размещает яблоко в случайной клетке игрового поля."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко как закрашенный квадрат с обводкой."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки — основного игрового объекта."""

    def __init__(self):
        """Создаёт змейку: задаёт цвет, начальное направление и позицию."""
        super().__init__()
        self.segments = [self.position]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки (первого сегмента)."""
        return self.segments[0]

    def change_direction(self, new_direction):
        """
        Устанавливает новое направление движения, если оно не противоположно текущему.

        :param new_direction:
