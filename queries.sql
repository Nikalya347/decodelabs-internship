SELECT OrderID, Product, Quantity, UnitPrice, PaymentMethod, OrderStatus
FROM orders 
WHERE UnitPrice > 350 
ORDER BY Quantity DESC;

SELECT Product, COUNT(OrderID) AS Total_Orders, SUM(Quantity) AS Total_Units_Sold, AVG(UnitPrice) AS Average_Unit_Price
FROM orders 
GROUP BY Product
ORDER BY Total_Units_Sold DESC;
