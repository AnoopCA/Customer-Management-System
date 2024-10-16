import pandas as pd
import streamlit as st
from mysql.connector import connect
from streamlit_option_menu import option_menu

mydb = connect(host="localhost", user="root", password="Anoop", database="cms")
cursor = mydb.cursor()
                   
st.title("CUSTOMER MANAGEMENT SYSTEM")

if 'login' not in st.session_state:
    st.session_state['login'] = False

if not st.session_state['login']:
    st.session_state['choice'] = st.sidebar.selectbox("Choose Your Role", 
                                 ("Home", "Customer", "Customer Relationship Manager", "Support Manager", "Sales Manager", "Product Manager"))
else:
    if not st.session_state['choice']:
        st.session_state['choice'] = None

if st.session_state['choice'] == "Customer":
    if not st.session_state['login']:
        uid = st.text_input("Enter User ID")
        pwd = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            cursor.execute("SELECT * FROM customer WHERE Customer_ID=%s AND Password=%s",(uid, pwd))
            if cursor.fetchone():
                st.session_state['login'] = True
                st.rerun()
    else:
        st.write("Test in Customer")
else:
    if not st.session_state['login']:
        cursor.execute("SELECT Department_ID FROM department WHERE ")
        
        # ***** There is a conflict between the department name and the choice values from the sidebar select box. Correct it and proceed *****
        
        uid = st.text_input("Enter User ID")
        pwd = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            cursor.execute("SELECT Department_ID FROM manager WHERE Manager_ID=%s AND Password=%s",(uid, pwd))
            if cursor.fetchone():
                st.session_state['login'] = True
                st.rerun()
    else:
        st.write("Test in Manager")

mydb.close()
cursor.close()
