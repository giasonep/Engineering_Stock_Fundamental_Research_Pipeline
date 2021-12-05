# import packages
import streamlit as st
import streamlit_page1
import streamlit_page2

# set the tab icon, tab title and page config
st.set_page_config(page_title='Powerful Stock Fundamentals', page_icon = '📉', layout = 'wide', initial_sidebar_state = 'auto')
 # set the page background color
page_bg_img = '''<style> div {background-color: #4d7554;}</style>'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# # example code
# page_bg_img = '''
# <style>
# section {
#     background-image: url(“https://images.unsplash.com/photo-1634022104045-e0e21b3e0bc0?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2070&q=80”);
#     background-repeat: no-repeat;
#     background-attachment: fixed;
#     background-size: cover;
# }
# </style>
# '''
# st.markdown(page_bg_img, unsafe_allow_html=True)

# multiple pages
PAGES = {
    "Research": streamlit_page1,
    "Leaderboard": streamlit_page2
}

st.sidebar.title('MENU')
selection = st.sidebar.radio(' ', list(PAGES.keys()))
page= PAGES[selection]
page.app()

