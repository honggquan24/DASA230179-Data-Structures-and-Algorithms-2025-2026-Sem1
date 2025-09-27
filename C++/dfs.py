graph = {               
    0: [1, 4],
    1: [0, 2, 5],
    2: [1],
    3: [5],
    4: [0, 5],
    5: [1, 3, 4]
}                           # đồ thị bằng adjacency list

# DFS Recursive
def dfs_recursive(graph, v, visited):
    visited.add(v)
    print(v, end=" ")   # In đỉnh được duyệt
    for neighbor in graph[v]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# DFS Iterative (dùng Stack)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        v = stack.pop()        # lấy phần tử cuối cùng
        if v not in visited:
            print(v, end=" ")
            visited.add(v)
            # push các neighbor chưa thăm
            for neighbor in reversed(graph[v]):
                if neighbor not in visited:
                    stack.append(neighbor)
print("DFS DEMO")
print("DFS Recursive (từ đỉnh 0):")
dfs_recursive(graph, 0, set())

print("\nDFS Iterative (từ đỉnh 0):")
dfs_iterative(graph, 0)






# mê cung : 0 = có thể đi, 1 = tường
maze = [
    [0, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 0, 0]
]

n, m = len(maze), len(maze[0])
target = (n - 1, m - 1)
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# Backtracking Recursive
def backtrack_recursive(x, y, path, visited):
    if (x, y) == target:
        print("Đường đi (recursive):", path)
        return True

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == 0 and (nx, ny) not in visited:
            visited.add((nx, ny))
            if backtrack_recursive(nx, ny, path + [(nx, ny)], visited):
                return True
            visited.remove((nx, ny))  # quay lui

    return False

# Backtracking Iterative (Stack)
def backtrack_iterative():
    stack = [((0, 0), [(0, 0)], {(0, 0)})]  # (vị trí, đường đi, visited)
    while stack:
        (x, y), path, visited = stack.pop()
        if (x, y) == target:
            print("Đường đi (iterative):", path)
            return True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == 0 and (nx, ny) not in visited:
                new_visited = set(visited)
                new_visited.add((nx, ny))
                stack.append(((nx, ny), path + [(nx, ny)], new_visited))
    return False


print("\BACKTRACKING DEMO")
print("Recursive:")
backtrack_recursive(0, 0, [(0, 0)], {(0, 0)})

print("\nIterative:")
backtrack_iterative()
