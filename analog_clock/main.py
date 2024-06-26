import cv2
import numpy as np
from typing import Callable, Tuple
import math

RADIUS_1 = 250
RADIUS_2 = 220
CENTER: tuple[int, int] = (400, 400)

color = {
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "RED": (255, 0, 0),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
}

combine_colors: Callable[[str, str], Tuple[int, ...]] = lambda a, b: tuple(
    map(int, (np.array(color[a]) * 0.5 + np.array(color[b]) * 0.5))
)


# Can Simulate Different Centers and radius so those sections are provided
def draw_markers(
    img, markers, thickness, center=CENTER, radi_1=RADIUS_1, radi_2=RADIUS_2
):
    add_points = lambda tup_1, tup_2: tuple(map(int, np.array(tup_1) + np.array(tup_2)))
    for angle in markers:
        print("Angles", angle)
        y_inc_r1 = math.sin(angle) *radi_1
        y_inc_r2 = math.sin(angle) * radi_2
        x_inc_r1 = math.sqrt(radi_1**2 - y_inc_r1**2)
        x_inc_r2 = math.sqrt(radi_2**2 - y_inc_r2**2)
        if (0<=math.degrees(angle)<=90 or 270<=math.degrees(angle)<=360):
            cv2.line(
                img=img,
                pt1=add_points(center, (x_inc_r1, y_inc_r1)),
                pt2=add_points(center, (x_inc_r2, y_inc_r2)),
                color=color["BLACK"],
                thickness=thickness,
                lineType=cv2.LINE_AA
            )
        else:
            cv2.line(
                img=img,
                pt1=add_points(center, (-x_inc_r1, -y_inc_r1)),
                pt2=add_points(center, (-x_inc_r2, -y_inc_r2)),
                color=color["BLACK"],
                thickness=thickness,
                lineType=cv2.LINE_AA
            )



def show_image(img):
    cv2.imshow("Clock", img)
    cv2.waitKey(delay=0)
    cv2.destroyAllWindows()


def main():
    img = np.ones((800, 800, 3), np.uint8) * 255
    # Big Circle
    cv2.circle(
        img, CENTER, RADIUS_1, color["BLACK"], thickness=20, lineType=cv2.LINE_AA
    )
    # Small Circle
    # cv2.circle(img,CENTER ,RADIUS_2,combine_colors('BLACK','WHITE'),thickness=2,lineType=cv2.LINE_AA)

    # 12 tick_sections  angles
    hour_markers:list[float]=[ math.radians(i*360/12) for i in range(12)]
    minute_markers=[math.radians(360/60* i) for i in range(60)]

    draw_markers(img, hour_markers, thickness=10)
    draw_markers(img,minute_markers, thickness=1)
    return img


if __name__ == "__main__":
    show_image(main())
