import pygame
import pygame.font


def read_file(file_name):
    with open(file_name, "r") as file:
        lines_list = file.readlines()
    mazes = []
    while lines_list:
        if int(lines_list[0].split()[0]) == 0 or int(lines_list[0].split()[1]) == 0:
            break
        m, n, ini_y, ini_x, goal_y, goal_x = [int(val) for val in lines_list.pop(0).split()]
        maze = [[int(val) for val in lines_list.pop(0).split()] for _ in range(m)]
        mazes.append(((m, n, ini_y, ini_x, goal_y, goal_x), maze))
    return mazes


def init_pygame(m, n, sqr_size):
    pygame.init()
    screen = pygame.display.set_mode((sqr_size * n, sqr_size * m))
    pygame.display.set_caption('Jump Maze')
    return screen, pygame.font.SysFont('Arial', 30)


def draw_maze(screen, font, m, n, maze, visited, ini_x, ini_y, goal_x, goal_y, path, sqr_size, sqr_border_size):
    screen.fill((0, 0, 0))
    for i in range(m):
        for j in range(n):
            square = pygame.Rect(sqr_size * j + sqr_border_size, sqr_size * i + sqr_border_size,
                                 sqr_size - sqr_border_size * 2, sqr_size - sqr_border_size * 2)
            pygame.draw.rect(screen, (255, 255, 255) if not visited[i][j] else (180, 180, 180), square)
            text = font.render(str(maze[i][j]), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (sqr_size * j + sqr_size / 2, sqr_size * i + sqr_size / 2)
            screen.blit(text, text_rect)
    pygame.draw.ellipse(screen, (120, 120, 120),
                        (ini_x * sqr_size + sqr_border_size, ini_y * sqr_size + sqr_border_size,
                         sqr_size - sqr_border_size * 2, sqr_size - sqr_border_size * 2), 4)
    pygame.draw.circle(screen, (120, 120, 120), (goal_x * sqr_size + sqr_size // 2, goal_y * sqr_size + sqr_size // 2),
                       sqr_size // 3)
    text = font.render("G", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (goal_x * sqr_size + sqr_size // 2, goal_y * sqr_size + sqr_size // 2)
    screen.blit(text, text_rect)

    pygame.display.flip()


def draw_path(screen, path, sqr_size, sqr_border_size):
    screen_path = [(sqr_size * x + sqr_size // 2, sqr_size * y + sqr_size // 2) for x, y in path]
    if len(screen_path) > 1:
        pygame.draw.lines(screen, (255, 0, 0), False, screen_path, 3)
    pygame.draw.ellipse(screen, (0, 180, 0),
                        (path[-1][0] * sqr_size + sqr_border_size, path[-1][1] * sqr_size + sqr_border_size,
                         sqr_size - sqr_border_size * 2, sqr_size - sqr_border_size * 2), 4)
    pygame.display.flip()


def main():
    sqr_size, sqr_border_size = 80, 2
    mazes = read_file("test.txt")
    for (m, n, ini_y, ini_x, goal_y, goal_x), maze in mazes:
        screen, font = init_pygame(m, n, sqr_size)
        visited = [[False for _ in range(n)] for _ in range(m)]
        path = [(ini_x, ini_y)]
        visited[ini_y][ini_x] = True

        while path:
            x, y = path[-1]
            if x == goal_x and y == goal_y:
                print("Path found. length:", len(path)-1)
                pygame.time.wait(3000)
                break
            jmp = maze[y][x]
            for dx, dy in [(jmp, 0), (0, jmp), (-jmp, 0), (0, -jmp)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m and not visited[ny][nx]:
                    path.append((nx, ny))
                    visited[ny][nx] = True
                    break
            draw_maze(screen, font, m, n, maze, visited, ini_x, ini_y, goal_x, goal_y, path, sqr_size, sqr_border_size)
            draw_path(screen, path, sqr_size, sqr_border_size)
            pygame.time.wait(100)

            if path[-1] == (x, y):
                path.pop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    path = None
                    break

        if not path:
            print("No path found")
            pygame.time.wait(3000)

        pygame.quit()


if __name__ == "__main__":
    main()
