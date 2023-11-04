ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE varchar(20),
ALTER COLUMN expiry_date TYPE varchar(5),
ALTER COLUMN date_payment_confirmed TYPE date;