--a script that creates a trigger that decreases the quantity
--of an item after adding a new order.
DROP TRIGGER IF EXISTS reduce_quantity;
DELIMINTER //
CREATE TRIGGER reduce_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.quantity
	WHERE name = NEW.item_id;
END;
//

DELIMITER ;
