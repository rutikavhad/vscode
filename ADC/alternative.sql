-- --- display all orders with customer details and item price 
-- --1st way join
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
select distinct c.fname 
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
join item i on ol.item_id = i.item_id 
where i.cost_price > 10;

--2nd
select distinct c.fname 
from customer c, item i, orderline ol, orderinfo oi
where c.customer_id = oi.customer_id 
AND oi.orderinfo_id = ol.orderinfo_id 
AND ol.item_id = i.item_id 
AND i.cost_price > 10;

--First name of custoers who orders the item Wood Puzzle

--1st
select distinct c.fname 
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
join item i on ol.item_id = i.item_id
where i.description = 'Wood Puzzle';

--2nd

select fname 
from customer 
where customer_id IN (
    select customer_id 
    from orderinfo 
    where orderinfo_id IN (
        select orderinfo_id 
        from orderline 
        where item_id IN (
            select item_id 
            from item 
            where description = 'Wood Puzzle'
        )
    )
);

--Get customer name and item description for orders with cost >10
--1st

select distinct c.fname, c.lname, i.description, i.cost_price 
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
join item i on ol.item_id = i.item_id
where i.cost_price > 10;

--2nd
select distinct c.fname, c.lname, i.description, i.cost_price 
from customer c, orderinfo oi, orderline ol, item i
where c.customer_id = oi.customer_id 
AND oi.orderinfo_id = ol.orderinfo_id 
AND ol.item_id = i.item_id 
AND i.cost_price > 10;

--Get customers name phone and items they bought with quantity is > 1
--1st

select c.fname, c.lname, c.phone, i.description, ol.quantity 
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
join item i on ol.item_id = i.item_id
where ol.quantity > 1;

--2nd

select fname, lname, phone 
from customer 
where customer_id IN (
  select customer_id 
  from orderinfo 
  where orderinfo_id IN (
    select orderinfo_id 
    from orderline 
    where quantity > 1
  )
);


-- show custoers item and barcodes of purhesed items
--1st
select c.fname, c.lname, i.description, b.barcode_ean 
from customer c, orderinfo oi, orderline ol, item i, barcode b
where c.customer_id = oi.customer_id 
AND oi.orderinfo_id = ol.orderinfo_id 
AND ol.item_id = i.item_id 
AND i.item_id = b.item_id;

--2nd
select c.fname, c.lname, i.description, b.barcode_ean 
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
join item i on ol.item_id = i.item_id
join barcode b on i.item_id = b.item_id;

--Give details of customers from Bingham who placed orders

--1st
select fname, lname, town
from customer 
where town = 'Bingham' 
AND customer_id IN (
  select customer_id from orderinfo
);

--2nd
select distinct c.fname, c.lname, c.town, oi.orderinfo_id, oi.date_placed
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
where c.town = 'Bingham';

--Give details of items never orders

--1st 
select item_id, description 
from item 
where item_id NOT IN (
  select item_id from orderline
);

--2nd

select i.item_id, i.description 
from item i
LEFT join orderline ol on i.item_id = ol.item_id
where ol.item_id IS NULL;

--Give a details of customers who have more then one orders
--1st

select c.customer_id, c.fname, c.lname, COUNT(*) as total_orders
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
GROUP BY c.customer_id, c.fname, c.lname
HAVING COUNT(*) > 1;

--2nd
select c.customer_id, c.fname, c.lname, COUNT(*) as total_orders
from customer c, orderinfo oi
where c.customer_id = oi.customer_id
GROUP BY c.customer_id, c.fname, c.lname
HAVING COUNT(*) > 1;

--Orders plaaced before july 2000

--1st
select oi.orderinfo_id, oi.date_placed, c.fname, c.lname 
from orderinfo oi
join customer c on c.customer_id = oi.customer_id
where oi.date_placed < '2000-07-01';

--2nd

select fname, lname 
from customer 
where customer_id IN (
  select customer_id 
  from orderinfo 
  where date_placed < '2000-07-01'
);



--Give details of orders placed in june 2000

--1st
select oi.orderinfo_id, c.fname
from orderinfo oi
join customer c on c.customer_id = oi.customer_id
where oi.date_placed BETWEEN '2000-06-01' AND '2000-06-30';

--2nd

select orderinfo_id
from orderinfo
where date_placed BETWEEN '2000-06-01' AND '2000-06-30';
