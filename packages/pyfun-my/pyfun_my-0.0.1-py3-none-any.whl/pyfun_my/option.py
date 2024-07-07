from typing import Optional, Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class Option:
    def __init__(self, value: Optional[T]):
        self._value = value

    def map(self, func: Callable[[T], U]) -> 'Option[U]':
        if self._value is None:
            return Option(None)
        else:
            return Option(func(self._value))

    def flat_map(self, func: Callable[[T], Optional[U]]) -> 'Option[U]':
        if self._value is None:
            return Option(None)
        else:
            return func(self._value)

    def filter(self, func: Callable[[T], bool]) -> 'Option':
        if self._value is None or not func(self._value):
            return Option(None)
        else:
            return self

    def get_or_else(self, default_value: U) -> U:
        return self._value if self._value is not None else default_value

    def is_some(self) -> bool:
        return self._value is not None

    def is_none(self) -> bool:
        return self._value is None

    def to_optional(self) -> Optional[T]:
        return self._value

    def fold(self, if_none: Callable[[], U], if_present: Callable[[T], U]) -> U:
        if self._value is None:
            return if_none()
        else:
            return if_present(self._value)


# Example usage
def increment(x: int) -> int:
    return x + 1


def square_root(x: int) -> Optional[float]:
    if x >= 0:
        return x ** 0.5
    else:
        return None


if __name__ == "__main__":

    value: Optional[int] = 4

    result = (
        Option(value)
        .map(increment)
        .flat_map(square_root)
        .get_or_else(0.0)
    )

    print(result)  # Output: 2.0
