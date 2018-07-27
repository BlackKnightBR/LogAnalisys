# LogAnalisys:
Project for Full Stack Web Developer Udacity

#Overview:
Reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

#What should it report:
 -1.What are the most popular three articles of all time?
 -2.Who are the most popular article authors of all time?
 -3.On which days did more than 1% of requests lead to errors?

#Tecnologies used:
-PostgreSQL.
-Python code with DB-API(psyscopg2).
-Linux-based virtual machine (VM) Vagrant, configurations by Udacity.

#Running:
-Paste the code inside your vagrant directory, in the shell inside your vagrant directory, start Vagrant
"vagrant up" and log in "vagrant ssh" be sure to have placed the "newsdata.sql" inside your vagrant directory,
 use "psql -d news -f newsdata.sql" to load data create the 3 views (listed bellow) and use
 "python2 LogAnalisys.py" to run the app.

#Views:
1-
  "create view totalStatus as
  select time::date, count(* ) as num from
  log group by time;

2-
  "create view logFailed as
  select time::date, count(* ) as num
  from log where status != '200 OK'
  group by time;"

3-
 "create view percentage as
 select logFailed.day,
 (logFailed.num::double precision/totalStatus.num::double precision) * 100 as percent
 from logFailed
 inner join totalStatus on logFailed.day = totalStatus.day;"

#References:
-W3School
-SQL Documentation
-PSQL Documentation
-Python Documentation
