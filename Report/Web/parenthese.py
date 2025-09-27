import streamlit as st
import time 

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


def render_stack_tab():
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
                            time.sleep(5)
                        else:
                            st.error(f"**Step {step['step_num']}**: {step['message']}")
                            st.write(f"**Remaining Stack:** `{step['stack_after'] if step['stack_after'] else '[]'}`")
                            time.sleep(5)
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
                        time.sleep(5)
            # Final result
            st.write("### Result:")
            if st.session_state.get('bracket_result'):
                st.success(f"The expression`{expression}` is valid")
            else:
                st.error(f"The expression`{expression}` is invalid")
        else:
            st.warning("Please enter an expression to check!")   
