from abc import ABC, abstractmethod

from tabulate import tabulate
from wcwidth import wcswidth


class PluginBase(ABC):
    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def index_plugins(plugins):
        plugin_class = []
        for plugin_key in plugins.keys():
            plugin_class.append(plugins[plugin_key]["class"])

        return plugin_class

    @staticmethod
    def display_plugins(plugins, headers=None, tablefmt="simple"):
        plugin_map = {}
        data = []

        index = 0
        for plugin_key in plugins.keys():
            index += 1
            plugin_map[index] = plugin_key

            data.append(
                [
                    index,
                    plugins[plugin_key]["name"],
                    plugins[plugin_key]["version"],
                    plugins[plugin_key]["description"],
                ]
            )

        # 计算每列最大显示宽度（按终端实际显示宽度）
        all_rows = data + ([headers] if headers else [])
        col_widths = [
            max(wcswidth(str(cell)) for cell in col) for col in zip(*all_rows)
        ]

        # 填充每一列到最大宽度
        def pad_cell(cell, width):
            """用空格填充到指定显示宽度"""
            cell_str = str(cell)
            diff = width - wcswidth(cell_str)
            return cell_str + (" " * max(0, diff))

        processed_data = [
            [pad_cell(cell, width) for cell, width in zip(row, col_widths)]
            for row in data
        ]

        processed_headers = (
            [pad_cell(h, w) for h, w in zip(headers, col_widths)] if headers else None
        )

        print(
            tabulate(
                processed_data,
                headers=processed_headers,
                maxcolwidths=[None, None, None, 80],
                tablefmt=tablefmt,
            )
        )
