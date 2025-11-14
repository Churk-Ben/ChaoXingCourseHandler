from pymsgbox import alert
import numpy as np
import pyautogui as pag
import cv2
import os
import time


# 加载并转换模板图像为灰度图
def load_grayscaled_template(img):
    if img is None:
        raise FileNotFoundError("模板图像不存在：templates/next_button.png")
    if isinstance(img, np.ndarray):
        if img.ndim == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img
    arr = np.array(img)
    if arr.ndim == 3:
        return cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    return arr


# 从屏幕截图中捕获灰度图像
def capture_gray_screen():
    screenshot = pag.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)


# 在屏幕截图中查找模板图像的位置
def find_template_on_screen(template, threshold=0.8):
    screen = capture_gray_screen()
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    points = list(zip(*loc[::-1]))
    # 获取第一个匹配点的坐标
    if points:
        return points[0]
    else:
        return None


# 决策点击下一步还是向下滚动(有模板按钮就点, 没有就滚)
def next_or_scroll(next_template):
    next_pos = find_template_on_screen(next_template)
    if next_pos:
        pag.click(
            next_pos[0] + next_template.shape[1] // 2,
            next_pos[1] + next_template.shape[0] // 2,
        )
        return True
    else:
        pag.scroll(-500)
        return False


if __name__ == "__main__":
    template_path = os.path.join("templates", "next_button.png")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"缺少模板文件: {template_path}")
    next_template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # 运行主循环
    alert("请打开目标应用程序窗口，并确保其在前台。点击确定后，脚本将开始运行。")
    time.sleep(3)  # 给用户3秒钟时间切换到目标窗口

    # 配置
    count = 0
    gap = 20
    total = 9000
    while True:
        clicked = next_or_scroll(next_template)
        if count >= total / gap:
            alert("已完成所有步骤，脚本即将退出。")
            break
        if clicked:
            count += 1
            print(f"已点击下一步按钮 {count} 次")
        time.sleep(gap)  # 等待
