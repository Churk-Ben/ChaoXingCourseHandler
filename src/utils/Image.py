import os
from tokenize import String
import cv2
from PIL import Image
import numpy as np
import easyocr
from shapely import points


class UnitImage:
    """
    Pillow和OpenCV联合图像类
    用于无缝结合两种图像类型
    """

    def __init__(self, pil_img: Image.Image, cv2_img: np.ndarray):
        self.pil = pil_img
        self.cv2 = cv2_img

    @staticmethod
    def from_path(img_path):
        if not os.path.isfile(img_path):
            raise FileNotFoundError(f"图像文件不存在: {img_path}")
        pil_img = Image.open(img_path).convert("RGB")
        cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        return UnitImage(pil_img, cv2_img)

    @staticmethod
    def from_pil(pil_img):
        cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        return UnitImage(pil_img, cv2_img)

    @staticmethod
    def from_cv2(cv2_img):
        pil_img = Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
        return UnitImage(pil_img, cv2_img)

    def to_grayscale(self):
        gray_cv2 = cv2.cvtColor(self.cv2, cv2.COLOR_BGR2GRAY)
        gray_pil = self.pil.convert("L")
        return UnitImage(gray_pil, gray_cv2)

    def save(self, path):
        self.pil.save(path)

    def show(self):
        self.pil.show()

    def size(self):
        return self.pil.size


class ImageProccecor:
    """
    图像处理类
    """

    @staticmethod
    def match_template(
        source_img: UnitImage,
        template_img: UnitImage,
        threshold=0.8,
        top_n=1,
    ):
        """最基本的模板识别"""
        res = cv2.matchTemplate(source_img.cv2, template_img.cv2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        points = list(zip(*loc[::-1]))
        if points:
            if top_n == 1:
                return points[0]
            elif top_n < len(points):
                return points[:top_n]
            else:
                return points
        else:
            return None

    @staticmethod
    def match_img(
        source_img: UnitImage,
        template_img: UnitImage,
        threshold=0.8,
        top_n=1,
    ):
        """用于静态常不变的图像识别"""
        res = cv2.matchTemplate(source_img.cv2, template_img.cv2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        points = list(zip(*loc[::-1]))

        # 计算中心
        center_points = []
        for pt in points:
            center_x = pt[0] + template_img.cv2.shape[1] // 2
            center_y = pt[1] + template_img.cv2.shape[0] // 2
            center_points.append((center_x, center_y))
        points = center_points

        if points:
            if top_n == 1:
                return points[0]
            elif top_n < len(points):
                return points[:top_n]
            else:
                return points
        else:
            return None

    @staticmethod
    def match_text(
        source_img: UnitImage,
        template_text: str,
        threshold=0.6,
        top_n=1,
    ):
        """用于忽视字体的文字识别"""
        reader = easyocr.Reader(["ch_sim", "en"])
        points = []

        results = reader.readtext(
            source_img.cv2,
            paragraph=False,
            text_threshold=threshold,
            low_text=0.4,
            link_threshold=0.7,
            decoder="beamsearch",
            beamWidth=5,
        )

        for bbox, text, prob in results:
            if template_text in text:
                # 计算中心点
                top_left = bbox[0]
                bottom_right = bbox[2]
                center = (
                    int((top_left[0] + bottom_right[0]) // 2),
                    int((top_left[1] + bottom_right[1]) // 2),
                )
                points.append(center)

        if points:
            if top_n == 1:
                return points[0]
            elif top_n < len(points):
                return points[:top_n]
            else:
                return points
        else:
            return None


if __name__ == "__main__":
    import pyautogui

    # 使用
    img = UnitImage.from_pil(pyautogui.screenshot())
    pos = ImageProccecor.match_text(img, "使用")
    if pos:
        pyautogui.click(pos)
