# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class RemoveSourcesFromTrafficMirrorSessionRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'traffic_mirror_session_id': 'str',
        'body': 'RemoveSourcesFromTrafficMirrorSessionRequestBody'
    }

    attribute_map = {
        'traffic_mirror_session_id': 'traffic_mirror_session_id',
        'body': 'body'
    }

    def __init__(self, traffic_mirror_session_id=None, body=None):
        """RemoveSourcesFromTrafficMirrorSessionRequest

        The model defined in huaweicloud sdk

        :param traffic_mirror_session_id: 流量镜像会话ID
        :type traffic_mirror_session_id: str
        :param body: Body of the RemoveSourcesFromTrafficMirrorSessionRequest
        :type body: :class:`huaweicloudsdkvpc.v3.RemoveSourcesFromTrafficMirrorSessionRequestBody`
        """
        
        

        self._traffic_mirror_session_id = None
        self._body = None
        self.discriminator = None

        self.traffic_mirror_session_id = traffic_mirror_session_id
        if body is not None:
            self.body = body

    @property
    def traffic_mirror_session_id(self):
        """Gets the traffic_mirror_session_id of this RemoveSourcesFromTrafficMirrorSessionRequest.

        流量镜像会话ID

        :return: The traffic_mirror_session_id of this RemoveSourcesFromTrafficMirrorSessionRequest.
        :rtype: str
        """
        return self._traffic_mirror_session_id

    @traffic_mirror_session_id.setter
    def traffic_mirror_session_id(self, traffic_mirror_session_id):
        """Sets the traffic_mirror_session_id of this RemoveSourcesFromTrafficMirrorSessionRequest.

        流量镜像会话ID

        :param traffic_mirror_session_id: The traffic_mirror_session_id of this RemoveSourcesFromTrafficMirrorSessionRequest.
        :type traffic_mirror_session_id: str
        """
        self._traffic_mirror_session_id = traffic_mirror_session_id

    @property
    def body(self):
        """Gets the body of this RemoveSourcesFromTrafficMirrorSessionRequest.

        :return: The body of this RemoveSourcesFromTrafficMirrorSessionRequest.
        :rtype: :class:`huaweicloudsdkvpc.v3.RemoveSourcesFromTrafficMirrorSessionRequestBody`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this RemoveSourcesFromTrafficMirrorSessionRequest.

        :param body: The body of this RemoveSourcesFromTrafficMirrorSessionRequest.
        :type body: :class:`huaweicloudsdkvpc.v3.RemoveSourcesFromTrafficMirrorSessionRequestBody`
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
        if not isinstance(other, RemoveSourcesFromTrafficMirrorSessionRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
