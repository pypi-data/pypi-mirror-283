# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ShowCeshierarchyRespNodes:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'name': 'str',
        'available_zone': 'str'
    }

    attribute_map = {
        'name': 'name',
        'available_zone': 'available_zone'
    }

    def __init__(self, name=None, available_zone=None):
        """ShowCeshierarchyRespNodes

        The model defined in huaweicloud sdk

        :param name: 节点名称。
        :type name: str
        :param available_zone: 可用区。
        :type available_zone: str
        """
        
        

        self._name = None
        self._available_zone = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if available_zone is not None:
            self.available_zone = available_zone

    @property
    def name(self):
        """Gets the name of this ShowCeshierarchyRespNodes.

        节点名称。

        :return: The name of this ShowCeshierarchyRespNodes.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ShowCeshierarchyRespNodes.

        节点名称。

        :param name: The name of this ShowCeshierarchyRespNodes.
        :type name: str
        """
        self._name = name

    @property
    def available_zone(self):
        """Gets the available_zone of this ShowCeshierarchyRespNodes.

        可用区。

        :return: The available_zone of this ShowCeshierarchyRespNodes.
        :rtype: str
        """
        return self._available_zone

    @available_zone.setter
    def available_zone(self, available_zone):
        """Sets the available_zone of this ShowCeshierarchyRespNodes.

        可用区。

        :param available_zone: The available_zone of this ShowCeshierarchyRespNodes.
        :type available_zone: str
        """
        self._available_zone = available_zone

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
        if not isinstance(other, ShowCeshierarchyRespNodes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
