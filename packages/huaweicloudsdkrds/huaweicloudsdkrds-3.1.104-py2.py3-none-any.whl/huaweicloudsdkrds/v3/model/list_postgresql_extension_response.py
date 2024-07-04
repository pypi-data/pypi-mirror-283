# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListPostgresqlExtensionResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'extensions': 'list[ExtensionsResponse]',
        'total_count': 'int'
    }

    attribute_map = {
        'extensions': 'extensions',
        'total_count': 'total_count'
    }

    def __init__(self, extensions=None, total_count=None):
        """ListPostgresqlExtensionResponse

        The model defined in huaweicloud sdk

        :param extensions: 
        :type extensions: list[:class:`huaweicloudsdkrds.v3.ExtensionsResponse`]
        :param total_count: 总插件数。
        :type total_count: int
        """
        
        super(ListPostgresqlExtensionResponse, self).__init__()

        self._extensions = None
        self._total_count = None
        self.discriminator = None

        if extensions is not None:
            self.extensions = extensions
        if total_count is not None:
            self.total_count = total_count

    @property
    def extensions(self):
        """Gets the extensions of this ListPostgresqlExtensionResponse.

        :return: The extensions of this ListPostgresqlExtensionResponse.
        :rtype: list[:class:`huaweicloudsdkrds.v3.ExtensionsResponse`]
        """
        return self._extensions

    @extensions.setter
    def extensions(self, extensions):
        """Sets the extensions of this ListPostgresqlExtensionResponse.

        :param extensions: The extensions of this ListPostgresqlExtensionResponse.
        :type extensions: list[:class:`huaweicloudsdkrds.v3.ExtensionsResponse`]
        """
        self._extensions = extensions

    @property
    def total_count(self):
        """Gets the total_count of this ListPostgresqlExtensionResponse.

        总插件数。

        :return: The total_count of this ListPostgresqlExtensionResponse.
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """Sets the total_count of this ListPostgresqlExtensionResponse.

        总插件数。

        :param total_count: The total_count of this ListPostgresqlExtensionResponse.
        :type total_count: int
        """
        self._total_count = total_count

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
        if not isinstance(other, ListPostgresqlExtensionResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
