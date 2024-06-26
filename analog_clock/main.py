import cv2
import numpy as np
from typing import Callable, Tuple
import math
from datetime import datetime

RADIUS_1: float = 250
RADIUS_2: float = 220
CENTER: tuple[int, int] = (400, 400)


# FORMAT BGR ??
color = {
    "GREEN": (0, 255, 0),
    "BLUE": (255, 0, 0),
    "RED": (0, 0, 255),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
}

combine_colors: Callable[[str, str], Tuple[int, ...]] = lambda a, b: tuple(
    map(int, (np.array(color[a]) * 0.5 + np.array(color[b]) * 0.5))
)


# Can Simulate Different Centers and radius so those sections are provided
def draw_markers(
    img,
    markers,
    thickness,
    center=CENTER,
    radi_1: float = RADIUS_1,
    radi_2: float = RADIUS_2,
    color=color["BLACK"],
):
    add_points = lambda tup_1, tup_2: tuple(map(int, np.array(tup_1) + np.array(tup_2)))
    for angle in markers:

        if 0 <= math.degrees(angle) <= 90 or 270 <= math.degrees(angle) <= 360:
            y_inc_r1 = math.sin(angle) * radi_1
            y_inc_r2 = math.sin(angle) * radi_2
            x_inc_r1 = math.sqrt(radi_1**2 - y_inc_r1**2)
            x_inc_r2 = math.sqrt(radi_2**2 - y_inc_r2**2)
            cv2.line(
                img=img,
                pt1=add_points(center, (x_inc_r1, y_inc_r1)),
                pt2=add_points(center, (x_inc_r2, y_inc_r2)),
                color=color,
                thickness=thickness,
                lineType=cv2.LINE_AA,
            )
        else:
            y_inc_r1 = math.sin((angle + math.pi) % (2 * math.pi)) * radi_1
            y_inc_r2 = math.sin((angle + math.pi) % (2 * math.pi)) * radi_2
            x_inc_r1 = math.sqrt(radi_1**2 - y_inc_r1**2)
            x_inc_r2 = math.sqrt(radi_2**2 - y_inc_r2**2)
            cv2.line(
                img=img,
                pt1=add_points(center, (-x_inc_r1, -y_inc_r1)),
                pt2=add_points(center, (-x_inc_r2, -y_inc_r2)),
                color=color,
                thickness=thickness,
                lineType=cv2.LINE_AA,
            )


def show_image(img):
    cv2.imshow("Clock", img)


def display_time(img):
    sec = 0
    while True:
        img_new = img.copy()
        current_time = datetime.now()
        hour = (((current_time.hour - 3) % 12 ) * 30)%360
        minute = ((current_time.minute - 15) * 6) % 360
        second = ((current_time.second - 15) * 6) % 360
        if second != sec:
            print(
                "CURRENT TIME :  HOUR : ",
                hour,
                "   SECOND :",
                second,
                "MINUTE :",
                minute,
            )
        sec = second
        draw_markers(
            img=img_new,
            markers=[math.radians(hour)],
            thickness=10,
            radi_1=(RADIUS_1 * 0.01),
            radi_2=(RADIUS_2 * 0.4),
            color=color["BLUE"],
        )
        draw_markers(
            img=img_new,
            markers=[math.radians(minute)],
            thickness=10,
            radi_1=(RADIUS_1 * 0.01),
            radi_2=(RADIUS_2 * 0.6),
            color=color["GREEN"],
        )
        draw_markers(
            img=img_new,
            markers=[math.radians(second)],
            thickness=10,
            radi_1=(RADIUS_1 * 0.01),
            radi_2=(RADIUS_2 * 0.8),
            color=color["RED"],
        )
        cv2.putText(
            img_new,
            f"{current_time.hour}:{current_time.minute}:{current_time.second}",
            (250, 750),
            cv2.FONT_HERSHEY_TRIPLEX,
            2,
            combine_colors("BLACK", "WHITE"),
            1,
            cv2.LINE_AA,
        )

        cv2.circle(
            img_new,
            CENTER,
            int(RADIUS_1 * 0.03),
            color["BLACK"],
            thickness=10,
            lineType=cv2.LINE_AA,
        )

        cv2.circle(
            img_new,
            CENTER,
            int(RADIUS_1 * 0.001),
            color["WHITE"],
            thickness=10,
            lineType=cv2.LINE_AA,
        )

        show_image(img_new)

        if cv2.waitKey(1) == ord("q"):
            break


def main():
    img = np.ones((800, 800, 3), np.uint8) * 255
    # Big Circle
    cv2.circle(
        img, CENTER, int(RADIUS_1), color["BLACK"], thickness=20, lineType=cv2.LINE_AA
    )

    # Small Circle
    # cv2.circle(img,CENTER ,RADIUS_2,combine_colors('BLACK','WHITE'),thickness=2,lineType=cv2.LINE_AA)

    # 12 tick_sections  angles
    hour_markers: list[float] = [math.radians(i * 360 / 12) for i in range(12)]
    minute_markers = [math.radians(360 / 60 * i) for i in range(60)]

    draw_markers(img, hour_markers, thickness=10)
    draw_markers(img, minute_markers, thickness=1)

    display_time(img)


if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
