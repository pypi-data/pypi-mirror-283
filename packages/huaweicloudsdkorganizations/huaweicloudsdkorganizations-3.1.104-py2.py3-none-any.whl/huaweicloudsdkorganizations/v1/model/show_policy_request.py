# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ShowPolicyRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'policy_id': 'str',
        'x_language': 'str'
    }

    attribute_map = {
        'policy_id': 'policy_id',
        'x_language': 'X-Language'
    }

    def __init__(self, policy_id=None, x_language=None):
        """ShowPolicyRequest

        The model defined in huaweicloud sdk

        :param policy_id: 策略的唯一标识符（ID）。
        :type policy_id: str
        :param x_language: 选择接口返回的信息的语言
        :type x_language: str
        """
        
        

        self._policy_id = None
        self._x_language = None
        self.discriminator = None

        self.policy_id = policy_id
        if x_language is not None:
            self.x_language = x_language

    @property
    def policy_id(self):
        """Gets the policy_id of this ShowPolicyRequest.

        策略的唯一标识符（ID）。

        :return: The policy_id of this ShowPolicyRequest.
        :rtype: str
        """
        return self._policy_id

    @policy_id.setter
    def policy_id(self, policy_id):
        """Sets the policy_id of this ShowPolicyRequest.

        策略的唯一标识符（ID）。

        :param policy_id: The policy_id of this ShowPolicyRequest.
        :type policy_id: str
        """
        self._policy_id = policy_id

    @property
    def x_language(self):
        """Gets the x_language of this ShowPolicyRequest.

        选择接口返回的信息的语言

        :return: The x_language of this ShowPolicyRequest.
        :rtype: str
        """
        return self._x_language

    @x_language.setter
    def x_language(self, x_language):
        """Sets the x_language of this ShowPolicyRequest.

        选择接口返回的信息的语言

        :param x_language: The x_language of this ShowPolicyRequest.
        :type x_language: str
        """
        self._x_language = x_language

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
        if not isinstance(other, ShowPolicyRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
