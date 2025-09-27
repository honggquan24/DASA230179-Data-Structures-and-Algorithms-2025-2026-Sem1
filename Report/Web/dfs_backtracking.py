import streamlit as st
import time

class AlgorithmVisualizer:
    def __init__(self):
        self.graph = {
            'A': ['B', 'D'],
            'B': ['A', 'C', 'E'],
            'C': ['B'],
            'D': ['A', 'E'],
            'E': ['B', 'D', 'F'],
            'F': ['E']
        }
        
        self.maze = [
            [0, 1, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 0]
        ]
    
    def dfs_recursive(self, graph, node, visited=None, path=None):
        """DFS đệ quy với theo dõi bước thực hiện"""
        if visited is None:
            visited = set()
        if path is None:
            path = []
            
        visited.add(node)
        path.append(f"Thăm {node}")
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                path.append(f"→ Từ {node} đến {neighbor}")
                self.dfs_recursive(graph, neighbor, visited, path)
        
        return visited, path
    
    def dfs_iterative(self, graph, start):
        """DFS lặp sử dụng stack"""
        visited = set()
        stack = [start]
        path = []
        order = []
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                path.append(f"Thăm {node}")
                
                # Thêm neighbors theo thứ tự ngược để giữ thứ tự nhất quán
                for neighbor in reversed(graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        path.append(f"Đẩy {neighbor} vào stack")
        
        return order, path
    
    def find_path_recursive(self, maze, start, end, path=None, visited=None, steps=None):
        """Tìm đường đi trong mê cung bằng đệ quy"""
        if path is None:
            path = [start]
        if visited is None:
            visited = {start}
        if steps is None:
            steps = [f"Bắt đầu tại {start}"]
            
        x, y = start
        
        # Đã đến đích
        if start == end:
            steps.append(f"✓ Tìm thấy đích: {path}")
            return True, path, steps
        
        # Thử 4 hướng: xuống, phải, lên, trái
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        direction_names = ["xuống", "phải", "lên", "trái"]
        
        for i, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            
            # Kiểm tra điều kiện hợp lệ
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and 
                maze[nx][ny] == 0 and (nx, ny) not in visited):
                
                # Thử đi
                visited.add((nx, ny))
                path.append((nx, ny))
                steps.append(f"→ Di chuyển {direction_names[i]} đến ({nx}, {ny})")
                
                # Đệ quy
                found, result_path, result_steps = self.find_path_recursive(
                    maze, (nx, ny), end, path, visited, steps
                )
                
                if found:
                    return True, result_path, result_steps
                
                # Quay lui
                path.pop()
                visited.remove((nx, ny))
                steps.append(f"← Quay lui từ ({nx}, {ny})")
        
        return False, None, steps
    
    def find_path_iterative(self, maze, start, end):
        """Tìm đường đi trong mê cung bằng lặp với stack"""
        stack = [(start, [start], {start})]
        steps = [f"Bắt đầu tại {start}"]
        
        while stack:
            (x, y), path, visited = stack.pop()
            
            if (x, y) == end:
                steps.append(f"✓ Tìm thấy đích: {path}")
                return True, path, steps
            
            # Thử 4 hướng
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and 
                    maze[nx][ny] == 0 and (nx, ny) not in visited):
                    
                    new_visited = visited | {(nx, ny)}
                    new_path = path + [(nx, ny)]
                    stack.append(((nx, ny), new_path, new_visited))
                    steps.append(f"→ Thêm đường đến ({nx}, {ny})")
        
        steps.append("✗ Không tìm thấy đường đi")
        return False, None, steps

def render_stack_tab():
    st.set_page_config(page_title="DFS & Backtracking Visualizer", layout="wide")
    st.title("DFS and Backtracking Visualizer")
    
    viz = AlgorithmVisualizer()
    
    # Tab selection
    tab1, tab2 = st.tabs(["🌳 DFS trên đồ thị", "🗺️ Tìm đường trong mê cung"])
    
    with tab1:
        st.header("Depth-First Search (DFS)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 Đồ thị mẫu")
            st.code("""
            A ─── B ─── C
            │     │
            D ─── E ─── F
            """)
            
            st.write("**Danh sách kề:**")
            for node, neighbors in viz.graph.items():
                st.write(f"{node}: {neighbors}")
        
        with col2:
            st.subheader("🎮 Điều khiển")
            start_node = st.selectbox("Chọn nút bắt đầu:", list(viz.graph.keys()))
            method = st.radio("Phương pháp:", ["Đệ quy", "Lặp (Stack)"])
            
            if st.button("🚀 Chạy DFS", type="primary"):
                with st.spinner("Đang thực hiện DFS..."):
                    if method == "Đệ quy":
                        visited, steps = viz.dfs_recursive(viz.graph, start_node)
                        st.success(f"**Kết quả:** Thăm {len(visited)} nút: {sorted(visited)}")
                    else:
                        order, steps = viz.dfs_iterative(viz.graph, start_node)
                        st.success(f"**Kết quả:** Thứ tự thăm: {' → '.join(order)}")
                    
                    # Hiển thị các bước
                    st.subheader("📋 Chi tiết các bước:")
                    for i, step in enumerate(steps, 1):
                        if "→" in step:
                            st.info(f"{i}. {step}")
                        else:
                            st.write(f"{i}. {step}")
    
    with tab2:
        st.header("Backtracking - Tìm đường trong mê cung")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🗺️ Mê cung")
            st.write("**Ký hiệu:** 🟩 = Đường đi, ⬛ = Tường, 🔴 = Bắt đầu, 🎯 = Đích")
            
            # Hiển thị mê cung
            maze_display = ""
            for i, row in enumerate(viz.maze):
                for j, cell in enumerate(row):
                    if (i, j) == (0, 0):
                        maze_display += "🔴 "
                    elif (i, j) == (len(viz.maze)-1, len(viz.maze[0])-1):
                        maze_display += "🎯 "
                    elif cell == 0:
                        maze_display += "🟩 "
                    else:
                        maze_display += "⬛ "
                maze_display += "\n"
            st.text(maze_display)
        
        with col2:
            st.subheader("🎮 Điều khiển")
            backtrack_method = st.radio("Phương pháp:", ["Đệ quy", "Lặp (Stack)"], key="backtrack")
            
            if st.button("🎯 Tìm đường đi", type="primary"):
                start = (0, 0)
                end = (len(viz.maze)-1, len(viz.maze[0])-1)
                
                with st.spinner("Đang tìm đường..."):
                    if backtrack_method == "Đệ quy":
                        found, path, steps = viz.find_path_recursive(viz.maze, start, end)
                    else:
                        found, path, steps = viz.find_path_iterative(viz.maze, start, end)
                    
                    if found:
                        st.success(f"✅ **Tìm thấy đường đi!** Độ dài: {len(path)} bước")
                        path_str = " → ".join([f"({x},{y})" for x, y in path])
                        st.write(f"**Đường đi:** {path_str}")
                    else:
                        st.error("❌ Không tìm thấy đường đi!")
                    
                    # Hiển thị các bước (giới hạn để tránh quá dài)
                    st.subheader("📋 Chi tiết các bước:")
                    max_steps = 15
                    for i, step in enumerate(steps[:max_steps], 1):
                        if "✓" in step:
                            st.success(f"{i}. {step}")
                        elif "→" in step:
                            st.info(f"{i}. {step}")
                        elif "←" in step:
                            st.warning(f"{i}. {step}")
                        elif "✗" in step:
                            st.error(f"{i}. {step}")
                        else:
                            st.write(f"{i}. {step}")
                    
                    if len(steps) > max_steps:
                        st.write(f"... và {len(steps) - max_steps} bước khác")