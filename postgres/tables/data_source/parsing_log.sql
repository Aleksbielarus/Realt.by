/********************************************************************
 					CREATE PARSING LOG TABLE 
 ********************************************************************/
drop sequence if exists data_source.seq_parse_log cascade;
create sequence data_source.seq_parse_log;

drop table if exists data_source.parse_log;
CREATE TABLE data_source.parse_log
	(
     id int not null default nextval('data_source.seq_parse_log'),
     source_id varchar(255),
     status varchar(255),
     created_at timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
	);

