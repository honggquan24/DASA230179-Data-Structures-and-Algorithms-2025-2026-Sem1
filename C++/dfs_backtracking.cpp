#include <bits/stdc++.h>
using namespace std;

map<int, vector<int>> graph = {
    {0, {1, 4}},
    {1, {0, 2, 5}},
    {2, {1}},
    {3, {5}},
    {4, {0, 5}},
    {5, {1, 3, 4}}
};

set<int> visited;

// DFS Recursive
void dfs_recursive(int v) {
    visited.insert(v);
    cout << v << " ";
    for (int neighbor : graph[v]) {
        if (visited.find(neighbor) == visited.end()) {
            dfs_recursive(neighbor);
        }
    }
}

// DFS Iterative (dùng Stack)
void dfs_iterative(int start) {
    set<int> visited_local;
    stack<int> st;
    st.push(start);
    while (!st.empty()) {
        int v = st.top();
        st.pop();
        if (visited_local.find(v) == visited_local.end()) {
            cout << v << " ";
            visited_local.insert(v);
            // đẩy ngược lại để duyệt đúng thứ tự
            for (auto it = graph[v].rbegin(); it != graph[v].rend(); ++it) {
                if (visited_local.find(*it) == visited_local.end()) {
                    st.push(*it);
                }
            }
        }
    }
}

int maze[4][4] = {
    {0, 0, 1, 0},
    {1, 0, 1, 0},
    {0, 0, 0, 0},
    {1, 1, 0, 0}
};

int n = 4, m = 4;
pair<int,int> target = {3, 3};
vector<pair<int,int>> directions = {{1,0},{-1,0},{0,1},{0,-1}};

// Backtracking Recursive
bool backtrack_recursive(int x, int y, vector<pair<int,int>> path, set<pair<int,int>> visited) {
    if (make_pair(x,y) == target) {
        cout << "Đường đi (recursive): ";
        for (auto &p : path) cout << "(" << p.first << "," << p.second << ") ";
        cout << "\n";
        return true;
    }

    for (auto d : directions) {
        int nx = x + d.first, ny = y + d.second;
        if (nx >= 0 && nx < n && ny >= 0 && ny < m &&
            maze[nx][ny] == 0 &&
            visited.find({nx, ny}) == visited.end()) {
            
            visited.insert({nx, ny});
            path.push_back({nx, ny});
            if (backtrack_recursive(nx, ny, path, visited)) return true;
            path.pop_back(); // quay lui
            visited.erase({nx, ny});
        }
    }
    return false;
}

// Backtracking Iterative (Stack)
bool backtrack_iterative() {
    stack<tuple<pair<int,int>, vector<pair<int,int>>, set<pair<int,int>>>> st;
    set<pair<int,int>> visited;
    visited.insert({0,0});
    st.push({{0,0}, {{0,0}}, visited});

    while (!st.empty()) {
        auto [pos, path, visited_now] = st.top();
        st.pop();

        int x = pos.first, y = pos.second;
        if (pos == target) {
            cout << "Đường đi (iterative): ";
            for (auto &p : path) cout << "(" << p.first << "," << p.second << ") ";
            cout << "\n";
            return true;
        }

        for (auto d : directions) {
            int nx = x + d.first, ny = y + d.second;
            if (nx >= 0 && nx < n && ny >= 0 && ny < m &&
                maze[nx][ny] == 0 &&
                visited_now.find({nx, ny}) == visited_now.end()) {
                
                set<pair<int,int>> new_visited = visited_now;
                new_visited.insert({nx, ny});
                auto new_path = path;
                new_path.push_back({nx, ny});
                st.push({{nx, ny}, new_path, new_visited});
            }
        }
    }
    return false;
}

int main() {
    cout << "DFS DEMO\n";
    cout << "DFS Recursive (từ đỉnh 0):\n";
    dfs_recursive(0);
    cout << "\nDFS Iterative (từ đỉnh 0):\n";
    dfs_iterative(0);

    cout << "\n\nBACKTRACKING DEMO\n";
    cout << "Recursive:\n";
    backtrack_recursive(0, 0, {{0,0}}, {{0,0}});

    cout << "\nIterative:\n";
    backtrack_iterative();

    return 0;
}
