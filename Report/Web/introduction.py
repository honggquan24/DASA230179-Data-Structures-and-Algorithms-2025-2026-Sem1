import streamlit as st
import sys

def render_stack_tab():
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
        
    with col1: 
        st.write("**Operations:**")
        
        # Input for new value
        value = st.text_input("Enter value:", key="stack_input")
        
        # Create buttons in columns for better layout
        btn_col1, btn_col2, btn_col3, btn_col4, btn_col5, btn_col6 = st.columns(6)
        
        with btn_col1:
            # Push operation
            if st.button('Push', key='push', use_container_width=True):
                if value and value.strip():
                    st.session_state['array_stack'].append(value.strip())
                    st.session_state['last_operation'] = f"[PUSH]: Added '{value.strip()}' to stack"
                    st.session_state['operation_result'] = "success"
                    st.rerun()
                else:
                    st.session_state['last_operation'] = "[PUSH]: Please enter a valid value"
                    st.session_state['operation_result'] = "error"
        
        with btn_col2:
            # Pop operation
            if st.button('Pop', key='pop', use_container_width=True):
                if st.session_state['array_stack']:
                    popped_value = st.session_state['array_stack'].pop()
                    st.session_state['last_operation'] = f"[POP]: Removed '{popped_value}' from stack"
                    st.session_state['operation_result'] = "success"
                    st.rerun()
                else:
                    st.session_state['last_operation'] = "[POP]: Stack is empty, cannot pop"
                    st.session_state['operation_result'] = "error"
        
        with btn_col3:
            # Peek operation
            if st.button('Peek', key='peek', use_container_width=True):
                if st.session_state['array_stack']:
                    top_value = st.session_state['array_stack'][-1]
                    st.session_state['last_operation'] = f"[PEEK]: Top element is '{top_value}'"
                    st.session_state['operation_result'] = "info"
                else:
                    st.session_state['last_operation'] = "[PEEK]: Stack is empty"
                    st.session_state['operation_result'] = "error"
        
        with btn_col4:
            # isEmpty operation
            if st.button('isEmpty', key='is_empty', use_container_width=True):
                is_empty = (len(st.session_state['array_stack']) == 0)
                if is_empty:
                    st.session_state['last_operation'] = "[IS_EMPTY]: Stack is empty"
                else:
                    st.session_state['last_operation'] = "[IS_EMPTY]: Stack has elements"
                st.session_state['operation_result'] = "info"
        
        with btn_col5:
            # Size operation
            if st.button('Size', key='size', use_container_width=True):
                size = len(st.session_state['array_stack'])
                st.session_state['last_operation'] = f"[SIZE]: Stack size is {size}"
                st.session_state['operation_result'] = "info"
        
        with btn_col6:
            # Clear stack operation
            if st.button('Clear Stack', key='clear', use_container_width=True):
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
                st.markdown("<br>", unsafe_allow_html=True)
                for i in range(len(st.session_state['array_stack']) - 1, -1, -1):
                    element = st.session_state['array_stack'][i]
                    
                    # Create expander title with TOP indicator
                    if i == len(st.session_state['array_stack']) - 1:
                        expander_title = f"Element {i + 1} (TOP)"
                        expander_expanded = True
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
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("Stack is empty - No elements")