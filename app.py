import os
import sys


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import json
from pymsgbox import alert
from src.Manager import Manager
from src.Base import PluginBase


def run_plugin(plugin: PluginBase):
    manager = Manager()

    try:
        manager.activate_plugin(plugin)
    except KeyboardInterrupt:
        manager.logger.info("运行已中断")
    except Exception as e:
        manager.logger.error(f"插件运行时出错: {e}")


def main():
    manager = Manager()
    plugins = manager.load_plugins()

    if not plugins:
        manager.logger.info("未找到可用插件, 请检查插件目录")
        return

    else:
        manager.logger.info(f"找到 {len(plugins)} 个可用插件: ")
        PluginBase.display_plugins(
            plugins,
            headers=["index", "name", "version", "description"],
        )

    i = int(input("输入一个将要运行的插件的index: "))
    classes = PluginBase.index_plugins(plugins)
    # alert("你可以将浏览器窗口切至前台, 然后点击确定")
    run_plugin(classes[i - 1])


if __name__ == "__main__":
    main()
