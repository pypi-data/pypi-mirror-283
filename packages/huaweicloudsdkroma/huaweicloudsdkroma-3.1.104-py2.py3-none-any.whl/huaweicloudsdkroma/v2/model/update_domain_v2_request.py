# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateDomainV2Request:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'instance_id': 'str',
        'group_id': 'str',
        'domain_id': 'str',
        'body': 'UrlDomainModify'
    }

    attribute_map = {
        'instance_id': 'instance_id',
        'group_id': 'group_id',
        'domain_id': 'domain_id',
        'body': 'body'
    }

    def __init__(self, instance_id=None, group_id=None, domain_id=None, body=None):
        """UpdateDomainV2Request

        The model defined in huaweicloud sdk

        :param instance_id: 实例ID
        :type instance_id: str
        :param group_id: 分组的编号
        :type group_id: str
        :param domain_id: 域名的编号
        :type domain_id: str
        :param body: Body of the UpdateDomainV2Request
        :type body: :class:`huaweicloudsdkroma.v2.UrlDomainModify`
        """
        
        

        self._instance_id = None
        self._group_id = None
        self._domain_id = None
        self._body = None
        self.discriminator = None

        self.instance_id = instance_id
        self.group_id = group_id
        self.domain_id = domain_id
        if body is not None:
            self.body = body

    @property
    def instance_id(self):
        """Gets the instance_id of this UpdateDomainV2Request.

        实例ID

        :return: The instance_id of this UpdateDomainV2Request.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this UpdateDomainV2Request.

        实例ID

        :param instance_id: The instance_id of this UpdateDomainV2Request.
        :type instance_id: str
        """
        self._instance_id = instance_id

    @property
    def group_id(self):
        """Gets the group_id of this UpdateDomainV2Request.

        分组的编号

        :return: The group_id of this UpdateDomainV2Request.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """Sets the group_id of this UpdateDomainV2Request.

        分组的编号

        :param group_id: The group_id of this UpdateDomainV2Request.
        :type group_id: str
        """
        self._group_id = group_id

    @property
    def domain_id(self):
        """Gets the domain_id of this UpdateDomainV2Request.

        域名的编号

        :return: The domain_id of this UpdateDomainV2Request.
        :rtype: str
        """
        return self._domain_id

    @domain_id.setter
    def domain_id(self, domain_id):
        """Sets the domain_id of this UpdateDomainV2Request.

        域名的编号

        :param domain_id: The domain_id of this UpdateDomainV2Request.
        :type domain_id: str
        """
        self._domain_id = domain_id

    @property
    def body(self):
        """Gets the body of this UpdateDomainV2Request.

        :return: The body of this UpdateDomainV2Request.
        :rtype: :class:`huaweicloudsdkroma.v2.UrlDomainModify`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this UpdateDomainV2Request.

        :param body: The body of this UpdateDomainV2Request.
        :type body: :class:`huaweicloudsdkroma.v2.UrlDomainModify`
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
        if not isinstance(other, UpdateDomainV2Request):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
