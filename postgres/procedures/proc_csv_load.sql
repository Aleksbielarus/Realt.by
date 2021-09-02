create or replace procedure data_source.csv_load()
language plpgsql
as $$
begin
	COPY data_source.main_page_results(title, link, address, info, seller_name, seller_contact, img, usd_price, byn_price)
	FROM '/home/aleks/PycharmProjects/Sept/flats.csv'
	DELIMITER ';';
end; $$



