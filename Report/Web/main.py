import streamlit as st
import time
import sys
from typing import List
import theme
import random

st.set_page_config(
    page_title="Stack Application",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(theme.get_css(), unsafe_allow_html=True)

st.markdown("""
            <div style="text-align: center;">
                <h1>Stack Applications</h1>
            </div>
        """, unsafe_allow_html=True)
st.markdown("<br></br>", unsafe_allow_html=True)

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

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Stack', 'Recursion', 'Infix to Postfix', 'Check Balance Parenthese', 
                                              'Convert Numver Base', 'Back Propagation'])

with tab1:
    st.header("Example of Stack")
    instruction_ = "A stack is a data structure that operates on the " \
    "LIFO (Last In First Out) principle. " \
    "Like a stack of plates: the last plate placed will be the first one taken " \
    "and you can only operate at the top."
    st.write(instruction_)
    
    # Initialize stack in session state
    if "array_stack" not in st.session_state:
        st.session_state['array_stack'] = []
    
    if "last_operation" not in st.session_state:
        st.session_state['last_operation'] = ""
    
    if "operation_result" not in st.session_state:
        st.session_state['operation_result'] = ""
    
    col1, col2 = st.columns([5, 5])
    
    words = ["apple", "zebra", "quantum", "banana", "galaxy", "penguin", "laptop", "oxygen"]
    
    random_word = random.choice(words)
    with col1: 
        st.write("**Operations:**")
        
        # Input for new value
        value = st.text_input("Enter value:", key="stack_input", value= random_word)
        
        # Create buttons in columns for better layout
        btn_col1, btn_col2, btn_col3, btn_col4, btn_col5, btn_col6 = st.columns(6)
        
        with btn_col1:
            # Push operation
            if st.button('Push', key='push', width= 'stretch'):
                if value and value.strip():
                    st.session_state['array_stack'].append(value.strip())
                    st.session_state['last_operation'] = f"[PUSH]: Added '{value.strip()}' to stack"
                    st.session_state['operation_result'] = "success"
                    # Clear input by rerunning
                    st.rerun()
                else:
                    st.session_state['last_operation'] = "[PUSH]: Please enter a valid value"
                    st.session_state['operation_result'] = "error"
        
        with btn_col2:
            # Pop operation
            if st.button('Pop', key='pop', width= 'stretch'):
                if st.session_state['array_stack']:
                    popped_value = st.session_state['array_stack'].pop()
                    st.session_state['last_operation'] = f"[POP]: Removed '{popped_value}'"
                    st.session_state['operation_result'] = "success"
                else:
                    st.session_state['last_operation'] = "[POP]: Stack is empty, cannot pop"
                    st.session_state['operation_result'] = "error"
        
        with btn_col3:
            # Peek operation
            if st.button('Peek', key='peek', width= 'stretch'):
                if st.session_state['array_stack']:
                    top_value = st.session_state['array_stack'][-1]
                    st.session_state['last_operation'] = f"[PEEK]: Top element is '{top_value}'"
                    st.session_state['operation_result'] = "info"
                else:
                    st.session_state['last_operation'] = "[PEEK]: Stack is empty"
                    st.session_state['operation_result'] = "error"
        
        with btn_col4:
            # isEmpty operation
            if st.button('isEmpty', key='is_empty', width= 'stretch'):
                is_empty = (len(st.session_state['array_stack']) == 0)
                if is_empty:
                    st.session_state['last_operation'] = f"[IS_EMPTY]: Stack is empty"
                else:
                    st.session_state['last_operation'] = f"[IS_EMPTY]: Stack has elements"
                st.session_state['operation_result'] = "info"
        
        with btn_col5:
            # Size operation
            if st.button('Size', key='size', width= 'stretch'):
                size = len(st.session_state['array_stack'])
                st.session_state['last_operation'] = f"[SIZE]: Stack size is {size}"
                st.session_state['operation_result'] = "info"
        
        with btn_col6:
            # Clear stack operation
            if st.button('Clear Stack', key='clear', width= 'stretch'):
                st.session_state['array_stack'] = []
                st.session_state['last_operation'] = "[CLEAR]: Cleared entire stack"
                st.session_state['operation_result'] = "success"
        
        # Display last operation result
        if st.session_state['last_operation']:
            if st.session_state['operation_result'] == "success":
                st.success(st.session_state['last_operation'])
            elif st.session_state['operation_result'] == "error":
                st.error(st.session_state['last_operation'])
            else:
                st.info(st.session_state['last_operation'])

    with col2:
        if st.session_state['array_stack']:
            empty, col, empty = st.columns([1, 3, 1])
            # Display stack elements using expanders from top to bottom
            with col:
                st.markdown("<br></br>", unsafe_allow_html=True)
                for i in range(len(st.session_state['array_stack']) - 1, -1, -1):
                    element = st.session_state['array_stack'][i]
                    
                    # Create expander title with TOP indicator
                    if i == len(st.session_state['array_stack']) - 1:
                        expander_title = f"Element {i + 1} (TOP)"
                        expander_expanded = False
                    else:
                        expander_title = f"Element {i + 1}"
                        expander_expanded = False
                    
                    with st.expander(expander_title, expanded=expander_expanded):
                        st.write(f"**Value:** `{element}`")
                        st.write(f"**Index:** {i}")
                        stack_len = len(st.session_state['array_stack'])
                        if i == stack_len - 1:
                            position_text = "Top of stack"
                        else:
                            position_text = f"{stack_len - 1 - i} from top"

                        st.write(f"**Position:** {position_text}")
                        st.write(f"**Size:** {sys.getsizeof(element)} bytes")
                        st.write(f"**Address:** 0x{id(element):x}")
        else:
            st.markdown("<br></br>", unsafe_allow_html=True)
            st.info(" Stack is empty - No elements")

with tab2:
    st.header("Recursion")
    st.write("Recursion is a programming technique where a function calls itself to solve a problem.")
    st.write("The stack is used to store function calls during recursion.")
    
    factorial_n = st.number_input("Enter n to calculate factorial:", min_value=0, max_value=10, value=5)
    
    col1, col2 = st.columns([5, 5])
    
    # Initialize recursion stack in session state
    if "recursion_stack" not in st.session_state:
        st.session_state['recursion_stack'] = []
    
    if "is_calculating" not in st.session_state:
        st.session_state['is_calculating'] = False
    
    if "final_result" not in st.session_state:
        st.session_state['final_result'] = None
    
    if "current_phase" not in st.session_state:
        st.session_state['current_phase'] = 0
    
    if "stack_built" not in st.session_state:
        st.session_state['stack_built'] = False

    with col1:        
        if st.button("Calculate Factorial", key="calc_factorial"):
            st.session_state['is_calculating'] = True
            st.session_state['recursion_stack'] = []
            st.session_state['final_result'] = None
            st.session_state['current_phase'] = 1
            st.session_state['stack_built'] = False
            st.rerun()

    # Dùng placeholder để xóa sạch UI cũ
    stack_placeholder = col2.empty()

    if st.session_state['is_calculating']:
        placeholder = col1.empty()
        
        # Phase 1: Building Call Stack
        if st.session_state['current_phase'] == 1 and not st.session_state['stack_built']:
            with col1:
                st.write("**Phase 1: Building Call Stack**")
            
            # Build stack từ factorial(n) xuống factorial(1)
            for i in range(factorial_n, 0, -1):
                call_info = {
                    'function': f'factorial({i})',
                    'parameter': i,
                    'status': 'waiting',
                    'result': None,
                    'call_order': factorial_n - i + 1,
                    'depth': factorial_n - i
                }
                st.session_state['recursion_stack'].append(call_info)
                
                # Ghi đè lên placeholder 
                with stack_placeholder.container():
                    st.write("**Call Stack:**")
                    for idx, call in enumerate(reversed(st.session_state['recursion_stack'])):
                        if idx == 0:  
                            expander_title = f"{call['function']} (TOP)"
                            expanded_fl = True
                        else:
                            expander_title = f"{call['function']}"
                            expanded_fl = False
                        
                        with st.expander(expander_title, expanded=expanded_fl):
                            st.write(f"**Function:** `{call['function']}`")
                            st.write(f"**Parameter:** {call['parameter']}")
                            st.write(f"**Status:** {call['status'].title()}")
                            st.write(f"**Call Depth:** {call['depth']}")
                            st.write(f"**Result:** Pending...")
                
                # Status update
                placeholder.info(f"Pushing factorial({i}) to stack...")
                time.sleep(1.5)
                placeholder.empty()

            with col1:
                st.success("All function calls pushed to stack!")
            
            st.session_state['stack_built'] = True
            st.session_state['current_phase'] = 2
            time.sleep(1)
            st.rerun()

        # Phase 2: Calculating and Returning 
        elif st.session_state['current_phase'] == 2:
            with col1:
                st.write("**Phase 2: Calculating and Returning**")

            # Khởi tạo result_map nếu chưa có
            if 'result_map' not in st.session_state:
                st.session_state['result_map'] = {}

            # Khởi tạo bước hiện tại trong phase 2
            if 'phase2_step' not in st.session_state:
                st.session_state['phase2_step'] = 1  # bắt đầu từ factorial(1)

            current_n = st.session_state['phase2_step']

            # Nếu chưa vượt quá n
            if current_n <= factorial_n:
                idx_in_stack = factorial_n - current_n

                if idx_in_stack < len(st.session_state['recursion_stack']):
                    call = st.session_state['recursion_stack'][idx_in_stack]
                    if call['parameter'] == current_n and call['status'] != 'completed':

                        # Tính toán kết quả
                        if current_n == 1:
                            result = 1
                            calc_text = "Base case: factorial(1) = 1"
                        else:
                            prev_result = st.session_state['result_map'].get(current_n - 1, 1)
                            result = current_n * prev_result
                            calc_text = f"factorial({current_n}) = {current_n} × {prev_result} = {result}"

                        st.session_state['result_map'][current_n] = result
                        st.session_state['recursion_stack'][idx_in_stack]['status'] = 'calculating'
                        st.session_state['recursion_stack'][idx_in_stack]['result'] = result

                        # Xóa sạch và render lại stack
                        stack_placeholder.empty()
                        with stack_placeholder.container():
                            st.write("**Call Stack:**")
                            active_calls = [call for call in st.session_state['recursion_stack'] if call['status'] != 'completed']
                            if not active_calls:
                                st.info("Stack is empty - All calls completed!")
                            else:
                                for idx_inner, call_inner in enumerate(reversed(active_calls)):
                                    if call_inner['parameter'] == current_n:
                                        expander_title = f"{call_inner['function']} - CALCULATING"
                                        expanded_fl = True
                                    else:
                                        expander_title = f"{call_inner['function']}"
                                        expanded_fl = False

                                    with st.expander(expander_title, expanded=expanded_fl):
                                        st.write(f"**Function:** `{call_inner['function']}`")
                                        st.write(f"**Parameter:** {call_inner['parameter']}")
                                        st.write(f"**Status:** {call_inner['status'].title()}")
                                        if call_inner['result'] is not None:
                                            st.success(f"**Result:** {call_inner['result']}")
                                            if call_inner['parameter'] == 1:
                                                st.write("**Calculation:** Base case returns 1")
                                            else:
                                                prev = st.session_state['result_map'].get(call_inner['parameter'] - 1, 1)
                                                st.write(f"**Calculation:** {call_inner['parameter']} × factorial({call_inner['parameter']-1}) = {call_inner['parameter']} × {prev} = {call_inner['result']}")
                                        else:
                                            st.write("**Result:** Waiting...")

                        # Hiển thị trạng thái
                        placeholder.info(f"{calc_text}")
                        time.sleep(3)  # Chờ 2s 

                        # Đánh dấu hoàn thành
                        st.session_state['recursion_stack'][idx_in_stack]['status'] = 'completed'
                        placeholder.success(f"Returned: factorial({current_n}) = {result}")
                        placeholder.empty()


                        # Tăng bước và rerun để tiếp tục bước tiếp theo
                        st.session_state['phase2_step'] += 1
                        st.rerun()  

            else:
                # Đã hoàn thành tất cả các bước
                st.session_state['final_result'] = st.session_state['result_map'].get(factorial_n, 1)
                st.session_state['is_calculating'] = False
                st.session_state['current_phase'] = 0
                del st.session_state['phase2_step']  # dọn sạch

                # Hiển thị stack rỗng
                stack_placeholder.empty()
                with stack_placeholder.container():
                    st.write("**Call Stack:**")
                    st.info("Stack is empty - All function calls completed!")

                with col1:
                    st.write(f"Final Result: {factorial_n}! = {st.session_state['final_result']}")
        
    elif not st.session_state['is_calculating'] and not st.session_state['recursion_stack']:
        with stack_placeholder:
            st.info("Click **Calculate Factorial** to visualize recursion.")
    
    with col1:
        if st.button("Clear", key="clear_recursion"):
            st.session_state['recursion_stack'] = []
            st.session_state['is_calculating'] = False
            st.session_state['final_result'] = None
            st.session_state['current_phase'] = 0
            st.session_state['stack_built'] = False
            st.rerun()

with tab3:
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

                    time.sleep(1.5)

                status_display.empty()

                if len(eval_stack) != 1:
                    raise ValueError("Invalid final result")

                result = eval_stack[0]
                st.subheader("Final Result")
                st.success(f"**{expr} = {result}**")

            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab4:
    st.header("Check Balanced Parentheses")
    
    # Algorithm explanation
    st.write("### Algorithm Concept:")
    st.info("""
    **Principle**: Traverse each character in the expression:
    - When encountering **opening brackets** `(`, `{`, `[` → **push** to stack
    - When encountering **closing brackets** `)`, `}`, `]` → check if **peek** matches → if yes, **pop**, else error
    - At the end, stack must be **empty** → expression is valid
    """)

    # Input section
    st.write("### Enter Expression:")
    expression = st.text_input(
        "Enter expression to check:", 
        value="(a+b)*[c-d]", 
        key="expr_input",
        help="Examples: (a+b)*[c-d], {x+(y-z)}, [(a+b)]"
    )
    
    # Control buttons
    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        check_btn = st.button("Check", key="check_brackets", type="primary")

    # Main processing
    if check_btn or 'bracket_steps' in st.session_state:
        if check_btn:
            # Reset state
            st.session_state['bracket_steps'] = []
            st.session_state['bracket_result'] = None

        # Stack implementation
        class Stack:
            def __init__(self, capacity=100):
                self.data = [None] * capacity
                self.top = -1
                self.capacity = capacity

            def is_empty(self):
                return self.top == -1

            def is_full(self):
                return self.top == self.capacity - 1

            def push(self, value):
                if self.is_full():
                    raise Exception("Stack overflow!")
                self.top += 1
                self.data[self.top] = value

            def pop(self):
                if self.is_empty():
                    raise Exception("Stack underflow!")
                value = self.data[self.top]
                self.top -= 1
                return value

            def peek(self):
                if self.is_empty():
                    raise Exception("Stack is empty!")
                return self.data[self.top]

            def get_stack_content(self):
                """Get current stack content"""
                return [self.data[i] for i in range(self.top + 1)]

        # Function to check with step-by-step details
        def check_balanced_brackets(expr):
            if not expr.strip():
                return True, [{"message": "Empty expression - valid"}]
                
            stack = Stack(len(expr))
            bracket_pairs = {')': '(', '}': '{', ']': '['}
            steps = []

            for i, char in enumerate(expr):
                step_info = {
                    'step_num': len(steps) + 1,
                    'char': char,
                    'position': i,
                    'action': '',
                    'stack_before': stack.get_stack_content().copy(),
                    'stack_after': [],
                    'status': 'normal',
                    'message': ''
                }

                # Process character
                if char in "({[":
                    # Opening bracket - push to stack
                    stack.push(char)
                    step_info['action'] = 'PUSH'
                    step_info['status'] = 'push'
                    step_info['message'] = f"Found opening bracket '{char}' → Push to stack"
                    
                elif char in ")}]":
                    # Closing bracket - check
                    if stack.is_empty():
                        step_info['action'] = 'ERROR'
                        step_info['status'] = 'error'
                        step_info['message'] = f"Error: Found closing bracket '{char}' but stack is empty!"
                        step_info['stack_after'] = stack.get_stack_content().copy()
                        steps.append(step_info)
                        return False, steps
                        
                    elif stack.peek() != bracket_pairs[char]:
                        step_info['action'] = 'ERROR'
                        step_info['status'] = 'error'
                        step_info['message'] = f"Error: '{char}' does not match with '{stack.peek()}'"
                        step_info['stack_after'] = stack.get_stack_content().copy()
                        steps.append(step_info)
                        return False, steps
                        
                    else:
                        # Matched - pop from stack
                        matched_bracket = stack.pop()
                        step_info['action'] = 'POP'
                        step_info['status'] = 'pop'
                        step_info['message'] = f"'{char}' matches with '{matched_bracket}' → Pop from stack"
                else:
                    # Other characters - skip
                    continue

                step_info['stack_after'] = stack.get_stack_content().copy()
                steps.append(step_info)

            # Final check
            is_valid = stack.is_empty()
            final_message = {
                'step_num': len(steps) + 1,
                'char': 'END',
                'action': 'CHECK',
                'status': 'success' if is_valid else 'error',
                'message': 'Stack is empty → Expression is valid!' if is_valid else 'Stack is not empty → Expression is invalid!',
                'stack_after': stack.get_stack_content().copy()
            }
            steps.append(final_message)
            
            return is_valid, steps

        # Perform check
        if expression.strip():
            is_valid, steps = check_balanced_brackets(expression)
            st.session_state['bracket_steps'] = steps
            st.session_state['bracket_result'] = is_valid

            # Display step-by-step process
            st.write("### Execution Process:")
            
            # Create container to display steps
            steps_container = st.container()
            
            with steps_container:
                for step in steps:
                    if step.get('char') == 'END':
                        # Final step
                        if step['status'] == 'success':
                            st.success(f"**Step {step['step_num']}**: {step['message']}")
                        else:
                            st.error(f"**Step {step['step_num']}**: {step['message']}")
                            st.write(f"**Remaining Stack:** `{step['stack_after'] if step['stack_after'] else '[]'}`")
                    else:
                        # Character processing steps
                        col1, col2, col3 = st.columns([1, 2, 2])
                        
                        with col1:
                            if step['status'] == 'push':
                                st.success(f"**Step {step['step_num']}**")
                            elif step['status'] == 'pop':
                                st.info(f"**Step {step['step_num']}**")
                            elif step['status'] == 'error':
                                st.error(f"**Step {step['step_num']}**")
                        
                        with col2:
                            st.write(f"**Character:** `{step['char']}` (position {step['position']})")
                            st.write(f"**Action:** {step['action']}")
                        
                        with col3:
                            # Message
                            if step['status'] == 'push':
                                st.success(step['message'])
                            elif step['status'] == 'pop':
                                st.info(step['message'])
                            elif step['status'] == 'error':
                                st.error(step['message'])
                                break
                        
                        st.write("")  # Spacing

            # Final result
            st.write("### Result:")
            if st.session_state.get('bracket_result'):
                st.success(f"The expression`{expression}` is valid")
            else:
                st.error(f"The expression`{expression}` is invalid")
        else:
            st.warning("Please enter an expression to check!")   

with tab5:
    st.header("Convert Number Base")
    st.write("""
    **Idea**: Repeatedly divide the number by base, push remainders to stack → then pop to reverse order.
    """)

    col_num, col_base = st.columns(2)
    with col_num:
        number = st.number_input("Number to convert:", min_value=0, max_value=1000000, value=125, step=1, key="num_input")
    with col_base:
        base = st.selectbox("Target base:", options=[2, 8, 10, 16], index=0, key="base_select")

    col_btn3, col_btn4 = st.columns([1, 1])
    with col_btn3:
        convert_btn = st.button("Convert", key="convert_base")
    with col_btn4:
        clear_btn2 = st.button("Clear", key="clear_base")

    steps_placeholder2 = st.empty()

    if clear_btn2:
        st.session_state['base_steps'] = []
        st.session_state['base_result'] = ""
        st.rerun()

    if convert_btn or 'base_steps' in st.session_state:
        if convert_btn:
            st.session_state['base_steps'] = []
            st.session_state['base_result'] = ""

        def convert_base_with_steps(num, base):
            if num == 0:
                return "0", [{"action": "Number is 0 → result is '0'", "stack": [], "result": "0"}]

            digits = "0123456789ABCDEF"
            stack = []
            steps = []
            n = num

            # Division process
            while n > 0:
                remainder = n % base
                digit = digits[remainder]
                stack.append(digit)
                step = {
                    'action': f"{n} divided by {base} → remainder {remainder} → push '{digit}'",
                    'stack': stack.copy(),
                    'result': ''
                }
                steps.append(step)
                n //= base

            # Pop process
            result = ""
            for i in range(len(stack)):
                digit = stack.pop()
                result += digit
                step = {
                    'action': f"Pop '{digit}' → temporary result: `{result}`",
                    'stack': stack.copy(),
                    'result': result
                }
                steps.append(step)

            return result, steps

        result, steps = convert_base_with_steps(number, base)
        st.session_state['base_steps'] = steps
        st.session_state['base_result'] = result

        # Display step-by-step
        st.write("### Step-by-step Process:")
        col1, col2 = st.columns([1, 1])
        for i, step in enumerate(steps):
            if "divided by" in step['action']:
                with col1:
                    st.info(f"**Step {i+1}:** {step['action']}")
                    st.write(f"**Stack:** `{' '.join(step['stack'])}`")
            elif "Pop" in step['action']:
                with col2:
                    st.success(f"**Step {i+1}:** {step['action']}")
                    st.write(f"**Remaining Stack:** `{' '.join(step['stack']) if step['stack'] else '[]'}`")
            time.sleep(1)

        st.success(f"### Final Result: `{number} (base 10) = {result} (base {base})`")

with tab6:
    st.header("Backpropagation with Arrays and Linked Lists")

    st.write("### Forward and Backward Pass")

    st.write("#### Forward Pass")
    st.code("""
    def forward(input):
        current = input
        for each layer in linked list:
            current = layer.forward(current)
        return current
    """)

    st.write("#### Backward Pass")
    st.code("""
    def backward(loss_gradient, learning_rate):
        current_grad = loss_gradient
        for each layer in reversed linked list:
            current_grad = layer.backward(current_grad, learning_rate)
    """)

    # Section 3: Training Process
    st.write("### Training Process")

    st.write("#### Loss Function (Mean Squared Error)")
    st.code("""
    loss = sum((predicted[i] - target[i])²) / n
    gradient = 2 * (predicted - target) / n
    """)

    st.write("#### Weight Update Rule")
    st.code("""
    weight = weight - learning_rate * (gradient * input)
    bias = bias - learning_rate * gradient
    """)

    # Section 4: XOR Example
    st.write("### XOR Problem Example")

    st.write("#### Training Data")
    st.code("""
    Inputs:    Targets:
    [0, 0]  →  0
    [0, 1]  →  1
    [1, 0]  →  1
    [1, 1]  →  0
    """)

    st.write("#### Network Architecture")
    st.code("""
    Input Layer:   2 neurons
    Hidden Layer:  4 neurons (sigmoid)
    Output Layer:  1 neuron  (sigmoid)
    """)

    # Simulate training (static example)
    if st.button("Run XOR Training Simulation"):
        placeholder = st.empty()
        
        # Simulate epochs
        losses = [0.25, 0.18, 0.12, 0.08, 0.05, 0.03, 0.02, 0.01, 0.008, 0.005]
        
        for i, loss in enumerate(losses):
            with placeholder.container():
                st.write(f"**Epoch {i*100}: Loss = {loss:.4f}**")
                st.progress((len(losses) - i - 1)/len(losses))  # Scale for visualization
            time.sleep(0.5)
        
        st.success("Training completed!")
        
        # Show results
        st.write("### Final Predictions:")
        results = [
            {"input": "[0, 0]", "predicted": "0.02", "target": "0"},
            {"input": "[0, 1]", "predicted": "0.98", "target": "1"},
            {"input": "[1, 0]", "predicted": "0.97", "target": "1"},
            {"input": "[1, 1]", "predicted": "0.03", "target": "0"}
        ]
        
        for r in results:
            st.write(f"Input: {r['input']} → Predicted: {r['predicted']} (Target: {r['target']})")