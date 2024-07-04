# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListInteractionRuleGroupsResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'count': 'int',
        'interaction_rule_groups': 'list[InteractionRuleGroupDetail]',
        'x_request_id': 'str'
    }

    attribute_map = {
        'count': 'count',
        'interaction_rule_groups': 'interaction_rule_groups',
        'x_request_id': 'X-Request-Id'
    }

    def __init__(self, count=None, interaction_rule_groups=None, x_request_id=None):
        """ListInteractionRuleGroupsResponse

        The model defined in huaweicloud sdk

        :param count: 互动规则总数。
        :type count: int
        :param interaction_rule_groups: 互动规则库列表。
        :type interaction_rule_groups: list[:class:`huaweicloudsdkmetastudio.v1.InteractionRuleGroupDetail`]
        :param x_request_id: 
        :type x_request_id: str
        """
        
        super(ListInteractionRuleGroupsResponse, self).__init__()

        self._count = None
        self._interaction_rule_groups = None
        self._x_request_id = None
        self.discriminator = None

        if count is not None:
            self.count = count
        if interaction_rule_groups is not None:
            self.interaction_rule_groups = interaction_rule_groups
        if x_request_id is not None:
            self.x_request_id = x_request_id

    @property
    def count(self):
        """Gets the count of this ListInteractionRuleGroupsResponse.

        互动规则总数。

        :return: The count of this ListInteractionRuleGroupsResponse.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this ListInteractionRuleGroupsResponse.

        互动规则总数。

        :param count: The count of this ListInteractionRuleGroupsResponse.
        :type count: int
        """
        self._count = count

    @property
    def interaction_rule_groups(self):
        """Gets the interaction_rule_groups of this ListInteractionRuleGroupsResponse.

        互动规则库列表。

        :return: The interaction_rule_groups of this ListInteractionRuleGroupsResponse.
        :rtype: list[:class:`huaweicloudsdkmetastudio.v1.InteractionRuleGroupDetail`]
        """
        return self._interaction_rule_groups

    @interaction_rule_groups.setter
    def interaction_rule_groups(self, interaction_rule_groups):
        """Sets the interaction_rule_groups of this ListInteractionRuleGroupsResponse.

        互动规则库列表。

        :param interaction_rule_groups: The interaction_rule_groups of this ListInteractionRuleGroupsResponse.
        :type interaction_rule_groups: list[:class:`huaweicloudsdkmetastudio.v1.InteractionRuleGroupDetail`]
        """
        self._interaction_rule_groups = interaction_rule_groups

    @property
    def x_request_id(self):
        """Gets the x_request_id of this ListInteractionRuleGroupsResponse.

        :return: The x_request_id of this ListInteractionRuleGroupsResponse.
        :rtype: str
        """
        return self._x_request_id

    @x_request_id.setter
    def x_request_id(self, x_request_id):
        """Sets the x_request_id of this ListInteractionRuleGroupsResponse.

        :param x_request_id: The x_request_id of this ListInteractionRuleGroupsResponse.
        :type x_request_id: str
        """
        self._x_request_id = x_request_id

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
        if not isinstance(other, ListInteractionRuleGroupsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
