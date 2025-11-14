import os
import sys


PLUGIN_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(PLUGIN_DIR, "plugin.config.json")
PROJECT_ROOT = os.path.abspath(os.path.join(PLUGIN_DIR, "..", "..", ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from src.utils import Image


class AutoReadPlugin:
    """
    自动阅读插件
    版本: 1.2.0
    """

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        import json

        config = json.load(f)

    # 载入模板图像为灰度图
    @staticmethod
    def load_grayscaled_template(img_path):
        img = Image.UnitImage.from_path(img_path)
        gray_img = img.to_grayscale()
        return gray_img

    # 捕获屏幕为灰度图
    @staticmethod
    def capture_grayscaled_screen():
        import pyautogui as pag

        screenshot = pag.screenshot()
        img = Image.UnitImage.from_pil(screenshot)
        gray_img = img.to_grayscale()
        return gray_img

    # 在屏幕截图中查找某模板的位置
    @staticmethod
    def find_template_on_screen(template: Image.UnitImage, threshold=0.8):
        screen = AutoReadPlugin.capture_grayscaled_screen()
        point = Image.ImageProccecor.match_template(
            screen, template, threshold=threshold, top_n=1
        )
        return point

    # 决策下一步
    @staticmethod
    def next_step():
        import pyautogui as pag

        prev_btn_img = AutoReadPlugin.load_grayscaled_template(
            os.path.join(PLUGIN_DIR, AutoReadPlugin.config["templates"]["prev_btn"])
        )
        next_btn_img = AutoReadPlugin.load_grayscaled_template(
            os.path.join(PLUGIN_DIR, AutoReadPlugin.config["templates"]["next_btn"])
        )

        prev_point = AutoReadPlugin.find_template_on_screen(prev_btn_img)
        next_point = AutoReadPlugin.find_template_on_screen(next_btn_img)

        if next_point:
            pag.click(
                next_point[0] + next_btn_img.cv2.shape[1] // 2,
                next_point[1] + next_btn_img.cv2.shape[0] // 2,
            )
            return True
        elif prev_point:
            pag.click(
                prev_point[0] + prev_btn_img.cv2.shape[1] // 2,
                prev_point[1] + prev_btn_img.cv2.shape[0] // 2,
            )
            return True
        else:
            pag.scroll(AutoReadPlugin.config["config"]["scroll_amount"])
            return False

    @staticmethod
    def run():
        import time

        print(AutoReadPlugin.config)
        time.sleep(3)
        interval = AutoReadPlugin.config["config"]["check_interval"]
        start_time = time.time()
        while True:
            AutoReadPlugin.next_step()
            time.sleep(interval)
            if (
                time.time() - start_time
                > AutoReadPlugin.config["config"]["max_runtime"]
            ):
                print("达到最大运行时间，停止插件")
                break


if __name__ == "__main__":
    AutoReadPlugin.run()
