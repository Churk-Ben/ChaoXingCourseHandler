import os
import sys


from pymsgbox import alert
from src.Manager import Manager

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


def main():
    alert("Hello, World!")
    manager = Manager()
    plugins = manager.load_plugins()

    try:
        manager.activate_plugin(plugins["AutoReadPlugin"])
    except KeyboardInterrupt:
        manager.logger.info("插件已被用户中断")
    except Exception as e:
        manager.logger.error(f"运行插件时出错: {e}")


if __name__ == "__main__":
    main()
