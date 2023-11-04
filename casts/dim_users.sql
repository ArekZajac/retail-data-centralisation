ALTER TABLE dim_users
ALTER COLUMN first_name TYPE varchar(225),
ALTER COLUMN last_name TYPE varchar(225),
ALTER COLUMN date_of_birth TYPE date,
ALTER COLUMN country_code TYPE varchar(3),
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN join_date TYPE date;
