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
		Account_Manager_ID VARCHAR(50),
		PRIMARY KEY(Customer_ID)
	);

INSERT INTO customer VALUES('C100', 'Jobin', 'C100', 'jobin@cms.com', ');