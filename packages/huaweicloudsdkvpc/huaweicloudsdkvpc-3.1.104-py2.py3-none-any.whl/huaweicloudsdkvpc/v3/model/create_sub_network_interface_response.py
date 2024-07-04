# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateSubNetworkInterfaceResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'request_id': 'str',
        'sub_network_interface': 'SubNetworkInterface'
    }

    attribute_map = {
        'request_id': 'request_id',
        'sub_network_interface': 'sub_network_interface'
    }

    def __init__(self, request_id=None, sub_network_interface=None):
        """CreateSubNetworkInterfaceResponse

        The model defined in huaweicloud sdk

        :param request_id: 请求ID
        :type request_id: str
        :param sub_network_interface: 
        :type sub_network_interface: :class:`huaweicloudsdkvpc.v3.SubNetworkInterface`
        """
        
        super(CreateSubNetworkInterfaceResponse, self).__init__()

        self._request_id = None
        self._sub_network_interface = None
        self.discriminator = None

        if request_id is not None:
            self.request_id = request_id
        if sub_network_interface is not None:
            self.sub_network_interface = sub_network_interface

    @property
    def request_id(self):
        """Gets the request_id of this CreateSubNetworkInterfaceResponse.

        请求ID

        :return: The request_id of this CreateSubNetworkInterfaceResponse.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this CreateSubNetworkInterfaceResponse.

        请求ID

        :param request_id: The request_id of this CreateSubNetworkInterfaceResponse.
        :type request_id: str
        """
        self._request_id = request_id

    @property
    def sub_network_interface(self):
        """Gets the sub_network_interface of this CreateSubNetworkInterfaceResponse.

        :return: The sub_network_interface of this CreateSubNetworkInterfaceResponse.
        :rtype: :class:`huaweicloudsdkvpc.v3.SubNetworkInterface`
        """
        return self._sub_network_interface

    @sub_network_interface.setter
    def sub_network_interface(self, sub_network_interface):
        """Sets the sub_network_interface of this CreateSubNetworkInterfaceResponse.

        :param sub_network_interface: The sub_network_interface of this CreateSubNetworkInterfaceResponse.
        :type sub_network_interface: :class:`huaweicloudsdkvpc.v3.SubNetworkInterface`
        """
        self._sub_network_interface = sub_network_interface

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
        if not isinstance(other, CreateSubNetworkInterfaceResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
