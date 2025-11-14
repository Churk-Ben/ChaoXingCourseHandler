import os
import cv2
from PIL import Image
import numpy as np


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
        source_img: UnitImage, template_img: UnitImage, threshold=0.8, top_n=1
    ):
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


if __name__ == "__main__":
    img_path = "./templates/next_button.png"
    unit_img = UnitImage.from_path(img_path)
    print("图像大小:", unit_img.size())
    gray_unit_img = unit_img.to_grayscale()
    unit_img.show()
    gray_unit_img.show()
