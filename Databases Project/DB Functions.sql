-- A function that takes 2 dates and returns a profit or net loss between those dates
-- This function is dependent on a view which takes the revenue made from each unique ID.
CREATE VIEW business_expenses AS
SELECT (wholesale_price * quantity) AS expenses, date_time
FROM business_purchase
GROUP BY acc_payable_id;

DELIMITER $$
CREATE FUNCTION net_profit(date1 DATETIME, date2 DATETIME)
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
	DECLARE profit DECIMAL(15,2);
	SELECT SUM(total) INTO @income FROM customer_purchase
    	WHERE date_time BETWEEN date1 AND date2;
    
   
	SELECT SUM(expenses) INTO @expenses
	FROM business_revenue
    	WHERE date_time BETWEEN date1 AND date2;
    
    SET profit = @income - @expenses; 
    RETURN profit;
END $$
DELIMITER ;


-- A function that takes 2 dates and shows all payments to a vendor between those dates
DELIMITER $$
CREATE PROCEDURE payments_to_vendor(date1 DATETIME, date2 DATETIME)
BEGIN
    SELECT vendor_name, date_time, product_id, wholesale_price
    FROM vendor v 
    NATURAL JOIN business_purchase b
    WHERE v.vendor_id = b.vendor_id
    AND v.date_time BETWEEN date1 AND date2
    AND b.date_time BETWEEN date1 AND date2
    GROUP BY vendor_name;
END $$
DELIMITER ;

-- A function that takes 2 dates and shows all customer transactions between those dates
DELIMITER $$
CREATE PROCEDURE show_customer_transactions(date1 DATETIME, date2 DATETIME)
BEGIN
    SELECT * FROM customer_purchase 
    WHERE date_time BETWEEN date1 AND date2;
END $$
DELIMITER ;

-- A function that shows all overdue accounts
/* In the generated data there are no overdue accounts they will need to be created */
SELECT * FROM accounts_payable
WHERE NOW() > pay_due_date;


-- A function that shows which vendor has late shipments
/* In the generated data there are no overdue shipments they will need to be created */
SELECT vendor_id, vendor_name
FROM vendor
NATURAL JOIN business_purchase b
NATURAL JOIN shipments s
WHERE b.shipment_id = s.shipment_id 
AND date_arrived > date_est_arrival
OR NOW() > date_est_arrival;

/* To add business_purchase data enter new records in this order */
-- 1st: add record to business_purchase
-- Then add/modify records to shipment, business_payments, or accounts_payable
