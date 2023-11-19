SELECT 
    ROUND(SUM(p.product_price * o.product_quantity)::numeric, 2) AS total_sales,
    d.year,
    d.month
FROM 
    orders_table o
JOIN 
    dim_date_times d ON o.date_uuid = d.date_uuid
JOIN
    dim_products p ON o.product_code = p.product_code
GROUP BY 
    d.year, d.month
ORDER BY 
    total_sales DESC
LIMIT 10;
