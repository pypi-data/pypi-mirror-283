# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class AssetSharedConfig:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'shared_type': 'str',
        'expire_time': 'str',
        'allowed_project_ids': 'list[str]'
    }

    attribute_map = {
        'shared_type': 'shared_type',
        'expire_time': 'expire_time',
        'allowed_project_ids': 'allowed_project_ids'
    }

    def __init__(self, shared_type=None, expire_time=None, allowed_project_ids=None):
        """AssetSharedConfig

        The model defined in huaweicloud sdk

        :param shared_type: 共享类型。 * PRIVATE: 私有，仅本租户可访问。 * PUBLIC: 公开，所有租户可访问。当前仅提供系统资产可公开访问。 * SHARED：共享，指定租户可访问。拥有者指定租户可访问。
        :type shared_type: str
        :param expire_time: 共享过期时间。默认过期时间为30天，即共享当天+30的23:59:59。
        :type expire_time: str
        :param allowed_project_ids: 允许访问本资产的租户列表。
        :type allowed_project_ids: list[str]
        """
        
        

        self._shared_type = None
        self._expire_time = None
        self._allowed_project_ids = None
        self.discriminator = None

        if shared_type is not None:
            self.shared_type = shared_type
        if expire_time is not None:
            self.expire_time = expire_time
        if allowed_project_ids is not None:
            self.allowed_project_ids = allowed_project_ids

    @property
    def shared_type(self):
        """Gets the shared_type of this AssetSharedConfig.

        共享类型。 * PRIVATE: 私有，仅本租户可访问。 * PUBLIC: 公开，所有租户可访问。当前仅提供系统资产可公开访问。 * SHARED：共享，指定租户可访问。拥有者指定租户可访问。

        :return: The shared_type of this AssetSharedConfig.
        :rtype: str
        """
        return self._shared_type

    @shared_type.setter
    def shared_type(self, shared_type):
        """Sets the shared_type of this AssetSharedConfig.

        共享类型。 * PRIVATE: 私有，仅本租户可访问。 * PUBLIC: 公开，所有租户可访问。当前仅提供系统资产可公开访问。 * SHARED：共享，指定租户可访问。拥有者指定租户可访问。

        :param shared_type: The shared_type of this AssetSharedConfig.
        :type shared_type: str
        """
        self._shared_type = shared_type

    @property
    def expire_time(self):
        """Gets the expire_time of this AssetSharedConfig.

        共享过期时间。默认过期时间为30天，即共享当天+30的23:59:59。

        :return: The expire_time of this AssetSharedConfig.
        :rtype: str
        """
        return self._expire_time

    @expire_time.setter
    def expire_time(self, expire_time):
        """Sets the expire_time of this AssetSharedConfig.

        共享过期时间。默认过期时间为30天，即共享当天+30的23:59:59。

        :param expire_time: The expire_time of this AssetSharedConfig.
        :type expire_time: str
        """
        self._expire_time = expire_time

    @property
    def allowed_project_ids(self):
        """Gets the allowed_project_ids of this AssetSharedConfig.

        允许访问本资产的租户列表。

        :return: The allowed_project_ids of this AssetSharedConfig.
        :rtype: list[str]
        """
        return self._allowed_project_ids

    @allowed_project_ids.setter
    def allowed_project_ids(self, allowed_project_ids):
        """Sets the allowed_project_ids of this AssetSharedConfig.

        允许访问本资产的租户列表。

        :param allowed_project_ids: The allowed_project_ids of this AssetSharedConfig.
        :type allowed_project_ids: list[str]
        """
        self._allowed_project_ids = allowed_project_ids

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
        if not isinstance(other, AssetSharedConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
