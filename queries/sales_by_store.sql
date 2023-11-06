WITH TotalSales AS (
    SELECT 
        s.store_type,
        SUM(p.product_price * o.product_quantity) AS total_sales
    FROM 
        orders_table o 
    JOIN 
        dim_store_details s ON o.store_code = s.store_code
    JOIN
        dim_products p ON o.product_code = p.product_code
    GROUP BY 
        s.store_type
),
GrandTotal AS (
    SELECT SUM(total_sales) AS grand_total_sales FROM TotalSales
)

SELECT 
    t.store_type, 
    t.total_sales, 
    ROUND((t.total_sales / g.grand_total_sales * 100)::numeric, 2) AS percentage_total
FROM 
    TotalSales t, GrandTotal g
ORDER BY 
    total_sales DESC;
