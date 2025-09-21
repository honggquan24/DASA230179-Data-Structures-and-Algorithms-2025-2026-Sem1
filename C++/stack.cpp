#include <iostream>
#include <stack>
#include <string>
#include <sstream>
#include <vector>
#include <cctype>
#include <stdexcept>
using namespace std;


// Kiểm tra token là toán tử
bool PhaiDauKo(const string& t) {
    return t.size() == 1 && (t[0] == '+' || t[0] == '-' || t[0] == '*' || t[0] == '/');
}

// Kiểm tra token là số (bao gồm số âm nhiều chữ số)
bool PhaiSoKo(const string& tok) {
    return !tok.empty() && (isdigit(tok[0]) || (tok[0] == '-' && tok.size() > 1 && isdigit(tok[1])));
}


//Tokenize chuỗi infix
vector<string> tokenize(const string& s) {
    vector<string> tokens;
    int n = s.size();
    for (int i = 0; i < n;) {
        if (isspace(s[i])) {
            ++i; continue;
        }

        // Đọc số (cả số âm)
        if (isdigit(s[i]) || (s[i] == '-' && i + 1 < n && isdigit(s[i + 1]))) {
            string num;
            // Nếu là số âm
            if (s[i] == '-') {
                num += '-';
                i++;
            }
            while (i < n && isdigit(s[i])) {
                num += s[i++];
            }
            tokens.push_back(num);
        }
        else if (isalpha(s[i])) {
            string var;
            while (i < n && isalnum(s[i])) {
                var += s[i++];
            }
            tokens.push_back(var);
        }
        else {
            // Xử lý unary minus (dấu âm đơn)
            if (s[i] == '-') {
                // Nếu '-' ở đầu chuỗi hoặc sau '(' hoặc sau toán tử
                if (tokens.empty() || tokens.back() == "(" || PhaiDauKo(tokens.back())) {
                    tokens.push_back("0"); // Thêm số 0 để thành "0 - x"
                    tokens.push_back("-");
                    i++;
                    continue;
                }
            }
            tokens.push_back(string(1, s[i]));
            i++;
        }
    }
    return tokens;
}

// ====== Chuyển đổi Infix -> Postfix ========

string ChuyenThanhHauTo(const string& infix) {
    auto tokens = tokenize(infix);
    stack<string> st;
    string out;

    auto precedence = [&](const string& op)->int {
        if (op == "+" || op == "-") return 1;
        if (op == "*" || op == "/") return 2;
        return 0;
        };

    for (const string& t : tokens) {
        if (PhaiSoKo(t) || isalpha(t[0])) { // toán hạng (số hoặc biến)
            out += t + " ";
        }
        else if (t == "(") {
            st.push(t);
        }
        else if (t == ")") {
            while (!st.empty() && st.top() != "(") {
                out += st.top() + " ";
                st.pop();
            }
            if (st.empty()) throw runtime_error("Ngoac khong hop le");
            st.pop(); // bỏ '('
        }
        else if (PhaiDauKo(t)) {
            while (!st.empty() && PhaiDauKo(st.top()) &&
                precedence(st.top()) >= precedence(t)) {
                out += st.top() + " ";
                st.pop();
            }
            st.push(t);
        }
        else {
            throw runtime_error("Token khong hop le: " + t);
        }
    }
    while (!st.empty()) {
        if (st.top() == "(" || st.top() == ")") throw runtime_error("Ngoac khong hop le!");
        out += st.top() + " ";
        st.pop();
    }
    return out;
}

// =====Đánh giá Postfix ======

int DanhGia(const string& postfix) {
    stack<int> st;
    stringstream ss(postfix);
    string token;

    while (ss >> token) {
        if (PhaiSoKo(token)) {
            st.push(stoi(token));
        }
        else if (PhaiDauKo(token)) {
            if (st.size() < 2) throw runtime_error("Bieu thuc hau to khong hop le");
            int b = st.top(); st.pop();
            int a = st.top(); st.pop();
            int res = 0;
            if (token == "+") res = a + b;
            else if (token == "-") res = a - b;
            else if (token == "*") res = a * b;
            else if (token == "/") {
                if (b == 0) throw runtime_error("Loi: chia cho 0");
                res = a / b;
            }
            st.push(res);
        }
        else {
            throw runtime_error("Token khong hop le trong postfix");
        }
    }
    if (st.size() != 1) throw runtime_error("Bieu thuc hau to khong hop le");
    return st.top();
}

// ======= Main ========

int main() {
    string infix;
    cout << "Nhap bieu thuc trung to: ";
    getline(cin, infix);

    try {
        string postfix = ChuyenThanhHauTo(infix);
        cout << "Bieu thuc hau to: " << postfix << endl;
        int result = DanhGia(postfix);
        cout << "Gia tri bieu thuc = " << result << endl;
    }
    catch (const exception& e) {
        cerr << "Loi: " << e.what() << endl;
    }

    return 0;
}
