# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ShowVodRetrievalRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'start_time': 'str',
        'end_time': 'str',
        'interval': 'int'
    }

    attribute_map = {
        'start_time': 'start_time',
        'end_time': 'end_time',
        'interval': 'interval'
    }

    def __init__(self, start_time=None, end_time=None, interval=None):
        """ShowVodRetrievalRequest

        The model defined in huaweicloud sdk

        :param start_time: 开始时间 
        :type start_time: str
        :param end_time: 结束时间 
        :type end_time: str
        :param interval: 采样间隔，单位：秒，取值说明： 时间跨度1天：1小时、4小时、8小时，分别对应3600秒、14400秒和28800秒。 时间跨度2~7天：1小时、4小时、8小时、1天，分别对应3600秒、14400秒、28800秒和86400秒。 时间跨度8~31天：4小时、8小时、1天，分别对应14400秒、28800秒和86400秒。 如果不传，默认取对应时间跨度的最小间隔。 
        :type interval: int
        """
        
        

        self._start_time = None
        self._end_time = None
        self._interval = None
        self.discriminator = None

        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if interval is not None:
            self.interval = interval

    @property
    def start_time(self):
        """Gets the start_time of this ShowVodRetrievalRequest.

        开始时间 

        :return: The start_time of this ShowVodRetrievalRequest.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this ShowVodRetrievalRequest.

        开始时间 

        :param start_time: The start_time of this ShowVodRetrievalRequest.
        :type start_time: str
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this ShowVodRetrievalRequest.

        结束时间 

        :return: The end_time of this ShowVodRetrievalRequest.
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this ShowVodRetrievalRequest.

        结束时间 

        :param end_time: The end_time of this ShowVodRetrievalRequest.
        :type end_time: str
        """
        self._end_time = end_time

    @property
    def interval(self):
        """Gets the interval of this ShowVodRetrievalRequest.

        采样间隔，单位：秒，取值说明： 时间跨度1天：1小时、4小时、8小时，分别对应3600秒、14400秒和28800秒。 时间跨度2~7天：1小时、4小时、8小时、1天，分别对应3600秒、14400秒、28800秒和86400秒。 时间跨度8~31天：4小时、8小时、1天，分别对应14400秒、28800秒和86400秒。 如果不传，默认取对应时间跨度的最小间隔。 

        :return: The interval of this ShowVodRetrievalRequest.
        :rtype: int
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this ShowVodRetrievalRequest.

        采样间隔，单位：秒，取值说明： 时间跨度1天：1小时、4小时、8小时，分别对应3600秒、14400秒和28800秒。 时间跨度2~7天：1小时、4小时、8小时、1天，分别对应3600秒、14400秒、28800秒和86400秒。 时间跨度8~31天：4小时、8小时、1天，分别对应14400秒、28800秒和86400秒。 如果不传，默认取对应时间跨度的最小间隔。 

        :param interval: The interval of this ShowVodRetrievalRequest.
        :type interval: int
        """
        self._interval = interval

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ShowVodRetrievalRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
