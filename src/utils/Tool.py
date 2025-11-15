"""
def find_template_on_screen(self, template: Image.UnitImage, threshold=None):
    if threshold is None:
        threshold = self.config["config"]["threshold"]
    screen = self.capture_grayscaled_screen()
    point = Image.ImageProccecor.match_img(
        screen, template, threshold=threshold, top_n=1
    )
    self.logger.debug(f"在屏幕上查找模板, 阈值: {threshold}, 结果: {point}")
    return point

def find_img_on_screen(self, template: Image.UnitImage, threshold=None):
    if threshold is None:
        threshold = self.config["config"]["threshold"]
    screen = self.capture_grayscaled_screen()
    point = Image.ImageProccecor.match_img(
        screen, template, threshold=threshold, top_n=1
    )
    self.logger.debug(f"在屏幕上查找模板图像 , 阈值: {threshold}, 结果: {point}")
    return point


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






















"""
