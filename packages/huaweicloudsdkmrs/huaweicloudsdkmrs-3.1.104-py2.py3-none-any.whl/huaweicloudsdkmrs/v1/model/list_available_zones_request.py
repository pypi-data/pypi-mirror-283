# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListAvailableZonesRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'region_id': 'str',
        'scope': 'str'
    }

    attribute_map = {
        'region_id': 'region_id',
        'scope': 'scope'
    }

    def __init__(self, region_id=None, scope=None):
        """ListAvailableZonesRequest

        The model defined in huaweicloud sdk

        :param region_id: 区域id，例如cn-north-4
        :type region_id: str
        :param scope: 可用区范围
        :type scope: str
        """
        
        

        self._region_id = None
        self._scope = None
        self.discriminator = None

        self.region_id = region_id
        if scope is not None:
            self.scope = scope

    @property
    def region_id(self):
        """Gets the region_id of this ListAvailableZonesRequest.

        区域id，例如cn-north-4

        :return: The region_id of this ListAvailableZonesRequest.
        :rtype: str
        """
        return self._region_id

    @region_id.setter
    def region_id(self, region_id):
        """Sets the region_id of this ListAvailableZonesRequest.

        区域id，例如cn-north-4

        :param region_id: The region_id of this ListAvailableZonesRequest.
        :type region_id: str
        """
        self._region_id = region_id

    @property
    def scope(self):
        """Gets the scope of this ListAvailableZonesRequest.

        可用区范围

        :return: The scope of this ListAvailableZonesRequest.
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this ListAvailableZonesRequest.

        可用区范围

        :param scope: The scope of this ListAvailableZonesRequest.
        :type scope: str
        """
        self._scope = scope

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
        if not isinstance(other, ListAvailableZonesRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
