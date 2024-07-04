# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class RunPoemResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'poem': 'list[str]',
        'error_code': 'str',
        'error_msg': 'str'
    }

    attribute_map = {
        'poem': 'poem',
        'error_code': 'error_code',
        'error_msg': 'error_msg'
    }

    def __init__(self, poem=None, error_code=None, error_msg=None):
        """RunPoemResponse

        The model defined in huaweicloud sdk

        :param poem: 根据文本请求体，返回生成的诗歌。调用失败时无此字段。
        :type poem: list[str]
        :param error_code: 调用失败时的错误码，具体请参见错误码。调用成功时无此字段。
        :type error_code: str
        :param error_msg: 调用失败时的错误信息。调用成功时无此字段。
        :type error_msg: str
        """
        
        super(RunPoemResponse, self).__init__()

        self._poem = None
        self._error_code = None
        self._error_msg = None
        self.discriminator = None

        if poem is not None:
            self.poem = poem
        if error_code is not None:
            self.error_code = error_code
        if error_msg is not None:
            self.error_msg = error_msg

    @property
    def poem(self):
        """Gets the poem of this RunPoemResponse.

        根据文本请求体，返回生成的诗歌。调用失败时无此字段。

        :return: The poem of this RunPoemResponse.
        :rtype: list[str]
        """
        return self._poem

    @poem.setter
    def poem(self, poem):
        """Sets the poem of this RunPoemResponse.

        根据文本请求体，返回生成的诗歌。调用失败时无此字段。

        :param poem: The poem of this RunPoemResponse.
        :type poem: list[str]
        """
        self._poem = poem

    @property
    def error_code(self):
        """Gets the error_code of this RunPoemResponse.

        调用失败时的错误码，具体请参见错误码。调用成功时无此字段。

        :return: The error_code of this RunPoemResponse.
        :rtype: str
        """
        return self._error_code

    @error_code.setter
    def error_code(self, error_code):
        """Sets the error_code of this RunPoemResponse.

        调用失败时的错误码，具体请参见错误码。调用成功时无此字段。

        :param error_code: The error_code of this RunPoemResponse.
        :type error_code: str
        """
        self._error_code = error_code

    @property
    def error_msg(self):
        """Gets the error_msg of this RunPoemResponse.

        调用失败时的错误信息。调用成功时无此字段。

        :return: The error_msg of this RunPoemResponse.
        :rtype: str
        """
        return self._error_msg

    @error_msg.setter
    def error_msg(self, error_msg):
        """Sets the error_msg of this RunPoemResponse.

        调用失败时的错误信息。调用成功时无此字段。

        :param error_msg: The error_msg of this RunPoemResponse.
        :type error_msg: str
        """
        self._error_msg = error_msg

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
        if not isinstance(other, RunPoemResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
