import os
import json
import importlib.util
from pathlib import Path
from src.Base import PluginBase
from src.utils import Logger

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
PLUGINS = os.path.join(THIS_DIR, "plugins")


class Manager:
    def __init__(self):
        self.plugins = {}  # name: path.classname
        self.logger = Logger.get_logger("PluginManager")

    def _load_class_from_path(self, module_path: Path, classname: str):
        path = module_path.resolve()

        # 动态加载模块
        spec = importlib.util.spec_from_file_location(f"plugin_{path.stem}", str(path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 获取类
        if not hasattr(module, classname):
            raise AttributeError(f"模块 {path} 中没有类 {classname}")

        return getattr(module, classname)

    def load_plugins(self, dir: str = PLUGINS):
        plugins = {}
        root = Path(dir)

        if not root.is_dir():
            self.logger.error(f"{dir} 不是有效的插件目录")
            return plugins

        for folder in root.iterdir():
            if folder.is_dir():
                plugin_config = folder / "plugin.config.json"
                plugin_module = folder / "plugin.py"

                if not plugin_config.exists():
                    self.logger.warning(f"{folder.name} 中未找到配置文件")
                    continue

                if not plugin_module.exists():
                    self.logger.warning(f"{folder.name} 中未找到插件主文件")
                    continue

                try:
                    data = json.loads(plugin_config.read_text(encoding="utf-8"))
                    plugins[data["classname"]] = {
                        "name": data["name"],
                        "version": data["version"],
                        "description": data["description"],
                        "classname": data["classname"],
                        "class": self._load_class_from_path(
                            plugin_module, data["classname"]
                        ),
                    }
                    self.logger.info(f"已加载插件: {data['name']} ")

                except json.JSONDecodeError as e:
                    self.logger.warning(f"{plugin_config} 解析失败: {e}")

                except Exception as e:
                    self.logger.error(f"加载插件 {folder.name} 失败: {e}")

        return plugins

    def activate_plugin(self, plugin: PluginBase):
        try:
            plugin_logger = Logger.get_logger(plugin.__name__)
            plugin_instance = plugin(logger=plugin_logger)
            plugin_instance.run()

        except KeyboardInterrupt:
            self.logger.info("运行已中断")
        except Exception as e:
            self.logger.error(f"插件运行时出错: {e}")
