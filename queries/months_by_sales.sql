SELECT 
    SUM(o.product_quantity) AS total_sales, 
    d.month
FROM 
    orders_table o 
JOIN 
    dim_date_times d ON o.date_uuid = d.date_uuid
GROUP BY 
    d.month
ORDER BY 
    total_sales DESC;
