# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ShowStorageUsedSpaceResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'node_id': 'str',
        'used': 'str'
    }

    attribute_map = {
        'node_id': 'node_id',
        'used': 'used'
    }

    def __init__(self, node_id=None, used=None):
        """ShowStorageUsedSpaceResponse

        The model defined in huaweicloud sdk

        :param node_id: 节点id。
        :type node_id: str
        :param used: 磁盘空间使用量。
        :type used: str
        """
        
        super(ShowStorageUsedSpaceResponse, self).__init__()

        self._node_id = None
        self._used = None
        self.discriminator = None

        if node_id is not None:
            self.node_id = node_id
        if used is not None:
            self.used = used

    @property
    def node_id(self):
        """Gets the node_id of this ShowStorageUsedSpaceResponse.

        节点id。

        :return: The node_id of this ShowStorageUsedSpaceResponse.
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id):
        """Sets the node_id of this ShowStorageUsedSpaceResponse.

        节点id。

        :param node_id: The node_id of this ShowStorageUsedSpaceResponse.
        :type node_id: str
        """
        self._node_id = node_id

    @property
    def used(self):
        """Gets the used of this ShowStorageUsedSpaceResponse.

        磁盘空间使用量。

        :return: The used of this ShowStorageUsedSpaceResponse.
        :rtype: str
        """
        return self._used

    @used.setter
    def used(self, used):
        """Sets the used of this ShowStorageUsedSpaceResponse.

        磁盘空间使用量。

        :param used: The used of this ShowStorageUsedSpaceResponse.
        :type used: str
        """
        self._used = used

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
        if not isinstance(other, ShowStorageUsedSpaceResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
