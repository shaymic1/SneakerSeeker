from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Results:
    seeker_start: float = 0
    sneaker_start: float = 0
    seekers_left: float = 0
    sneaker_left: float = 0

    @property
    def percentage(self) -> float:
        if self.sneaker_left > 0:
            return 100 * (self.sneaker_start - self.sneaker_left) / self.sneaker_start
        return 100

    def __str__(self):
        return f"start: {self.sneaker_start}\tleft: {self.sneaker_left}\tpercentage: {self.percentage}"

    def __truediv__(self, other: int) -> Results:
        if other == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return Results(
            seeker_start=self.seeker_start / other,
            sneaker_start=self.sneaker_start / other,
            seekers_left=self.seekers_left / other,
            sneaker_left=self.sneaker_left / other
        )

    def __itruediv__(self, other: int) -> Results:
        if other == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        self.seeker_start /= other
        self.sneaker_start /= other
        self.seekers_left /= other
        self.sneaker_left /= other
        return self

    def __iadd__(self, other: Results) -> Results:
        self.seeker_start += other.seeker_start
        self.sneaker_start += other.sneaker_start
        self.seekers_left += other.seekers_left
        self.sneaker_left += other.sneaker_left
        return self