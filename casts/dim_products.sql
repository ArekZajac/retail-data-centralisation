UPDATE dim_products 
SET product_price = REPLACE(product_price, '£', '')::numeric;

-- ALTER TABLE dim_products 
-- ADD COLUMN weight_class VARCHAR(50);

UPDATE dim_products 
SET weight_class = 
    CASE 
        WHEN weight < 2 THEN 'Light'
        WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
        WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
        ELSE 'Truck_Required'
    END;

UPDATE dim_products
SET still_available =
    CASE
        WHEN still_available = 'Still_avaliable' THEN true
        ELSE false
    END;

ALTER TABLE dim_products
ALTER COLUMN product_price TYPE float USING product_price::float,
ALTER COLUMN weight TYPE float,
ALTER COLUMN "EAN" TYPE varchar(17),
ALTER COLUMN product_code TYPE varchar(12),
ALTER COLUMN date_added TYPE date,
ALTER COLUMN uuid TYPE uuid USING uuid::uuid,
ALTER COLUMN still_available TYPE bool USING still_available::bool,
ALTER COLUMN weight_class TYPE varchar(14);