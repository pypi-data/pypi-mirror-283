# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class AuthorizerBase:

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
        'type': 'str',
        'authorizer_type': 'str',
        'authorizer_uri': 'str',
        'authorizer_version': 'str',
        'authorizer_alias_uri': 'str',
        'identities': 'list[Identity]',
        'ttl': 'int',
        'user_data': 'str',
        'ld_api_id': 'str',
        'need_body': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'type': 'type',
        'authorizer_type': 'authorizer_type',
        'authorizer_uri': 'authorizer_uri',
        'authorizer_version': 'authorizer_version',
        'authorizer_alias_uri': 'authorizer_alias_uri',
        'identities': 'identities',
        'ttl': 'ttl',
        'user_data': 'user_data',
        'ld_api_id': 'ld_api_id',
        'need_body': 'need_body'
    }

    def __init__(self, name=None, type=None, authorizer_type=None, authorizer_uri=None, authorizer_version=None, authorizer_alias_uri=None, identities=None, ttl=None, user_data=None, ld_api_id=None, need_body=None):
        """AuthorizerBase

        The model defined in huaweicloud sdk

        :param name: 自定义认证的名称。 长度为3 ~ 64位的字符串，字符串由中文、英文字母、数字、“_”组成，且只能以英文或中文开头。 
        :type name: str
        :param type: 自定义认证类型  - FRONTEND：前端 - BACKEND：后端
        :type type: str
        :param authorizer_type: 自定义认证函数类型： - LD：自定义后端函数 - FUNC：[函数服务函数](tag:hws,hws_hk,hcs,hcs_sm,fcs,g42)[暂不支持](tag:Site)
        :type authorizer_type: str
        :param authorizer_uri: 函数地址。  注意：使用自定义后端的函数API，API请求方法必须为POST，且API状态必须为已部署。
        :type authorizer_uri: str
        :param authorizer_version: 函数版本。  当函数别名URN和函数版本同时传入时，函数版本将被忽略，只会使用函数别名URN
        :type authorizer_version: str
        :param authorizer_alias_uri: 函数别名地址。  当函数别名URN和函数版本同时传入时，函数版本将被忽略，只会使用函数别名URN
        :type authorizer_alias_uri: str
        :param identities: 认证来源
        :type identities: list[:class:`huaweicloudsdkroma.v2.Identity`]
        :param ttl: 缓存时间
        :type ttl: int
        :param user_data: 用户数据
        :type user_data: str
        :param ld_api_id: 自定义后端服务ID。  自定义认证函数类型为LD时必填
        :type ld_api_id: str
        :param need_body: 是否发送body
        :type need_body: bool
        """
        
        

        self._name = None
        self._type = None
        self._authorizer_type = None
        self._authorizer_uri = None
        self._authorizer_version = None
        self._authorizer_alias_uri = None
        self._identities = None
        self._ttl = None
        self._user_data = None
        self._ld_api_id = None
        self._need_body = None
        self.discriminator = None

        self.name = name
        self.type = type
        self.authorizer_type = authorizer_type
        self.authorizer_uri = authorizer_uri
        if authorizer_version is not None:
            self.authorizer_version = authorizer_version
        if authorizer_alias_uri is not None:
            self.authorizer_alias_uri = authorizer_alias_uri
        if identities is not None:
            self.identities = identities
        if ttl is not None:
            self.ttl = ttl
        if user_data is not None:
            self.user_data = user_data
        if ld_api_id is not None:
            self.ld_api_id = ld_api_id
        if need_body is not None:
            self.need_body = need_body

    @property
    def name(self):
        """Gets the name of this AuthorizerBase.

        自定义认证的名称。 长度为3 ~ 64位的字符串，字符串由中文、英文字母、数字、“_”组成，且只能以英文或中文开头。 

        :return: The name of this AuthorizerBase.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AuthorizerBase.

        自定义认证的名称。 长度为3 ~ 64位的字符串，字符串由中文、英文字母、数字、“_”组成，且只能以英文或中文开头。 

        :param name: The name of this AuthorizerBase.
        :type name: str
        """
        self._name = name

    @property
    def type(self):
        """Gets the type of this AuthorizerBase.

        自定义认证类型  - FRONTEND：前端 - BACKEND：后端

        :return: The type of this AuthorizerBase.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this AuthorizerBase.

        自定义认证类型  - FRONTEND：前端 - BACKEND：后端

        :param type: The type of this AuthorizerBase.
        :type type: str
        """
        self._type = type

    @property
    def authorizer_type(self):
        """Gets the authorizer_type of this AuthorizerBase.

        自定义认证函数类型： - LD：自定义后端函数 - FUNC：[函数服务函数](tag:hws,hws_hk,hcs,hcs_sm,fcs,g42)[暂不支持](tag:Site)

        :return: The authorizer_type of this AuthorizerBase.
        :rtype: str
        """
        return self._authorizer_type

    @authorizer_type.setter
    def authorizer_type(self, authorizer_type):
        """Sets the authorizer_type of this AuthorizerBase.

        自定义认证函数类型： - LD：自定义后端函数 - FUNC：[函数服务函数](tag:hws,hws_hk,hcs,hcs_sm,fcs,g42)[暂不支持](tag:Site)

        :param authorizer_type: The authorizer_type of this AuthorizerBase.
        :type authorizer_type: str
        """
        self._authorizer_type = authorizer_type

    @property
    def authorizer_uri(self):
        """Gets the authorizer_uri of this AuthorizerBase.

        函数地址。  注意：使用自定义后端的函数API，API请求方法必须为POST，且API状态必须为已部署。

        :return: The authorizer_uri of this AuthorizerBase.
        :rtype: str
        """
        return self._authorizer_uri

    @authorizer_uri.setter
    def authorizer_uri(self, authorizer_uri):
        """Sets the authorizer_uri of this AuthorizerBase.

        函数地址。  注意：使用自定义后端的函数API，API请求方法必须为POST，且API状态必须为已部署。

        :param authorizer_uri: The authorizer_uri of this AuthorizerBase.
        :type authorizer_uri: str
        """
        self._authorizer_uri = authorizer_uri

    @property
    def authorizer_version(self):
        """Gets the authorizer_version of this AuthorizerBase.

        函数版本。  当函数别名URN和函数版本同时传入时，函数版本将被忽略，只会使用函数别名URN

        :return: The authorizer_version of this AuthorizerBase.
        :rtype: str
        """
        return self._authorizer_version

    @authorizer_version.setter
    def authorizer_version(self, authorizer_version):
        """Sets the authorizer_version of this AuthorizerBase.

        函数版本。  当函数别名URN和函数版本同时传入时，函数版本将被忽略，只会使用函数别名URN

        :param authorizer_version: The authorizer_version of this AuthorizerBase.
        :type authorizer_version: str
        """
        self._authorizer_version = authorizer_version

    @property
    def authorizer_alias_uri(self):
        """Gets the authorizer_alias_uri of this AuthorizerBase.

        函数别名地址。  当函数别名URN和函数版本同时传入时，函数版本将被忽略，只会使用函数别名URN

        :return: The authorizer_alias_uri of this AuthorizerBase.
        :rtype: str
        """
        return self._authorizer_alias_uri

    @authorizer_alias_uri.setter
    def authorizer_alias_uri(self, authorizer_alias_uri):
        """Sets the authorizer_alias_uri of this AuthorizerBase.

        函数别名地址。  当函数别名URN和函数版本同时传入时，函数版本将被忽略，只会使用函数别名URN

        :param authorizer_alias_uri: The authorizer_alias_uri of this AuthorizerBase.
        :type authorizer_alias_uri: str
        """
        self._authorizer_alias_uri = authorizer_alias_uri

    @property
    def identities(self):
        """Gets the identities of this AuthorizerBase.

        认证来源

        :return: The identities of this AuthorizerBase.
        :rtype: list[:class:`huaweicloudsdkroma.v2.Identity`]
        """
        return self._identities

    @identities.setter
    def identities(self, identities):
        """Sets the identities of this AuthorizerBase.

        认证来源

        :param identities: The identities of this AuthorizerBase.
        :type identities: list[:class:`huaweicloudsdkroma.v2.Identity`]
        """
        self._identities = identities

    @property
    def ttl(self):
        """Gets the ttl of this AuthorizerBase.

        缓存时间

        :return: The ttl of this AuthorizerBase.
        :rtype: int
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """Sets the ttl of this AuthorizerBase.

        缓存时间

        :param ttl: The ttl of this AuthorizerBase.
        :type ttl: int
        """
        self._ttl = ttl

    @property
    def user_data(self):
        """Gets the user_data of this AuthorizerBase.

        用户数据

        :return: The user_data of this AuthorizerBase.
        :rtype: str
        """
        return self._user_data

    @user_data.setter
    def user_data(self, user_data):
        """Sets the user_data of this AuthorizerBase.

        用户数据

        :param user_data: The user_data of this AuthorizerBase.
        :type user_data: str
        """
        self._user_data = user_data

    @property
    def ld_api_id(self):
        """Gets the ld_api_id of this AuthorizerBase.

        自定义后端服务ID。  自定义认证函数类型为LD时必填

        :return: The ld_api_id of this AuthorizerBase.
        :rtype: str
        """
        return self._ld_api_id

    @ld_api_id.setter
    def ld_api_id(self, ld_api_id):
        """Sets the ld_api_id of this AuthorizerBase.

        自定义后端服务ID。  自定义认证函数类型为LD时必填

        :param ld_api_id: The ld_api_id of this AuthorizerBase.
        :type ld_api_id: str
        """
        self._ld_api_id = ld_api_id

    @property
    def need_body(self):
        """Gets the need_body of this AuthorizerBase.

        是否发送body

        :return: The need_body of this AuthorizerBase.
        :rtype: bool
        """
        return self._need_body

    @need_body.setter
    def need_body(self, need_body):
        """Sets the need_body of this AuthorizerBase.

        是否发送body

        :param need_body: The need_body of this AuthorizerBase.
        :type need_body: bool
        """
        self._need_body = need_body

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
        if not isinstance(other, AuthorizerBase):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
