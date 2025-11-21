# Advanced Python: Dictionaries & Functions
## Corporate Training Session - IT Graduates

Hey everyone! Today we're going deep into dictionaries and functions. I know you've probably used these before, but trust me - there's a lot more under the hood that'll make you a better developer. Let's get started.

---

## Part 1: Dictionaries - Beyond the Basics

### What's Really Happening Under the Hood?

You know dictionaries are fast, right? But *why* are they fast? Let's talk about hash tables.

When you do `user['name']`, Python doesn't search through all the keys. It uses something called a **hash function** to convert 'name' into a number, which tells it exactly where to look in memory. That's why it's O(1) - constant time!

```python
# Let's see this in action
key = "username"
print(f"Hash of '{key}': {hash(key)}")
print(f"Same hash again? {hash(key) == hash(key)}")  # Always True!

# This is why you can't use lists as keys
try:
    bad_dict = {[1, 2]: "value"}
except TypeError as e:
    print(f"Nope! {e}")
```

**Quick experiment**: Try checking the memory size of dictionaries at different sizes. You'll notice Python resizes them automatically when they get too full (around 2/3 capacity).

```python
import sys

small = {i: i**2 for i in range(10)}
large = {i: i**2 for i in range(10000)}

print(f"Small: {sys.getsizeof(small)} bytes")
print(f"Large: {sys.getsizeof(large)} bytes")
# Notice it's not exactly proportional? That's resizing in action!
```

---

### Dictionary Methods You Should Actually Use

Let's be honest - most people just use `dict['key']` and maybe `.get()`. But there's more that'll save you lines of code.

#### setdefault() - The underrated hero

```python
# Old way (2 operations = slower)
user_data = {}
if 'login_count' not in user_data:
    user_data['login_count'] = 0
user_data['login_count'] += 1

# Better way (1 atomic operation)
user_data.setdefault('login_count', 0)
user_data['login_count'] += 1
```

Why does this matter? In production code with thousands of requests per second, every operation counts. Plus it's cleaner.

#### Handling messy API responses

Ever work with external APIs? The data structure is never guaranteed. Here's how to handle it safely:

```python
# Typical API response - not all fields are always there
api_response = {
    'user': {'id': 123, 'name': 'Alice'},
    'metadata': {'timestamp': 1234567890}
}

# This won't crash if 'email' is missing
user_email = api_response.get('user', {}).get('email', 'no-email@example.com')

# Merging configs - super common in real apps
default_config = {'timeout': 30, 'retries': 3, 'debug': False}
user_config = {'timeout': 60, 'debug': True}
default_config.update(user_config)
print(default_config)  # timeout=60, retries=3, debug=True
```

#### Dictionary comprehensions with filtering

This one-liner replaces like 5 lines of code:

```python
grades = {'Alice': 85, 'Bob': 72, 'Charlie': 90, 'Diana': 68}
passed = {name: grade for name, grade in grades.items() if grade >= 70}

# Real-world example: Parsing log files
logs = [
    ('ERROR', 'Database connection failed'),
    ('INFO', 'User logged in'),
    ('ERROR', 'Timeout occurred'),
    ('WARNING', 'Deprecated API used')
]

# Group by severity level
grouped = {}
for level, message in logs:
    grouped.setdefault(level, []).append(message)

print(grouped['ERROR'])  # All error messages in one list
```

---

### Nested Dictionaries (Welcome to Real-World Data)

In actual projects, you're dealing with complex nested structures all the time - configs, API responses, database results. Let's model something realistic.

```python
# Multi-tenant SaaS application structure
organization = {
    'org_id': 'ORG-001',
    'departments': {
        'engineering': {
            'budget': 500000,
            'employees': [
                {'id': 'E001', 'name': 'John', 'role': 'Senior Dev'},
                {'id': 'E002', 'name': 'Jane', 'role': 'Tech Lead'}
            ],
            'projects': {
                'proj_alpha': {'status': 'active', 'deadline': '2025-12-31'},
                'proj_beta': {'status': 'completed', 'deadline': '2025-06-30'}
            }
        },
        'sales': {
            'budget': 300000,
            'employees': [],
            'targets': {'Q1': 100000, 'Q2': 150000}
        }
    }
}
```

Now, how do you safely navigate this? One KeyError and your app crashes.

```python
# Defensive navigation helper
def get_nested(data, *keys, default=None):
    """Navigate nested dicts without fear of KeyError"""
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data

# Usage - no more crashes!
eng_budget = get_nested(organization, 'departments', 'engineering', 'budget')
proj_status = get_nested(organization, 'departments', 'engineering', 
                         'projects', 'proj_alpha', 'status')
missing = get_nested(organization, 'departments', 'marketing', 'budget')  # None
```

**Challenge for you**: Try flattening this nested structure into a single-level dictionary with keys like `'departments_engineering_budget'`. (Hint: use recursion!)

```python
def flatten_dict(d, parent_key='', sep='_'):
    """Your homework: implement this!"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
```

---

### Performance: When Does This Actually Matter?

Let me show you something that'll blow your mind:

```python
import time

# Search in a list with 100k items
data_list = list(range(100000))
data_dict = {i: i for i in range(100000)}

# Finding the last element
start = time.time()
99999 in data_list  # Has to check every element
list_time = time.time() - start

start = time.time()
99999 in data_dict  # Direct hash lookup
dict_time = time.time() - start

print(f"List: {list_time:.6f}s")
print(f"Dict: {dict_time:.6f}s")
print(f"Dict is {list_time/dict_time:.0f}x faster!")
```

On my machine, the dict is literally thousands of times faster. This matters when you're processing millions of records.

**When NOT to use dictionaries:**
- You need ordered sequences → use `list`
- Memory is tight and you have millions of objects → consider `__slots__` or `namedtuple`
- You're storing simple key-value pairs that don't change → `tuple` pairs might be lighter

---

## Part 2: Functions - Writing Production Code

### Let's Talk About Documentation

You know what separates junior devs from senior devs? Documentation. Not just comments - proper docstrings.

```python
def process_transaction(account_id: str, amount: float, 
                       transaction_type: str = 'debit') -> dict:
    """
    Process a financial transaction for an account.
    
    Look, I know writing docs is boring, but 6 months from now when you're
    debugging at 2 AM, you'll thank yourself. Here's what this does:
    
    Args:
        account_id: The account ID (format: ACC-XXXXX)
        amount: Transaction amount in USD (must be positive)
        transaction_type: Either 'debit' or 'credit' (default: 'debit')
    
    Returns:
        dict: Transaction result with these keys:
            - transaction_id: Unique transaction ID
            - status: 'success' or 'failure'
            - balance: New account balance
            - timestamp: When this happened
    
    Raises:
        ValueError: If amount is negative or type is invalid
        AccountNotFoundError: If account doesn't exist
    
    Examples:
        >>> process_transaction('ACC-00123', 100.50, 'debit')
        {'transaction_id': 'TXN-001', 'status': 'success', ...}
    
    Warning:
        Not thread-safe! Use locks if you're doing concurrent transactions.
    """
    # Your code here
    pass
```

See? Anyone can understand what this function does without reading the implementation.

---

### Parameters: Let's Get This Straight Once and For All

This is where people get confused. There's an ORDER to parameters in Python, and you MUST follow it.

**The Golden Rule: positional → default → *args → **kwargs**

```python
def create_user(username, email, age=18, is_active=True, role='user'):
    """Basic parameter types - nothing fancy yet"""
    return {
        'username': username,
        'email': email,
        'age': age,
        'is_active': is_active,
        'role': role
    }

# You can call it different ways:
user1 = create_user('john', 'john@mail.com')
user2 = create_user('jane', 'jane@mail.com', 25)
user3 = create_user('admin', 'admin@mail.com', role='admin', age=30)
```

#### *args - When you don't know how many arguments you'll get

Classic use case: functions that need to work with any number of values.

```python
def calculate_stats(*numbers):
    """
    Pass in as many numbers as you want.
    Common in: logging functions, math operations, aggregations
    """
    if not numbers:
        return None
    
    return {
        'count': len(numbers),
        'sum': sum(numbers),
        'average': sum(numbers) / len(numbers),
        'min': min(numbers),
        'max': max(numbers)
    }

# Works with any number of arguments
stats = calculate_stats(10, 20, 30, 40, 50)

# Or unpack a list
values = [1, 2, 3, 4, 5]
stats = calculate_stats(*values)  # The * unpacks the list
```

#### **kwargs - Dynamic keyword arguments

This is HUGE for building flexible APIs and handling configuration.

```python
def build_query(**filters):
    """
    Build a database query with any filters you want.
    This is how ORMs like SQLAlchemy work internally!
    """
    conditions = []
    for field, value in filters.items():
        conditions.append(f"{field} = '{value}'")
    
    query = "SELECT * FROM users WHERE " + " AND ".join(conditions)
    return query

# Completely flexible
query1 = build_query(status='active', role='admin')
query2 = build_query(age=25, city='New York', verified=True)

# Or pass a dict
filters = {'department': 'engineering', 'level': 'senior'}
query3 = build_query(**filters)  # ** unpacks the dict
```

#### Putting it all together (this is the tricky part)

```python
def api_request(endpoint, method='GET', *args, timeout=30, **headers):
    """
    CRITICAL: The order MUST be:
    1. Required positional (endpoint)
    2. Optional with defaults (method, timeout)
    3. *args
    4. **kwargs (headers)
    
    Mix this up and Python will yell at you!
    """
    print(f"Endpoint: {endpoint}")
    print(f"Method: {method}")
    print(f"Extra args: {args}")
    print(f"Timeout: {timeout}")
    print(f"Headers: {headers}")

# Valid call
api_request('/users', 'POST', 'data1', 'data2', 
            timeout=60, Authorization='Bearer token')
```

#### Python 3.8+ bonus: Force positional or keyword-only

Sometimes you want to enforce HOW people call your function:

```python
def secure_function(api_key, /, username, *, role, permissions):
    """
    api_key: MUST be positional (before the /)
    username: Can be either positional or keyword
    role & permissions: MUST be keyword-only (after the *)
    """
    pass

# Valid
secure_function('secret', 'john', role='admin', permissions=['read'])

# Invalid - Python won't let you
# secure_function(api_key='secret', ...)  # Error! Must be positional
# secure_function('secret', 'john', 'admin', [...])  # Error! role must be keyword
```

Why would you do this? Security. If `api_key` can be passed by name, someone might log it accidentally in `**kwargs`.

---

### Advanced Stuff: Iterators, Generators, Decorators

Okay, this is where things get interesting. These patterns separate decent code from great code.

#### Iterators - Custom looping logic

```python
class DatabaseCursor:
    """
    Imagine fetching 1 million rows from a database.
    You can't load them all into memory at once!
    So you fetch them in chunks (pages).
    """
    def __init__(self, query, page_size=100):
        self.query = query
        self.page_size = page_size
        self.current_page = 0
        self.total_pages = 10  # In reality, you'd get this from the DB
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_page >= self.total_pages:
            raise StopIteration
        
        # Fetch next page from database
        results = [f"Record {i}" for i in range(
            self.current_page * self.page_size,
            (self.current_page + 1) * self.page_size
        )]
        self.current_page += 1
        return results

# Usage - looks like a normal loop!
cursor = DatabaseCursor("SELECT * FROM huge_table")
for page in cursor:
    print(f"Processing {len(page)} records...")
    # Process this page before fetching the next one
```

#### Generators - Same idea, simpler syntax

Generators are iterators but way easier to write. Use `yield` instead of `return`.

```python
def read_large_file(filepath):
    """
    Reading a 10GB log file? No problem.
    Only one line in memory at a time.
    """
    with open(filepath, 'r') as file:
        for line in file:
            yield line.strip()

# Process a massive file without running out of memory
error_count = 0
for line in read_large_file('huge_app.log'):
    if 'ERROR' in line:
        error_count += 1
        print(line)
```

**Generator expressions** - like list comprehensions but lazy:

```python
# This creates a list of 1 million numbers (uses memory!)
squares_list = [x**2 for x in range(1000000)]

# This creates a generator (uses almost no memory!)
squares_gen = (x**2 for x in range(1000000))

# Compute values only when needed
first_ten = [next(squares_gen) for _ in range(10)]
```

Here's a classic interview question: Fibonacci with generators

```python
def fibonacci(limit=None):
    """
    Generate Fibonacci sequence.
    If limit is None, this is infinite!
    """
    a, b = 0, 1
    count = 0
    while limit is None or count < limit:
        yield a
        a, b = b, a + b
        count += 1

# Get first 10 Fibonacci numbers
for num in fibonacci(10):
    print(num, end=' ')
# Output: 0 1 1 2 3 5 8 13 21 34
```

#### Decorators - Modify functions without changing them

This is Python magic. Decorators let you wrap functions to add functionality.

```python
import time
from functools import wraps

def timing_decorator(func):
    """Measure how long a function takes - super useful for optimization"""
    @wraps(func)  # Preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# Using the decorator
@timing_decorator
def slow_function():
    time.sleep(2)
    return "Done!"

# When you call slow_function(), it's actually wrapped!
slow_function()  # Prints timing info automatically
```

**Decorators with parameters** - now it gets fancy:

```python
def retry(max_attempts=3):
    """Retry a function if it fails - common for network calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise  # Last attempt failed, give up
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
        return wrapper
    return decorator

# Stack decorators - they apply bottom to top!
@timing_decorator
@retry(max_attempts=3)
def fetch_data(url):
    """Simulated API call that might fail"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network blip")
    return {"data": "success"}

# Calling this will retry up to 3 times AND time the total duration
result = fetch_data("https://api.example.com/data")
```

**Real-world decorator patterns** you'll see everywhere:

```python
# Authentication check
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_user_logged_in():
            raise PermissionError("Login required")
        return func(*args, **kwargs)
    return wrapper

# Caching results (memoization)
def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def expensive_calculation(n):
    """First call is slow, subsequent calls are instant"""
    time.sleep(2)  # Simulate expensive work
    return n ** 2

print(expensive_calculation(5))  # Takes 2 seconds
print(expensive_calculation(5))  # Instant! Returns cached result

# Logging every function call
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"→ Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"← {func.__name__} returned {result}")
        return result
    return wrapper
```

---

## Part 3: Let's Code!

Alright, theory is great, but let's put this into practice. Here are three challenges that'll test what you've learned.

### Challenge 1: Build a Smart Cache

```python
"""
Create a caching system that:
1. Stores API responses with timestamps
2. Automatically expires entries older than 5 minutes
3. Tracks cache hits and misses
4. Uses setdefault(), pop(), and other dict methods we learned

Bonus: Add a decorator to cache function results automatically
"""
```

### Challenge 2: Configuration Manager

```python
"""
Build a config system that:
1. Accepts multiple config files as *args
2. Allows runtime overrides with **kwargs
3. Validates required fields (use a decorator!)
4. Uses a generator to yield any validation errors
5. Has proper docstrings with type hints

Think about how Flask or Django handle configuration!
"""
```

### Challenge 3: Log Analysis Tool

```python
"""
Real-world scenario - you have a 1GB log file:
1. Create an iterator that reads the file line by line
2. Use a generator to filter only ERROR and CRITICAL logs
3. Build a dictionary of error counts grouped by error type
4. Add a timing decorator to measure performance
5. Implement retry logic for file access

Memory constraint: Your program should use < 100MB RAM 
even with a 1GB file!
"""
```

Take 30 minutes, work in pairs if you want. I'll come around to help. Don't worry about getting it perfect - the goal is to practice combining these concepts.

---

## Wrap-Up: What You Should Remember

### Dictionaries
- They're fast (O(1)) because of hashing - understand WHY
- Use `.get()` and `.setdefault()` to write defensive code
- Master all the methods: items(), keys(), values(), update(), pop()
- Nested dicts are everywhere in real projects - learn to navigate them safely
- Know when to use dicts vs. other data structures

### Functions  
- Write docstrings! Your future self will thank you
- Parameter order: positional → default → *args → **kwargs (memorize this!)
- Use type hints for better code clarity
- Generators save memory when dealing with large datasets
- Decorators let you enhance functions without modifying them

### The Production Mindset
- Performance matters: Think about O(1) vs O(n)
- Memory matters: Generators > lists for big data
- Reusability matters: DRY (Don't Repeat Yourself)
- Safety matters: Always handle edge cases

---

## What's Next?

Next session we're covering:
- Object-Oriented Programming (classes, inheritance, the works)
- Context managers (the `with` statement)
- Error handling that doesn't suck

Come prepared with questions! And seriously, practice the challenges - you learn by doing, not by watching me code.

## Resources

If you want to dig deeper:
- PEP 8: Python Style Guide (how to write clean code)
- PEP 257: Docstring Conventions
- Check out Python's `collections` module: defaultdict, Counter, OrderedDict
- The `functools` module: wraps, lru_cache, partial
- Learn Big O notation if you haven't already

Got questions? Slack me anytime. Now let's start coding!
