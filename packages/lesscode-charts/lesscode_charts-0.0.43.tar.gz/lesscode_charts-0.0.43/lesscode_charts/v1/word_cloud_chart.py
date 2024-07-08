from typing import List


class WordCloudChart:
    @staticmethod
    def word_cloud_chart(data: List[dict], **kwargs):
        """
        :param data:[{"name": "气压信号","value": 2},{"name": "织物张力","value": 2}]
        :param kwargs:
        :return:
        """
        result = {
            "chart_type": "word_cloud",
            "data": data
        }
        if kwargs:
            result["pool"] = kwargs

        return result
