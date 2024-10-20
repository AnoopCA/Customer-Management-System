import pandas as pd
import time
import streamlit as st
from mysql.connector import connect
from streamlit_option_menu import option_menu
from datetime import datetime

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
            cust_info = pd.read_sql(f"SELECT * FROM customer WHERE Customer_ID='{st.session_state['uid']}'", mydb)
            cust_info = cust_info.T
            st.dataframe(cust_info)

        elif selected_feat == "Update Personal Info":
            st.markdown("#### Update Personal Information")
            cursor.execute("SELECT * FROM customer WHERE Customer_ID=%s",(st.session_state["uid"],))
            emp_data = cursor.fetchone()
            if emp_data:
                st.session_state['emp_data'] = emp_data
            if 'emp_data' in st.session_state:
                Customer_Name = st.text_input("Name", value=st.session_state['emp_data'][1])
                Password = st.text_input("Password", value=st.session_state['emp_data'][2])
                Contact_No = st.text_input("Contact Number", value=st.session_state['emp_data'][3])
                Email_ID = st.text_input("Email ID", value=st.session_state['emp_data'][4])
                Address = st.text_input("Address", value=st.session_state['emp_data'][5])
                Date_of_Birth = st.date_input("Date Of Birth", value=st.session_state['emp_data'][6])
                Gender = st.selectbox("Gender", ["Male", "Female"], index = 0 if st.session_state['emp_data'][7]=="Male" else 1)

                if st.button("Save Changes"):
                    cursor.execute("""UPDATE customer SET Customer_Name=%s,Password=%s,Contact_No=%s,Email_ID=%s,Address=%s,Date_of_Birth=%s,Gender=%s
                                      WHERE Customer_ID=%s""", (Customer_Name,Password,Contact_No,Email_ID,Address,Date_of_Birth,Gender,st.session_state["uid"]))
                    mydb.commit()
                    st.success("Personal details updated successfully!")
                    st.session_state.pop('emp_data', None)

        elif selected_feat == "View Purchases":
            st.markdown("#### View Purchases")
            cursor.execute("""SELECT PH.Customer_ID, PH.Purchase_Date, PH.Product_ID, PD.Product_Name, PD.Category, PD.Price, PH.Quantity, PH.Total_Amount
                              FROM purchases PH JOIN products PD on PH.Product_ID = PD.Product_ID WHERE PH.Customer_ID=%s""", (st.session_state['uid'],))
            purchase_data = cursor.fetchall()
            purchase_data = pd.DataFrame(purchase_data, columns=[desc[0] for desc in cursor.description])
            st.dataframe(purchase_data)
        
        elif selected_feat == "Submit Support Request":
            st.markdown("#### Submit Support Request")
            cursor.execute("SELECT Request_ID FROM Customer_Support_Requests ORDER BY Request_ID DESC LIMIT 1")
            Request_ID = int(cursor.fetchone()[0][1:])
            Request_ID = f'R{Request_ID+1:03}'
            Purchase_ID = st.text_input("Enter the Purchase ID if any:")
            Product_ID = st.text_input("Enter the Product ID if any:")
            Request_Date = datetime.date(datetime.today())
            Request_Description = st.text_area("Enter the description of the issue:")
            if st.button("Submit The Request"):
                cursor.execute("INSERT INTO Customer_Support_Requests VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                               (Request_ID, st.session_state['uid'], Purchase_ID, Product_ID, Request_Date, Request_Description, "Pending", "NULL"))
                popup("Support Request Submitted Successfully!")
                mydb.commit()

        elif selected_feat == "View Support Request Status":
            st.markdown("#### View Support Request Status")
            cust_info = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Customer_ID='{st.session_state['uid']}'", mydb)
            st.dataframe(cust_info)

        elif selected_feat == "Submit Feedback":
            st.markdown("#### Submit Feedback")
            cursor.execute("SELECT Feedback_ID FROM Customer_Feedback ORDER BY Feedback_ID DESC LIMIT 1")
            Feedback_ID = int(cursor.fetchone()[0][1:])
            Feedback_ID = f'F{Feedback_ID+1:03}'
            cursor.execute("SELECT DISTINCT Product_Name FROM Products")
            Products = cursor.fetchall()
            Products = [i[0] for i in Products]
            Products.insert(0, "General Feedback")
            Products = st.selectbox("Enter a General Feedback or select a specific Product", Products)
            Feedback_Date = datetime.date(datetime.today())
            Rating = st.selectbox("Rating", [1, 2, 3, 4, 5], index=4)
            Comments = st.text_area("Comments")
            if st.button("Submit The Feedback"):
                cursor.execute("INSERT INTO Customer_Feedback VALUES (%s,%s,%s,%s,%s,%s)",
                               (Feedback_ID, st.session_state['uid'], Products, Feedback_Date, Rating, Comments))
                popup("Feedback Submitted Successfully!")
                mydb.commit()

        elif selected_feat == "View Loyalty Points":
            st.markdown("#### View Loyalty Points")
            cursor.execute("""SELECT * FROM Loyalty_Program WHERE Customer_ID=%s""", (st.session_state['uid'],))
            loyalty_points = cursor.fetchall()
            loyalty_points = pd.DataFrame(loyalty_points, columns=[desc[0] for desc in cursor.description])
            st.dataframe(loyalty_points)

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

        st.session_state['uid'] = st.text_input("Enter User ID", value='M001')
        pwd = st.text_input("Enter Password", type="password", value='M001')
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

            # -------------- Enter code for the Customer Relationship Mananger Features here --------------- #
            
            if selected_feat == "View Customer Info":
                st.markdown("#### View Customer Info")
                cust_id = st.text_input("Enter the Customer ID to find the details:")
                if st.button("Fetch Customer Details"):
                    cust_data = pd.read_sql(f"SELECT * FROM customer WHERE Customer_ID='{cust_id}'", mydb)
                    if cust_data.empty:
                        st.warning("No details found for the given Customer ID. Please enter the correct Customer ID!")
                    else:
                        st.dataframe(cust_data)
            
            if selected_feat == "Add New Customer":
                st.markdown("#### Add New Customer")
                st.write("Enter the Customer Details below")
                cursor.execute("SELECT Customer_ID FROM Customer ORDER BY Customer_ID DESC LIMIT 1")
                Customer_ID = int(cursor.fetchone()[0][1:])
                Customer_ID = f'C{Customer_ID+1:03}'
                Customer_Name = st.text_input("Customer Name:")
                Password = st.text_input("Password:")
                Contact_No = st.text_input("Contact Number:")
                Email_ID = st.text_input("Email ID:")
                Address = st.text_input("Address:")
                Date_of_Birth = st.date_input("Date Of Birth:")
                Gender = st.selectbox("Gender:", ["Male", "Female"])
                Registration_Date = datetime.date(datetime.today())
                Manager_ID = st.text_input("")
                        

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
