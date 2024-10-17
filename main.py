import pandas as pd
import time
import streamlit as st
from mysql.connector import connect
from streamlit_option_menu import option_menu

mydb = connect(host="localhost", user="root", password="Anoop", database="cms")
cursor = mydb.cursor()

def popup(message):
    placeholder = st.empty()
    placeholder.success(message)
    time.sleep(1)
    placeholder.empty()

st.session_state['popup'] = False
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
        st.session_state['uid'] = st.text_input("Enter User ID", value="C001")
        pwd = st.text_input("Enter Password", type="password", value="C001")
        if st.button("Login"):
            cursor.execute("SELECT * FROM customer WHERE Customer_ID=%s AND Password=%s",(st.session_state['uid'], pwd))
            if cursor.fetchone():
                st.session_state['login'] = True
                st.rerun()
            else:
                st.error("Incorrect User ID or Password!")
    else:
        with st.sidebar:
            selected_feat = option_menu("Customer", ["View Personal Info", "Update Personal Info", "View Purchases",
                                   "Submit Support Request", "View Support Request Status", "Submit Feedback", "View Loyalty Points"],
                                   menu_icon="cast")
        
        # -------------------------- Enter code for the Customer Features here ------------------------- #
        
        if selected_feat == "View Personal Info":
            st.markdown("#### View Personal Information")
            cursor.execute("SELECT * FROM customer WHERE Customer_ID=%s", (st.session_state['uid'],))
            cust_info = cursor.fetchall()
            cust_info = pd.read_sql(f"SELECT * FROM customer WHERE Customer_ID='{st.session_state['uid']}'", mydb)
            cust_info = cust_info.T
            st.dataframe(cust_info)

        # ---------------------------------------------------------------------------------------------- #

        with st.sidebar:
                st.markdown("<br>" * 5, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True
                        
else:
    if not st.session_state['login']:
        if st.session_state['choice'] == "Customer Relationship Manager":
            dept = "Customer Relationship Management"
        elif st.session_state['choice'] == "Support Manager":
            dept = "Customer Support"
        elif st.session_state['choice'] == "Sales Manager":
            dept = "Sales"
        elif st.session_state['choice'] == "Product Manager":
            dept = "Production"

        st.session_state['uid'] = st.text_input("Enter User ID")
        pwd = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            cursor.execute("SELECT Dept_Name FROM department WHERE Manager_ID=%s", (st.session_state['uid'],))
            user_dept = cursor.fetchall()
            if user_dept:
                if dept == user_dept[0][0]:
                    cursor.execute("SELECT Department_ID FROM manager WHERE Manager_ID=%s AND Password=%s",(st.session_state['uid'], pwd))
                    if cursor.fetchone():
                        st.session_state['login'] = True
                        st.rerun()
                    else:
                        st.error("Incorrect Password!")
                else:
                    st.warning("You are not authorized to select this login option!")
            else:
                st.error("Incorrect User ID!")
                
    else:
        if st.session_state['choice'] == "Customer Relationship Manager":
            with st.sidebar:
                selected_feat = option_menu("Customer Relationship Manager", ["View Customer Info", "Add New Customer", "Delete Customer", 
                                            "Update Customer Details", "View Customer Support Requests", "Assign Support Requests", 
                                            "View & Respond to Customer Feedback", "Manage Loyalty Program"],
                                    menu_icon="cast")

            # -------------- Enter code for the Customer Relationship Mamanger Features here --------------- #
            st.write(f"Selected option is : {selected_feat}")

            # ---------------------------------------------------------------------------------------------- #

            with st.sidebar:
                st.markdown("<br>" * 1, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True
                        
        elif st.session_state['choice'] == "Support Manager":
            with st.sidebar:
                selected_feat = option_menu("Support Manager", ["View All Support Requests", "Update Support Request", "Generate Support Reports", 
                                                         "View Customer Purchases"],
                                    menu_icon="cast")

            # ---------------------- Enter code for the Support Manager Features here ---------------------- #
            st.write(f"Selected option is : {selected_feat}")

            # ---------------------------------------------------------------------------------------------- #

            with st.sidebar:
                st.markdown("<br>" * 10, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True
                        
        elif st.session_state['choice'] == "Sales Manager":
            with st.sidebar:
                selected_feat = option_menu("Sales Manager", ["Upload Sales Data", "Generate Sales Report", "View Product Feedback"],
                                    menu_icon="cast")

            # ----------------------- Enter code for the Sales Manager Features here ----------------------- #
            st.write(f"Selected option is : {selected_feat}")

            # ---------------------------------------------------------------------------------------------- #

            with st.sidebar:
                    st.markdown("<br>" * 12, unsafe_allow_html=True)
                    st.sidebar.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button("Logout"):
                            st.session_state['popup'] = True
                            
        elif st.session_state['choice'] == "Product Manager":
            with st.sidebar:
                selected_feat = option_menu("Product Manager", ["Add New Products", "Update Products", "Delete Products", 
                                                         "Manage Product Categories", "View Product Feedback", "Update Product Pricing"],
                                    menu_icon="cast")

            # ---------------------- Enter code for the Product Manager Features here ---------------------- #
            st.write(f"Selected option is : {selected_feat}")
            
            # ---------------------------------------------------------------------------------------------- #

            with st.sidebar:
                    st.markdown("<br>" * 7, unsafe_allow_html=True)
                    st.sidebar.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button("Logout"):
                            st.session_state['popup'] = True
                            

if st.session_state['popup']:
    st.session_state['login'] = False
    st.session_state['choice'] = None
    st.session_state['uid'] = None
    popup("You have been logged out!")
    st.rerun()

mydb.close()
cursor.close()
