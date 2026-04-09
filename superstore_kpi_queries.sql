-- End-to-End Supply Chain & Profitability Analysis
-- These SQL queries assume a table name: superstore_orders

-- 1) Overall KPI snapshot
SELECT
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    CASE WHEN SUM(Sales) = 0 THEN 0 ELSE (SUM(Profit) * 100.0 / SUM(Sales)) END AS profit_margin_pct,
    AVG(DATEDIFF(day, [Order Date], [Ship Date])) AS avg_delivery_time_days,
    COUNT(DISTINCT [Order ID]) AS total_orders,
    COUNT(DISTINCT [Customer ID]) AS total_customers
FROM superstore_orders;

-- 2) Shipping efficiency by ship mode
SELECT
    [Ship Mode],
    AVG(DATEDIFF(day, [Order Date], [Ship Date])) AS avg_delivery_time_days,
    COUNT(DISTINCT [Order ID]) AS total_orders,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore_orders
GROUP BY [Ship Mode]
ORDER BY avg_delivery_time_days ASC;

-- 3) Regional profitability
SELECT
    Region,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    CASE WHEN SUM(Sales) = 0 THEN 0 ELSE (SUM(Profit) * 100.0 / SUM(Sales)) END AS profit_margin_pct
FROM superstore_orders
GROUP BY Region
ORDER BY total_profit ASC;

-- 4) Loss-making products
SELECT
    [Product ID],
    [Product Name],
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore_orders
GROUP BY [Product ID], [Product Name]
HAVING SUM(Profit) < 0
ORDER BY total_profit ASC;

-- 5) Category and sub-category profitability
SELECT
    Category,
    [Sub-Category],
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore_orders
GROUP BY Category, [Sub-Category]
ORDER BY total_profit ASC;

-- 6) Monthly trend (sales and profit)
SELECT
    FORMAT([Order Date], 'yyyy-MM') AS order_year_month,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore_orders
GROUP BY FORMAT([Order Date], 'yyyy-MM')
ORDER BY order_year_month;
