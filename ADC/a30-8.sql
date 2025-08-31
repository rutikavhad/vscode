-- explain select 12 as test;

-- select * from customer limit 5;


--  select * from customer limit 5 offset 5;


-- explain select * from customer, orderinfo;



-- select * from customer,orderinfo where custocustomer_id=12;

-- explain select * from customer,orderinfo where customer.customer_id=12;


-- vacuum customer 


-- vacuum orderinfo ;

-- explain select * from customer,orderinfo where customer.customer_id=12;

--##############################################################################################################################################################
-- bst and b+ tree and memory manegement

-- explain select * from orderinfo where customer_id=12;


-- \h create index;

-- create index m on customer using

-- brin btree gin gust hash spgist

-- create a hash tabel using our names BUCKET LINKLIST
--##############################################################################################################################################################


--\dS+
--create table commant(a integer, b text);

-- explain select * from customer ,orderinfo where customer.customer_id=orderinfo.customer_id;

-- create table student (roll integer ,name varchar(20), bdate date);

-- insert into student values (1,'bob','03-04-2004');
--##############################################################################################################################################################

--aggregate and normal function in database
--##############################################################################################################################################################

-- explain select count(*), lname from customer group by lname;

-- set enable_hashagg to off;


-- explain select count(*), lname from customer group by lname;

explain select lname from customer group by lname;