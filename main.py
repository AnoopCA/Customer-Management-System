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
        
        # ---------------------------------- Customer Management -------------------------------------------- #
        
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

        with st.sidebar:
                st.markdown("<br>" * 5, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True

# ---------------------------------------------------------------------------------------------- #

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

        st.session_state['uid'] = st.text_input("Enter User ID", value='M004')
        pwd = st.text_input("Enter Password", type="password", value='M004')
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

        # ---------------------------------- Customer Relationship Manager ---------------------------------- #
        
        if st.session_state['choice'] == "Customer Relationship Manager":
            with st.sidebar:
                selected_feat = option_menu("Customer Relationship Manager", ["View Customer Info", "Add New Customer", "Delete Customer", 
                                            "Update Customer Details", "View Customer Support Requests", "Assign Support Requests", 
                                            "View & Respond to Customer Feedback", "Manage Loyalty Program"],
                                    menu_icon="cast")
    
            if selected_feat == "View Customer Info":
                st.markdown("#### View Customer Info")
                cust_id = st.text_input("Enter the Customer ID to find the details:")
                if st.button("Fetch Customer Details"):
                    cust_data = pd.read_sql(f"SELECT * FROM customer WHERE Customer_ID='{cust_id}'", mydb)
                    if cust_data.empty:
                        st.warning("No details found for the given Customer ID. Please enter the correct Customer ID!")
                    else:
                        st.dataframe(cust_data)
            
            elif selected_feat == "Add New Customer":
                st.markdown("#### Add New Customer")
                st.write("Enter the Customer Details below")
                cursor.execute("SELECT Customer_ID FROM Customer ORDER BY Customer_ID DESC LIMIT 1")
                Customer_ID = int(cursor.fetchone()[0][1:])
                Customer_ID = f'C{Customer_ID+1:03}'
                Customer_Name = st.text_input("Customer Name:")
                Password = Customer_ID
                Contact_No = st.text_input("Contact Number:")
                Email_ID = st.text_input("Email ID:")
                Address = st.text_input("Address:")
                Date_of_Birth = st.date_input("Date Of Birth:")
                Gender = st.selectbox("Gender:", ["Male", "Female"])
                Registration_Date = datetime.date(datetime.today())
                Manager_ID = None
                if st.button("Submit"):
                    cursor.execute("INSERT INTO Customer VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                                (Customer_ID, Customer_Name, Password, Contact_No, Email_ID, Address, Date_of_Birth, Gender, Registration_Date, Manager_ID))
                    mydb.commit()
                    st.success(f"""Customer added successfully with the user ID -  "{Customer_ID}".
                                   The password is the User ID itself. User can change the password by using the option "Update Personal Info".""")
            
            elif selected_feat == "Delete Customer":
                dlt_cust_id = st.text_input("Enter the Customer ID to delete:")
                cursor.execute("SELECT Customer_Name FROM Customer WHERE Customer_ID=%s", (dlt_cust_id,))
                dlt_cust_name = cursor.fetchone()
                if st.button(f"Delete Customer Data"):
                    if dlt_cust_name:
                        cursor.execute("DELETE FROM Customer WHERE Customer_ID=%s", (dlt_cust_id,))
                        mydb.commit()
                        st.success("Customer data is deleted!")
                    else:
                        st.error("Customer details not found!")

            elif selected_feat == "Update Customer Details":
                st.markdown("#### Update Customer Details")
                updt_cust_id = st.text_input("Enter the Customer ID to update the details:")
                if st.button("Fetch Customer Details"):
                    cursor.execute("SELECT * FROM customer WHERE Customer_ID=%s",(updt_cust_id,))
                    cust_data = cursor.fetchone()
                    if cust_data:
                        st.session_state['cust_data'] = cust_data
                    elif updt_cust_id != "":
                            st.error("Customer ID is not found!")
                            st.session_state['cust_data'] = None
                if 'cust_data' in st.session_state:
                    if st.session_state['cust_data'] is not None:
                        Customer_Name = st.text_input("Name", value=st.session_state['cust_data'][1])
                        Password = st.text_input("Password", value=st.session_state['cust_data'][2])
                        Contact_No = st.text_input("Contact Number", value=st.session_state['cust_data'][3])
                        Email_ID = st.text_input("Email ID", value=st.session_state['cust_data'][4])
                        Address = st.text_input("Address", value=st.session_state['cust_data'][5])
                        Date_of_Birth = st.date_input("Date Of Birth", value=st.session_state['cust_data'][6])
                        Gender = st.selectbox("Gender", ["Male", "Female"], index = 0 if st.session_state['cust_data'][7]=="Male" else 1)
                        if st.button("Save Changes"):
                            if 'cust_data' in st.session_state:
                                if st.session_state['cust_data'] is not None:
                                    cursor.execute("""UPDATE customer SET Customer_Name=%s,Password=%s,Contact_No=%s,Email_ID=%s,Address=%s,Date_of_Birth=%s,Gender=%s
                                                    WHERE Customer_ID=%s""", (Customer_Name,Password,Contact_No,Email_ID,Address,Date_of_Birth,Gender,updt_cust_id))
                                    mydb.commit()
                                    st.success("Customer details updated successfully!")
                                    st.session_state.pop('cust_data', None)

            elif selected_feat == "View Customer Support Requests":
                st.markdown("#### View Customer Support Requests")
                suppt_cust_id = st.text_input("Enter the Customer ID:")
                if st.button("Fetch the Details"):
                    suppt_data = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Customer_ID='{suppt_cust_id}'", mydb)
                    if suppt_data.empty:
                        st.error("Support Requests not found for the given Customer ID!")
                    else:
                        st.dataframe(suppt_data)

            elif selected_feat == "Assign Support Requests":
                st.markdown("#### Assign Support Requests")
                st.markdown("##### All open Support Requests")
                suppt_rqsts = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Request_Status != 'Closed' AND Request_Status != 'Cancelled'", mydb)
                if suppt_rqsts.empty:
                    st.success("No pending Support Requests!")
                else:
                    st.dataframe(suppt_rqsts)
                    suppt_rqst_id = st.selectbox("Select the Request ID:", suppt_rqsts['Request_ID'])
                    cursor.execute("SELECT Manager_ID from Manager WHERE Department_ID='D002'")
                    mngr_ids = cursor.fetchall()
                    mngr_ids = [m[0] for m in mngr_ids]
                    suppt_mngr_id = st.selectbox("Select the Manager ID:", mngr_ids)
                    if st.button("Assign Manager"):
                        cursor.execute("UPDATE Customer_Support_Requests SET Assigned_Manager_ID=%s WHERE Request_ID=%s", (suppt_mngr_id, suppt_rqst_id))
                        mydb.commit()
                        popup("Assigned the Support Manager Successfully!")
                        st.rerun()

            elif selected_feat == "View & Respond to Customer Feedback":
                st.markdown("#### Customer Feedbacks")
                feedbacks = pd.read_sql("SELECT * FROM Customer_Feedback ORDER BY Feedback_Date DESC", mydb)
                if feedbacks.empty:
                    st.warning("No Feedbacks to display!")
                else:
                    st.dataframe(feedbacks)
                fdbk_id = st.text_input("Enter the Feedback ID to provide a response:")
                fdbk_rspns = st.text_area("Enter the response here:")
                if st.button("Submit Response"):
                    cursor.execute("UPDATE Customer_Feedback SET CRM_Response=%s WHERE Feedback_ID=%s", (fdbk_rspns, fdbk_id))
                    mydb.commit()
                    popup("Feedback Response submitted successfully!")
                    st.rerun()
            
            elif selected_feat == "Manage Loyalty Program":
                st.markdown("Customer Loyalty Points Overview")
                lylt_data = pd.read_sql("SELECT * FROM Loyalty_Program", mydb)
                if lylt_data.empty:
                    st.warning("No data to display!")
                else:
                    st.dataframe(lylt_data)
                st.markdown("Provide Loyalty Points to Customers")
                lylt_cust_id = st.text_input("Enter the Customer ID")
                lylt_cust_pnts = st.number_input("Enter the Points to add")
                if st.button("Submit"):
                    cursor.execute("UPDATE Loyalty_Program SET Points_Earned=Points_Earned+%s WHERE Customer_ID=%s", (lylt_cust_pnts, lylt_cust_id))
                    mydb.commit()
                    popup("Points Addedd Successfully!")
                    st.rerun()

            with st.sidebar:
                st.markdown("<br>" * 1, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True

        # ---------------------------------- Customer Support Manager --------------------------------------- #
            
        elif st.session_state['choice'] == "Support Manager":
            with st.sidebar:
                selected_feat = option_menu("Support Manager", ["View & Update Support Requests", "Generate Support Reports", 
                                                         "View Customer Purchases"],
                                    menu_icon="cast")

            if selected_feat == "View & Update Support Requests":
                st.markdown("#### All Open Support Requests")
                suppt_data = pd.read_sql(f"""SELECT * FROM Customer_Support_Requests WHERE Assigned_Manager_ID='{st.session_state['uid']}' AND 
                                             Request_Status != 'Closed' AND Request_Status != 'Cancelled'""", mydb)
                if suppt_data.empty:
                    st.warning("No Data to Display!")
                else:
                    st.dataframe(suppt_data)
                    st.markdown("#### Update Support Requests")
                    updt_suppt_rqst_id = st.text_input("Enter the Request ID:")
                    updt_suppt_rqst_status = st.selectbox("Select the status", ["Open", "In Progress", "Pending", "Closed", "Cancelled"])
                    if st.button("Submit"):
                        cursor.execute("UPDATE Customer_Support_Requests SET Request_Status=%s WHERE Request_ID=%s", (updt_suppt_rqst_status, updt_suppt_rqst_id))
                        mydb.commit()
                        popup("Support Request status updated successfully!")
                        st.rerun()

            elif selected_feat == "Generate Support Reports":
                st.markdown("#### Generate Support Reports")
                st.markdown("#### Date-wise Report:")
                suppt_rqst_rpt_sdate = st.date_input("Select the Start Date:")
                suppt_rqst_rpt_edate = st.date_input("Select the End Date:")
                suppt_rqst_rpt_date = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Request_Date BETWEEN '{suppt_rqst_rpt_sdate}' AND '{suppt_rqst_rpt_edate}'", mydb)
                if st.button("Generate Report - Date"):
                    if suppt_rqst_rpt_date.empty:
                        st.warning("No data available for the given date range!")
                    else:
                        st.dataframe(suppt_rqst_rpt_date)
                st.markdown("#### Manager-wise Report:")
                suppt_rqst_rpt_mngr_id = st.text_input("Enter the Manager ID:")
                suppt_rqst_rpt_mngr = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Assigned_Manager_ID='{suppt_rqst_rpt_mngr_id}'", mydb)
                if st.button("Generate Report - Manager"):
                    if suppt_rqst_rpt_mngr.empty:
                        st.warning("No data available for the given Manager ID")
                    else:
                        st.dataframe(suppt_rqst_rpt_mngr)
                st.markdown("#### Product-wise Report:")
                suppt_rqst_rpt_prdt_id = st.text_input("Enter the Product ID:")
                suppt_rqst_rpt_prdt = pd.read_sql(f"SELECT * FROM Customer_Support_Requests WHERE Product_ID='{suppt_rqst_rpt_prdt_id}'", mydb)
                if st.button("Generate Report - Product"):
                    if suppt_rqst_rpt_prdt.empty:
                        st.warning("No data available for the given Product ID")
                    else:
                        st.dataframe(suppt_rqst_rpt_prdt)

            elif selected_feat == "View Customer Purchases":
                st.markdown("#### Customer Purchase Data")
                cust_prchs_data = pd.read_sql("SELECT * FROM Purchases", mydb)
                if cust_prchs_data.empty:
                    st.warning("No Data found!")
                else:
                    st.dataframe(cust_prchs_data)
                st.markdown("#### View Year-wise Data")
                cust_prchs_yr = st.number_input("Enter the desired Year:", min_value=1980, max_value=datetime.date(datetime.today()).year, value=2024)
                cust_prchs_data = pd.read_sql(f"SELECT * FROM Purchases WHERE YEAR(Purchase_Date)={cust_prchs_yr}", mydb)
                if st.button("Get The Report"):
                    if cust_prchs_data.empty:
                        st.warning("No data found!")
                    else:
                        st.dataframe(cust_prchs_data)

            with st.sidebar:
                st.markdown("<br>" * 10, unsafe_allow_html=True)
                st.sidebar.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Logout"):
                        st.session_state['popup'] = True
        
        # ---------------------------------- Sales Manager -------------------------------------------------- #
                 
        elif st.session_state['choice'] == "Sales Manager":
            with st.sidebar:
                selected_feat = option_menu("Sales Manager", ["Upload Sales Data", "Generate Sales Report", "View Product Feedback"],
                                    menu_icon="cast")

            if selected_feat == "Upload Sales Data":
                st.markdown("#### Upload Sales Data")
                sales_data = st.file_uploader("Please upload the Sales data file in CSV format:")
                if sales_data is not None:
                    sales_data = pd.read_csv(sales_data)
                    st.dataframe(sales_data)
            
                if st.button("Upload"):
                    for index, row in sales_data.iterrows():
                        cursor.execute("INSERT INTO Purchases VALUES (%s,%s,%s,%s,%s,%s)", tuple(row))
                        mydb.commit()
                    st.success("Data uploaded successfully!")

            if selected_feat == "Generate Sales Report":
                st.markdown("#### Generate Sales Report")
                cust_prchs_data = pd.read_sql("SELECT * FROM Purchases", mydb)
                if cust_prchs_data.empty:
                    st.warning("No Data found!")
                else:
                    st.dataframe(cust_prchs_data)
                st.markdown("#### View Year-wise Data")
                cust_prchs_yr = st.number_input("Enter the desired Year:", min_value=1980, max_value=datetime.date(datetime.today()).year, value=2024)
                cust_prchs_data = pd.read_sql(f"SELECT * FROM Purchases WHERE YEAR(Purchase_Date)={cust_prchs_yr}", mydb)
                if st.button("Get The Report"):
                    if cust_prchs_data.empty:
                        st.warning("No data found!")
                    else:
                        st.dataframe(cust_prchs_data)

            if selected_feat == "View Product Feedback":
                st.markdown("#### View Product Feedbacks")
                prdt_fdbk = pd.read_sql("""SELECT PD.Product_ID, PD.Product_Name, PD.Price, PD.Category, CF.Feedback_Date, CF.Rating, CF.Feedback 
                                        FROM Customer_Feedback CF JOIN Products PD ON CF.Product_ID=PD.Product_ID WHERE CF.Product_ID IS NOT NULL""", mydb)
                if prdt_fdbk.empty:
                    st.warning("No Data Found!")
                else:
                    st.dataframe(prdt_fdbk)

            with st.sidebar:
                    st.markdown("<br>" * 12, unsafe_allow_html=True)
                    st.sidebar.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button("Logout"):
                            st.session_state['popup'] = True
                            
        # ---------------------------------- Product Manager ------------------------------------------------ #

        elif st.session_state['choice'] == "Product Manager":
            with st.sidebar:
                selected_feat = option_menu("Product Manager", ["View All Products", "Add New Products", "Update Products", "Delete Products", 
                                                         "Update Product Categories", "View Product Feedback"],
                                    menu_icon="cast")
            
            if selected_feat == "View All Products":
                st.markdown("#### View All Products")
                prdt_dtls = pd.read_sql("SELECT * FROM Products", mydb)
                if prdt_dtls.empty:
                    st.warning("No data to display!")
                else:
                    st.dataframe(prdt_dtls)

            elif selected_feat == "Add New Products":
                st.markdown("#### Add New Products")
                cursor.execute("SELECT Product_ID FROM Products ORDER BY Product_ID DESC LIMIT 1")
                Product_ID = int(cursor.fetchone()[0][3:])
                Product_ID = f'PRD{Product_ID+1:03}'
                Product_Name = st.text_input("Enter Product Name:")
                Price = st.number_input("Enter the Price:")
                Category = st.text_input("Enter the Category:")
                if st.button("Add Product"):
                    cursor.execute("INSERT INTO Products VALUES (%s,%s,%s,%s)", (Product_ID,Product_Name,Price, Category))
                    mydb.commit()
                    st.success("Product added successfully!")
            
            elif selected_feat == "Update Products":
                st.markdown("#### Update Products")
                Product_ID = st.text_input("Enter the Product ID:")
                if st.button("Fetch Details"):
                    cursor.execute("SELECT * FROM Products WHERE Product_ID=%s", (Product_ID,))
                    prdt_dtls = cursor.fetchone()
                    if prdt_dtls:
                        st.session_state['prdt_id'] = prdt_dtls[0]
                        st.session_state['prdt_name'] = prdt_dtls[1]
                        st.session_state['prdt_price'] = prdt_dtls[2]
                        st.session_state['prdt_category'] = prdt_dtls[3]
                    else:
                        st.error("No details found for the given Product ID!")
                if 'prdt_id' in st.session_state:
                        st.session_state['prdt_name'] = st.text_input("Product Name:", value=st.session_state['prdt_name'])
                        st.session_state['prdt_price'] = st.number_input("Price:", value=st.session_state['prdt_price'])
                        st.session_state['prdt_category'] = st.text_input("Category:", value=st.session_state['prdt_category'])
                if st.button("Update Product Details"):
                    if 'prdt_id' not in st.session_state:
                        st.error("No details to update!")
                    else:
                        cursor.execute("UPDATE Products SET Product_Name=%s, Price=%s, Category=%s WHERE Product_ID=%s", 
                                    (st.session_state['prdt_name'],st.session_state['prdt_price'],st.session_state['prdt_category'], st.session_state['prdt_id']))
                        mydb.commit()
                        popup("Product details updated successfully!")
                        st.session_state.pop('prdt_id', None)
                        st.rerun()
            
            elif selected_feat == "Delete Products":
                st.markdown("#### Delete Products")
                dlt_prdt_id = st.text_input("Enter the Product ID")
                if st.button("Delete Product"):
                    cursor.execute("DELETE FROM Products WHERE Product_ID=%s", (dlt_prdt_id,))
                    mydb.commit()
                    if cursor.rowcount > 0:
                        st.success("Product Deleted Successfully!")
                    else:
                        st.error("Incorrect Product ID!")
            
            elif selected_feat == "Update Product Categories":
                st.markdown("##### Update Product Category")
                cursor.execute("SELECT DISTINCT Category FROM Products")
                updt_ctgrs = cursor.fetchall()
                updt_ctgrs = [ct[0] for ct in updt_ctgrs]
                updt_ctgry = st.selectbox("Select the Category to update:", updt_ctgrs)
                updt_ctgry_nw = st.text_input("Enter the New Category name:")
                if st.button("Update Category"):
                    if updt_ctgry_nw:
                        cursor.execute("UPDATE Products SET Category=%s WHERE Category=%s", (updt_ctgry_nw, updt_ctgry))
                        mydb.commit()
                        if cursor.rowcount > 0:
                            popup("Category Name updated successfully!")
                            st.rerun()
                    else:
                        st.warning("Provide a valid Category Name!")

            elif selected_feat == "View Product Feedback":
                st.markdown("#### View Product Feedback")
                feedbacks = pd.read_sql("SELECT * FROM Customer_Feedback ORDER BY Feedback_Date DESC", mydb)
                if feedbacks.empty:
                    st.warning("No Feedbacks to display!")
                else:
                    st.dataframe(feedbacks)

            with st.sidebar:
                    st.markdown("<br>" * 7, unsafe_allow_html=True)
                    st.sidebar.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button("Logout"):
                            st.session_state['popup'] = True
                            
        # ---------------------------------------------------------------------------------------------- #

if st.session_state['popup']:
    st.session_state['login'] = False
    st.session_state['choice'] = None
    st.session_state['uid'] = None
    popup("You have been logged out!")
    st.rerun()

mydb.close()
cursor.close()
