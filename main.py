# Importing necessary libraries
import pandas as pd
import time
import streamlit as st
from mysql.connector import connect
from streamlit_option_menu import option_menu
from datetime import datetime

# Establishing connection to the MySQL database named "cms"
cms_db = connect(host="localhost", user="root", password="Anoop", database="cms")
cursor = cms_db.cursor()

# Function to display a popup message for 1 second
def popup(message):
    placeholder = st.empty()
    placeholder.success(message)
    time.sleep(1)
    placeholder.empty()

# Initializing session state variable 'popup'
st.session_state['popup'] = False
# Setting the title of the app
st.title("CUSTOMER MANAGEMENT SYSTEM")

# If the session state 'login' is not set, initialize it as False
if 'login' not in st.session_state:
    st.session_state['login'] = False
# If the user is not logged in, allow them to choose their role from the sidebar
if not st.session_state['login']:
    st.session_state['choice'] = st.sidebar.selectbox("Choose Your Role", 
                                 ("Home", "Customer", "Customer Relationship Manager", "Support Manager", "Sales Manager", "Product Manager"))
else:
    # If already logged in, set 'choice' to None if it's not defined
    if not st.session_state['choice']:
        st.session_state['choice'] = None

# Display home page if "Home" is selected
if st.session_state['choice'] == "Home":
    st.image("D:/ML_Projects/Customer-Management-System/Archives/Customer_1.jpg")
    st.write("")
    st.markdown("""The Customer Management System (CMS) enables seamless interaction between customers and the company while efficiently 
                   managing key business operations. Customers can view and update personal information, track purchases, submit support requests,
                   and view loyalty points. The system allows managers, such as the Customer Relationship Manager, Support Manager, Sales Manager, 
                   and Product Manager, to handle customer information, support requests, sales data, product management, and feedback. This 
                   centralized system ensures efficient customer service, streamlined operations, and improved communication across departments.""")

# If "Customer" role is selected display options for Customer
elif st.session_state['choice'] == "Customer":
    # If the user is not logged in, prompt for User ID and Password
    if not st.session_state['login']:
        st.session_state['uid'] = st.text_input("Enter User ID")
        pwd = st.text_input("Enter Password", type="password")
        # Check login credentials when login button is clicked
        if st.button("Login"):
            cursor.execute("SELECT * FROM customer WHERE Customer_ID=%s AND Password=%s",(st.session_state['uid'], pwd))
            if cursor.fetchone():
                st.session_state['login'] = True
                st.rerun()
            else:
                st.error("Incorrect User ID or Password!")
    else:
        # Sidebar menu for logged-in customers to access different features
        with st.sidebar:
            selected_feat = option_menu("Customer", ["View Personal Info", "Update Personal Info", "View Purchases",
                                   "Submit Support Request", "View Support Request Status", "Submit Feedback", "View Loyalty Points"],
                                   menu_icon="cast")
        
        # ---------------------------------- Customer Management -------------------------------------------- #
        
        # Customer Feature 1: View Personal Info
        if selected_feat == "View Personal Info":
            st.markdown("#### View Personal Information")
            cust_info = pd.read_sql(f"SELECT * FROM customer WHERE Customer_ID='{st.session_state['uid']}'", cms_db)
            cust_info = cust_info.T
            st.dataframe(cust_info)

        # Customer Feature 2: Update Personal Info
        elif selected_feat == "Update Personal Info":
            st.markdown("#### Update Personal Information")
            # Fetch customer details from the database using their User ID
            cursor.execute("SELECT * FROM customer WHERE Customer_ID=%s",(st.session_state["uid"],))
            emp_data = cursor.fetchone()
            if emp_data:
                st.session_state['emp_data'] = emp_data
            # If customer data is found, display input fields to update their information
            if 'emp_data' in st.session_state:
                Customer_Name = st.text_input("Name", value=st.session_state['emp_data'][1])
                Password = st.text_input("Password", value=st.session_state['emp_data'][2])
                Contact_No = st.text_input("Contact Number", value=st.session_state['emp_data'][3])
                Email_ID = st.text_input("Email ID", value=st.session_state['emp_data'][4])
                Address = st.text_input("Address", value=st.session_state['emp_data'][5])
                Date_of_Birth = st.date_input("Date Of Birth", value=st.session_state['emp_data'][6])
                Gender = st.selectbox("Gender", ["Male", "Female"], index = 0 if st.session_state['emp_data'][7]=="Male" else 1)
                
                # Save changes when the button is clicked and update the database
                if st.button("Save Changes"):
                    cursor.execute("""UPDATE customer SET Customer_Name=%s,Password=%s,Contact_No=%s,Email_ID=%s,Address=%s,Date_of_Birth=%s,Gender=%s
                                      WHERE Customer_ID=%s""", (Customer_Name,Password,Contact_No,Email_ID,Address,Date_of_Birth,Gender,st.session_state["uid"]))
                    cms_db.commit()
                    st.success("Personal details updated successfully!")
                    st.session_state.pop('emp_data', None)

        # Customer Feature 3: View Purchases
        elif selected_feat == "View Purchases":
            st.markdown("#### View Purchases")
            cursor.execute("""SELECT PH.Customer_ID, PH.Purchase_Date, PH.Product_ID, PD.Product_Name, PD.Category, PD.Price, PH.Quantity, PH.Total_Amount
                              FROM purchases PH JOIN products PD on PH.Product_ID = PD.Product_ID WHERE PH.Customer_ID=%s""", (st.session_state['uid'],))
            purchase_data = cursor.fetchall()
            purchase_data = pd.DataFrame(purchase_data, columns=[desc[0] for desc in cursor.description])
            st.dataframe(purchase_data)
        
        # Customer Feature 4: Submit Support Request
        elif selected_feat == "Submit Support Request":
            st.markdown("#### Submit Support Request")
             # Fetch the latest Request_ID from the database and increment it for the new request
            cursor.execute("SELECT Request_ID FROM Customer_Support_Requests ORDER BY Request_ID DESC LIMIT 1")
            Request_ID = int(cursor.fetchone()[0][1:])
            Request_ID = f'R{Request_ID+1:03}'
            # Input fields for support request details
            Purchase_ID = st.text_input("Enter the Purchase ID if any:")
            Product_ID = st.text_input("Enter the Product ID if any:")
            Request_Date = datetime.date(datetime.today())
            Request_Description = st.text_area("Enter the description of the issue:")
            # When "Submit The Request" button is clicked
            if st.button("Submit The Request"):
                cursor.execute("INSERT INTO Customer_Support_Requests VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                               (Request_ID, st.session_state['uid'], Purchase_ID, Product_ID, Request_Date, Request_Description, "Pending", "NULL"))
                popup("Support Request Submitted Successfully!")
                cms_db.commit()

        # If the selected feature is "View Support Request Status"
        elif selected_feat == "View Support Request Status":
            st.markdown("#### View Support Request Status")
            cust_info = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Customer_ID='{st.session_state['uid']}'", cms_db)
            st.dataframe(cust_info)

        # If the selected feature is "Submit Feedback"
        elif selected_feat == "Submit Feedback":
            st.markdown("#### Submit Feedback")
            # Fetch the latest Feedback_ID from the database and increment it for the new feedback
            cursor.execute("SELECT Feedback_ID FROM Customer_Feedback ORDER BY Feedback_ID DESC LIMIT 1")
            Feedback_ID = int(cursor.fetchone()[0][1:])
            Feedback_ID = f'F{Feedback_ID+1:03}'
            # Fetch product names to provide a selection for feedback
            cursor.execute("SELECT DISTINCT Product_Name FROM Products")
            Products = cursor.fetchall()
            Products = [i[0] for i in Products]
            Products.insert(0, "General Feedback")
            Products = st.selectbox("Enter a General Feedback or select a specific Product", Products)
            Feedback_Date = datetime.date(datetime.today())
            Rating = st.selectbox("Rating", [1, 2, 3, 4, 5], index=4)
            Comments = st.text_area("Comments")
            # When "Submit The Feedback" button is clicked insert the new feedback into the database
            if st.button("Submit The Feedback"):
                cursor.execute("INSERT INTO Customer_Feedback VALUES (%s,%s,%s,%s,%s,%s)",
                               (Feedback_ID, st.session_state['uid'], Products, Feedback_Date, Rating, Comments))
                popup("Feedback Submitted Successfully!")
                cms_db.commit()

        # If the selected feature is "View Loyalty Points"
        elif selected_feat == "View Loyalty Points":
            st.markdown("#### View Loyalty Points")
            # Fetch and display loyalty points for the current user
            cursor.execute("""SELECT * FROM Loyalty_Program WHERE Customer_ID=%s""", (st.session_state['uid'],))
            loyalty_points = cursor.fetchall()
            loyalty_points = pd.DataFrame(loyalty_points, columns=[desc[0] for desc in cursor.description])
            st.dataframe(loyalty_points)

        # Sidebar section with logout button
        with st.sidebar:
                st.markdown("<br>" * 5, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True

# ---------------------------------------------------------------------------------------------- #

else:
    # Set department based on user's choice during login
    if not st.session_state['login']:
        if st.session_state['choice'] == "Customer Relationship Manager":
            dept = "Customer Relationship Management"
        elif st.session_state['choice'] == "Support Manager":
            dept = "Customer Support"
        elif st.session_state['choice'] == "Sales Manager":
            dept = "Sales"
        elif st.session_state['choice'] == "Product Manager":
            dept = "Production"

        # Input fields for User ID and Password
        st.session_state['uid'] = st.text_input("Enter User ID")
        pwd = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            # Check if the User ID exists in the department
            cursor.execute("SELECT Dept_Name FROM department WHERE Manager_ID=%s", (st.session_state['uid'],))
            user_dept = cursor.fetchall()
            if user_dept:
                # If department matches, verify password
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

        # ---------------------------------- Customer Relationship Manager ---------------------------------- #
        
        # If the user selects "Customer Relationship Manager" from the main menu, the following features are displayed in the sidebar
        if st.session_state['choice'] == "Customer Relationship Manager":
            with st.sidebar:
                # Sidebar menu options for managing customer-related tasks
                selected_feat = option_menu("Customer Relationship Manager", ["View Customer Info", "Add New Customer", "Delete Customer", 
                                            "Update Customer Details", "View Customer Support Requests", "Assign Support Requests", 
                                            "View & Respond to Customer Feedback", "Manage Loyalty Program"],
                                    menu_icon="cast")

            # Feature to view customer information by entering a customer ID
            if selected_feat == "View Customer Info":
                st.markdown("#### View Customer Info")
                cust_id = st.text_input("Enter the Customer ID to find the details:")
                if st.button("Fetch Customer Details"):
                    # Query to fetch customer details based on input customer ID
                    cust_data = pd.read_sql(f"SELECT * FROM customer WHERE Customer_ID='{cust_id}'", cms_db)
                    if cust_data.empty:
                        st.warning("No details found for the given Customer ID. Please enter the correct Customer ID!")
                    else:
                        st.dataframe(cust_data)
            
            # Feature to add a new customer by entering relevant details
            elif selected_feat == "Add New Customer":
                st.markdown("#### Add New Customer")
                st.write("Enter the Customer Details below")
                # Auto-generate the next customer ID by fetching the last entered ID and incrementing it
                cursor.execute("SELECT Customer_ID FROM Customer ORDER BY Customer_ID DESC LIMIT 1")
                Customer_ID = int(cursor.fetchone()[0][1:])
                Customer_ID = f'C{Customer_ID+1:03}'
                # Collecting necessary details from the user
                Customer_Name = st.text_input("Customer Name:")
                Password = Customer_ID
                Contact_No = st.text_input("Contact Number:")
                Email_ID = st.text_input("Email ID:")
                Address = st.text_input("Address:")
                Date_of_Birth = st.date_input("Date Of Birth:")
                Gender = st.selectbox("Gender:", ["Male", "Female"])
                Registration_Date = datetime.date(datetime.today())
                Manager_ID = None
                # Insert the new customer data into the database when 'Submit' button is clicked
                if st.button("Submit"):
                    cursor.execute("INSERT INTO Customer VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                                (Customer_ID, Customer_Name, Password, Contact_No, Email_ID, Address, Date_of_Birth, Gender, Registration_Date, Manager_ID))
                    cms_db.commit()
                    st.success(f"""Customer added successfully with the user ID -  "{Customer_ID}".
                                   The password is the User ID itself. User can change the password by using the option "Update Personal Info".""")
            
            # Feature to delete a customer by entering their customer ID
            elif selected_feat == "Delete Customer":
                dlt_cust_id = st.text_input("Enter the Customer ID to delete:")
                cursor.execute("SELECT Customer_Name FROM Customer WHERE Customer_ID=%s", (dlt_cust_id,))
                dlt_cust_name = cursor.fetchone()
                if st.button(f"Delete Customer Data"):
                    if dlt_cust_name:
                        cursor.execute("DELETE FROM Customer WHERE Customer_ID=%s", (dlt_cust_id,))
                        cms_db.commit()
                        st.success("Customer data is deleted!")
                    else:
                        st.error("Customer details not found!")

            # Feature to update customer details
            elif selected_feat == "Update Customer Details":
                st.markdown("#### Update Customer Details")
                updt_cust_id = st.text_input("Enter the Customer ID to update the details:")
                if st.button("Fetch Customer Details"):
                    cursor.execute("SELECT * FROM customer WHERE Customer_ID=%s",(updt_cust_id,))
                    cust_data = cursor.fetchone()
                    # Store fetched customer data in the session state for later use
                    if cust_data:
                        st.session_state['cust_data'] = cust_data
                    elif updt_cust_id != "":
                            st.error("Customer ID is not found!")
                            st.session_state['cust_data'] = None
                # If customer data is available, allow the user to update the details
                if 'cust_data' in st.session_state:
                    if st.session_state['cust_data'] is not None:
                        Customer_Name = st.text_input("Name", value=st.session_state['cust_data'][1])
                        Password = st.text_input("Password", value=st.session_state['cust_data'][2])
                        Contact_No = st.text_input("Contact Number", value=st.session_state['cust_data'][3])
                        Email_ID = st.text_input("Email ID", value=st.session_state['cust_data'][4])
                        Address = st.text_input("Address", value=st.session_state['cust_data'][5])
                        Date_of_Birth = st.date_input("Date Of Birth", value=st.session_state['cust_data'][6])
                        Gender = st.selectbox("Gender", ["Male", "Female"], index = 0 if st.session_state['cust_data'][7]=="Male" else 1)
                        # Save the updated customer data when the "Save Changes" button is clicked
                        if st.button("Save Changes"):
                            if 'cust_data' in st.session_state:
                                if st.session_state['cust_data'] is not None:
                                    cursor.execute("""UPDATE customer SET Customer_Name=%s,Password=%s,Contact_No=%s,Email_ID=%s,Address=%s,Date_of_Birth=%s,Gender=%s
                                                    WHERE Customer_ID=%s""", (Customer_Name,Password,Contact_No,Email_ID,Address,Date_of_Birth,Gender,updt_cust_id))
                                    cms_db.commit()
                                    st.success("Customer details updated successfully!")
                                    st.session_state.pop('cust_data', None)

            # Handling the "View Customer Support Requests" feature 
            elif selected_feat == "View Customer Support Requests":
                st.markdown("#### View Customer Support Requests")
                suppt_cust_id = st.text_input("Enter the Customer ID:")
                if st.button("Fetch the Details"):
                    suppt_data = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Customer_ID='{suppt_cust_id}'", cms_db)
                    if suppt_data.empty:
                        st.error("Support Requests not found for the given Customer ID!")
                    else:
                        st.dataframe(suppt_data)

            # Handling the "Assign Support Requests" feature
            elif selected_feat == "Assign Support Requests":
                st.markdown("#### Assign Support Requests")
                st.markdown("##### All open Support Requests")
                # SQL query to retrieve all open support requests (not closed or cancelled)
                suppt_rqsts = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Request_Status != 'Closed' AND Request_Status != 'Cancelled'", cms_db)
                # Check if there are no open requests, otherwise display the pending requests
                if suppt_rqsts.empty:
                    st.success("No pending Support Requests!")
                else:
                    # Display the pending support requests in a table
                    st.dataframe(suppt_rqsts)
                    # Dropdown to select the request ID to assign a manager
                    suppt_rqst_id = st.selectbox("Select the Request ID:", suppt_rqsts['Request_ID'])
                    # Retrieve manager IDs from a specific department
                    cursor.execute("SELECT Manager_ID from Manager WHERE Department_ID='D002'")
                    mngr_ids = cursor.fetchall()
                    mngr_ids = [m[0] for m in mngr_ids]
                    suppt_mngr_id = st.selectbox("Select the Manager ID:", mngr_ids)
                    # Button to assign the selected manager to the support request
                    if st.button("Assign Manager"):
                        cursor.execute("UPDATE Customer_Support_Requests SET Assigned_Manager_ID=%s WHERE Request_ID=%s", (suppt_mngr_id, suppt_rqst_id))
                        cms_db.commit()
                        popup("Assigned the Support Manager Successfully!")
                        st.rerun()

            # Handling the "View & Respond to Customer Feedback" feature
            elif selected_feat == "View & Respond to Customer Feedback":
                st.markdown("#### Customer Feedbacks")
                feedbacks = pd.read_sql("SELECT * FROM Customer_Feedback ORDER BY Feedback_Date DESC", cms_db)
                # Check if there are no feedbacks to display, otherwise display the feedbacks
                if feedbacks.empty:
                    st.warning("No Feedbacks to display!")
                else:
                    st.dataframe(feedbacks)
                fdbk_id = st.text_input("Enter the Feedback ID to provide a response:")
                fdbk_rspns = st.text_area("Enter the response here:")
                # Button to submit the response to the feedback
                if st.button("Submit Response"):
                    cursor.execute("UPDATE Customer_Feedback SET CRM_Response=%s WHERE Feedback_ID=%s", (fdbk_rspns, fdbk_id))
                    cms_db.commit()
                    popup("Feedback Response submitted successfully!")
                    # Refresh the app to reflect changes
                    st.rerun()
            
            # Handling the "Manage Loyalty Program" feature
            elif selected_feat == "Manage Loyalty Program":
                st.markdown("Customer Loyalty Points Overview")
                lylt_data = pd.read_sql("SELECT * FROM Loyalty_Program", cms_db)
                if lylt_data.empty:
                    st.warning("No data to display!")
                else:
                    st.dataframe(lylt_data)
                st.markdown("Provide Loyalty Points to Customers")
                lylt_cust_id = st.text_input("Enter the Customer ID")
                lylt_cust_pnts = st.number_input("Enter the Points to add")
                # Button to submit the points to the loyalty program for the customer
                if st.button("Submit"):
                    cursor.execute("UPDATE Loyalty_Program SET Points_Earned=Points_Earned+%s WHERE Customer_ID=%s", (lylt_cust_pnts, lylt_cust_id))
                    cms_db.commit()
                    popup("Points Addedd Successfully!")
                    st.rerun()

            # Sidebar section for logout button and separation
            with st.sidebar:
                st.markdown("<br>" * 1, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True

        # ---------------------------------- Customer Support Manager --------------------------------------- #
        
        # Check if the selected option is "Support Manager"
        elif st.session_state['choice'] == "Support Manager":
            with st.sidebar:
                selected_feat = option_menu("Support Manager", ["View & Update Support Requests", "Generate Support Reports", 
                                                         "View Customer Purchases"],
                                    menu_icon="cast")

            # If the user selects "View & Update Support Requests" display all open support requests assigned to the logged-in manager
            if selected_feat == "View & Update Support Requests":
                st.markdown("#### All Open Support Requests")
                suppt_data = pd.read_sql(f"""SELECT * FROM Customer_Support_Requests WHERE Assigned_Manager_ID='{st.session_state['uid']}' AND 
                                             Request_Status != 'Closed' AND Request_Status != 'Cancelled'""", cms_db)
                if suppt_data.empty:
                    st.warning("No Data to Display!")
                else:
                    st.dataframe(suppt_data)
                    st.markdown("#### Update Support Requests")
                    updt_suppt_rqst_id = st.text_input("Enter the Request ID:")
                    updt_suppt_rqst_status = st.selectbox("Select the status", ["Open", "In Progress", "Pending", "Closed", "Cancelled"])
                    # Update the status of the selected request when the "Submit" button is clicked
                    if st.button("Submit"):
                        cursor.execute("UPDATE Customer_Support_Requests SET Request_Status=%s WHERE Request_ID=%s", (updt_suppt_rqst_status, updt_suppt_rqst_id))
                        cms_db.commit()
                        popup("Support Request status updated successfully!")
                        st.rerun()

            # If the user selects "Generate Support Reports" display section to generate reports based on date range
            elif selected_feat == "Generate Support Reports":
                st.markdown("#### Generate Support Reports")
                st.markdown("#### Date-wise Report:")
                suppt_rqst_rpt_sdate = st.date_input("Select the Start Date:")
                suppt_rqst_rpt_edate = st.date_input("Select the End Date:")
                suppt_rqst_rpt_date = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Request_Date BETWEEN '{suppt_rqst_rpt_sdate}' AND '{suppt_rqst_rpt_edate}'", cms_db)
                if st.button("Generate Report - Date"):
                    if suppt_rqst_rpt_date.empty:
                        st.warning("No data available for the given date range!")
                    else:
                        st.dataframe(suppt_rqst_rpt_date)
                # Section to generate reports based on manager ID
                st.markdown("#### Manager-wise Report:")
                suppt_rqst_rpt_mngr_id = st.text_input("Enter the Manager ID:")
                suppt_rqst_rpt_mngr = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Assigned_Manager_ID='{suppt_rqst_rpt_mngr_id}'", cms_db)
                if st.button("Generate Report - Manager"):
                    if suppt_rqst_rpt_mngr.empty:
                        st.warning("No data available for the given Manager ID")
                    else:
                        st.dataframe(suppt_rqst_rpt_mngr)
                # Section to generate reports based on product ID
                st.markdown("#### Product-wise Report:")
                suppt_rqst_rpt_prdt_id = st.text_input("Enter the Product ID:")
                suppt_rqst_rpt_prdt = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Product_ID='{suppt_rqst_rpt_prdt_id}'", cms_db)
                if st.button("Generate Report - Product"):
                    if suppt_rqst_rpt_prdt.empty:
                        st.warning("No data available for the given Product ID")
                    else:
                        st.dataframe(suppt_rqst_rpt_prdt)

            # If the user selects "View Customer Purchases" display the customer purchase data
            elif selected_feat == "View Customer Purchases":
                st.markdown("#### Customer Purchase Data")
                cust_prchs_data = pd.read_sql("SELECT * FROM Purchases", cms_db)
                if cust_prchs_data.empty:
                    st.warning("No Data found!")
                else:
                    st.dataframe(cust_prchs_data)
                # Section to view year-wise purchase data
                st.markdown("#### View Year-wise Data")
                cust_prchs_yr = st.number_input("Enter the desired Year:", min_value=1980, max_value=datetime.date(datetime.today()).year, value=2024)
                cust_prchs_data = pd.read_sql(f"SELECT * FROM Purchases WHERE YEAR(Purchase_Date)={cust_prchs_yr}", cms_db)
                if st.button("Get The Report"):
                    if cust_prchs_data.empty:
                        st.warning("No data found!")
                    else:
                        st.dataframe(cust_prchs_data)

            # Sidebar section to log out
            with st.sidebar:
                st.markdown("<br>" * 10, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True
        
        # ---------------------------------- Sales Manager -------------------------------------------------- #
        
        # Check if the selected option is "Sales Manager"
        elif st.session_state['choice'] == "Sales Manager":
            with st.sidebar:
                selected_feat = option_menu("Sales Manager", ["Upload Sales Data", "Generate Sales Report", "View Product Feedback"],
                                    menu_icon="cast")

            # If the user selects "Upload Sales Data", display the sales data
            if selected_feat == "Upload Sales Data":
                st.markdown("#### Upload Sales Data")
                sales_data = st.file_uploader("Please upload the Sales data file in CSV format:")
                if sales_data is not None:
                    sales_data = pd.read_csv(sales_data)
                    st.dataframe(sales_data)
            
                # Insert the uploaded data into the database
                if st.button("Upload"):
                    for index, row in sales_data.iterrows():
                        cursor.execute("INSERT INTO Purchases VALUES (%s,%s,%s,%s,%s,%s)", tuple(row))
                        cms_db.commit()
                    st.success("Data uploaded successfully!")

            # If the user selects "Generate Sales Report", display the data
            if selected_feat == "Generate Sales Report":
                st.markdown("#### Generate Sales Report")
                cust_prchs_data = pd.read_sql("SELECT * FROM Purchases", cms_db)
                if cust_prchs_data.empty:
                    st.warning("No Data found!")
                else:
                    st.dataframe(cust_prchs_data)
                # Section to view year-wise sales data
                st.markdown("#### View Year-wise Data")
                cust_prchs_yr = st.number_input("Enter the desired Year:", min_value=1980, max_value=datetime.date(datetime.today()).year, value=2024)
                cust_prchs_data = pd.read_sql(f"SELECT * FROM Purchases WHERE YEAR(Purchase_Date)={cust_prchs_yr}", cms_db)
                if st.button("Get The Report"):
                    if cust_prchs_data.empty:
                        st.warning("No data found!")
                    else:
                        st.dataframe(cust_prchs_data)

            # If the user selects "View Product Feedback", display the feedback data
            if selected_feat == "View Product Feedback":
                st.markdown("#### View Product Feedbacks")
                prdt_fdbk = pd.read_sql("""SELECT PD.Product_ID, PD.Product_Name, PD.Price, PD.Category, CF.Feedback_Date, CF.Rating, CF.Feedback 
                                        FROM Customer_Feedback CF JOIN Products PD ON CF.Product_ID=PD.Product_ID WHERE CF.Product_ID IS NOT NULL""", cms_db)
                if prdt_fdbk.empty:
                    st.warning("No Data Found!")
                else:
                    st.dataframe(prdt_fdbk)
            
            # Sidebar section to log out
            with st.sidebar:
                    st.markdown("<br>" * 12, unsafe_allow_html=True)
                    st.sidebar.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button("Logout"):
                            st.session_state['popup'] = True
                            
        # ---------------------------------- Product Manager ------------------------------------------------ #

        # Check if the selected menu option is "Product Manager"
        elif st.session_state['choice'] == "Product Manager":
            # Sidebar menu for the Product Manager section
            with st.sidebar:
                selected_feat = option_menu("Product Manager", ["View All Products", "Add New Products", "Update Products", "Delete Products", 
                                                         "Update Product Categories", "View Product Feedback"],
                                    menu_icon="cast")
            
            # Handle "View All Products" functionality
            if selected_feat == "View All Products":
                st.markdown("#### View All Products")
                # Fetch all product details from the Products table
                prdt_dtls = pd.read_sql("SELECT * FROM Products", cms_db)
                if prdt_dtls.empty:
                    st.warning("No data to display!")
                else:
                    # Display the products data in a table
                    st.dataframe(prdt_dtls)

            # Handle "Add New Products" functionality
            elif selected_feat == "Add New Products":
                st.markdown("#### Add New Products")
                cursor.execute("SELECT Product_ID FROM Products ORDER BY Product_ID DESC LIMIT 1")
                Product_ID = int(cursor.fetchone()[0][3:])
                Product_ID = f'PRD{Product_ID+1:03}'
                Product_Name = st.text_input("Enter Product Name:")
                Price = st.number_input("Enter the Price:")
                Category = st.text_input("Enter the Category:")
                # Add new product on button click
                if st.button("Add Product"):
                    cursor.execute("INSERT INTO Products VALUES (%s,%s,%s,%s)", (Product_ID,Product_Name,Price, Category))
                    cms_db.commit()
                    st.success("Product added successfully!")
            
            # Handle "Update Products" functionality
            elif selected_feat == "Update Products":
                st.markdown("#### Update Products")
                Product_ID = st.text_input("Enter the Product ID:")
                # Fetch product details from the database if the user clicks the "Fetch Details" button
                if st.button("Fetch Details"):
                    cursor.execute("SELECT * FROM Products WHERE Product_ID=%s", (Product_ID,))
                    prdt_dtls = cursor.fetchone()
                    if prdt_dtls:
                        # Store fetched details in session state
                        st.session_state['prdt_id'] = prdt_dtls[0]
                        st.session_state['prdt_name'] = prdt_dtls[1]
                        st.session_state['prdt_price'] = prdt_dtls[2]
                        st.session_state['prdt_category'] = prdt_dtls[3]
                    else:
                        st.error("No details found for the given Product ID!")
                # Display fields with the fetched product details for the user to update
                if 'prdt_id' in st.session_state:
                        st.session_state['prdt_name'] = st.text_input("Product Name:", value=st.session_state['prdt_name'])
                        st.session_state['prdt_price'] = st.number_input("Price:", value=st.session_state['prdt_price'])
                        st.session_state['prdt_category'] = st.text_input("Category:", value=st.session_state['prdt_category'])
                # Update product details in the database
                if st.button("Update Product Details"):
                    if 'prdt_id' not in st.session_state:
                        st.error("No details to update!")
                    else:
                        cursor.execute("UPDATE Products SET Product_Name=%s, Price=%s, Category=%s WHERE Product_ID=%s", 
                                    (st.session_state['prdt_name'],st.session_state['prdt_price'],st.session_state['prdt_category'], st.session_state['prdt_id']))
                        cms_db.commit()
                        popup("Product details updated successfully!")
                        st.session_state.pop('prdt_id', None)
                        st.rerun()
            
            # Handle "Delete Products" functionality
            elif selected_feat == "Delete Products":
                st.markdown("#### Delete Products")
                dlt_prdt_id = st.text_input("Enter the Product ID")
                # Delete the product on button click
                if st.button("Delete Product"):
                    cursor.execute("DELETE FROM Products WHERE Product_ID=%s", (dlt_prdt_id,))
                    cms_db.commit()
                    if cursor.rowcount > 0:
                        st.success("Product Deleted Successfully!")
                    else:
                        st.error("Incorrect Product ID!")
            
            # Handle "Update Product Categories" functionality
            elif selected_feat == "Update Product Categories":
                st.markdown("##### Update Product Category")
                # Fetch distinct categories from the 'Products' table
                cursor.execute("SELECT DISTINCT Category FROM Products")
                updt_ctgrs = cursor.fetchall()
                updt_ctgrs = [ct[0] for ct in updt_ctgrs]
                updt_ctgry = st.selectbox("Select the Category to update:", updt_ctgrs)
                updt_ctgry_nw = st.text_input("Enter the New Category name:")
                # Update the category on button click
                if st.button("Update Category"):
                    if updt_ctgry_nw:
                        cursor.execute("UPDATE Products SET Category=%s WHERE Category=%s", (updt_ctgry_nw, updt_ctgry))
                        cms_db.commit()
                        if cursor.rowcount > 0:
                            popup("Category Name updated successfully!")
                            st.rerun()
                    else:
                        st.warning("Provide a valid Category Name!")

            # Handle "View Product Feedback" functionality
            elif selected_feat == "View Product Feedback":
                st.markdown("#### View Product Feedback")
                feedbacks = pd.read_sql("SELECT * FROM Customer_Feedback ORDER BY Feedback_Date DESC", cms_db)
                if feedbacks.empty:
                    st.warning("No Feedbacks to display!")
                else:
                    st.dataframe(feedbacks)

            # Sidebar: Logout button with centered alignment
            with st.sidebar:
                    st.markdown("<br>" * 7, unsafe_allow_html=True)
                    st.sidebar.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button("Logout"):
                            st.session_state['popup'] = True
                            
        # ---------------------------------------------------------------------------------------------- #

# Handle the logout action and reset session variables
if st.session_state['popup']:
    st.session_state['login'] = False
    st.session_state['choice'] = None
    st.session_state['uid'] = None
    popup("You have been logged out!")
    st.rerun()

# Handle the logout action and reset session variables
cms_db.close()
cursor.close()

