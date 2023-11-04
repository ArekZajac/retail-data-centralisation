ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE float,
ALTER COLUMN locality TYPE varchar(255),
ALTER COLUMN store_code TYPE varchar(12),
ALTER COLUMN staff_numbers TYPE smallint,
ALTER COLUMN opening_date TYPE date,
ALTER COLUMN store_type TYPE varchar(255),
ALTER COLUMN latitude TYPE float,
ALTER COLUMN country_code TYPE varchar(3),
ALTER COLUMN continent TYPE varchar(255);