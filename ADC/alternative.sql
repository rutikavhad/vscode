-- --- display all orders with customer details and item price 
-- --1st way JOIN
-- select distinct c.fname from customer c
-- join orderinfo oi on c.customer_id = oi.customer_id 
-- join orderline ol on oi.orderinfo_id = ol.orderinfo_id 
-- join item i on ol.item_id = i.item_id where i.cost_price>10;

-- --2nd way AND
 select distinct c.fname from customer c,item i,orderline oi, orderinfo of   where  c.customer_id=of.customer_id and i.item_id=oi.item_id and of.orderinfo_id=oi.orderinfo_id and i.cost_price>10;

--customer_id in customer_id
--3rd way IN
 select distinct fname from customer where customer_id in
(select customer_id from orderinfo where orderinfo_id in
(select orderinfo_id from orderline where item_id in 
( select item_id from item where cost_price>10)));


-- -- set enable_hashjoin to off/on#

-- --\i file.sql
-- -- explain select * from X;

-- --vacuum X;  -- delete unwanted data garbage values

-- -- qurys palan

-- -- set enable_seqscan to off/on

-- --set enable_indexscan to off/on

-- --set enable_bitmapscan to off/on

-- --

-- First name of customers who ordered items priced over 10


--1st way
SELECT DISTINCT c.fname 
FROM customer c
JOIN orderinfo oi ON c.customer_id = oi.customer_id
JOIN orderline ol ON oi.orderinfo_id = ol.orderinfo_id
JOIN item i ON ol.item_id = i.item_id 
WHERE i.cost_price > 10;

--2nd
SELECT DISTINCT c.fname 
FROM customer c, item i, orderline ol, orderinfo oi
WHERE c.customer_id = oi.customer_id 
AND oi.orderinfo_id = ol.orderinfo_id 
AND ol.item_id = i.item_id 
AND i.cost_price > 10;

--First name of custoers who orders the item Wood Puzzle

--1st
SELECT DISTINCT c.fname 
FROM customer c
JOIN orderinfo oi ON c.customer_id = oi.customer_id
JOIN orderline ol ON oi.orderinfo_id = ol.orderinfo_id
JOIN item i ON ol.item_id = i.item_id
WHERE i.description = 'Wood Puzzle';

--2nd

SELECT fname 
FROM customer 
WHERE customer_id IN (
    SELECT customer_id 
    FROM orderinfo 
    WHERE orderinfo_id IN (
        SELECT orderinfo_id 
        FROM orderline 
        WHERE item_id IN (
            SELECT item_id 
            FROM item 
            WHERE description = 'Wood Puzzle'
        )
    )
);

--Get customer name and item description for orders with cost >10
--1st

SELECT DISTINCT c.fname, c.lname, i.description, i.cost_price 
FROM customer c
JOIN orderinfo oi ON c.customer_id = oi.customer_id
JOIN orderline ol ON oi.orderinfo_id = ol.orderinfo_id
JOIN item i ON ol.item_id = i.item_id
WHERE i.cost_price > 10;

--2nd
SELECT DISTINCT c.fname, c.lname, i.description, i.cost_price 
FROM customer c, orderinfo oi, orderline ol, item i
WHERE c.customer_id = oi.customer_id 
AND oi.orderinfo_id = ol.orderinfo_id 
AND ol.item_id = i.item_id 
AND i.cost_price > 10;

--Get customers name phone and items they bought with quantity is > 1
--1st

SELECT c.fname, c.lname, c.phone, i.description, ol.quantity 
FROM customer c
JOIN orderinfo oi ON c.customer_id = oi.customer_id
JOIN orderline ol ON oi.orderinfo_id = ol.orderinfo_id
JOIN item i ON ol.item_id = i.item_id
WHERE ol.quantity > 1;

--2nd

SELECT fname, lname, phone 
FROM customer 
WHERE customer_id IN (
  SELECT customer_id 
  FROM orderinfo 
  WHERE orderinfo_id IN (
    SELECT orderinfo_id 
    FROM orderline 
    WHERE quantity > 1
  )
);


-- show custoers item and barcodes of purhesed items
--1st
SELECT c.fname, c.lname, i.description, b.barcode_ean 
FROM customer c, orderinfo oi, orderline ol, item i, barcode b
WHERE c.customer_id = oi.customer_id 
AND oi.orderinfo_id = ol.orderinfo_id 
AND ol.item_id = i.item_id 
AND i.item_id = b.item_id;

--2nd
SELECT c.fname, c.lname, i.description, b.barcode_ean 
FROM customer c
JOIN orderinfo oi ON c.customer_id = oi.customer_id
JOIN orderline ol ON oi.orderinfo_id = ol.orderinfo_id
JOIN item i ON ol.item_id = i.item_id
JOIN barcode b ON i.item_id = b.item_id;

--Give details of customers from Bingham who placed orders

--1st
SELECT fname, lname, town
FROM customer 
WHERE town = 'Bingham' 
AND customer_id IN (
  SELECT customer_id FROM orderinfo
);

--2nd
SELECT DISTINCT c.fname, c.lname, c.town, oi.orderinfo_id, oi.date_placed
FROM customer c
JOIN orderinfo oi ON c.customer_id = oi.customer_id
WHERE c.town = 'Bingham';

--Give details of items never orders

--1st 
SELECT item_id, description 
FROM item 
WHERE item_id NOT IN (
  SELECT item_id FROM orderline
);

--2nd

SELECT i.item_id, i.description 
FROM item i
LEFT JOIN orderline ol ON i.item_id = ol.item_id
WHERE ol.item_id IS NULL;

--Give a details of customers who have more then one orders
--1st

SELECT c.customer_id, c.fname, c.lname, COUNT(*) as total_orders
FROM customer c
JOIN orderinfo oi ON c.customer_id = oi.customer_id
GROUP BY c.customer_id, c.fname, c.lname
HAVING COUNT(*) > 1;

--2nd
SELECT c.customer_id, c.fname, c.lname, COUNT(*) as total_orders
FROM customer c, orderinfo oi
WHERE c.customer_id = oi.customer_id
GROUP BY c.customer_id, c.fname, c.lname
HAVING COUNT(*) > 1;

--Orders plaaced before july 2000

--1st
SELECT oi.orderinfo_id, oi.date_placed, c.fname, c.lname 
FROM orderinfo oi
JOIN customer c ON c.customer_id = oi.customer_id
WHERE oi.date_placed < '2000-07-01';

--2nd

SELECT fname, lname 
FROM customer 
WHERE customer_id IN (
  SELECT customer_id 
  FROM orderinfo 
  WHERE date_placed < '2000-07-01'
);



--Give details of orders placed in june 2000

--1st
SELECT oi.orderinfo_id, c.fname
FROM orderinfo oi
JOIN customer c ON c.customer_id = oi.customer_id
WHERE oi.date_placed BETWEEN '2000-06-01' AND '2000-06-30';

--2nd

SELECT orderinfo_id
FROM orderinfo
WHERE date_placed BETWEEN '2000-06-01' AND '2000-06-30';
