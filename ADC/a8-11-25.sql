--create table class(courseld char(7),year smallint,Student text[]);

--create table exam(Studid int,Stud_name char(10),Cources_and_Grades text[]);

--\d exam

--\dS+ exam

--insert into class values ('CA-504',2024,'{"ajinkya","aniket","prashant","rutik","dhiraj","rohit","rushi","swami"}');

--insert into class values ('CA-501',2024,'{"ganesh","mangesh","prashant","rutik","pandu","vijay","rushi","harshal"}');

--insert into class values ('CA-503',2024,'{"raja","aniket","sanket","rutik","jitya","rohit","rushikesh","swami"}');

--select * from class;

--insert into exam values (21113,'aniket','{{"CA-504"},{"A"}}');

--insert into exam values (21213,'rushi','{{"CA-501","CA-503","CA-504"},{"A","A","B"}}');


--select Student from class where courseld='CA-504'

--select Student[2] from class where courseld='CA-504';


--select Cources_and_Grades[1][2] as cource, Cources_and_Grades[2][2] as Grade from exam where Stud_name='rushi';


-- array slice

--select Student[4:8] from class where courseld='CA-504';

--update array

--update exam set Cources_and_Grades[2][1]='A+' where Stud_name='rushi';
--update class set Student[8]='swami' where courseld='CA-504';
--update exam set Cources_and_Grades='{{"CA-504","CA-503"},{"A","B"}}' where Stud_name='aniket';

-- concatnating array


--update class set Student=Student || array['aniket','prashant'] where courseld='CA-504';

--select courseld from class where 'rushi'=any(Student);

--select * from exam where 'CA-504'=any(array['CA-504','CA-505','CA-506']);


--make own

--create table students(r_no serial primary key,names text,skill text[],preferred_companies text[]);

--create table companies(cmp_id serial primary key,cmp_name text,req_skills text[],offerroll text[]);

--create table placed(pid serial primary key,r_no int references students(r_no),cmp_id int references companies(cmp_id),offerroll text[]);





--insert into students (names, skill, preferred_companies) values('aniket', array['java','python','sql'], array['google','microsoft']),('prashant', array['java','django','postgresql'], array['google','microsoft','wipro']),('rutik', array['java','python','cyber security'], array['tcs','microsoft','apple']),('dhiraj', array['django','python','mongodb'], array['google','microsoft','wipro']),('ajinkay', array['machine learning','python','mongodb'], array['tcs','amazon']);

--insert into companies (cmp_name, req_skills, offerroll) values('google', array['python','machine learning'], array['ml engineer','data analyst']),('tcs', array['java','machine learning'], array['software development','data analyst']),('wipro', array['python','kotlin'], array['ml engineer','android app development']),('platform 9', array['python','java','sql'], array['ml engineer','software development','sql developer']);

--insert into placed (r_no, cmp_id, offerroll) values(1, 1, array['ml engineer']),(2, 3, array['android app development']),(3, 2, array['data analyst']),(4, 2, array['software development']);


--sql in skill array
select names from students where 'sql' = any(skill);

select cmp_name from companies where 'python'=any(skill);
select names from students where 'google'=any(skill);

select s.names, c.cmp_name, p.offerroll from placed p join students s on p.r_no = s.r_no join companies c on p.cmp_id = c.cmp_id where 'data analyst' = any(p.offerroll);
