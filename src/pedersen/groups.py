from __future__ import annotations

from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Union

from asn1crypto.core import Asn1Value

import asn1 as _asn1


class PreGroup(ABC):
    """
    Additive group of integers modulo a prime.
    """

    @abstractmethod
    def __call__(self, value: Union[int, Asn1Value, Fraction]) -> PreGroupValue:
        """
        Convert an integer into a group element

        Returns:
            Group element
        """

    @property
    @abstractmethod
    def len(self) -> int:
        """
        Get number of elements in this group

        Returns:
            group size
        """

    @property
    @abstractmethod
    def rand(self) -> PreGroupValue:
        """
        Create random element of this group

        Returns:
            Random group element
        """

    @property
    @abstractmethod
    def rand_nonzero(self) -> PreGroupValue:
        """
        Create random element of this group, but never the neutral element.

        Returns:
            Random group element
        """

    @abstractmethod
    def __repr__(self) -> str:
        """
        Outputs a representation of this group.

        Returns:
            Representation of this group
        """


class PreGroupValue(ABC):
    """
    Abstract pre-group value, e.g. some private key.
    """

    group: PreGroup

    @abstractmethod
    def __int__(self) -> int:
        """
        Implement int(a)

        Returns:
            value
        """

    @abstractmethod
    def __neg__(self) -> PreGroupValue:
        """
        Implement -a

        Returns:
            inverse value
        """

    @abstractmethod
    def __add__(self, other: PgvOrInt) -> PreGroupValue:
        """
        Implement a + b

        Args:
            other: Second operand

        Returns:
            Sum of `self` and `other`
        """

    def __radd__(self, other: PgvOrInt) -> PreGroupValue:
        """
        Implement b + a

        Args:
            other: First operand

        Returns:
            Sum of `other` and `self`
        """

        return self.__add__(other)

    @abstractmethod
    def __mul__(self, other: PgvOrInt) -> PreGroupValue:
        """
        Implement a * b

        Args:
            other: Second operand

        Returns:
            Product of `self` and `other`
        """

    def __rmul__(self, other: PgvOrInt) -> PreGroupValue:
        """
        Implement b * a

        Args:
            other: First operand

        Returns:
            Product of `other` and `self`
        """

        return self.__mul__(other)

    @property
    @abstractmethod
    def inv(self) -> PreGroupValue:
        """
        Implement multiplicative inverse such that inv(x) * x == 1

        Returns:
            Multiplicative inverse of `self`
        """

    @abstractmethod
    def __repr__(self) -> str:
        """
        Outputs a representation of this value.

        Returns:
            Representation of this value
        """

    @property
    @abstractmethod
    def asn1(self) -> _asn1.PreGroupValue:
        """
        Convert value to an ASN.1 type so it can be serialized to DER.

        Returns:
            Value converted to an ASN.1 value
        """


PgvOrInt = Union[PreGroupValue, int]
