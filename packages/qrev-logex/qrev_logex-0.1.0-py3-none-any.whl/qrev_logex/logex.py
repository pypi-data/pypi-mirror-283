from abc import ABC, abstractmethod
from typing import Callable, Union, Any


class LogicalExpression(ABC):
    """
    Abstract base class for logical expressions.

    This class defines the interface for logical expressions and provides
    basic logical operations through operator overloading.
    """

    @abstractmethod
    def evaluate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Evaluate the logical expression.

        Args:
            *args: Positional arguments for evaluation.
            **kwargs: Keyword arguments for evaluation.

        Returns:
            bool: The result of the logical expression evaluation.
        """
        ...

    def __and__(self, other: Union["LogicalExpression", type["LogicalExpression"]]) -> "And":
        """Implement the logical AND operation."""
        return And(self, other)

    def __or__(self, other: Union["LogicalExpression", type["LogicalExpression"]]) -> "Or":
        """Implement the logical OR operation."""
        return Or(self, other)

    def __invert__(self) -> "Not":
        """Implement the logical NOT operation."""
        return Not(self)

    def __xor__(self, other: Union["LogicalExpression", type["LogicalExpression"]]) -> "Xor":
        """Implement the logical XOR operation."""
        return Xor(self, other)

    def __rshift__(self, other: Union["LogicalExpression", type["LogicalExpression"]]) -> "Implies":
        """Implement the logical IMPLIES operation."""
        return Implies(self, other)


class And(LogicalExpression):
    """
    Represents a logical AND operation.
    """

    def __init__(self, *args: Union[LogicalExpression, type[LogicalExpression]]):
        """
        Initialize an AND operation with multiple arguments.

        Args:
            *args: LogicalExpression instances or types to be AND-ed together.
        """
        self.args = list(args)

    def evaluate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Evaluate the AND operation.

        Returns True if all arguments evaluate to True, False otherwise.
        """
        return all(
            (
                arg().evaluate(*args, **kwargs)
                if isinstance(arg, type)
                else arg.evaluate(*args, **kwargs)
            )
            for arg in self.args
        )


class Or(LogicalExpression):
    """
    Represents a logical OR operation.
    """

    def __init__(self, *args: Union[LogicalExpression, type[LogicalExpression]]):
        """
        Initialize an OR operation with multiple arguments.

        Args:
            *args: LogicalExpression instances or types to be OR-ed together.
        """
        self.args = list(args)

    def evaluate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Evaluate the OR operation.

        Returns True if any argument evaluates to True, False otherwise.
        """
        return any(
            (
                arg().evaluate(*args, **kwargs)
                if isinstance(arg, type)
                else arg.evaluate(*args, **kwargs)
            )
            for arg in self.args
        )


class Not(LogicalExpression):
    """
    Represents a logical NOT operation.
    """

    def __init__(self, arg: Union[LogicalExpression, type[LogicalExpression]]):
        """
        Initialize a NOT operation.

        Args:
            arg: The LogicalExpression instance or type to be negated.
        """
        self.arg = arg

    def evaluate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Evaluate the NOT operation.

        Returns the logical negation of the argument's evaluation.
        """
        return not (
            self.arg().evaluate(*args, **kwargs)
            if isinstance(self.arg, type)
            else self.arg.evaluate(*args, **kwargs)
        )


class Xor(LogicalExpression):
    """
    Represents a logical XOR operation.
    """

    def __init__(
        self,
        left: Union[LogicalExpression, type[LogicalExpression]],
        right: Union[LogicalExpression, type[LogicalExpression]],
    ):
        """
        Initialize an XOR operation.

        Args:
            left: The left operand (LogicalExpression instance or type).
            right: The right operand (LogicalExpression instance or type).
        """
        self.left = left
        self.right = right

    def evaluate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Evaluate the XOR operation.

        Returns True if exactly one of the operands evaluates to True, False otherwise.
        """
        left_result = (
            self.left().evaluate(*args, **kwargs)
            if isinstance(self.left, type)
            else self.left.evaluate(*args, **kwargs)
        )
        right_result = (
            self.right().evaluate(*args, **kwargs)
            if isinstance(self.right, type)
            else self.right.evaluate(*args, **kwargs)
        )
        return left_result != right_result


class Implies(LogicalExpression):
    """
    Represents a logical IMPLIES operation.
    """

    def __init__(
        self,
        antecedent: Union[LogicalExpression, type[LogicalExpression]],
        consequent: Union[LogicalExpression, type[LogicalExpression]],
    ):
        """
        Initialize an IMPLIES operation.

        Args:
            antecedent: The antecedent (LogicalExpression instance or type).
            consequent: The consequent (LogicalExpression instance or type).
        """
        self.antecedent = antecedent
        self.consequent = consequent

    def evaluate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Evaluate the IMPLIES operation.

        Returns True if the antecedent is False or both antecedent and consequent are True.
        """
        antecedent_result = (
            self.antecedent().evaluate(*args, **kwargs)
            if isinstance(self.antecedent, type)
            else self.antecedent.evaluate(*args, **kwargs)
        )
        if not antecedent_result:
            return True
        consequent_result = (
            self.consequent().evaluate(*args, **kwargs)
            if isinstance(self.consequent, type)
            else self.consequent.evaluate(*args, **kwargs)
        )
        return consequent_result


def custom_operator(
    name: str, func: Callable[[bool, bool], bool]
) -> Callable[[LogicalExpression, LogicalExpression], LogicalExpression]:
    """
    Create a custom logical operator.

    Args:
        name: The name of the custom operator.
        func: A function that takes two boolean arguments and returns a boolean.

    Returns:
        A function that creates a new LogicalExpression subclass implementing the custom operator.
    """

    class CustomOperator(LogicalExpression):
        def __init__(
            self,
            left: Union[LogicalExpression, type[LogicalExpression]],
            right: Union[LogicalExpression, type[LogicalExpression]],
        ):
            self.left = left
            self.right = right

        def evaluate(self, *args: Any, **kwargs: Any) -> bool:
            left_result = (
                self.left().evaluate(*args, **kwargs)
                if isinstance(self.left, type)
                else self.left.evaluate(*args, **kwargs)
            )
            right_result = (
                self.right().evaluate(*args, **kwargs)
                if isinstance(self.right, type)
                else self.right.evaluate(*args, **kwargs)
            )
            return func(left_result, right_result)

    CustomOperator.__name__ = name
    return lambda left, right: CustomOperator(left, right)
