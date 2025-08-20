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

