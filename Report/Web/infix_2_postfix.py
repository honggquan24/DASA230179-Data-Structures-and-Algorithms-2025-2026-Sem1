import streamlit as st
import time
from typing import List

def is_operator(token: str) -> bool:
    return len(token) == 1 and token in "+-*/"

def is_valid_number(token: str) -> bool:
    if not token:
        return False
    if token[0] == '-' and len(token) > 1:
        return token[1:].isdigit()
    return token.isdigit()

def tokenize(expression: str) -> List[str]:
    tokens = []
    index = 0
    length = len(expression)
    
    while index < length:
        # Skip whitespace
        if expression[index].isspace():
            index += 1
            continue

        # Handle numbers (including negative numbers)
        if expression[index].isdigit() or (
            expression[index] == '-' 
            and index + 1 < length 
            and expression[index + 1].isdigit()
        ):
            number = ""
            if expression[index] == '-':
                number += '-'
                index += 1
            while index < length and expression[index].isdigit():
                number += expression[index]
                index += 1
            tokens.append(number)

        else:
            # Handle unary minus: e.g., "-x" or "(-5)"
            if expression[index] == '-':
                if not tokens or tokens[-1] == "(" or is_operator(tokens[-1]):
                    tokens.append("0")
                    tokens.append("-")
                    index += 1
                    continue

            # Default: treat as a single-character token (operator, parenthesis, etc.)
            tokens.append(expression[index])
            index += 1

    return tokens

def precedence(op: str) -> int:
    if op in "+-":
        return 1
    if op in "*/":
        return 2
    return 0

def infix_to_postfix(infix: str) -> str:
    tokens = tokenize(infix)
    stack = []
    output = []
    with st.expander(f"Infix to postfix step-by-step", expanded=False):
        for step, token in enumerate(tokens, 1):
            if is_valid_number(token) or token.isidentifier():
                output.append(token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()  # remove '('
            elif is_operator(token):
                while (
                    stack 
                    and is_operator(stack[-1]) 
                    and precedence(stack[-1]) >= precedence(token)
                ):
                    output.append(stack.pop())
                stack.append(token)
            else:
                raise ValueError(f"Invalid token: {token}")
            
            
            st.write(f"**Step** {step}: Read token `{token}`")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Output:**")
                st.code(" ".join(output) if output else "", language=None)
            with col2:
                st.markdown("**Stack:**")
                st.code(" ".join(stack) if stack else "", language=None)
            st.divider()
            time.sleep(1.5) 

    while stack:
        if stack[-1] in "()":
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())

    result = " ".join(output)
    
    return result

def evaluate_postfix(postfix: str) -> int:
    stack = []
    tokens = postfix.split()

    with st.expander("Step-by-step Evaluation of Postfix", expanded=False):
        for i, token in enumerate(tokens, 1):
            action = ""
            
            if is_valid_number(token):
                num = int(token)
                stack.append(num)
                action = f"Push number {num}"

            elif is_operator(token):
                if len(stack) < 2:
                    raise ValueError("Invalid postfix expression: not enough operands")
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
                action = f"Pop {a}, {b} → {a} {token} {b} = {res} → Push {res}"

            else:
                if token.isidentifier():
                    stack.append(0)
                    action = f"Push variable '{token}' (assumed value = 0)"
                else:
                    raise ValueError(f"Invalid token in postfix: {token}")

            st.markdown(f"**Step {i}**: Token = `{token}`")
            st.caption(action)
            st.write("**Stack:**", stack)
            
            
            st.divider()
            time.sleep(1.5)

        if len(stack) != 1:
            raise ValueError("Invalid postfix expression: too many/few operands")

        result = stack[0]

    return result

def render_stack_tab():
    st.header("Infix to Postfix Expression Evaluator")
    st.write("""
    This program:
    - Parses an infix expression (e.g., `3 + 4 * 2`)
    - Converts it to postfix notation (e.g., `3 4 2 * +`)
    - Evaluates the result step by step
    - Handles negative numbers, unary minus (e.g., `-5`, `(-x)`), and variables
    """)

    expr = st.text_input("Enter an infix expression:", value="3 + 4 * 2 - (-5 + 3)")

    if st.button("Convert and Calculate", key="calc_infix"):
        if not expr.strip():
            st.error("Please enter a valid expression!")
            return

        try:
            st.subheader("Step 1: Tokenization")
            tokens = tokenize(expr)
            with st.expander("View Tokens", expanded=False):
                st.write("**Token list:**", tokens)
            st.code(" → ".join(f"'{t}'" for t in tokens), language="text")

            st.subheader("Step 2: Infix → Postfix Conversion")
            postfix = infix_to_postfix(expr, )
            st.code(postfix, language="text")

            st.subheader("Step 3: Postfix Evaluation")
            result = evaluate_postfix(postfix, )

            st.divider()
            st.subheader("Final Result")
            st.success(f"**{expr} = {result}**")

        except Exception as e:
            st.error(f"**Error:** {str(e)}")
            st.info("Check for mismatched parentheses, invalid tokens, or division by zero.")