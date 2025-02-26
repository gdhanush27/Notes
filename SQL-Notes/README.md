# DBMS-Notes
 ### **1. Introduction to DBMS & MySQL**
- **DBMS (Database Management System)**: Software to store, manage, and retrieve structured data efficiently.
- **MySQL**: A popular open-source relational DBMS (RDBMS) that uses SQL (Structured Query Language).
- **Advantages**: Data integrity, security, concurrent access, and elimination of redundancy.

---

### **2. Basic Concepts**
#### **Relational Database**
- **Tables**: Store data in rows (records) and columns (fields).
- **Primary Key**: Unique identifier for a row (e.g., `student_id`).
- **Foreign Key**: Links two tables (e.g., `course_id` in `Students` references `Courses`).
- **Composite Key**: A primary key made of multiple columns.

---

### **3. SQL Basics**
#### **Data Definition Language (DDL)**
- **CREATE**: Create databases/tables.
- **ALTER**: Modify tables.
- **DROP**: Delete databases/tables.

#### **Data Manipulation Language (DML)**
- **INSERT**: Add records.
- **UPDATE**: Modify records.
- **DELETE**: Remove records.

#### **Data Query Language (DQL)**
- **SELECT**: Retrieve data.

#### **Data Control Language (DCL)**
- **GRANT/REVOKE**: Manage user permissions.

---

### **4. Normalization**

- **1NF**: Eliminate duplicate columns and ensure atomic values.
- **2NF**: Remove partial dependencies (all non-key columns depend on the full primary key).
- **3NF**: Remove transitive dependencies (non-key columns depend only on the primary key).
- **BCNF**: Stricter than 3NF; all determinants are candidate keys.
- **4NF**: Eliminates independent multi-valued facts.
- **5NF**: Ensures lossless decomposition for complex relationships.
[Detailed Explanation](Normalization.md)
---

### **5. SQL Implementation Examples**

#### **Create a Database**
```sql
CREATE DATABASE SchoolDB;
USE SchoolDB;
```

#### **Create a Table**
```sql
CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT,
    email VARCHAR(100) UNIQUE
) ENGINE=InnoDB;
```

#### **Insert Data**
```sql
INSERT INTO Students (name, age, email)
VALUES ('Alice', 20, 'alice@example.com');
```

#### **Query Data**
```sql
SELECT name, age FROM Students WHERE age > 18;
```

#### **Update Data**
```sql
UPDATE Students SET age = 21 WHERE name = 'Alice';
```

#### **Delete Data**
```sql
DELETE FROM Students WHERE student_id = 1;
```

---

### **6. Joins**
- **INNER JOIN**: Returns matching rows from both tables.
  ```sql
  SELECT Students.name, Courses.course_name
  FROM Students
  INNER JOIN Enrollments ON Students.student_id = Enrollments.student_id
  INNER JOIN Courses ON Enrollments.course_id = Courses.course_id;
  ```

---

### **7. Indexes**
Improve query speed on large tables:
```sql
CREATE INDEX idx_student_name ON Students(name);
```

---

### **8. Transactions**
Ensure ACID properties (Atomicity, Consistency, Isolation, Durability):
```sql
START TRANSACTION;
UPDATE Accounts SET balance = balance - 100 WHERE user_id = 1;
UPDATE Accounts SET balance = balance + 100 WHERE user_id = 2;
COMMIT; -- or ROLLBACK on error
```

---

### **9. Stored Procedures**
Reusable SQL code:
```sql
DELIMITER $$
CREATE PROCEDURE GetAdultStudents()
BEGIN
    SELECT * FROM Students WHERE age >= 18;
END $$
DELIMITER ;

-- Call the procedure
CALL GetAdultStudents();
```

---

### **10. Security**
Create users and grant permissions:
```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON SchoolDB.* TO 'admin'@'localhost';
REVOKE DELETE ON SchoolDB.Students FROM 'admin'@'localhost';
```

---
### **SQL Best Practices**
[SQL Best Practices](SQL_Best_Practices.md)

### **Practice Problems**

#### **Problem 1: Normalization**
**Given Table (Unnormalized):**
| student_id | name  | course       | instructor      |
|------------|-------|--------------|-----------------|
| 1          | Alice | Math, Physics| Dr. Smith, Dr. Brown |

**Normalize to 3NF.**

**Solution:**
- **Students** (student_id, name)
- **Courses** (course_id, course_name, instructor)
- **Enrollments** (student_id, course_id)

---

#### **Problem 2: SQL Query**
**Task**: Write a query to find students enrolled in "Mathematics".
```sql
SELECT Students.name 
FROM Students
INNER JOIN Enrollments ON Students.student_id = Enrollments.student_id
INNER JOIN Courses ON Enrollments.course_id = Courses.course_id
WHERE Courses.course_name = 'Mathematics';
```

---

#### **Problem 3: Create a Table**
**Task**: Create a `Books` table with columns: `book_id`, `title`, `author`, `published_year`.
```sql
CREATE TABLE Books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(50),
    published_year YEAR
);
```

Here’s an expanded explanation of **all normal forms up to 5NF**, including **BCNF (3.5NF)**, **4NF**, and **5NF**, with theoretical explanations, examples, and SQL implementations:

---