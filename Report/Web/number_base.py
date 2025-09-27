import streamlit as st
import time

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

def render_stack_tab():
    st.header("Convert Number Base")
    st.write("""
    **Idea**: Repeatedly divide the number by base, push remainders to stack → then pop to reverse order.
    """)

    col_num, col_base = st.columns(2)
    with col_num:
        number = st.number_input("Number to convert:", min_value=0, max_value=10000, value=233, step=1, key="num_input")
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
            time.sleep(5)

        st.success(f"### Final Result: `{number} (base 10) = {result} (base {base})`")