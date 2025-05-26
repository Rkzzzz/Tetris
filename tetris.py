# Импортируем необходимые библиотеки
import pygame  # Для создания игры
import random  # Для случайного выбора фигур

# Настройка цветов в формате RGB (Red, Green, Blue)
BLACK = (0, 0, 0)        # Черный цвет для фона
WHITE = (255, 255, 255)  # Белый цвет для текста
GRAY = (128, 128, 128)   # Серый цвет для сетки
# Цвета для разных типов фигур:
COLORS = [
    (0, 255, 255),  # Голубой - I-образная
    (0, 0, 255),    # Синий - J-образная
    (255, 128, 0),  # Оранжевый - L-образная
    (255, 255, 0),  # Желтый - O-образная
    (0, 255, 0),    # Зеленый - S-образная
    (255, 0, 0),    # Красный - Z-образная
    (128, 0, 255)   # Фиолетовый - T-образная
]

# Настройки игрового поля
GRID_WIDTH = 10     # Ширина в клетках
GRID_HEIGHT = 20    # Высота в клетках
CELL_SIZE = 30      # Размер одной клетки в пикселях
# Рассчитываем размер окна игры:
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 60            # Частота обновления экрана (кадров в секунду)

# Все возможные фигуры Тетриса (матрицы из 0 и 1)
PIECES = [
    [[1, 1, 1, 1]],              # I-образная
    [[1, 0, 0], [1, 1, 1]],      # J-образная
    [[0, 0, 1], [1, 1, 1]],      # L-образная
    [[1, 1], [1, 1]],            # O-образная
    [[0, 1, 1], [1, 1, 0]],      # S-образная
    [[1, 1, 0], [0, 1, 1]],      # Z-образная
    [[0, 1, 0], [1, 1, 1]]       # T-образная
]
# Созжание игровой сетки
def create_grid(width, height):
    # Создаем список списков (матрицу), заполненную нулями
    return [[0 for _ in range(width)] for _ in range(height)]

def draw_grid(surface, grid):
    """Рисует игровое поле на экране"""
    for y, row in enumerate(grid):     # y - номер строки
        for x, cell in enumerate(row):  # x - номер столбца
            if cell:  # Если клетка не пустая (0 - пустая)
                # Рисуем цветной квадрат
                pygame.draw.rect(
                    surface,
                    COLORS[cell-1],  # Выбираем цвет из списка
                    (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
                # Рисуем серую границу вокруг квадрата
                pygame.draw.rect(
                    surface,
                    GRAY,
                    (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    1  # Толщина линии
                )

def generate_piece():
    """Создает случайную фигуру"""
    random_index = random.randint(0, len(PIECES)-1)
    return PIECES[random_index], random_index + 1  # Фигура + цвет

def is_valid_move(piece, grid, offset_x, offset_y):
    """Проверяет можно ли поставить фигуру в указанную позицию"""
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:  # Если часть фигуры есть в этой клетке
                # Вычисляем позицию на игровом поле
                new_x = offset_x + x
                new_y = offset_y + y
                # Проверяем выход за границы и пересечение с другими фигурами
                if (new_x < 0 or new_x >= GRID_WIDTH or
                    new_y >= GRID_HEIGHT or
                    grid[new_y][new_x] != 0):
                    return False
    return True

def place_piece(piece, grid, offset_x, offset_y, color):
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                # Заполняем клетку на поле соответствующим цветом
                grid[offset_y + y][offset_x + x] = color

def remove_full_rows(grid):
    rows_to_remove = []
    # Ищем заполненные строки
    for i, row in enumerate(grid):
        if all(row):  # Если все элементы в строке не нули
            rows_to_remove.append(i)
    
    # Удаляем найденные строки и добавляем новые сверху
    for i in rows_to_remove:
        del grid[i]
        grid.insert(0, [0]*GRID_WIDTH)
    
    return len(rows_to_remove)  # Количество удаленных строк

def rotate_piece(piece):
    """Поворачивает фигуру на 90 градусов по часовой стрелке"""
    # Получаем размеры оригинальной фигуры
    rows = len(piece)
    cols = len(piece[0])
    # Создаем новую матрицу для повернутой фигуры
    new_piece = [[0]*rows for _ in range(cols)]
    # Заполняем новую матрицу
    for y in range(rows):
        for x in range(cols):
            new_piece[x][rows-1-y] = piece[y][x]
    return new_piece

def main():
    """Главная функция с игровым циклом"""
    # Инициализация игры
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Создаем игровое поле
    grid = create_grid(GRID_WIDTH, GRID_HEIGHT)
    
    # Начальные настройки игры
    current_piece, current_color = generate_piece()  # Первая фигура
    piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2  # Центр по X
    piece_y = 0                 # Начальная позиция по Y
    game_over = False           # Флаг окончания игры
    fall_speed = 1              # Начальная скорость падения
    fall_timer = 0              # Счетчик времени для падения
    score = 0                   # Счет игрока
    level = 1                   # Уровень сложности
    cleared_lines = 0           # Всего очищено линий

    # Главный игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Движение влево
                    if is_valid_move(current_piece, grid, piece_x-1, piece_y):
                        piece_x -= 1
                elif event.key == pygame.K_d:  # Движение вправо
                    if is_valid_move(current_piece, grid, piece_x+1, piece_y):
                        piece_x += 1
                elif event.key == pygame.K_s:  # Ускоренное падение
                    if is_valid_move(current_piece, grid, piece_x, piece_y+1):
                        piece_y += 1
                elif event.key == pygame.K_w:  # Поворот фигуры
                    rotated = rotate_piece(current_piece)
                    if is_valid_move(rotated, grid, piece_x, piece_y):
                        current_piece = rotated
                elif event.key == pygame.K_SPACE:  # Мгновенное падение
                    while is_valid_move(current_piece, grid, piece_x, piece_y+1):
                        piece_y += 1

        # Логика игры
        if not game_over:
            # Обновляем таймер падения
            fall_timer += clock.get_time() / 1000  # Преобразуем в секунды
            
            # Автоматическое падение фигуры
            if fall_timer >= 1 / fall_speed:
                fall_timer = 0  # Сбрасываем таймер
                if is_valid_move(current_piece, grid, piece_x, piece_y+1):
                    piece_y += 1
                else:
                    # Фиксируем фигуру на поле
                    place_piece(current_piece, grid, piece_x, piece_y, current_color)
                    # Проверяем заполненные строки
                    cleared = remove_full_rows(grid)
                    if cleared > 0:
                        score += cleared * 100 * level  # Начисляем очки
                        cleared_lines += cleared
                        # Повышаем уровень каждые 5 очищенных линий
                        if cleared_lines >= 5:
                            level += 1
                            fall_speed += 0.5  # Увеличиваем скорость
                            cleared_lines -= 5
                    
                    # Создаем новую фигуру
                    current_piece, current_color = generate_piece()
                    piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
                    piece_y = 0
                    
                    # Проверяем проигрыш
                    if not is_valid_move(current_piece, grid, piece_x, piece_y):
                        game_over = True

        # Отрисовка
        screen.fill(BLACK)  # Заливаем фон
        draw_grid(screen, grid)  # Рисуем поле
        
        # Рисуем текущую падающую фигуру
        for y, row in enumerate(current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        COLORS[current_color-1],
                        ((piece_x + x)*CELL_SIZE,
                        (piece_y + y)*CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE)
                    )
        
        # Отображение счета и уровня
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        
        # Сообщение о конце игры
        if game_over:
            font = pygame.font.Font(None, 50)
            text = font.render("GAME OVER!", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text, text_rect)
            
            text_score = font.render(f"Final Score: {score}", True, WHITE)
            text_rect = text_score.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
            screen.blit(text_score, text_rect)

        pygame.display.flip()  # Обновляем экран
        clock.tick(FPS)       # Контроль частоты кадров

    pygame.quit()  # Завершаем игру

# Запуск игры
if __name__ == "__main__":
    main()
