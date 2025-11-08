create table students(r_no serial primary key,names text,skill text[],preferred_companies text[]);

create table companies(cmp_id serial primary key,cmp_name text,req_skills text[],offerroll text[]);

create table placed(pid serial primary key,r_no int references students(r_no),cmp_id int references companies(cmp_id),offerroll text[]);


insert into students (names, skill, preferred_companies) values('aniket', array['java','python','sql'], array['google','microsoft']),('prashant', array['java','django','postgresql'], array['google','microsoft','wipro']),('rutik', array['java','python','cyber security'], array['tcs','microsoft','apple']),('dhiraj', array['django','python','mongodb'], array['google','microsoft','wipro']),('ajinkay', array['machine learning','python','mongodb'], array['tcs','amazon']);

insert into companies (cmp_name, req_skills, offerroll) values('google', array['python','machine learning'], array['ml engineer','data analyst']),('tcs', array['java','machine learning'], array['software development','data analyst']),('wipro', array['python','kotlin'], array['ml engineer','android app development']),('platform 9', array['python','java','sql'], array['ml engineer','software development','sql developer']);

insert into placed (r_no, cmp_id, offerroll) values(1, 1, array['ml engineer']),(2, 3, array['android app development']),(3, 2, array['data analyst']),(4, 2, array['software development']);


--Display the names of all students who have 'SQL' in their skill array.
select names from students where 'sql' = any(skill);

/* matrix=# select names from students where 'sql' = any(skill);
 names  
--------
 aniket
(1 row)
*/

--Retrieve all company names that require 'Python' as one of thei
select cmp_name from companies where 'python'=any(req_skills);

/*
matrix=# select cmp_name from companies where 'python'=any(req_skills);
  cmp_name  
------------
 google
 wipro
 platform 9
(3 rows)

*/

--Find students whose preferred companies include 'Google'.
select names from students where 'google'=any(preferred_companies);
/*
matrix=# select names from students where 'google'=any(preferred_companies);
  names   
----------
 aniket
 prashant
 dhiraj
(3 rows)
*/

--Find all placed students where one of the offered roles is 'Data Analyst'
select s.names, c.cmp_name, p.offerroll from placed p join students s on p.r_no = s.r_no join companies c on p.cmp_id = c.cmp_id where 'data analyst' = any(p.offerroll);

/*
matrix=# select s.names, c.cmp_name, p.offerroll from placed p join students s on p.r_no = s.r_no join companies c on p.cmp_id = c.cmp_id where 'data analyst' = any(p.offerroll);
 names | cmp_name |    offerroll     
-------+----------+------------------
 rutik | tcs      | {"data analyst"}
(1 row)
*/
