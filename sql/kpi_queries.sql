-- QUERY 1: Executive KPIs
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold
FROM transactions;


-- QUERY 2: Revenue by category
SELECT
    category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM transactions
GROUP BY category
ORDER BY total_revenue DESC;


-- QUERY 3: Daily revenue
SELECT
    DATE(event_time) AS sales_date,
    ROUND(SUM(revenue), 2) AS daily_revenue
FROM transactions
GROUP BY DATE(event_time)
ORDER BY sales_date;


-- QUERY 4: Regional performance
SELECT
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM transactions
GROUP BY region
ORDER BY total_revenue DESC;