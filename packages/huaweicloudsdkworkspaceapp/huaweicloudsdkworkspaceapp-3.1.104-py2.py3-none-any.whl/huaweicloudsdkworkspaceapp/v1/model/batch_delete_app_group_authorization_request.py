# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class BatchDeleteAppGroupAuthorizationRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'x_language': 'str',
        'body': 'AppGroupAuthorizeReq'
    }

    attribute_map = {
        'x_language': 'X-Language',
        'body': 'body'
    }

    def __init__(self, x_language=None, body=None):
        """BatchDeleteAppGroupAuthorizationRequest

        The model defined in huaweicloud sdk

        :param x_language: 语言： - zh-cn：中文 - en-us：英文 - fr-fr: 法文
        :type x_language: str
        :param body: Body of the BatchDeleteAppGroupAuthorizationRequest
        :type body: :class:`huaweicloudsdkworkspaceapp.v1.AppGroupAuthorizeReq`
        """
        
        

        self._x_language = None
        self._body = None
        self.discriminator = None

        if x_language is not None:
            self.x_language = x_language
        if body is not None:
            self.body = body

    @property
    def x_language(self):
        """Gets the x_language of this BatchDeleteAppGroupAuthorizationRequest.

        语言： - zh-cn：中文 - en-us：英文 - fr-fr: 法文

        :return: The x_language of this BatchDeleteAppGroupAuthorizationRequest.
        :rtype: str
        """
        return self._x_language

    @x_language.setter
    def x_language(self, x_language):
        """Sets the x_language of this BatchDeleteAppGroupAuthorizationRequest.

        语言： - zh-cn：中文 - en-us：英文 - fr-fr: 法文

        :param x_language: The x_language of this BatchDeleteAppGroupAuthorizationRequest.
        :type x_language: str
        """
        self._x_language = x_language

    @property
    def body(self):
        """Gets the body of this BatchDeleteAppGroupAuthorizationRequest.

        :return: The body of this BatchDeleteAppGroupAuthorizationRequest.
        :rtype: :class:`huaweicloudsdkworkspaceapp.v1.AppGroupAuthorizeReq`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this BatchDeleteAppGroupAuthorizationRequest.

        :param body: The body of this BatchDeleteAppGroupAuthorizationRequest.
        :type body: :class:`huaweicloudsdkworkspaceapp.v1.AppGroupAuthorizeReq`
        """
        self._body = body

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
        if not isinstance(other, BatchDeleteAppGroupAuthorizationRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
