/********************************************************************
 			CREATE TECH TABLE FOR INCREMENTAL LOAD
 ********************************************************************/
drop sequence if exists data_source.seq_tech_table cascade;
create sequence data_source.seq_tech_table;

drop table if exists data_source.tech_table;
CREATE TABLE data_source.tech_table
	(
     id int not null default nextval('data_source.seq_tech_table'),
     parsing_date date default CURRENT_DATE,
     parsing_datetime timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
	);