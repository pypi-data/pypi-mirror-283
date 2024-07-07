# Logical Expression Framework

This module provides a flexible and extensible framework for creating and evaluating logical expressions in Python. It allows you to construct complex logical structures using basic logical operators and custom-defined operators.

## Features

- Abstract base class `LogicalExpression` for creating logical expressions
- Built-in logical operators: AND, OR, NOT, XOR, IMPLIES
- Support for custom logical operators
- Operator overloading for intuitive expression construction
- Type hinting for better code readability and IDE support

## Installation

```poetry add qrev-logex```

## Usage

### Basic Usage

```python
from logical_expression import LogicalExpression, And, Or, Not, Xor, Implies

# Define some simple logical expressions
class A(LogicalExpression):
    def evaluate(self, x):
        return x > 0

class B(LogicalExpression):
    def evaluate(self, x):
        return x < 10

# Construct a complex expression
expr = (A() & B()) | ~A()

# Evaluate the expression
result = expr.evaluate(5)  # True

# Alternative
a = A()
b = B()
c = C()

expr = (a | (b & c) )
result = expr.evaluate(5)  # True

```

### Custom Operators

You can create custom logical operators using the `custom_operator` function:

```python
from logical_expression import custom_operator

# Define a custom NAND operator
nand = custom_operator("Nand", lambda a, b: not (a and b))

# Use the custom operator in expressions
expr = nand(A(), B())
```

## API Reference

### Classes

- `LogicalExpression`: Abstract base class for logical expressions
- `And`: Represents logical AND operation
- `Or`: Represents logical OR operation
- `Not`: Represents logical NOT operation
- `Xor`: Represents logical XOR operation
- `Implies`: Represents logical IMPLIES operation

### Functions

- `custom_operator(name: str, func: Callable[[bool, bool], bool]) -> Callable`: Creates a custom logical operator

