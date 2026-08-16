# Lesson 01 — Running Python

> Python for Cloud & DevOps Engineering

---

## 1. Where I Am in the Roadmap

This is the first lesson of the Python for DevOps roadmap.

```text
Python for DevOps
│
├── Phase 1 — Python Fundamentals
├── Phase 2 — Python Automation
├── Phase 3 — DevOps Python
└── Phase 4 — Professional Python
```

The goal of this lesson is not to learn lots of Python syntax.

The goal is to understand the basic workflow:

```text
Write Python code
       ↓
Save it in a .py file
       ↓
Open Linux terminal
       ↓
Run the file with Python 3
       ↓
See the output
```

---

# 2. What Is Python?

Python is a programming language.

A programming language allows us to give instructions to a computer in a form that humans can write and understand.

For example:

```python
print("Hello, Python!")
```

This tells Python to display:

```text
Hello, Python!
```

Python is useful for DevOps because it can be used to automate repetitive infrastructure and system tasks.

Examples of tasks we will eventually automate:

- Managing files
- Checking servers
- Running Linux commands
- Reading logs
- Calling APIs
- Working with AWS
- Managing cloud resources
- Collecting monitoring information
- Automating deployment tasks

---

# 3. Why Are We Learning Python for DevOps?

The goal of this course is not to become a backend web developer.

Python will be used as an automation tool.

A DevOps engineer might have a repetitive task such as:

```text
Find 100 log files
       ↓
Check their contents
       ↓
Find errors
       ↓
Generate a report
```

Doing this manually is inefficient.

Python can automate the process:

```text
Python script
      ↓
Find files
      ↓
Read files
      ↓
Analyze data
      ↓
Generate report
```

Later, Python will also communicate with APIs and cloud platforms.

For example:

```text
Python
   ↓
AWS API
   ↓
EC2 instances
   ↓
Get information
   ↓
Process information
   ↓
Take action
```

We will learn these capabilities gradually.

---

# 4. Our First Python Program

Our first program is:

```python
print("Hello, Python!")
```

The program contains a function called `print()`.

---

# 5. Understanding `print()`

`print()` is a built-in Python function used to display information.

Example:

```python
print("Hello, Python!")
```

The general structure is:

```text
print("text")
  │      │
  │      └── text we want to display
  │
  └── Python's print function
```

The parentheses `()` are used to provide information to the function.

The text is surrounded by quotation marks:

```python
"Hello, Python!"
```

This is called a **string**.

We will study strings and data types properly in later lessons.

---

# 6. What Is a `.py` File?

Python source code is commonly stored in files ending with:

```text
.py
```

For example:

```text
hello.py
backup.py
server_check.py
log_analyzer.py
```

The `.py` extension tells us that the file contains Python source code.

Our first file was:

```text
hello.py
```

It contained:

```python
print("Hello, Python!")
```

---

# 7. Creating a Python File on Linux

We used the Linux terminal to navigate to our lesson directory.

Example:

```bash
cd ~/my-journey/devops-journey/python-for-devops/Python-lessons/Lesson-01-Running-Python
```

Then we created a file:

```bash
touch hello.py
```

`touch` is a Linux command that can create an empty file.

We then opened the file using an editor and wrote our Python code.

---

# 8. Running a Python Program

We ran our program with:

```bash
python3 hello.py
```

The command can be understood as:

```text
python3
   │
   └── Python 3 interpreter

hello.py
   │
   └── Python file to execute
```

Python reads the instructions in the file and executes them.

Our output was:

```text
Hello, Python!
```

---

# 9. What Does `python3` Mean?

`python3` refers to the Python 3 interpreter available on our Linux system.

The interpreter is the program that reads our Python source code and executes it.

When we run:

```bash
python3 hello.py
```

we are essentially saying:

> "Use Python 3 to execute this Python file."

We will study how Python executes programs internally in more detail later.

At this stage, we only need to understand the practical workflow.

---

# 10. Python Interpreter

The Python interpreter is the program responsible for executing Python code.

Conceptually:

```text
hello.py
   │
   │ Python source code
   ↓
Python 3 interpreter
   │
   ↓
Computer executes instructions
   │
   ↓
Output
```

For example:

```python
print("Hello, Python!")
```

becomes:

```text
Python interpreter
       ↓
Execute print()
       ↓
Display text
       ↓
Hello, Python!
```

We will revisit Python's internal execution model later after we have written several programs.

---

# 11. Linux and Python

Python and Linux work extremely well together.

A DevOps engineer commonly works from a Linux terminal.

For example:

```bash
python3 script.py
```

A Python script can eventually:

- Read files
- Create directories
- Run Linux commands
- Inspect processes
- Read environment variables
- Analyze logs
- Communicate with servers
- Call APIs
- Automate cloud resources

This is one reason Python is useful for DevOps.

---

