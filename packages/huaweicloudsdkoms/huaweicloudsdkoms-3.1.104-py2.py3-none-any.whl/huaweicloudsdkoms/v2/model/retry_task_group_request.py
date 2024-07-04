# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class RetryTaskGroupRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'group_id': 'str',
        'body': 'RetryTaskGroupReq'
    }

    attribute_map = {
        'group_id': 'group_id',
        'body': 'body'
    }

    def __init__(self, group_id=None, body=None):
        """RetryTaskGroupRequest

        The model defined in huaweicloud sdk

        :param group_id: 任务组id
        :type group_id: str
        :param body: Body of the RetryTaskGroupRequest
        :type body: :class:`huaweicloudsdkoms.v2.RetryTaskGroupReq`
        """
        
        

        self._group_id = None
        self._body = None
        self.discriminator = None

        self.group_id = group_id
        if body is not None:
            self.body = body

    @property
    def group_id(self):
        """Gets the group_id of this RetryTaskGroupRequest.

        任务组id

        :return: The group_id of this RetryTaskGroupRequest.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """Sets the group_id of this RetryTaskGroupRequest.

        任务组id

        :param group_id: The group_id of this RetryTaskGroupRequest.
        :type group_id: str
        """
        self._group_id = group_id

    @property
    def body(self):
        """Gets the body of this RetryTaskGroupRequest.

        :return: The body of this RetryTaskGroupRequest.
        :rtype: :class:`huaweicloudsdkoms.v2.RetryTaskGroupReq`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this RetryTaskGroupRequest.

        :param body: The body of this RetryTaskGroupRequest.
        :type body: :class:`huaweicloudsdkoms.v2.RetryTaskGroupReq`
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
        if not isinstance(other, RetryTaskGroupRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
