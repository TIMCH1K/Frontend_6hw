import pygame
import numpy as np
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DBSCAN Clustering")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Радиус точки
RADIUS = 5

# Список точек
points = []


# Функция для рисования точки
def draw_point(win, point, color=BLACK):
    pygame.draw.circle(win, color, point, RADIUS)


# Функция для вычисления евклидова расстояния
def euclidean_distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


# Алгоритм DBSCAN
def dbscan(points, eps, min_pts):
    clusters = []
    noise = []
    visited = set()
    point_status = {}  # 0 - noise, 1 - border, 2 - core

    def region_query(point):
        neighbors = []
        for other_point in points:
            if euclidean_distance(point, other_point) < eps:
                neighbors.append(other_point)
        return neighbors

    def expand_cluster(point, neighbors, cluster):
        point_status[point] = 2  # Core point
        cluster.append(point)
        while neighbors:
            neighbor = neighbors.pop()
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor_neighbors = region_query(neighbor)
                if len(neighbor_neighbors) >= min_pts:
                    neighbors.extend(neighbor_neighbors)
                    point_status[neighbor] = 2  # Core point
                else:
                    point_status[neighbor] = 1  # Border point
            if neighbor not in sum(clusters, []):  # Check if neighbor is not already in any cluster
                cluster.append(neighbor)

    for point in points:
        if point not in visited:
            visited.add(point)
            neighbors = region_query(point)
            if len(neighbors) < min_pts:
                noise.append(point)
                point_status[point] = 0  # Noise point
            else:
                cluster = []
                expand_cluster(point, neighbors, cluster)
                clusters.append(cluster)

    return clusters, noise, point_status


# Главный цикл
running = True
try:
    while running:
        WIN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    pos = pygame.mouse.get_pos()
                    points.append(pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and points:
                    eps = 50
                    min_pts = 3
                    clusters, noise, point_status = dbscan(points, eps, min_pts)

                    # Визуализация точек по их статусу
                    WIN.fill(WHITE)
                    color_map = {0: YELLOW, 1: RED, 2: GREEN}
                    for point in points:
                        draw_point(WIN, point, color_map[point_status[point]])

                    pygame.display.update()

                    # Задержка для визуализации
                    pygame.time.wait(2000)

                    # Визуализация кластеров
                    cluster_colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE]
                    WIN.fill(WHITE)
                    for i, cluster in enumerate(clusters):
                        color = cluster_colors[i % len(cluster_colors)]
                        for point in cluster:
                            draw_point(WIN, point, color)
                    pygame.display.update()

        for point in points:
            draw_point(WIN, point)

        pygame.display.update()

except KeyboardInterrupt:
    running = False
finally:
    pygame.quit()
    sys.exit()