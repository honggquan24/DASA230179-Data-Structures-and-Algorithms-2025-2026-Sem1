import streamlit as st
import time

def render_stack_tab():
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
                time.sleep(5)
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