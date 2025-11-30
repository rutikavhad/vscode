--DATE 19/11/25
-- create or replace  function testfunction() returns text as 
-- $$
-- declare 
--     Five constant integer :=5;
--     Ten integer NOT NULL :=10;
--     mylatter char default 'a';

-- begin
-- return mylatter;
-- end;
-- $$ language plpgsql; 


-- create or replace function update_marks(marks integer) returns integer as $$
-- begin
--     return marks+5;
-- end;
-- $$ language plpgsql;


-- select update_marks(10);


--\df
              
           --\dfS+ testfunction   
           --select * from pg_proc where proname like 'test%';


--alias for $1




-- create or replace function update_marks1(integer) returns integer as $$
-- begin
--     return $1+5;
-- end;
-- $$ language plpgsql;

-- get data from table
-- create or replace function get_name(text) returns text as $$
-- declare
-- first_name alias for $1;
-- last_name customer.lname%type;

-- begin
--     select into last_name lname from customer where fname=first_name;
--     return first_name || ' ' || last_name;
-- end;
-- $$ language plpgsql;



--get data from using a  customer_id
-- create or replace function get_cust(integer) returns text as $$
-- declare
-- cust_no alias for $1;
-- cust customer%rowtype;

-- begin
--     select into cust * from customer where customer_id=cust_no;
--     return cust.fname || ' ' || cust.lname || ' ' ||cust.town; 
-- end;
-- $$ language plpgsql;





-- create or replace function get_cust1(text,text) returns integer as $$
-- declare
-- First_name alias for $1;
-- Last_name alias for $2;
-- cust_id customer.customer_id%type;

-- begin

--     select into cust_id customer_id from customer where First_name=fname and last_name=lname;
--     if not found then
--         return -1;
--     else
--         return cust_id;
--     end if;
-- end;
-- $$ language plpgsql;





-- create or replace function get_cust2(text,text) returns text as $$
-- declare
-- First_name alias for $1;
-- Last_name alias for $2;
-- cust_id customer.customer_id%type;

-- begin

--     select into cust_id customer_id from customer where First_name=fname and last_name=lname;
--     if not found then
--         return 'not found';
--     else
--         return 'found';
--     end if;
-- end;
-- $$ language plpgsql;


-- case statment

-- -case ... when ... then ... else ... end case

-- loop 
--     statments
-- end loop[lable];

-- exit:
-- exit[leble][when boolean expration];



-- ///
-- continue [leble][when boolean expration]



-- while boolean-expration


-- for name in[reverse] exprassion .. exprassion [by exprassion] loop
--     statments
-- end loop [leble];






----THIS EVEN AND ODD NUMBERS
-- create or replace function my_even(integer) returns text as $$
-- declare
-- num alias for $1;
-- Txt text;

-- begin
--     if num % 2 = 0 then
--         Txt = num || ' is even number';
--     else
--         Txt = num || ' is odd number';
--     end if;
-- return Txt;
-- end;
-- $$ language plpgsql;







----FIBONACHI NUMBER
-- create or replace function my_fib(fib_for integer) returns integer as $$
-- declare
--     ret integer:=0;
--     nxt integer :=1;
--     tmp integer;

-- begin
--     for num in 1..fib_for loop  
--         tmp:=ret;
--         ret:=nxt;
--         nxt:=tmp+nxt;
--     end loop;
--     return ret; 
-- end;
-- $$ language plpgsql;


--DATE 20/11/25


-- create or replace function my_fib2(fib_for integer) returns setof integer as $$
-- declare
--     retval integer:=0;
--     nxtval integer :=1;
--     tmpval integer;

-- begin
--     for num in 1..fib_for loop  
--         return next retval;
--         tmpval:=retval;
--         retval:=nxtval;
--         nxtval:=tmpval+nxtval;
--     end loop;
-- end;
-- $$ language plpgsql;



----FROM 0 TO N NUMBER ODD

-- create or replace function my_odd(integer) returns setof integer as $$
-- declare
-- n alias for $1;
-- num integer;
-- begin
--     for num in 1..n loop 
--          if num % 2 != 0 then
--            return next num;
--         end if;
--     end loop;
--     return;
-- end;
-- $$ language plpgsql;

--recarsion
-- create or replace function my_fib3(fib_for integer) returns integer as $$

-- begin
--     if fib_for<2 then
--         return fib_for;
--     end if;
--     return my_fib3(fib_for-2)+my_fib3(fib_for-1);
-- end;
-- $$ language plpgsql;


-- create or replace function my_sum(text,text) returns text as $$
-- select $1 || ' ' ||  $2

-- $$ language sql;

--             create OPERATOR + (
--                 procedure = my_sum,
--                 leftarg= text,
--                 rightarg= text
--             );



-- create or replace function my_power(integer,integer) returns integer as $$
-- declare
-- num alias for $1;
-- raiseto alias for $2;
-- index1 integer;
-- product integer :=1;
-- begin
--     for index1 in 1..raiseto loop
--         product:=product * num;
--     end loop;
-- return product;
-- end;
-- $$ language plpgsql;




-- factotrial number not working

-- create or replace function my_facto(integer) returns integer as $$

-- declare
-- num integer;
-- result integer :=1;
-- begin
--     for i  in  1..num loop
--         result := result*i;
--         --return  result;
--     end loop;
-- end;
-- $$ language plpgsql;


-- create or replace function my_sum(text,text) returns text as $$
-- select $1 || ' ' ||  $2

-- $$ language sql;

--             create OPERATOR + (
--                 procedure = my_sum,
--                 leftarg= text,
--                 rightarg= text
--             );



-- create or replace function my_power(integer,integer) returns integer as $$
-- declare
-- num alias for $1;
-- raiseto alias for $2;
-- index1 integer;
-- product integer :=1;
-- begin
--     for index1 in 1..raiseto loop
--         product:=product * num;
--     end loop;
-- return product;
-- end;
-- $$ language plpgsql;



-- create function myappend(anyarray,anyelement) returns anyarray as
-- $$

-- select $1 || $2;

-- $$language sql;


-- select myappend(Array[42,6],21), myappend(Array['ab','df'],''); --- only same datatypes



-- imporrt from other files
-- create or replace function gen_sub(a int , b int) returns table(i int) language sql as $$
--     select generate_series(a,b);
-- $$;



-- create or replace function my_min(VARIADIC numeric[]) returns numeric as $$
-- select min($1[i]) from gen_sub(1, array_length($1, 1)) g(i);
-- $$ language sql;


-- select my_min(10,-1,5,4,4);

-- create or replace function my_comb(VARIADIC text[]) returns text as $$
-- select array_to_string($1,''); 
-- $$ language 'sql'

-- select my_comb('dbms','test','on','11/11/13','at','11.00am') as result


--date 26-11-25

-- create or replace function sum_of_squre(state integer, value integer) returns integer language plpgsql as $$

-- begin
--     if value is null then
--         return state;
--     end if;
--     return state+value;
-- end;
-- $$;


-- create aggregate sum_of_squres(integer)(
--     sfunc=sum_of_squre,
--     stype=integer,
--     initcond=0

-- );


-- create or replace aggregate my_agg1(integer)(
--     sfunc=sum_of_squre,
--     stype=integer,
--     initcond=1

-- );

-- create or replace aggregate my_agg2(integer)(
--     sfunc=sum_of_squre,
--     stype=integer,
--     initcond=1

-- );


-- select my_agg2(customer_id) from customer where customer_id<4;



-- create or replace function myavg_ignore_small_state(state numeric[],value numeric) returns numeric[] language plpgsql
-- as $$

-- begin 
--     if value is null then
--         return state;
--     end if;
--     if value>10 then
--         state[1]:=state[1]+value;
--         state[2]:=state[2]+1;
--     end if;
--     return state;
-- end;
-- $$;




-- create or replace function my_agg3(state numeric[]) returns numeric language plpgsql as $$
-- begin
--     if state[2] = 0 or state is null then
--         return null;
--     else
--         return state[1]/state[2];
--     end if;
-- end;
-- $$;


-- create or replace aggregate my_avg_small(numeric)(
--     sfunc=myavg_ignore_small_state,
--     stype=numeric[],
--     finalfunc=my_agg3,
--     initcond="{0,0}"

-- );



-- -- select my_agg2(customer_id) from customer where customer_id<4;

-- -- select my_avg_small(customer_id) form customer;
-- -- select my_agg3(3);



create or replace function myavg_state(state integer[],value integer) returns integer[] as $$
declare
    total integer:=0;
    cnt integer:=0;
begin
    if state is not null then
        total:=state[1];
        cnt:=state[2];
        end if;

        if value >=10 then
            total:=total+value;
            cnt:=cnt+1;
        end if;

    return array[total,cnt];
    end;
    $$ language plpgsql;



create or replace function avg_final(state integer[]) returns numeric as $$
declare
    total integer:=0;
    cnt integer:=0;
begin
    if state is null then
        return null;
    end if;

    total:=state[1];
    cnt:=state[2];

    if cnt = 0 then
        return null;
    end if;

    return total::numeric/cnt;

end;
$$language plpgsql;


create or replace aggregate abgten(integer)(
    sfunc=myavg_state,
    stype=integer[],
    initcond='{0,0}',
    finalfunc=avg_final

);

