create table users(id integer primary key AUTOINCREMENT, name text not null,
 password text not null, admin boolean not null DEFAULT '0');

create table emp (empid integer primary key AUTOINCREMENT, name text not null, email text, phone integer, address text,
joining_date timestamp DEFAULT current_timestamp, total_projects integer default 1,
total_test_case integer default 1, total_defect_found integer DEFAULT 1, total_defects_pending integer default 1);
