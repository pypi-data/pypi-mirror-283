# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListRolesResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'roles': 'list[Role]',
        'page_info': 'PagedInfo'
    }

    attribute_map = {
        'roles': 'roles',
        'page_info': 'page_info'
    }

    def __init__(self, roles=None, page_info=None):
        """ListRolesResponse

        The model defined in huaweicloud sdk

        :param roles: 
        :type roles: list[:class:`huaweicloudsdklakeformation.v1.Role`]
        :param page_info: 
        :type page_info: :class:`huaweicloudsdklakeformation.v1.PagedInfo`
        """
        
        super(ListRolesResponse, self).__init__()

        self._roles = None
        self._page_info = None
        self.discriminator = None

        if roles is not None:
            self.roles = roles
        if page_info is not None:
            self.page_info = page_info

    @property
    def roles(self):
        """Gets the roles of this ListRolesResponse.

        :return: The roles of this ListRolesResponse.
        :rtype: list[:class:`huaweicloudsdklakeformation.v1.Role`]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this ListRolesResponse.

        :param roles: The roles of this ListRolesResponse.
        :type roles: list[:class:`huaweicloudsdklakeformation.v1.Role`]
        """
        self._roles = roles

    @property
    def page_info(self):
        """Gets the page_info of this ListRolesResponse.

        :return: The page_info of this ListRolesResponse.
        :rtype: :class:`huaweicloudsdklakeformation.v1.PagedInfo`
        """
        return self._page_info

    @page_info.setter
    def page_info(self, page_info):
        """Sets the page_info of this ListRolesResponse.

        :param page_info: The page_info of this ListRolesResponse.
        :type page_info: :class:`huaweicloudsdklakeformation.v1.PagedInfo`
        """
        self._page_info = page_info

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
        if not isinstance(other, ListRolesResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
