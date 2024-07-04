# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateAppRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'app_group_id': 'str',
        'app_id': 'str',
        'body': 'UpdateAppReq'
    }

    attribute_map = {
        'app_group_id': 'app_group_id',
        'app_id': 'app_id',
        'body': 'body'
    }

    def __init__(self, app_group_id=None, app_id=None, body=None):
        """UpdateAppRequest

        The model defined in huaweicloud sdk

        :param app_group_id: 应用组ID。
        :type app_group_id: str
        :param app_id: 应用ID。
        :type app_id: str
        :param body: Body of the UpdateAppRequest
        :type body: :class:`huaweicloudsdkworkspaceapp.v1.UpdateAppReq`
        """
        
        

        self._app_group_id = None
        self._app_id = None
        self._body = None
        self.discriminator = None

        self.app_group_id = app_group_id
        self.app_id = app_id
        if body is not None:
            self.body = body

    @property
    def app_group_id(self):
        """Gets the app_group_id of this UpdateAppRequest.

        应用组ID。

        :return: The app_group_id of this UpdateAppRequest.
        :rtype: str
        """
        return self._app_group_id

    @app_group_id.setter
    def app_group_id(self, app_group_id):
        """Sets the app_group_id of this UpdateAppRequest.

        应用组ID。

        :param app_group_id: The app_group_id of this UpdateAppRequest.
        :type app_group_id: str
        """
        self._app_group_id = app_group_id

    @property
    def app_id(self):
        """Gets the app_id of this UpdateAppRequest.

        应用ID。

        :return: The app_id of this UpdateAppRequest.
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """Sets the app_id of this UpdateAppRequest.

        应用ID。

        :param app_id: The app_id of this UpdateAppRequest.
        :type app_id: str
        """
        self._app_id = app_id

    @property
    def body(self):
        """Gets the body of this UpdateAppRequest.

        :return: The body of this UpdateAppRequest.
        :rtype: :class:`huaweicloudsdkworkspaceapp.v1.UpdateAppReq`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this UpdateAppRequest.

        :param body: The body of this UpdateAppRequest.
        :type body: :class:`huaweicloudsdkworkspaceapp.v1.UpdateAppReq`
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
        if not isinstance(other, UpdateAppRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
