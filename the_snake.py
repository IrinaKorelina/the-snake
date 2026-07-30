from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
# ---------------------------------------------------------
# Базовый класс GameObject
# ---------------------------------------------------------
class GameObject:
    def __init__(self):
        # Центральная точка экрана
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = (0, 0, 0)

    def draw(self, surface):
        pass


# ---------------------------------------------------------
# Класс Apple (яблоко)
# ---------------------------------------------------------
class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайную позицию яблока на сетке"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


# ---------------------------------------------------------
# Класс Snake (змейка)
# ---------------------------------------------------------
class Snake(GameObject):
    def __init__(self):
        super().__init__()
        # Змейка — это список сегментов (координат)
        self.segments = [self.position]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.last = None  # последний сегмент перед движением (для стирания)

    def get_head_position(self):
        return self.segments[0]

    def change_direction(self, new_direction):
        # Нельзя развернуться на 180 градусов
        opposite = {
            UP: DOWN,
            DOWN: UP,
            LEFT: RIGHT,
            RIGHT: LEFT
        }
        if new_direction != opposite.get(self.direction):
            self.next_direction = new_direction

    def move(self):
        # Если есть новое направление — обновляем текущее
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)

        # Сохраняем последний сегмент, чтобы потом стереть его
        self.last = self.segments[-1]

        # Добавляем новый сегмент головы
        self.segments.insert(0, new_head)

        # Удаляем хвост (если не было роста) — рост будем обрабатывать отдельно
        self.segments.pop()

    def grow(self):
        # Просто не удаляем хвост при следующем движении
        # Для этого добавим флаг или просто не будем делать pop в move
        # Самый простой способ — добавить лишний сегмент и не удалять его в следующем шаге.
        # Но в этой реализации проще: при поедании яблока мы просто не делаем pop в move.
        # Чтобы это работало, нужно передать флаг grow в move, либо сделать отдельный метод.
        # Сделаем проще: добавим сегмент и пометим, что рост уже учтён.
        self.segments.append(self.last)  # дублируем последний сегмент

    def check_collision(self):
        head = self.get_head_position()
        # Столкновение со стенами
        if not (0 <= head[0] < SCREEN_WIDTH and 0 <= head[1] < SCREEN_HEIGHT):
            return True
        # Столкновение с собой (кроме головы)
        if head in self.segments[1:]:
            return True
        return False

    def draw(self, surface):
        # Отрисовка всех сегментов
        for position in self.segments:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    # Флаг роста: если змейка съела яблоко, в следующем кадре не удаляем хвост
    grow_next_frame = False

    # while True:
    #     clock.tick(SPEED)

          handle_keys(snake)

        # Тут опишите основную логику игры.
        # # Логика движения
        if grow_next_frame:
            # Сначала добавляем сегмент (рост)
            snake.grow()
            grow_next_frame = False
        snake.move()

        # Проверка столкновений
        if snake.check_collision():
            # Здесь можно добавить экран «Game Over», пока просто перезапускаем
            snake = Snake()
            apple = Apple()
            continue

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            grow_next_frame = True

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
