# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ResetActiveCodeRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'x_app_user_id': 'str',
        'active_code_id': 'str'
    }

    attribute_map = {
        'x_app_user_id': 'X-App-UserId',
        'active_code_id': 'active_code_id'
    }

    def __init__(self, x_app_user_id=None, active_code_id=None):
        """ResetActiveCodeRequest

        The model defined in huaweicloud sdk

        :param x_app_user_id: 第三方用户ID。不允许输入中文。
        :type x_app_user_id: str
        :param active_code_id: 激活码ID。
        :type active_code_id: str
        """
        
        

        self._x_app_user_id = None
        self._active_code_id = None
        self.discriminator = None

        if x_app_user_id is not None:
            self.x_app_user_id = x_app_user_id
        self.active_code_id = active_code_id

    @property
    def x_app_user_id(self):
        """Gets the x_app_user_id of this ResetActiveCodeRequest.

        第三方用户ID。不允许输入中文。

        :return: The x_app_user_id of this ResetActiveCodeRequest.
        :rtype: str
        """
        return self._x_app_user_id

    @x_app_user_id.setter
    def x_app_user_id(self, x_app_user_id):
        """Sets the x_app_user_id of this ResetActiveCodeRequest.

        第三方用户ID。不允许输入中文。

        :param x_app_user_id: The x_app_user_id of this ResetActiveCodeRequest.
        :type x_app_user_id: str
        """
        self._x_app_user_id = x_app_user_id

    @property
    def active_code_id(self):
        """Gets the active_code_id of this ResetActiveCodeRequest.

        激活码ID。

        :return: The active_code_id of this ResetActiveCodeRequest.
        :rtype: str
        """
        return self._active_code_id

    @active_code_id.setter
    def active_code_id(self, active_code_id):
        """Sets the active_code_id of this ResetActiveCodeRequest.

        激活码ID。

        :param active_code_id: The active_code_id of this ResetActiveCodeRequest.
        :type active_code_id: str
        """
        self._active_code_id = active_code_id

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
        if not isinstance(other, ResetActiveCodeRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
