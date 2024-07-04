# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class IpExtraSetOption:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'ip': 'str',
        'remarks': 'str'
    }

    attribute_map = {
        'ip': 'ip',
        'remarks': 'remarks'
    }

    def __init__(self, ip=None, remarks=None):
        """IpExtraSetOption

        The model defined in huaweicloud sdk

        :param ip: 功能说明：单个IP地址、IP地址范围或ip地址网段，支持IPv4、IPv6
        :type ip: str
        :param remarks: 功能说明：IP的备注信息 取值范围：0-255个字符，不能包含“&lt;”和“&gt;”。
        :type remarks: str
        """
        
        

        self._ip = None
        self._remarks = None
        self.discriminator = None

        self.ip = ip
        if remarks is not None:
            self.remarks = remarks

    @property
    def ip(self):
        """Gets the ip of this IpExtraSetOption.

        功能说明：单个IP地址、IP地址范围或ip地址网段，支持IPv4、IPv6

        :return: The ip of this IpExtraSetOption.
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this IpExtraSetOption.

        功能说明：单个IP地址、IP地址范围或ip地址网段，支持IPv4、IPv6

        :param ip: The ip of this IpExtraSetOption.
        :type ip: str
        """
        self._ip = ip

    @property
    def remarks(self):
        """Gets the remarks of this IpExtraSetOption.

        功能说明：IP的备注信息 取值范围：0-255个字符，不能包含“<”和“>”。

        :return: The remarks of this IpExtraSetOption.
        :rtype: str
        """
        return self._remarks

    @remarks.setter
    def remarks(self, remarks):
        """Sets the remarks of this IpExtraSetOption.

        功能说明：IP的备注信息 取值范围：0-255个字符，不能包含“<”和“>”。

        :param remarks: The remarks of this IpExtraSetOption.
        :type remarks: str
        """
        self._remarks = remarks

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
        if not isinstance(other, IpExtraSetOption):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
