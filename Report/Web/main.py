import streamlit as st
import time
import sys
from typing import List
import theme, introduction, in_2_post, dfs_backtracking, number_base, parenthese, recursion
from theme import THEME_LIGHTMODE, THEME_DARKMODE

st.set_page_config(
    page_title="Stack Application",
    layout="wide",
    initial_sidebar_state="expanded",
)

light_mode = st.toggle("🌙 / ☀️ Mode", value=False)

if light_mode:
    st.markdown(theme.get_css(THEME_LIGHTMODE), unsafe_allow_html=True)
else:
    st.markdown(theme.get_css(THEME_DARKMODE), unsafe_allow_html=True)

st.markdown("""
            <div style="text-align: center;">
                <h1>Stack Applications</h1>
            </div>
        """, unsafe_allow_html=True)
st.markdown("<br></br>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Introduction', 'Recursion', 'Infix to Postfix', 'Check Balance Parenthese', 
                                              'Convert Numver Base'])

with tab1:
    introduction.render_stack_tab()

with tab2:
    recursion.render_stack_tab()

with tab3:
    in_2_post.render_stack_tab()

with tab4:
    parenthese.render_stack_tab()

with tab5:
    number_base.render_stack_tab()

# with tab6:
#     dfs_backtracking.render_stack_tab()