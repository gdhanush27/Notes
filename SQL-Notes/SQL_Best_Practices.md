### **1. Use Indexes Wisely**
**Bad Practice**:  
Not indexing columns used in `WHERE`, `JOIN`, or `ORDER BY`, leading to full table scans.  
```sql
SELECT * FROM Users WHERE email = 'alice@example.com'; -- No index on `email`
```

**Good Practice**:  
Create indexes on frequently queried columns.  
```sql
CREATE INDEX idx_users_email ON Users(email); -- Index creation
SELECT * FROM Users WHERE email = 'alice@example.com'; -- Uses index
```

---

### **2. Avoid `SELECT *`**  
**Bad Practice**:  
Fetching all columns when only a few are needed.  
```sql
SELECT * FROM Orders; -- Returns 20 columns when only 3 are needed
```

**Good Practice**:  
Explicitly list required columns.  
```sql
SELECT order_id, customer_id, amount FROM Orders;
```

---

### **3. Use `JOIN` Instead of Subqueries**  
**Bad Practice**:  
Using slow, nested subqueries.  
```sql
SELECT name FROM Users 
WHERE id IN (SELECT user_id FROM Orders WHERE amount > 100); -- Subquery
```

**Good Practice**:  
Use `JOIN` for better readability and performance.  
```sql
SELECT u.name 
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
WHERE o.amount > 100;
```

---

### **4. Filter Early with `WHERE`**  
**Bad Practice**:  
Joining large tables before filtering.  
```sql
SELECT u.name, o.amount 
FROM Users u
INNER JOIN Orders o ON u.id = o.user_id
WHERE u.country = 'USA'; -- Filters AFTER joining
```

**Good Practice**:  
Filter first to reduce the dataset.  
```sql
SELECT u.name, o.amount 
FROM (SELECT * FROM Users WHERE country = 'USA') u -- Filters EARLY
INNER JOIN Orders o ON u.id = o.user_id;
```

---

### **5. Avoid Functions on Indexed Columns**  
**Bad Practice**:  
Applying functions to indexed columns, disabling index usage.  
```sql
SELECT * FROM Users WHERE UPPER(email) = 'ALICE@EXAMPLE.COM'; -- Index ignored
```

**Good Practice**:  
Store data in the required format or use computed columns.  
```sql
SELECT * FROM Users WHERE email = 'alice@example.com'; -- Uses index
```

---

### **6. Limit Results with `LIMIT`**  
**Bad Practice**:  
Fetching 10,000 rows when only 10 are needed.  
```sql
SELECT * FROM Orders; -- Returns all rows
```

**Good Practice**:  
Use `LIMIT` (or `FETCH FIRST`) for pagination/sampling.  
```sql
SELECT * FROM Orders LIMIT 10;
```

---

### **7. Use `EXISTS` Instead of `COUNT`**  
**Bad Practice**:  
Using `COUNT` to check for existence.  
```sql
SELECT * FROM Users 
WHERE (SELECT COUNT(*) FROM Orders WHERE user_id = Users.id) > 0; -- Slow
```

**Good Practice**:  
Use `EXISTS` for faster existence checks.  
```sql
SELECT * FROM Users u
WHERE EXISTS (SELECT 1 FROM Orders WHERE user_id = u.id);
```

---

### **8. Avoid Multiple `OR` Conditions**  
**Bad Practice**:  
Using `OR` with non-indexed columns.  
```sql
SELECT * FROM Products 
WHERE category = 'Electronics' OR price > 1000; -- Full scan
```

**Good Practice**:  
Break into `UNION ALL` for separate indexed queries.  
```sql
SELECT * FROM Products WHERE category = 'Electronics'
UNION ALL
SELECT * FROM Products WHERE price > 1000;
```

---

### **9. Use `UNION ALL` Instead of `UNION`**  
**Bad Practice**:  
Using `UNION` (which removes duplicates) unnecessarily.  
```sql
SELECT name FROM Employees 
UNION
SELECT name FROM Managers; -- Slow duplicate removal
```

**Good Practice**:  
Use `UNION ALL` if duplicates are acceptable.  
```sql
SELECT name FROM Employees 
UNION ALL
SELECT name FROM Managers; -- Faster
```

---

### **10. Normalize Data**  
**Bad Practice**:  
Storing redundant data in denormalized tables.  
```sql
CREATE TABLE Orders (
    order_id INT,
    customer_name VARCHAR(50), -- Redundant
    product_name VARCHAR(50)   -- Redundant
);
```

**Good Practice**:  
Normalize tables to reduce redundancy.  
```sql
CREATE TABLE Orders (
    order_id INT,
    customer_id INT,
    product_id INT
);
```

---

### **11. Use Batch Operations**  
**Bad Practice**:  
Inserting rows one by one.  
```sql
INSERT INTO Users (name) VALUES ('Alice');
INSERT INTO Users (name) VALUES ('Bob'); -- Multiple roundtrips
```

**Good Practice**:  
Use bulk inserts.  
```sql
INSERT INTO Users (name) 
VALUES ('Alice'), ('Bob'); -- Single query
```

---

### **12. Avoid Cursors**  
**Bad Practice**:  
Using cursors for row-by-row processing.  
```sql
DECLARE @id INT;
DECLARE cursor CURSOR FOR SELECT user_id FROM Users;
OPEN cursor;
FETCH NEXT FROM cursor INTO @id;
-- Slow loop
```

**Good Practice**:  
Use set-based operations.  
```sql
UPDATE Users SET status = 'active' WHERE last_login > '2023-01-01'; -- Single query
```

---

### **13. Optimize Data Types**  
**Bad Practice**:  
Using overly large or inappropriate data types.  
```sql
CREATE TABLE Logs (
    log_id VARCHAR(100), -- Should be INT
    message TEXT
);
```

**Good Practice**:  
Choose the smallest/data-appropriate type.  
```sql
CREATE TABLE Logs (
    log_id INT PRIMARY KEY,
    message VARCHAR(255) -- Enough for most logs
);
```

---

### **14. Use Stored Procedures**  
**Bad Practice**:  
Sending raw SQL repeatedly from the app.  
```sql
-- App code sends this query every time:
SELECT * FROM Users WHERE country = 'USA';
```

**Good Practice**:  
Encapsulate logic in a stored procedure.  
```sql
CREATE PROCEDURE GetUSUsers
AS
BEGIN
    SELECT * FROM Users WHERE country = 'USA';
END;
-- Call once: EXEC GetUSUsers;
```

---

### **15. Analyze Execution Plans**  
**Bad Practice**:  
Ignoring query execution plans.  
```sql
SELECT * FROM Products WHERE price > 100; -- No idea why it’s slow
```

**Good Practice**:  
Use `EXPLAIN` (or `EXPLAIN ANALYZE`) to optimize.  
```sql
EXPLAIN SELECT * FROM Products WHERE price > 100; -- Check for full scans
```

---

### **Summary**  
| **Tip**               | **Bad Practice**                          | **Good Practice**                          |  
|-----------------------|-------------------------------------------|--------------------------------------------|  
| Indexes               | No index on filtered columns.             | Create targeted indexes.                   |  
| `SELECT *`            | Fetching unnecessary columns.             | List specific columns.                     |  
| Subqueries            | Nested subqueries.                        | Use `JOIN`.                                |  
| Filtering             | Filter after joining.                     | Filter early with `WHERE`.                 |  
| Functions on columns  | `WHERE UPPER(column) = ...`               | Precompute or avoid functions.             |  
| `LIMIT`               | Fetching all rows.                        | Use `LIMIT` for small results.             |  
| `EXISTS` vs `COUNT`   | `COUNT(*) > 0`                            | `EXISTS(...)`.                             |  
| Multiple `OR`         | `WHERE a OR b`                            | Split into `UNION ALL`.                    |  
| `UNION` vs `UNION ALL`| Using `UNION` unnecessarily.              | Use `UNION ALL` for speed.                 |  
| Normalization         | Redundant data storage.                   | Normalize tables.                          |  
| Batch operations      | Row-by-row inserts.                       | Bulk inserts.                              |  
| Cursors               | Row-by-row processing.                    | Set-based operations.                      |  
| Data types            | `VARCHAR` for numbers/dates.              | Use `INT`, `DATE`, etc.                    |  
| Stored procedures     | Repeated raw SQL from apps.               | Encapsulate logic in procedures.           |  
| Execution plans       | Ignoring query optimization.              | Use `EXPLAIN` to diagnose issues.          |  
