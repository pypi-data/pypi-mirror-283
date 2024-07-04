# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListLogStreamsResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'log_streams': 'list[ListLogStreamsResponseBody1LogStreams]'
    }

    attribute_map = {
        'log_streams': 'log_streams'
    }

    def __init__(self, log_streams=None):
        """ListLogStreamsResponse

        The model defined in huaweicloud sdk

        :param log_streams: 日志流数组
        :type log_streams: list[:class:`huaweicloudsdklts.v2.ListLogStreamsResponseBody1LogStreams`]
        """
        
        super(ListLogStreamsResponse, self).__init__()

        self._log_streams = None
        self.discriminator = None

        if log_streams is not None:
            self.log_streams = log_streams

    @property
    def log_streams(self):
        """Gets the log_streams of this ListLogStreamsResponse.

        日志流数组

        :return: The log_streams of this ListLogStreamsResponse.
        :rtype: list[:class:`huaweicloudsdklts.v2.ListLogStreamsResponseBody1LogStreams`]
        """
        return self._log_streams

    @log_streams.setter
    def log_streams(self, log_streams):
        """Sets the log_streams of this ListLogStreamsResponse.

        日志流数组

        :param log_streams: The log_streams of this ListLogStreamsResponse.
        :type log_streams: list[:class:`huaweicloudsdklts.v2.ListLogStreamsResponseBody1LogStreams`]
        """
        self._log_streams = log_streams

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
        if not isinstance(other, ListLogStreamsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
