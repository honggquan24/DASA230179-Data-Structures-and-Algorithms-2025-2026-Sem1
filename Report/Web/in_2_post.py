import streamlit as st
import time
from typing import List

def is_operator(t: str) -> bool:
    return len(t) == 1 and t in "+-*/"

def is_number(tok: str) -> bool:
    if not tok:
        return False
    if tok[0] == '-' and len(tok) > 1:
        return tok[1:].isdigit()
    return tok.isdigit()

def tokenize(s: str) -> List[str]:
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        if s[i].isspace():
            i += 1
            continue
        # Handle numbers (including negative)
        if s[i].isdigit() or (s[i] == '-' and i + 1 < n and s[i+1].isdigit()):
            num = ""
            if s[i] == '-':
                num += '-'
                i += 1
            while i < n and s[i].isdigit():
                num += s[i]
                i += 1
            tokens.append(num)
        # Handle variables
        elif s[i].isalpha():
            var = ""
            while i < n and (s[i].isalnum() or s[i] == '_'):
                var += s[i]
                i += 1
            tokens.append(var)
        else:
            # Handle unary minus
            if s[i] == '-':
                if not tokens or tokens[-1] == "(" or is_operator(tokens[-1]):
                    tokens.append("0")
                    tokens.append("-")
                    i += 1
                    continue
            tokens.append(s[i])
            i += 1
    return tokens

def infix_to_postfix(infix: str) -> str:
    tokens = tokenize(infix)
    stack = []
    output = []
    
    def precedence(op: str) -> int:
        if op in "+-":
            return 1
        if op in "*/":
            return 2
        return 0

    for t in tokens:
        if is_number(t) or t.isidentifier():  # number or variable
            output.append(t)
        elif t == "(":
            stack.append(t)
        elif t == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses")
            stack.pop()  # remove '('
        elif is_operator(t):
            while (stack and is_operator(stack[-1]) and
                   precedence(stack[-1]) >= precedence(t)):
                output.append(stack.pop())
            stack.append(t)
        else:
            raise ValueError(f"Invalid token: {t}")

    while stack:
        if stack[-1] in "()":
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())

    return " ".join(output)

def evaluate_postfix(postfix: str) -> int:
    stack = []
    tokens = postfix.split()
    
    for token in tokens:
        if is_number(token):
            stack.append(int(token))
        elif token.isidentifier():
            stack.append(0)  # temporary: assign 0 to any variable
        elif is_operator(token):
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                res = a + b
            elif token == "-":
                res = a - b
            elif token == "*":
                res = a * b
            elif token == "/":
                if b == 0:
                    raise ValueError("Division by zero")
                res = a // b
            stack.append(res)
        else:
            raise ValueError(f"Invalid token in postfix: {token}")

    if len(stack) != 1:
        raise ValueError("Invalid postfix expression")
    return stack[0]


def render_stack_tab():
    st.header("Infix to Postfix Expression Evaluator")
    st.write("""
    This program:
    - Parses an infix expression
    - Converts it to postfix notation
    - Evaluates the result step by step
    - Handles negative numbers and unary minus
    """)

    expr = st.text_input("Enter expression:", value="3 + 4 * 2 - (-5 + 3)")

    if st.button("Convert and Calculate", key="calc_infix"):
        if not expr.strip():
            st.error("Please enter an expression!")
        else:
            try:
                # Step 1: Tokenize
                tokens = tokenize(expr)
                st.subheader("Step 1: Tokenized Expression")
                st.code(" → ".join(tokens), language="text")

                # Step 2: Convert to postfix
                postfix = infix_to_postfix(expr)
                st.subheader("Step 2: Postfix Expression")
                st.code(postfix, language="text")

                # Step 3: Evaluate with animation
                st.subheader("Step 3: Step-by-step Evaluation")

                stack_display = st.empty()
                status_display = st.empty()

                tokens_eval = postfix.split()
                eval_stack = []

                for i, token in enumerate(tokens_eval):
                    if is_number(token):
                        eval_stack.append(int(token))
                        status_display.info(f"Push number {token} onto stack")
                    elif token.isidentifier():
                        eval_stack.append(0)
                        status_display.info(f"Push variable '{token}' (value = 0) onto stack")
                    elif is_operator(token):
                        if len(eval_stack) < 2:
                            raise ValueError("Stack underflow during evaluation")
                        b = eval_stack.pop()
                        a = eval_stack.pop()
                        if token == "+":
                            res = a + b
                        elif token == "-":
                            res = a - b
                        elif token == "*":
                            res = a * b
                        elif token == "/":
                            if b == 0:
                                raise ValueError("Division by zero")
                            res = a // b
                        eval_stack.append(res)
                        status_display.success(f"Calculate {a} {token} {b} = {res}")

                    # Display current stack
                    with stack_display.container():
                        st.write("**Current Stack:**")
                        st.write(eval_stack)
                        if eval_stack:
                            st.write(" → ".join(str(x) for x in reversed(eval_stack)) + " (Top)")
                            time.sleep(1)
                        else:
                            st.info("Stack is empty")

                    time.sleep(5)

                status_display.empty()

                if len(eval_stack) != 1:
                    raise ValueError("Invalid final result")

                result = eval_stack[0]
                st.subheader("Final Result")
                st.success(f"**{expr} = {result}**")

            except Exception as e:
                st.error(f"Error: {str(e)}")