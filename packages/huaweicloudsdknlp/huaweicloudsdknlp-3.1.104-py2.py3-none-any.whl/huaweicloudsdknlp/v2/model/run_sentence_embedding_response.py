# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class RunSentenceEmbeddingResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'vectors': 'list[list[float]]',
        'error_code': 'str',
        'error_msg': 'str'
    }

    attribute_map = {
        'vectors': 'vectors',
        'error_code': 'error_code',
        'error_msg': 'error_msg'
    }

    def __init__(self, vectors=None, error_code=None, error_msg=None):
        """RunSentenceEmbeddingResponse

        The model defined in huaweicloud sdk

        :param vectors: 句向量结果列表，按输入句子顺序返回句向量。调用失败时无此字段。
        :type vectors: list[list[float]]
        :param error_code: 调用失败时的错误码，具体请参见错误码。调用成功时无此字段。
        :type error_code: str
        :param error_msg: 调用失败时的错误信息。调用成功时无此字段。
        :type error_msg: str
        """
        
        super(RunSentenceEmbeddingResponse, self).__init__()

        self._vectors = None
        self._error_code = None
        self._error_msg = None
        self.discriminator = None

        if vectors is not None:
            self.vectors = vectors
        if error_code is not None:
            self.error_code = error_code
        if error_msg is not None:
            self.error_msg = error_msg

    @property
    def vectors(self):
        """Gets the vectors of this RunSentenceEmbeddingResponse.

        句向量结果列表，按输入句子顺序返回句向量。调用失败时无此字段。

        :return: The vectors of this RunSentenceEmbeddingResponse.
        :rtype: list[list[float]]
        """
        return self._vectors

    @vectors.setter
    def vectors(self, vectors):
        """Sets the vectors of this RunSentenceEmbeddingResponse.

        句向量结果列表，按输入句子顺序返回句向量。调用失败时无此字段。

        :param vectors: The vectors of this RunSentenceEmbeddingResponse.
        :type vectors: list[list[float]]
        """
        self._vectors = vectors

    @property
    def error_code(self):
        """Gets the error_code of this RunSentenceEmbeddingResponse.

        调用失败时的错误码，具体请参见错误码。调用成功时无此字段。

        :return: The error_code of this RunSentenceEmbeddingResponse.
        :rtype: str
        """
        return self._error_code

    @error_code.setter
    def error_code(self, error_code):
        """Sets the error_code of this RunSentenceEmbeddingResponse.

        调用失败时的错误码，具体请参见错误码。调用成功时无此字段。

        :param error_code: The error_code of this RunSentenceEmbeddingResponse.
        :type error_code: str
        """
        self._error_code = error_code

    @property
    def error_msg(self):
        """Gets the error_msg of this RunSentenceEmbeddingResponse.

        调用失败时的错误信息。调用成功时无此字段。

        :return: The error_msg of this RunSentenceEmbeddingResponse.
        :rtype: str
        """
        return self._error_msg

    @error_msg.setter
    def error_msg(self, error_msg):
        """Sets the error_msg of this RunSentenceEmbeddingResponse.

        调用失败时的错误信息。调用成功时无此字段。

        :param error_msg: The error_msg of this RunSentenceEmbeddingResponse.
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
        if not isinstance(other, RunSentenceEmbeddingResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
