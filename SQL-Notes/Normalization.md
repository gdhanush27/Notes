### **1. First Normal Form (1NF)**  
**Definition**:  
- Eliminate **repeating groups** and ensure **atomic values** (each column holds a single value).  
- Every table must have a **primary key**.  

**Violation Example**:  
| student_id | name  | courses         |  
|------------|-------|-----------------|  
| 1          | Alice | Math, Physics   |  

**Normalization**:  
- Split the `courses` column into individual rows.  
- Create a separate table for courses.  

**SQL Implementation**:  
```sql  
-- Students Table  
CREATE TABLE Students (  
    student_id INT PRIMARY KEY,  
    name VARCHAR(50)  
);  

-- Courses Table  
CREATE TABLE Courses (  
    course_id INT PRIMARY KEY AUTO_INCREMENT,  
    student_id INT,  
    course_name VARCHAR(50),  
    FOREIGN KEY (student_id) REFERENCES Students(student_id)  
);  
```  

**Summary**:  
- **Goal**: Remove duplicates and ensure atomicity.  
- **Key Rule**: No multi-valued attributes.  

---

### **2. Second Normal Form (2NF)**  
**Definition**:  
- Remove **partial dependencies** (all non-key columns must depend on the **full primary key**).  

**Violation Example**:  
| student_id | course_id | course_name | grade |  
|------------|-----------|-------------|-------|  
| 1          | 101       | Math        | A     |  

**Problem**: `course_name` depends only on `course_id`, not the composite key (`student_id + course_id`).  

**Normalization**:  
- Split into `StudentsGrades` and `Courses`.  

**SQL Implementation**:  
```sql  
-- StudentsGrades Table  
CREATE TABLE StudentsGrades (  
    student_id INT,  
    course_id INT,  
    grade VARCHAR(2),  
    PRIMARY KEY (student_id, course_id)  
);  

-- Courses Table  
CREATE TABLE Courses (  
    course_id INT PRIMARY KEY,  
    course_name VARCHAR(50)  
);  
```  

**Summary**:  
- **Goal**: Eliminate partial dependencies.  
- **Key Rule**: Non-key attributes depend on the **entire primary key**.  

---

### **3. Third Normal Form (3NF)**  
**Definition**:  
- Remove **transitive dependencies** (non-key columns must not depend on other non-key columns).  

**Violation Example**:  
| student_id | name  | birth_year | age |  
|------------|-------|------------|-----|  
| 1          | Alice | 2000       | 23  |  

**Problem**: `age` depends on `birth_year` (a non-key attribute).  

**Normalization**:  
- Split into `Students` and `StudentAges`.  

**SQL Implementation**:  
```sql  
-- Students Table  
CREATE TABLE Students (  
    student_id INT PRIMARY KEY,  
    name VARCHAR(50),  
    birth_year INT  
);  

-- Calculate age dynamically (no separate table needed).  
```  

**Summary**:  
- **Goal**: Eliminate transitive dependencies.  
- **Key Rule**: Non-key attributes depend **only on the primary key**.  

---

### **Boyce-Codd Normal Form (BCNF / 3.5NF)**  
**Definition**:  
- Every **determinant** (left side of a functional dependency) must be a **candidate key**.  

**Violation Example**:  
| student_id | course  | instructor      |  
|------------|---------|-----------------|  
| 1          | Math    | Dr. Smith       |  

**Problem**: `course → instructor`, but `course` is not a candidate key.  

**Normalization**:  
- Split into `StudentCourses` and `CourseInstructors`.  

**SQL Implementation**:  
```sql  
-- StudentCourses Table  
CREATE TABLE StudentCourses (  
    student_id INT,  
    course VARCHAR(50),  
    PRIMARY KEY (student_id, course)  
);  

-- CourseInstructors Table  
CREATE TABLE CourseInstructors (  
    course VARCHAR(50) PRIMARY KEY,  
    instructor VARCHAR(50)  
);  
```  

**Summary**:  
- **Goal**: Stricter than 3NF.  
- **Key Rule**: All determinants are candidate keys.  

---

### **4. Fourth Normal Form (4NF)**  
**Definition**:  
- Eliminate **multi-valued dependencies (MVDs)** unless the determinant is a superkey.  

**Violation Example**:  
| emp_id | skill    | language  |  
|--------|----------|-----------|  
| 1      | Python   | English   |  
| 1      | Python   | Spanish   |  

**Problem**: Skills and languages are independent, causing redundant combinations.  

**Normalization**:  
- Split into `EmployeeSkills` and `EmployeeLanguages`.  

**SQL Implementation**:  
```sql  
-- EmployeeSkills Table  
CREATE TABLE EmployeeSkills (  
    emp_id INT,  
    skill VARCHAR(50),  
    PRIMARY KEY (emp_id, skill)  
);  

-- EmployeeLanguages Table  
CREATE TABLE EmployeeLanguages (  
    emp_id INT,  
    language VARCHAR(50),  
    PRIMARY KEY (emp_id, language)  
);  
```  

**Summary**:  
- **Goal**: Handle independent multi-valued facts.  
- **Key Rule**: No non-trivial MVDs.  

---

### **5. Fifth Normal Form (5NF)**  
**Definition**:  
- Eliminate **join dependencies**. Data cannot be decomposed further without loss.  

**Violation Example**:  
| supplier | part    | project  |  
|----------|---------|----------|  
| S1       | P1      | J1       |  
| S1       | P2      | J2       |  

**Problem**: The table cannot be decomposed into smaller tables without losing relationships.  

**Normalization**:  
- Split into `SupplierPart`, `PartProject`, and `ProjectSupplier`.  

**SQL Implementation**:  
```sql  
-- SupplierPart Table  
CREATE TABLE SupplierPart (  
    supplier VARCHAR(50),  
    part VARCHAR(50),  
    PRIMARY KEY (supplier, part)  
);  

-- PartProject Table  
CREATE TABLE PartProject (  
    part VARCHAR(50),  
    project VARCHAR(50),  
    PRIMARY KEY (part, project)  
);  

-- ProjectSupplier Table  
CREATE TABLE ProjectSupplier (  
    project VARCHAR(50),  
    supplier VARCHAR(50),  
    PRIMARY KEY (project, supplier)  
);  
```  

**Summary**:  
- **Goal**: Ensure lossless decomposition.  
- **Key Rule**: No spurious tuples on re-join.  

---

### **Summary Table**  
| **Normal Form** | **Focus**                     | **Key Rule**                                |  
|------------------|-------------------------------|---------------------------------------------|  
| 1NF             | Atomic values                 | No repeating groups.                        |  
| 2NF             | Partial dependencies          | Non-key columns depend on full primary key. |  
| 3NF             | Transitive dependencies       | Non-key columns depend only on primary key. |  
| BCNF            | Determinants as candidate keys| All determinants are candidate keys.        |  
| 4NF             | Multi-valued dependencies     | No non-trivial MVDs.                        |  
| 5NF             | Join dependencies             | Lossless decomposition.                     |  

---

### **Practice Problems**  
**Problem 1**: Normalize this table to 2NF:  
| order_id | product_id | product_name | quantity |  
|----------|------------|--------------|----------|  

**Solution**:  
- Split into `Orders` (`order_id`, `product_id`, `quantity`) and `Products` (`product_id`, `product_name`).  

**Problem 2**: Normalize to 4NF:  
| emp_id | skill    | certification |  
|--------|----------|---------------|  
| 1      | SQL      | AWS           |  
| 1      | Python   | AWS           |  

**Solution**:  
- Split into `EmployeeSkills` (`emp_id`, `skill`) and `EmployeeCerts` (`emp_id`, `certification`).  

---

### **Key Takeaways**  
- Normalization reduces redundancy and improves data integrity.  
- Over-normalization can lead to performance issues (too many joins).  
- BCNF and 3NF are widely used; 4NF/5NF are niche for complex scenarios.  