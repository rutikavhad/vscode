--1:Show all orders with customers name and order date
select oi.orderinfo_id, c.fname, c.lname, oi.date_placed
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
join orderline ol on oi.orderinfo_id = ol.orderinfo_id;


--2:List item ordered by each customer

select c.fname, c.lname, i.description
from customer c
join orderinfo oi on c.customer_id = oi.customer_id
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
join item i on ol.item_id = i.item_id;

--3: Show orders that are not shipped yet

select oi.orderinfo_id, c.fname, c.lname
from orderinfo oi
join customer c on oi.customer_id = c.customer_id
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
WHERE oi.date_shipped is NULL;

--4:Show stock for items that have been ordered

select i.description, s.quantity
from item i
join stock s on i.item_id = s.item_id
join orderline ol on i.item_id = ol.item_id;


--5:Show barcode and item name for ordered items

select b.barcode_ean, i.description
from barcode b
join item i on b.item_id = i.item_id
join orderline ol on i.item_id = ol.item_id;


