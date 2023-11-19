SELECT 
    SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM 
    dim_store_details
GROUP BY 
    country_code
ORDER BY 
    total_staff_numbers DESC;
