# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class CustomerUpgradeDatabaseVersionReqNew:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'is_delayed': 'bool'
    }

    attribute_map = {
        'is_delayed': 'is_delayed'
    }

    def __init__(self, is_delayed=None):
        """CustomerUpgradeDatabaseVersionReqNew

        The model defined in huaweicloud sdk

        :param is_delayed: 是否延迟至可维护时间段内升级。 取值范围： - true：延迟升级。表示实例将在设置的可维护时间段内升级。 - false：立即升级，默认该方式。
        :type is_delayed: bool
        """
        
        

        self._is_delayed = None
        self.discriminator = None

        if is_delayed is not None:
            self.is_delayed = is_delayed

    @property
    def is_delayed(self):
        """Gets the is_delayed of this CustomerUpgradeDatabaseVersionReqNew.

        是否延迟至可维护时间段内升级。 取值范围： - true：延迟升级。表示实例将在设置的可维护时间段内升级。 - false：立即升级，默认该方式。

        :return: The is_delayed of this CustomerUpgradeDatabaseVersionReqNew.
        :rtype: bool
        """
        return self._is_delayed

    @is_delayed.setter
    def is_delayed(self, is_delayed):
        """Sets the is_delayed of this CustomerUpgradeDatabaseVersionReqNew.

        是否延迟至可维护时间段内升级。 取值范围： - true：延迟升级。表示实例将在设置的可维护时间段内升级。 - false：立即升级，默认该方式。

        :param is_delayed: The is_delayed of this CustomerUpgradeDatabaseVersionReqNew.
        :type is_delayed: bool
        """
        self._is_delayed = is_delayed

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
        if not isinstance(other, CustomerUpgradeDatabaseVersionReqNew):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
