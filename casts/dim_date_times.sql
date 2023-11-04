ALTER TABLE dim_date_times
ALTER COLUMN month TYPE varchar(2),
ALTER COLUMN year TYPE varchar(4),
ALTER COLUMN day TYPE varchar(2),
ALTER COLUMN time_period TYPE varchar(10),
ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid;