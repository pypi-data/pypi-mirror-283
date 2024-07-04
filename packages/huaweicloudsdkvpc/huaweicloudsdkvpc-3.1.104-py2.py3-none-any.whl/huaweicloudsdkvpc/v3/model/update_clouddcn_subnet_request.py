# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateClouddcnSubnetRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'clouddcn_subnet_id': 'str',
        'body': 'UpdateClouddcnSubnetRequestBody'
    }

    attribute_map = {
        'clouddcn_subnet_id': 'clouddcn_subnet_id',
        'body': 'body'
    }

    def __init__(self, clouddcn_subnet_id=None, body=None):
        """UpdateClouddcnSubnetRequest

        The model defined in huaweicloud sdk

        :param clouddcn_subnet_id: clouddcn子网ID
        :type clouddcn_subnet_id: str
        :param body: Body of the UpdateClouddcnSubnetRequest
        :type body: :class:`huaweicloudsdkvpc.v3.UpdateClouddcnSubnetRequestBody`
        """
        
        

        self._clouddcn_subnet_id = None
        self._body = None
        self.discriminator = None

        self.clouddcn_subnet_id = clouddcn_subnet_id
        if body is not None:
            self.body = body

    @property
    def clouddcn_subnet_id(self):
        """Gets the clouddcn_subnet_id of this UpdateClouddcnSubnetRequest.

        clouddcn子网ID

        :return: The clouddcn_subnet_id of this UpdateClouddcnSubnetRequest.
        :rtype: str
        """
        return self._clouddcn_subnet_id

    @clouddcn_subnet_id.setter
    def clouddcn_subnet_id(self, clouddcn_subnet_id):
        """Sets the clouddcn_subnet_id of this UpdateClouddcnSubnetRequest.

        clouddcn子网ID

        :param clouddcn_subnet_id: The clouddcn_subnet_id of this UpdateClouddcnSubnetRequest.
        :type clouddcn_subnet_id: str
        """
        self._clouddcn_subnet_id = clouddcn_subnet_id

    @property
    def body(self):
        """Gets the body of this UpdateClouddcnSubnetRequest.

        :return: The body of this UpdateClouddcnSubnetRequest.
        :rtype: :class:`huaweicloudsdkvpc.v3.UpdateClouddcnSubnetRequestBody`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this UpdateClouddcnSubnetRequest.

        :param body: The body of this UpdateClouddcnSubnetRequest.
        :type body: :class:`huaweicloudsdkvpc.v3.UpdateClouddcnSubnetRequestBody`
        """
        self._body = body

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
        if not isinstance(other, UpdateClouddcnSubnetRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
