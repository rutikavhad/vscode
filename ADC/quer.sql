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

--6:show all customers who have placed at least one order

select distinct c.customer_id, c.fname, c.lname
from customer c
join orderinfo oi on c.customer_id = oi.customer_id;

--7:list customers who have never placed an order

select c.customer_id, c.fname, c.lname
from customer c
left join orderinfo oi on c.customer_id = oi.customer_id
where oi.orderinfo_id is null;

--8:show total number of items ordered in each order

select oi.orderinfo_id, sum(ol.quantity) as total_items
from orderinfo oi
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
group by oi.orderinfo_id;

--9:show total price of each order
select oi.orderinfo_id, sum(ol.quantity * ol.unit_price) as order_total
from orderinfo oi
join orderline ol on oi.orderinfo_id = ol.orderinfo_id
group by oi.orderinfo_id;

--10:list items that have never been ordered

select i.item_id, i.description
from item i
left join orderline ol on i.item_id = ol.item_id
where ol.orderline_id is null;


--11:list customers and number of orders placed

select c.customer_id, c.fname, c.lname, count(oi.orderinfo_id) as total_orders
from customer c
left join orderinfo oi on c.customer_id = oi.customer_id
group by c.customer_id, c.fname, c.lname;


--12: show items with stock less than 10

select i.item_id, i.description, s.quantity
from item i
join stock s on i.item_id = s.item_id
where s.quantity < 10;


--13:show last 5 orders placed

select oi.orderinfo_id, oi.date_placed
from orderinfo oi
order by oi.date_placed desc
limit 5;
