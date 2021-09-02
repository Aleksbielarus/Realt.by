create schema data_source;

create table data_source.main_page_results
	(
     title varchar(255),
     link varchar(255),
     address varchar(255),
     info varchar(255),
     seller_name varchar(255),
     seller_contact varchar(255),
     img varchar(255),
     usd_price varchar(255),
     byn_price varchar(255)
	);