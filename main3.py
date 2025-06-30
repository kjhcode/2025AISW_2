import pygame
import random

# 🎨 게임 설정
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30 # 한 칸의 크기 (픽셀)
PLAY_WIDTH = 10 * GRID_SIZE # 게임판 너비 (10칸)
PLAY_HEIGHT = 20 * GRID_SIZE # 게임판 높이 (20칸)
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT

# 🌈 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# 🧱 테트리스 블록 모양 (7가지)
# 각 블록은 4x4 그리드 내에서 정의돼. (0,0)은 블록의 왼쪽 위 기준점이야.
# 0은 빈 공간, 1은 블록 조각을 의미해.
S = [['.00.',
      '00..',
      '....',
      '....'],
     ['.0..',
      '.00.',
      '..0.',
      '....']]

Z = [['00..',
      '.00.',
      '....',
      '....'],
     ['..0.',
      '.00.',
      '.0..',
      '....']]

I = [['.0..',
      '.0..',
      '.0..',
      '.0..'],
     ['....',
      '0000',
      '....',
      '....']]

O = [['00..',
      '00..',
      '....',
      '....']] # O 블록은 회전해도 모양이 같아서 하나만 정의해.

J = [['.0..',
      '.000',
      '....',
      '....'],
     ['.00.',
      '.0..',
      '.0..',
      '....'],
     ['000.',
      '..0.',
      '....',
      '....'],
     ['..0.',
      '..0.',
      '.00.',
      '....']]

L = [['..0.',
      '000.',
      '....',
      '....'],
     ['.0..',
      '.0..',
      '.00.',
      '....'],
     ['.000',
      '.0..',
      '....',
      '....'],
     ['.00.',
      '..0.',
      '..0.',
      '....']]

T = [['.0..',
      '000.',
      '....',
      '....'],
     ['.0..',
      '.00.',
      '.0..',
      '....'],
     ['000.',
      '.0..',
      '....',
      '....'],
     ['.0..',
      '00..',
      '.0..',
      '....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [RED, GREEN, BLUE, ORANGE, CYAN, PURPLE, YELLOW]

# 🎮 블록 객체 정의
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0 # 현재 회전 상태

# ⚙️ 게임판 만들기
# 게임판은 블록 조각들이 쌓이는 공간이야. 0은 빈 공간, 0이 아니면 블록 조각이 있다는 뜻.
grid = [[BLACK for _ in range(10)] for _ in range(20)]

# 🎲 새로운 블록 생성
def create_new_piece():
    shape = random.choice(SHAPES)
    return Piece(5, 0, shape) # x=5, y=0에서 시작 (가운데 위)

# 🔄 블록 모양 가져오기 (회전된 상태 포함)
def get_shape_format(piece):
    return piece.shape[piece.rotation % len(piece.shape)]

# 🔍 유효한 공간인지 확인 (충돌 감지)
def check_valid_space(piece, current_grid):
    # 블록 조각이 차지할 공간이 게임판 안에 있고, 다른 블록과 겹치지 않는지 확인
    formatted_shape = get_shape_format(piece)
    
    for i, line in enumerate(formatted_shape):
        row = list(line)
        for j, char in enumerate(row):
            if char == '0':
                # 블록 조각의 실제 위치 계산
                x_pos = piece.x + j
                y_pos = piece.y + i

                # 게임판을 벗어나는지 확인 (좌우, 아래)
                if not (0 <= x_pos < 10 and y_pos < 20):
                    return False
                # 이미 블록이 있는 공간과 겹치는지 확인 (y_pos가 0보다 클 때만)
                if y_pos >= 0 and current_grid[y_pos][x_pos] != BLACK:
                    return False
    return True

# 📌 블록을 게임판에 고정
def fix_piece(piece, current_grid):
    formatted_shape = get_shape_format(piece)
    for i, line in enumerate(formatted_shape):
        row = list(line)
        for j, char in enumerate(row):
            if char == '0':
                # 블록 조각의 실제 위치
                x_pos = piece.x + j
                y_pos = piece.y + i
                if y_pos >= 0: # 게임판 위로 넘어가지 않도록
                    current_grid[y_pos][x_pos] = piece.color
    return current_grid

# 🧹 줄 지우기
def clear_rows(current_grid):
    lines_cleared = 0
    # 아래부터 위로 스캔
    for i in range(len(current_grid) - 1, -1, -1):
        row = current_grid[i]
        # 한 줄이 모두 채워졌는지 확인
        if BLACK not in row:
            lines_cleared += 1
            # 해당 줄을 지우고, 그 위 줄들을 한 칸씩 아래로 내림
            del current_grid[i]
            current_grid.insert(0, [BLACK for _ in range(10)]) # 맨 위에 빈 줄 추가
    return lines_cleared, current_grid

# 📊 점수 계산
def calculate_score(lines_cleared):
    if lines_cleared == 1:
        return 100
    elif lines_cleared == 2:
        return 300
    elif lines_cleared == 3:
        return 500
    elif lines_cleared == 4: # 테트리스!
        return 800
    return 0

# 🖼️ 게임판 그리기
def draw_grid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (sx + j * GRID_SIZE, sy + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
    
    # 게임판 경계선 그리기
    pygame.draw.rect(surface, WHITE, (sx, sy, PLAY_WIDTH, PLAY_HEIGHT), 4)

# 🧱 현재 블록 그리기
def draw_current_piece(surface, piece):
    formatted_shape = get_shape_format(piece)
    for i, line in enumerate(formatted_shape):
        row = list(line)
        for j, char in enumerate(row):
            if char == '0':
                pygame.draw.rect(surface, piece.color,
                                 (TOP_LEFT_X + (piece.x + j) * GRID_SIZE,
                                  TOP_LEFT_Y + (piece.y + i) * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE), 0)

# 📝 텍스트 메시지 표시
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("malgungothic", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (SCREEN_WIDTH / 2 - (label.get_width() / 2), SCREEN_HEIGHT / 2 - (label.get_height() / 2)))

# 🚀 게임 시작 함수
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("팬더의 테트리스")

    current_piece = create_new_piece()
    next_piece = create_new_piece()
    global grid # 전역 변수로 grid 사용
    grid = [[BLACK for _ in range(10)] for _ in range(20)] # 게임 시작 시 grid 초기화

    fall_time = 0
    fall_speed = 0.27 # 블록이 떨어지는 속도 (초)
    level_time = 0
    score = 0
    game_over = False
    
    clock = pygame.time.Clock()

    run = True
    while run:
        # 시간 계산 (블록이 자동으로 떨어지게)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # 일정 시간마다 블록 속도 증가
        if level_time/1000 > 5: # 5초마다 속도 조금씩 빠르게
            level_time = 0
            if fall_speed > 0.12: # 너무 빨라지지 않게 최소 속도 제한
                fall_speed -= 0.005

        # 블록 자동 낙하
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not check_valid_space(current_piece, grid) and current_piece.y > 0:
                # 블록이 바닥에 닿거나 다른 블록과 겹치면
                current_piece.y -= 1 # 한 칸 위로 되돌리고
                grid = fix_piece(current_piece, grid) # 게임판에 고정
                lines_cleared, grid = clear_rows(grid) # 줄 지우기
                score += calculate_score(lines_cleared) # 점수 추가
                current_piece = next_piece # 다음 블록 가져오기
                next_piece = create_new_piece() # 새로운 다음 블록 생성
                if not check_valid_space(current_piece, grid): # 새 블록이 시작부터 겹치면 게임 오버
                    game_over = True

        # ⌨️ 이벤트 처리 (키보드 입력)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # 왼쪽 화살표
                    current_piece.x -= 1
                    if not check_valid_space(current_piece, grid):
                        current_piece.x += 1 # 유효하지 않으면 되돌리기
                elif event.key == pygame.K_RIGHT: # 오른쪽 화살표
                    current_piece.x += 1
                    if not check_valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN: # 아래 화살표 (빨리 떨어뜨리기)
                    current_piece.y += 1
                    if not check_valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP: # 위 화살표 (회전)
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not check_valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape) # 유효하지 않으면 회전 취소
                elif event.key == pygame.K_SPACE: # 스페이스바 (한 번에 떨어뜨리기)
                    while check_valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1 # 마지막 유효한 위치로 되돌리기
                    # 블록 즉시 고정
                    grid = fix_piece(current_piece, grid)
                    lines_cleared, grid = clear_rows(grid)
                    score += calculate_score(lines_cleared)
                    current_piece = next_piece
                    next_piece = create_new_piece()
                    if not check_valid_space(current_piece, grid):
                        game_over = True
        
        # 🖥️ 화면 그리기
        screen.fill(BLACK) # 화면을 검은색으로 채우기
        draw_grid(screen, grid) # 게임판 그리기
        draw_current_piece(screen, current_piece) # 현재 떨어지는 블록 그리기

        # 다음 블록 미리보기
        font = pygame.font.SysFont("malgungothic", 20)
        label = font.render("다음 블록:", 1, WHITE)
        screen.blit(label, (TOP_LEFT_X + PLAY_WIDTH + 50, TOP_LEFT_Y + 50))
        
        # 다음 블록 그리기 (게임판 밖에)
        next_piece_format = get_shape_format(next_piece)
        for i, line in enumerate(next_piece_format):
            row = list(line)
            for j, char in enumerate(row):
                if char == '0':
                    pygame.draw.rect(screen, next_piece.color,
                                     (TOP_LEFT_X + PLAY_WIDTH + 50 + j * GRID_SIZE,
                                      TOP_LEFT_Y + 100 + i * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE), 0)
        
        # 점수 표시
        score_label = font.render(f"점수: {score}", 1, WHITE)
        screen.blit(score_label, (TOP_LEFT_X + PLAY_WIDTH + 50, TOP_LEFT_Y + 200))

        # 게임 오버 메시지
        if game_over:
            draw_text_middle(screen, "게임 오버!", 60, WHITE)
            pygame.display.update() # 화면 업데이트
            pygame.time.delay(2000) # 2초 대기
            run = False # 게임 종료

        pygame.display.update() # 화면 업데이트

# 게임 시작!
if __name__ == '__main__':
    main()
