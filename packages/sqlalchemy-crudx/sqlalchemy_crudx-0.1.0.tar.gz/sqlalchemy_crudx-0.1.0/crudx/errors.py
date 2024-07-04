#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CRUDException(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class ModelColumnError(CRUDException):
    """Error raised when an SCP column is invalid."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class SelectExpressionError(CRUDException):
    """Error raised when a select expression is invalid."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class FilterExpressionError(CRUDException):
    """Error raised when a filter expression is invalid."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class SortExpressionError(CRUDException):
    """Error raised when a sort expression is invalid."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class JoinExpressionError(CRUDException):
    """Error raised when a join expression is invalid."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)