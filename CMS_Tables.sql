CREATE DATABASE cms;
USE cms;

CREATE TABLE customer(
		Customer_ID VARCHAR(50),
		Customer_Name VARCHAR(255),
		Password VARCHAR(50),
		Contact_No VARCHAR(15),
		Email_ID VARCHAR(50),
		Address VARCHAR(255),
		Date_of_Birth DATE,
		Gender VARCHAR(20),
		Registration_Date DATE,
		Manager_ID VARCHAR(50),
		PRIMARY KEY(Customer_ID)
	);

INSERT INTO customer VALUES ('C001', 'Anitha', 'C001', 9123456789, 'anitha@cms.com', '123  ABC Street,  Cochin', '1985-07-15', 'Female', '2010-02-15', 'M001'),
							('C002', 'Ravi', 'C002', 7890123456, 'ravi@cms.com', '456  XYZ Avenue,  Bangalore', '1990-11-20', 'Male', '2012-06-30', 'M002'),
							('C003', 'Lakshmi', 'C003', 7012345678, 'lakshmi@cms.com', '789  DEF Road,  Chennai', '1992-01-10', 'Female', '2018-04-10', 'M003'),
							('C004', 'Rajesh', 'C004', 7012345679, 'rajesh@cms.com', '123  ABC Street,  Bangalore', '1990-05-15', 'Male', '2017-06-12', 'M001'),
							('C005', 'Sunita', 'C005', 7012345680, 'sunita@cms.com', '456  XYZ Lane,  Hyderabad', '1985-11-20', 'Female', '2019-08-25', 'M002'),
							('C006', 'Baiju', 'C006', 7012345680, 'baiju@cms.com', '567  TXM Lane,  Telengana', '1985-2-28', 'Male', '2016-08-25', 'M010'),
							('C007', 'Ravi', 'C007', 8934533253, 'ravi@cms.com', '4567  NY Lane,  New York', '1988-6-17', 'Male', '2020-08-25', 'M011'),
							('C008', 'Uthaman', 'C008', 7983445354, 'uthaman@cms.com', '234  ABC Lane,  Kerala', '1996-4-16', 'Male', '2020-08-25', 'M012'),
							('C009', 'Swati', 'C009', 7898723435, 'swati@cms.com', 'ABC  Trrn,  Haryana', '1991-6-15', 'Female', '2012-08-25', 'M015'),
							('C010', 'Jenil', 'C010', 9845445635, 'jenil@cms.com', '5623 Brooke St, Delaware', '1995-8-28', 'Male', '2012-08-25', 'M003');
SELECT * FROM customer;

CREATE TABLE Manager(
		Manager_ID VARCHAR(50),
        Password VARCHAR(50),
		Manager_Name VARCHAR(255),
		Contact_No VARCHAR(15),
		Email_ID VARCHAR(50),
		Department_ID VARCHAR(50),
        PRIMARY KEY(Manager_ID)
);

INSERT INTO manager VALUES ('M001', 'M001', 'John Smith', '9876543210', 'john.smith@cms.com', 'D001'),
						   ('M002', 'M002', 'Jane Doe', '8765432109', 'jane.doe@cms.com', 'D002'),
						   ('M003', 'M003', 'Michael Johnson', '7654321098', 'michael.j@cms.com', 'D003'),
						   ('M004', 'M004', 'Emily Davis', '6543210987', 'emily.davis@cms.com', 'D004'),
						   ('M005', 'M005', 'David Wilson', '5432109876', 'david.wilson@cms.com', 'D005'),
						   ('M006', 'M006', 'Laura Brown', '4321098765', 'laura.brown@cms.com', 'D006'),
						   ('M007', 'M007', 'James Anderson', '3210987654', 'james.anderson@cms.com', 'D007'),
						   ('M008', 'M008', 'Sophia Martin', '2109876543', 'sophia.martin@cms.com', 'D008'),
						   ('M009', 'M009', 'William Lee', '1098765432', 'william.lee@cms.com', 'D009'),
						   ('M010', 'M010', 'Olivia Clark', '0987654321', 'olivia.clark@cms.com', 'D010');
SELECT * FROM manager;

CREATE TABLE Department(
		Dept_ID VARCHAR(50),
		Dept_Name VARCHAR(255),
		Manager_ID VARCHAR(50),
        PRIMARY KEY(Dept_ID)
);

INSERT INTO department VALUES ('D001', 'Customer Relationship Management', 'M001'),
							  ('D002', 'Customer Support', 'M002'),
							  ('D003', 'Sales', 'M003'),
							  ('D004', 'Production', 'M004'),
							  ('D005', 'IT', 'M005'),
							  ('D006', 'Operations', 'M006'),
							  ('D007', 'Human Resource', 'M007'),
							  ('D008', 'Research and Development', 'M008'),
							  ('D009', 'Logistics', 'M009'),
							  ('D010', 'Legal', 'M010');
SELECT * FROM department;

CREATE TABLE Customer_Support_Requests(
		Request_ID VARCHAR(50),
		Customer_ID VARCHAR(50),
		Purchase_ID VARCHAR(50),
		Product_ID VARCHAR(50),
		Request_Date DATE,
		Request_Description VARCHAR(255),
		Request_Status VARCHAR(50),
		Assigned_Manager_ID VARCHAR(50),
        PRIMARY KEY(Request_ID)
);

INSERT INTO customer_support_requests VALUES ('R001', 'C001','P001',  'PRD001', '2024-01-15', 'Issue with login', 'Open', 'M001'),
											 ('R002', 'C002','P0011',  'PRD002', '2024-02-18', 'Billing discrepancy', 'Closed', 'M002'),
											 ('R003', 'C003','P0012',  'PRD003', '2024-03-22', 'Unable to reset password', 'Open', 'M003'),
											 ('R004', 'C004','P002',  'PRD002', '2024-04-05', 'Shipping delay', 'In Progress', 'M004'),
											 ('R005', 'C005','P003',  'PRD003', '2024-05-12', 'Request for refund', 'Closed', 'M005'),
											 ('R006', 'C006','P004',  'PRD004', '2024-06-08', 'Product not received', 'In Progress', 'M006'),
											 ('R007', 'C007','P005',  'PRD005', '2024-07-19', 'Technical issue with website', 'Open', 'M007'),
											 ('R008', 'C008','P006',  'PRD006', '2024-08-02', 'Request for product exchange', 'Closed', 'M008'),
											 ('R009', 'C009','P007',  'PRD007', '2024-09-14', 'Incorrect order received', 'In Progress', 'M009'),
											 ('R010', 'C010','P008',  'PRD008', '2024-10-01', 'Question about warranty', 'Open', 'M010');
SELECT * FROM customer_support_requests;

CREATE TABLE Purchases(
		Purchase_ID VARCHAR(50),
		Customer_ID VARCHAR(50),
		Product_ID VARCHAR(50),
		Purchase_Date DATE,
		Quantity INT,
		Total_Amount INT,
        PRIMARY KEY(Purchase_ID)
);

INSERT INTO purchases VALUES ('P001', 'C001', 'PRD001', '2024-01-10', 2, 200),
							 ('P0011', 'C001', 'PRD002', '2024-02-10', 4, 450),
							 ('P0012', 'C001', 'PRD003', '2024-01-18', 1, 128),
							 ('P002', 'C002', 'PRD002', '2024-01-15', 1, 150),
							 ('P003', 'C003', 'PRD003', '2024-02-05', 3, 450),
							 ('P004', 'C004', 'PRD004', '2024-02-12', 1, 100),
							 ('P005', 'C005', 'PRD005', '2024-03-01', 4, 600),
							 ('P006', 'C006', 'PRD006', '2024-03-10', 2, 300),
							 ('P007', 'C007', 'PRD007', '2024-04-02', 1, 120),
							 ('P008', 'C008', 'PRD008', '2024-04-15', 5, 750),
							 ('P009', 'C009', 'PRD009', '2024-05-07', 2, 400),
							 ('P010', 'C010', 'PRD010', '2024-05-20', 3, 500);
SELECT * FROM purchases;

CREATE TABLE Products(
		Product_ID VARCHAR(50),
		Product_Name VARCHAR(255),
		Price INT,
		Category VARCHAR(255),
        PRIMARY KEY(Product_ID)
);

INSERT INTO products VALUES ('PRD001', 'Wireless Mouse', 100, 'Electronics'),
							('PRD002', 'Bluetooth Headphones', 150, 'Electronics'),
							('PRD003', 'Laptop Stand', 120, 'Accessories'),
							('PRD004', 'Water Bottle', 50, 'Home & Kitchen'),
							('PRD005', 'Smartphone', 300, 'Electronics'),
							('PRD006', 'Desk Lamp', 80, 'Home & Kitchen'),
							('PRD007', 'USB Cable', 20, 'Accessories'),
							('PRD008', 'Backpack', 150, 'Accessories'),
							('PRD009', 'Yoga Mat', 200, 'Fitness'),
							('PRD010', 'Coffee Maker', 250, 'Home & Kitchen');
SELECT * FROM products;

CREATE TABLE Customer_Feedback(
		Feedback_ID VARCHAR(50),
		Customer_ID VARCHAR(50),
		Product_ID VARCHAR(50),
		Feedback_Date DATE,
		Rating INT,
		Comments VARCHAR(255),
        PRIMARY KEY(Feedback_ID)
);

INSERT INTO customer_feedback VALUES ('F001', 'C001', 'PRD001', '2024-01-12', 4, 'Great mouse, very responsive.'),
									 ('F002', 'C002', 'PRD002', '2024-01-18', 5, 'Excellent sound quality!'),
									 ('F003', 'C003', 'PRD003', '2024-02-07', 3, 'Sturdy but a bit expensive.'),
									 ('F004', 'C004', 'PRD004', '2024-02-14', 5, 'Keeps drinks cold for hours!'),
									 ('F005', 'C005', 'PRD005', '2024-03-03', 4, 'Very fast, but battery life could be better.'),
									 ('F006', 'C006', 'PRD006', '2024-03-12', 4, 'Good light for the price.'),
									 ('F007', 'C007', 'PRD007', '2024-04-04', 3, 'Works well, but could be longer.'),
									 ('F008', 'C008', 'PRD008', '2024-04-18', 5, 'Perfect size for travel.'),
									 ('F009', 'C009', 'PRD009', '2024-05-09', 4, 'Comfortable and durable mat.'),
									 ('F010', 'C010', 'PRD010', '2024-05-22', 5, 'Makes excellent coffee quickly.');
SELECT * FROM customer_feedback;

CREATE TABLE Loyalty_Program(
		Customer_ID VARCHAR(50),
		Points_Earned INT,
		Points_Redeemed INT,
		Last_Redeemed_Date DATE
);

INSERT INTO loyalty_program VALUES ('C001', 1200, 300, '2024-01-10'),
								   ('C002', 1500, 500, '2024-02-15'),
								   ('C003', 900, 200, '2024-03-05'),
								   ('C004', 1800, 600, '2024-03-22'),
								   ('C005', 2100, 700, '2024-04-12'),
								   ('C006', 1000, 100, '2024-04-25'),
								   ('C007', 800, 0, NULL),
								   ('C008', 2500, 1000, '2024-05-10'),
								   ('C009', 1100, 300, '2024-06-01'),
								   ('C010', 1700, 400, '2024-06-15');
SELECT * FROM loyalty_program;

