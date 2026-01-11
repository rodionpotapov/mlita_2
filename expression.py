from dataclasses import dataclass
from Deduction import *
from main import *
from proofs import *
from proof import *

class Expression:
    pass


@dataclass(frozen=True)
class Variable(Expression):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Implication(Expression):
    left: Expression
    right: Expression

    def __str__(self) -> str:
        return f"({self.left} -> {self.right})"


@dataclass(frozen=True)
class Negation(Expression):
    operand: Expression

    def __str__(self) -> str:
        return f"¬{self.operand}"


def implies(left: Expression, other: Expression) -> Implication:
    return Implication(left, other)


def expr_or(left: Expression, other: Expression) -> Expression:
    return implies(Negation(left), other)


def expr_and(left: Expression, other: Expression) -> Expression:
    return Negation(implies(left, Negation(other)))


def v(name: str) -> Variable:
    return Variable(name)


def _expr_implies(self: Expression, other: Expression) -> Implication:
    return Implication(self, other)


