from dataclasses import dataclass


# Định nghĩa vị trí theo ô (x;y)

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    # Phép cộng hai điểm
    def __add__(self, p1: "Point")-> "Point":
        return Point(self.x + p1.x, self.y + p1.y)
    

    # Nhân tọa độ với một số thực vô hướng
    def __mul__(self, scalar: int) -> "Point":
        return Point(self.x * scalar, self.y * scalar)
    

    __radd__ = __add__
    __rmul__ = __mul__