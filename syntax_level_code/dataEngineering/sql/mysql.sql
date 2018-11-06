--install mysql
sudo apt-get install mysql-server
sudo apt-get install mysql-client

-- sql commands to start structured query linux
$mysql -u username -p
password:

--show port number sql in server
>> show variables WHERE Variable_name = 'port';

--create database
>>create database <databasename>

--show databases in the server
>>show databases;

--acess the database
>>use <databasename>

--show tables in the database
>>show tables;

--show the user sql
select user();



--to generate unique doc_id md5
 mysql>select md5(concat(title,link)) from oercommons limit 5;
 mysql>update oercommons set document_id=md5(concat(title,link))  where title=title;

--How do I set the initial value for column which has auto_increment in a MySQL table that start from 1001 and not 0?
  mysql>ALTER TABLE <tablename> AUTO_INCREMENT=<value>;
  --ex.
  mysql>ALTER TABLE users AUTO_INCREMENT=1001;

--use sub strip to cut the string (negative count will give u from last)
  SUBSTRING_INDEX(str, delim, count)
  --ex.
  mysql> SELECT SUBSTRING_INDEX('www.mytestpage.info','.',2);
+----------------------------------------------+
| SUBSTRING_INDEX('www.mytestpage.info','.',2) |
+----------------------------------------------+
| www.mytestpage                               | 
+----------------------------------------------+
1 row in set (0.02 sec)

mysql> SELECT SUBSTRING_INDEX('www.mytestpage.info','.',-2); 
+-----------------------------------------------+
| SUBSTRING_INDEX('www.mytestpage.info','.',-2) |
+-----------------------------------------------+
| mytestpage.info                               | 
+-----------------------------------------------+
1 row in set (0.00 sec
  --more details http://www.w3resource.com/mysql/string-functions/mysql-substring_index-function.php

--dump tables from one database to another database on the same server with no data.
$ mysqldump  -uaceuser -paceuser <databasename1> <tablenames> --no-data | mysql -uaceuser -paceuser <databasename2>
ex.$ mysqldump  -uaceuser -paceuser devry_oer_v2 keywords youtube_meta merlot_assets ebsco_metadata --no-data | mysql -uaceuser -paceuser saintleo_oer_v2

--how to mysql dump a backup copy of table to database
$ mysql -uaceuser -paceuser saintleo_oer_v2 < ebsco_metadata.sql

--how to create mysql dump backup copy of table schema
$ mysql -uaceuser -paceuser saintleo_oer_v2 ebsco_metadata --no-data > ebsco_metadata.sql

--To remove the contents we use delete
delete from <tablename>


--if their are two rows with same values change the only one row(when their are two course_id=345 first one will be updated)
$update table set cousrse_id=324 where course_id=345 limit 1;

--how to find length of column
select length(columnname) from table;

--copy one table to another
create table tmp_textbook_toc as select * from textbook_toc;

--select to output file (tmp file must be the file you can save this file only)
select src_domain,widget,advertiser_domain,count(advertiser_domain) from all_widget group by src_domain,advertiser_domain INTO OUTFILE '/tmp/count.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';


--change auto increment value
ALTER TABLE tbl AUTO_INCREMENT = 5;

--get random values 
ORDER BY RAND() limit 2

--drop column from table
ALTER TABLE feeds_master DROP COLUMN iab_status;

--add foregin key constrain
Alter table advertiser ADD CONSTRAINT advertiser_ibfk_2 FOREIGN KEY (feedid) REFERENCES feeds_master(feedid);

--check how table was created
show create table <table_name>;

--To remove all the numbers in the string
update new_keyword set keyword = common_schema.replace_all(keyword,'0123456789.','');

--load data
we must set the option to load the file from local
mysql -uaceuser -paceuser opentextbooks --enable-local-infile
LOAD DATA LOCAL INFILE '/tmp/opentextbook.csv' INTO TABLE toc FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';


-remove spaces from mysql column
update toc set document_id=trim(document_id);

--join the columns in a table
select document_id,GROUP_CONCAT(subject_title SEPARATOR ',') from opentextbooks group by document_id;

--rename a column in mysql
ALTER TABLE xyz CHANGE manufacurerid manufacturerid INT
ALTER TABLE opentextbooks CHANGE document_id textbook_id INT

#log the mysql
SET global log_output = 'FILE';
SET global general_log_file='/tmp/mysql.sql'
SET global general_log = 1;

#how to log the mysql error
mysql [options] < createUsers.sql >> error.log 2>&1


#how to make increment
select title,concat("#chap",@s := @s + 1) from toc2 ,(SELECT @s:= 0) AS s where ebookid=10342;
