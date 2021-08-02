DROP TABLE IF EXISTS vendor;
DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS business_payments;
DROP TABLE IF EXISTS accounts_payable;
DROP TABLE IF EXISTS business_purchase;
DROP TABLE IF EXISTS shipment;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS customer_purchase;

/*Holds vendor information and what they sell*/
CREATE TABLE vendor(
     vendor_id INTEGER NOT NULL,
     vendor_name VARCHAR(100) NOT NULL,
     product_name VARCHAR(100) NOT NULL,
     product_id VARCHAR(8) NOT NULL,
     wholesale_price DECIMAL (7,2) NOT NULL,
     PRIMARY KEY(vendor_id)
);

/*Holds all account information for the business and vendors */
-- The accounts with a null vendor_id are your own accounts --
CREATE TABLE account(
     account_number VARCHAR(20) NOT NULL,
     account_owner VARCHAR(100) NOT NULL,
     vendor_id INTEGER,
     balance DECIMAL (9,2) NOT NULL,
     PRIMARY KEY(account_number)
);

/* Holds business purchases, who, what, when, where
quantity, price, and shipment id */
-- this table has 3 primary keys because it allows:
-- multiple products to be purchased from one vendor on same acc_payable_id
-- products bought at the same time might come in multiple shipments
/* Creates/Updates an accounts payable record via trigger */
CREATE TABLE business_purchase(
     acc_payable_id INTEGER NOT NULL,
     vendor_id INTEGER NOT NULL,
     date_time DATETIME NOT NULL,
     shipment_id INTEGER NOT NULL,
     product_id VARCHAR(8) NOT NULL,
     quantity INTEGER NOT NULL,
     wholesale_price DECIMAL (7,2) NOT NULL,
     PRIMARY KEY(acc_payable_id, shipment_id, product_id)
);

/*This table is updated from the business_purchases relation,
it holds a running balance for each unique acc_payable_id 
from the business_purchase table, including when accounts_payable item is due */
CREATE TABLE accounts_payable(
     acc_payable_id INTEGER NOT NULL,
     amount_paid DECIMAL (9,2) NOT NULL,
     amount_pending DECIMAL (9,2) NOT NULL,
     pay_due_date DATE,
     PRIMARY KEY(acc_payable_id),
     FOREIGN KEY(acc_payable_id) REFERENCES business_purchase(acc_payable_id)
);

/*This holds information about single payments made on acccounts_payable records,
this way one can make multiple small payments on a single accounts_payable item
until it is paid off, also updates accounts and accounts_payable via trigger */
CREATE TABLE business_payments(
     acc_payable_id INTEGER NOT NULL,
     trans_id INTEGER AUTO_INCREMENT NOT NULL,
     date_time DATETIME NOT NULL,
     transfer_amount DECIMAL (9,2) NOT NULL,
     from_account_number VARCHAR(20) NOT NULL,
     account_number VARCHAR(20) NOT NULL,
     PRIMARY KEY(trans_id),
     FOREIGN KEY (acc_payable_id) REFERENCES accounts_payable(acc_payable_id)
);


/*This table holds shipment information and updates
the inventory relation via a trigger when a shipment arrives*/
CREATE TABLE shipment(
     shipment_id INTEGER NOT NULL,
     date_shipped DATE,
     date_est_arrival DATE,
     date_arrived DATE,
     PRIMARY KEY (shipment_id)
);

/*Holds all possible product types, and how much is in stock */
-- NEW products must be placed in inventory first
-- with a quantity of 0 before they can be purchased from a vendor
CREATE TABLE inventory(
     product_id VARCHAR(8) NOT NULL,
     product_name VARCHAR(32) NOT NULL,
     quantity INTEGER NOT NULL,
     retail_price DECIMAL (7,2) NOT NULL,
     PRIMARY KEY(product_id)
);

/*Holds basic customer information */
CREATE TABLE customer(
     customer_id INTEGER NOT NULL,
     customer_name VARCHAR(32),
     PRIMARY KEY(customer_id)
);

/*holds all information for a customer purchase,
who, what , price, quantity and the account the paid
money will be deposited into */
-- updates inventory and account balances via triggers
CREATE TABLE customer_purchase(
     purchase_id INTEGER AUTO_INCREMENT NOT NULL,
     customer_id INTEGER NOT NULL,
     product_id VARCHAR(8) NOT NULL,
     retail_price DECIMAL (7,2) NOT NULL,
     quantity INTEGER NOT NULL,
     total DECIMAL (7,2) NOT NULL,
     payment_method VARCHAR(20) NOT NULL,
     account_number VARCHAR(20) NOT NULL,
     date_time DATETIME NOT NULL,
     PRIMARY KEY(purchase_id, product_id)
);
     
     