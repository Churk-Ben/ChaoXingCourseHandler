import os
import sys


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG = os.path.join(THIS_DIR, "plugin.config.json")

PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, "..", "..", ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from src.utils import Image
from src.Base import PluginBase


class AutoReadPlugin(PluginBase):
    """
    自动阅读插件
    """

    def __init__(self, logger=None):
        self.logger = logger
        self.config = None
        self.load_config()

    def load_config(self):
        with open(CONFIG, "r", encoding="utf-8") as f:
            import json

            self.config = json.load(f)
            if self.config is None:
                raise ValueError("无法加载插件配置文件")

            if self.logger is None:
                raise ValueError("无法加载日志记录器")

            self.logger.info(f"插件 {self.config['name']} 激活成功")
            self.logger.info(f"插件版本: {self.config['version']} ")
            self.logger.info(f"插件描述: {self.config['description']} ")

    def load_grayscaled_template(self, img_path):
        img = Image.UnitImage.from_path(img_path)
        gray_img = img.to_grayscale()
        self.logger.debug(f"加载并转换模板图像: {img_path}")
        return gray_img

    def capture_grayscaled_screen(self):
        import pyautogui as pag

        screenshot = pag.screenshot()
        img = Image.UnitImage.from_pil(screenshot)
        gray_img = img.to_grayscale()
        self.logger.debug("捕获并转换屏幕截图为灰度图像")
        return gray_img

    def find_template_on_screen(self, template: Image.UnitImage, threshold=None):
        if threshold is None:
            threshold = self.config["config"]["threshold"]
        screen = self.capture_grayscaled_screen()
        point = Image.ImageProccecor.match_template(
            screen, template, threshold=threshold, top_n=1
        )
        self.logger.debug(f"在屏幕上查找模板, 阈值: {threshold}, 结果: {point}")
        return point

    def next_step(self):
        import pyautogui as pag

        prev_btn_img = self.load_grayscaled_template(
            os.path.join(THIS_DIR, self.config["templates"]["prev_btn"])
        )
        next_btn_img = self.load_grayscaled_template(
            os.path.join(THIS_DIR, self.config["templates"]["next_btn"])
        )
        more_btn_img = self.load_grayscaled_template(
            os.path.join(THIS_DIR, self.config["templates"]["more_btn"])
        )

        prev_point = self.find_template_on_screen(prev_btn_img)
        next_point = self.find_template_on_screen(next_btn_img)
        more_point = self.find_template_on_screen(more_btn_img)

        if more_point:
            pag.click(
                more_point[0] + more_btn_img.cv2.shape[1] // 2,
                more_point[1] + more_btn_img.cv2.shape[0] // 2,
            )
            self.logger.info('点击了"加载更多"按钮')
            return True

        elif next_point:
            pag.click(
                next_point[0] + next_btn_img.cv2.shape[1] // 2,
                next_point[1] + next_btn_img.cv2.shape[0] // 2,
            )
            self.logger.info('点击了"下一页"按钮')
            return True

        elif prev_point:
            pag.click(
                prev_point[0] + prev_btn_img.cv2.shape[1] // 2,
                prev_point[1] + prev_btn_img.cv2.shape[0] // 2,
            )
            self.logger.info('点击了"上一页"按钮')
            return True

        else:
            pag.scroll(self.config["config"]["scroll_amount"])
            self.logger.info("未找到任何按钮, 执行滚动操作")
            return False

    def run(self):
        import time

        interval = self.config["config"]["check_interval"]
        start_time = time.time()
        while True:
            if time.time() - start_time > self.config["config"]["max_runtime"]:
                self.logger.info("达到最大运行时间, 插件停止运行")
                break
            self.next_step()
            time.sleep(interval)


if __name__ == "__main__":
    import logging
    from src.utils import Logger

    main_logger = Logger.get_logger("PluginManager", level=logging.DEBUG)

    def activate_plugin(plugin: PluginBase):
        plugin_logger = Logger.get_logger(plugin.__name__, level=logging.DEBUG)
        plugin_instance = plugin(logger=plugin_logger)
        plugin_instance.run()

    try:
        activate_plugin(AutoReadPlugin)
    except KeyboardInterrupt:
        main_logger.info("插件已被用户中断")
