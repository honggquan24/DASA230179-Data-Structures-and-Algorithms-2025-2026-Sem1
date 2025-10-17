import streamlit as st
import time

def check_balanced_brackets(expr):
    if not expr.strip():
        return True, [{"message": "Empty expression - valid"}]
    
    stack = []
    bracket_pairs = {')': '(', '}': '{', ']': '['}
    steps = []

    for i, char in enumerate(expr):
        # Skip non-bracket characters
        if char not in "(){}[]":
            continue
            
        step_info = {
            'step_num': len(steps) + 1,
            'char': char,
            'position': i,
            'stack_before': stack.copy(),
        }

        # Opening bracket - push to stack
        if char in "({[":
            stack.append(char)
            step_info['action'] = 'PUSH'
            step_info['status'] = 'push'
            step_info['message'] = f"Found opening bracket '{char}' -> Push to stack"
            
        # Closing bracket - check and pop
        else:
            if not stack:
                step_info['action'] = 'ERROR'
                step_info['status'] = 'error'
                step_info['message'] = f"Error: Found closing bracket '{char}' but stack is empty!"
                step_info['stack_after'] = stack.copy()
                steps.append(step_info)
                return False, steps
                
            if stack[-1] != bracket_pairs[char]:
                step_info['action'] = 'ERROR'
                step_info['status'] = 'error'
                step_info['message'] = f"Error: '{char}' does not match with '{stack[-1]}'"
                step_info['stack_after'] = stack.copy()
                steps.append(step_info)
                return False, steps
            
            matched = stack.pop()
            step_info['action'] = 'POP'
            step_info['status'] = 'pop'
            step_info['message'] = f"'{char}' matches with '{matched}' -> Pop from stack"

        step_info['stack_after'] = stack.copy()
        steps.append(step_info)

    # Final check
    is_valid = len(stack) == 0
    steps.append({
        'step_num': len(steps) + 1,
        'char': 'END',
        'action': 'CHECK',
        'status': 'success' if is_valid else 'error',
        'message': 'Stack is empty -> Expression is valid!' if is_valid else 'Stack is not empty -> Expression is invalid!',
        'stack_after': stack.copy()
    })
    
    return is_valid, steps


def render_stack_tab():
    st.header("Check Balanced Parentheses")
    
    # Algorithm explanation
    st.write("### Algorithm Concept:")
    st.info("""
    **Principle**: Traverse each character in the expression:
    - When encountering **opening brackets** `(`, `{`, `[` -> **push** to stack
    - When encountering **closing brackets** `)`, `}`, `]` -> check if **peek** matches -> if yes, **pop**, else error
    - At the end, stack must be **empty** -> expression is valid
    """)

    # Input section
    st.write("### Enter Expression:")
    expression = st.text_input(
        "Enter expression to check:", 
        value="{x+[(a+b)*c]}", 
        key="expr_input",
        help="Examples: (a+b)*[c-d], {x+(y-z)}, [(a+b)]"
    )
    
    # Control button
    check_btn = st.button("Check", key="check_brackets", type="primary")

    # Main processing
    if check_btn:
        if not expression.strip():
            st.warning("Please enter an expression to check!")
            return
            
        # Perform check and save to session state
        is_valid, steps = check_balanced_brackets(expression)
        st.session_state['bracket_steps'] = steps
        st.session_state['bracket_result'] = is_valid
        st.session_state['bracket_expr'] = expression

    # Display results if available
    if 'bracket_steps' in st.session_state:
        st.write("### Execution Process:")
        
        for step in st.session_state['bracket_steps']:
            if step.get('char') == 'END':
                # Final step
                if step['status'] == 'success':
                    st.success(f"**Step {step['step_num']}**: {step['message']}")
                else:
                    st.error(f"**Step {step['step_num']}**: {step['message']}")
                    remaining = step['stack_after'] if step['stack_after'] else []
                    st.write(f"**Remaining Stack:** `{remaining}`")
            else:
                # Character processing steps
                col1, col2, col3 = st.columns([1, 2, 2])
                
                with col1:
                    if step['status'] == 'push':
                        st.success(f"**Step {step['step_num']}**")
                    elif step['status'] == 'pop':
                        st.info(f"**Step {step['step_num']}**")
                    else:
                        st.error(f"**Step {step['step_num']}**")
                
                with col2:
                    st.write(f"**Character:** `{step['char']}` (position {step['position']})")
                    st.write(f"**Action:** {step['action']}")
                    st.write(f"**Stack:** `{step['stack_after']}`")
                
                with col3:
                    if step['status'] == 'push':
                        st.success(step['message'])
                    elif step['status'] == 'pop':
                        st.info(step['message'])
                    else:
                        st.error(step['message'])
                        break
                
                st.divider()
            time.sleep(1.5)
        # Final result
        st.write("### Result:")
        expr = st.session_state.get('bracket_expr', expression)
        if st.session_state.get('bracket_result'):
            st.success(f"The expression `{expr}` is valid")
        else:
            st.error(f"The expression `{expr}` is invalid")
