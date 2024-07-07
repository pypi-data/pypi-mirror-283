from setuptools import setup, find_packages

setup(
    name="passwordguard",
    version="1.0",
    packages=find_packages(),
    author="Shankhosuvro Ghosh",
    author_email="shankhosuvro.ghosh@gmail.com",
    description="passwordguard: A library for evaluating password strength and estimating cracking time.",
    long_description="""
passwordguard 1.0

A library for evaluating password strength and estimating cracking time.

To install use pip install passwordguard

---

### passwordguard

passwordguard is a Python library that provides functionalities to assess the strength of passwords based on length, character sets, and common patterns. It also estimates the time required to crack a password using brute-force methods. Use passwordguard to enhance security measures in your applications by ensuring stronger passwords.

passwordguard includes two main functions:
- `passwordguard.calculate_password_strength` evaluates the strength of a given password.
- `passwordguard.calculate_cracking_time` estimates the time required to crack a given password.

#### Example

Here is an example of how to use the passwordguard library in your Python programs:

```python
from passwordguard import calculate_password_strength, calculate_cracking_time

strength = calculate_password_strength(password)
cracking_time = calculate_cracking_time(password)

print(f"Password: {password} - Strength: {strength} - Estimated Cracking Time: {cracking_time}")
""",
    long_description_content_type="text/plain",
    url="https://github.com/Shankhosuvro-G/FortifyPass",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)
