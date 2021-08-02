DROP TRIGGER IF EXISTS b_purchase_insert_accounts_payable;
DROP TRIGGER IF EXISTS b_payments_insert_accounts_payable;
DROP TRIGGER IF EXISTS shipment_insert_inventory;
DROP TRIGGER IF EXISTS shipment_update_inventory;
DROP TRIGGER IF EXISTS c_purchase_update_inventory_account;


/*DELIMITER !
CREATE TRIGGER b_purchase_insert_shipment AFTER INSERT
ON business_purchase
FOR EACH ROW
BEGIN

INSERT INTO shipment VALUES(NEW.shipment_id,NULL,NULL,NULL);

END
DELIMITER ;*/

-- [TRIGGER 1]
/*This Trigger works after insertion on the business 
purchase relation and updates accounts_payable and the 
account relations*/

DELIMITER !
CREATE TRIGGER b_purchase_insert_accounts_payable AFTER INSERT
ON business_purchase
FOR EACH ROW
BEGIN

DECLARE old_acc_payable_id INTEGER DEFAULT NULL;
SET old_acc_payable_id = (SELECT acc_payable_id
                          FROM accounts_payable
                          WHERE acc_payable_id = NEW.acc_payable_id);
                          
/*UPDATES an accounts_payable ID in the accounts payable relation
 if it already exists ,otherwise, creates new record in accounts_payable */
 IF(NEW.acc_payable_id = old_acc_payable_id)
     THEN UPDATE accounts_payable
          SET amount_pending = amount_pending + NEW.wholesale_price*NEW.quantity
          WHERE acc_payable_id = NEW.acc_payable_id;
		/*NOTE - DEFAULT PAYMENT DUE DATE IS THE NEXT DAY IF NOT MANUALLY CHANGED */
     ELSE INSERT INTO accounts_payable 
          VALUES(NEW.acc_payable_id,0,NEW.wholesale_price*NEW.quantity,
		  DATE(NEW.date_time)+ INTERVAL 1 day);
END IF;

UPDATE account
SET balance = balance - (NEW.wholesale_price*NEW.quantity)
WHERE account.vendor_id = NEW.vendor_id;
      

END !
DELIMITER ;



-- [TRIGGER 2 ]
/*This Trigger updates after insertion on the business_payments 
relations  and updates acccounts_payable and account*/

DELIMITER !
CREATE TRIGGER b_payments_insert_accounts_payable AFTER INSERT
ON business_payments
FOR EACH ROW
BEGIN

-- updates accounts_payable to reflect lower amount_pending
UPDATE accounts_payable
SET amount_paid = amount_paid + NEW.transfer_amount,
     amount_pending = amount_pending - NEW.transfer_amount
WHERE accounts_payable.acc_payable_id = NEW.acc_payable_id;

-- updates the 'from_account' in the account relation
UPDATE account
SET balance = balance - NEW.transfer_amount
WHERE account.account_number = NEW.from_account_number;

-- updates the balance that is paid in the account relation
UPDATE account
SET balance = balance + NEW.transfer_amount
WHERE account.account_number = NEW.account_number;

END !
DELIMITER ;



-- [TRIGGERS 2 AND 3]
/*These triggers run on the Shipment Relation and updates inventory */
/* On insert */
DELIMITER !
CREATE TRIGGER shipment_insert_inventory AFTER INSERT
ON shipment
FOR EACH ROW
BEGIN

IF(DATEDIFF(CURDATE(),NEW.date_arrived) >= 0)
THEN UPDATE inventory
     SET quantity = quantity + (SELECT sum(quantity)
					  FROM business_purchase
                      WHERE NEW.shipment_id = business_purchase.shipment_id)
	 WHERE inventory.product_id = (SELECT product_id
                                   FROM business_purchase
                                   WHERE NEW.shipment_id = business_purchase.shipment_id);
END IF;
END !
DELIMITER ;
/* and then On update */
DELIMITER !
CREATE TRIGGER shipment_update_inventory AFTER UPDATE
ON shipment
FOR EACH ROW
BEGIN

IF(DATEDIFF(CURDATE(),NEW.date_arrived) >=0) THEN
     UPDATE inventory
     SET quantity = quantity +(SELECT sum(quantity)
					  FROM business_purchase
                      WHERE NEW.shipment_id = business_purchase.shipment_id)
	 WHERE inventory.product_id = (SELECT product_id
                                   FROM business_purchase
                                   WHERE NEW.shipment_id = business_purchase.shipment_id);
END IF;
END !
DELIMITER ;




-- [TRIGGER 4]
/*This trigger is on the customer_purchase relation and updates 
the inventory and account relations */

DELIMITER !
CREATE TRIGGER c_purchase_update_inventory_account AFTER INSERT
ON customer_purchase
FOR EACH ROW
BEGIN
	/*Subtracts what a customer purchased from the inventory */
     UPDATE inventory
     SET quantity = quantity - NEW.quantity
     WHERE inventory.product_id = NEW.product_id;
	
    /*Updates the balance of the account listed in the
    customer_purchase record */
     UPDATE account
     SET balance = balance + NEW.total
     WHERE account_number = NEW.account_number;
     
END !
DELIMITER ;
     


