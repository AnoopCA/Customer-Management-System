import pandas as pd
import streamlit as st
from mysql.connector import connect
from streamlit_option_menu import option_menu
from datetime import datetime
import time
import calendar

mydb = connect(host="localhost", user="root", password="Anoop", database="cms")
cursor = mydb.cursor()

def login_screen(choice):
    if not st.session_state['login']:
        uid = st.text_input("Enter User ID")
        pwd = st.text_input("Enter Password", type="password")
        btn = st.button("Login")
        if btn:
            if choice == "Customer":
                cursor.execute("SELECT * FROM customer")


            else:
                cursor.execute("SELECT * FROM manager")
                for user in cursor:
                    if user[0]==uid and user[12]==pwd:
                        st.session_state['uid'] = user[0]
                        st.session_state['uname'] = user[1]
                        st.session_state['Dept_ID'] = user[2]
                        st.session_state['Role_ID'] = user[3]
                        st.session_state['auth'] = False
                        if choice == "Employee":
                            st.session_state['login'] = True
                            st.session_state['auth'] = True
                            break
                        elif choice == "HR":
                            if st.session_state['Dept_ID'] == "HR":
                                st.session_state['login'] = True
                                st.session_state['auth'] = True
                                break
                        elif choice == "Department Head":
                            if st.session_state['Role_ID'] == "HOD":
                                st.session_state['login'] = True
                                st.session_state['auth'] = True
                                break
                        elif choice == "Manager":
                            if st.session_state['Role_ID'] == "MGR":
                                st.session_state['login'] = True
                                st.session_state['auth'] = True
                                break
                        elif choice == "Project Manager":
                            if st.session_state['Role_ID'] == "PM":
                                st.session_state['login'] = True
                                st.session_state['auth'] = True
                                break
                if st.session_state['auth'] == False:
                    st.error("You are not Authorized to login for this Role!")
                    return False
                if not st.session_state['login']:
                    st.error("Incorrect ID or Password")
                    return False
    else:
        return True

st.title("CUSTOMER MANAGEMENT SYSTEM")

if 'login' not in st.session_state:
    st.session_state['login'] = False

if not st.session_state['login']:
    st.session_state['choice'] = st.sidebar.selectbox("Choose Your Role", 
                                 ("Home", "Customer", "Customer Relationship Manager", "Support Manager", "Sales Manager", "Product Manager"))
else:
    if not st.session_state['choice']:
        st.session_state['choice'] = None




st.session_state['popup'] = False
with st.sidebar:
    st.markdown("<br>" * 20, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Logout"):
            st.session_state['login'] = False
            st.session_state['choice'] = None
            st.session_state['popup'] = True

def popup(message):
    placeholder = st.empty()
    placeholder.success(message)
    time.sleep(2)
    placeholder.empty()

if st.session_state['popup']:
    popup("You have been logged out!")

mydb.close()
cursor.close()
