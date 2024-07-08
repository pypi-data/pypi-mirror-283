from lesscode_charts.utils.common_utils import find_child

"""
矩形树图、旭日图
"""


class RectChart:
    @staticmethod
    def render_rect_chart(data: list, key: str, parent_key: str, unit: str, name: str = ""):
        """

        :param data: 父子关系的数据字典，需要包含父子关系的字段
        :param key: 子key
        :param parent_key: 父key
        :param unit: 单位
        :param name: 名字
        :return:
        """
        _data = find_child(data, key=key, parent_key=parent_key)
        result = {
            "chart_type": "rect",
            "series": {
                "name": name,
                "data": _data,
                "unit": unit
            }
        }
        return result
