# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListObsObjectRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'bucket_name': 'str',
        'marker': 'str',
        'limit': 'int',
        'prefix': 'str'
    }

    attribute_map = {
        'bucket_name': 'bucket_name',
        'marker': 'marker',
        'limit': 'limit',
        'prefix': 'prefix'
    }

    def __init__(self, bucket_name=None, marker=None, limit=None, prefix=None):
        """ListObsObjectRequest

        The model defined in huaweicloud sdk

        :param bucket_name: obs桶名称
        :type bucket_name: str
        :param marker: 查询起始object名称
        :type marker: str
        :param limit: 单次查询条数
        :type limit: int
        :param prefix: 搜索前缀
        :type prefix: str
        """
        
        

        self._bucket_name = None
        self._marker = None
        self._limit = None
        self._prefix = None
        self.discriminator = None

        self.bucket_name = bucket_name
        if marker is not None:
            self.marker = marker
        self.limit = limit
        if prefix is not None:
            self.prefix = prefix

    @property
    def bucket_name(self):
        """Gets the bucket_name of this ListObsObjectRequest.

        obs桶名称

        :return: The bucket_name of this ListObsObjectRequest.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """Sets the bucket_name of this ListObsObjectRequest.

        obs桶名称

        :param bucket_name: The bucket_name of this ListObsObjectRequest.
        :type bucket_name: str
        """
        self._bucket_name = bucket_name

    @property
    def marker(self):
        """Gets the marker of this ListObsObjectRequest.

        查询起始object名称

        :return: The marker of this ListObsObjectRequest.
        :rtype: str
        """
        return self._marker

    @marker.setter
    def marker(self, marker):
        """Sets the marker of this ListObsObjectRequest.

        查询起始object名称

        :param marker: The marker of this ListObsObjectRequest.
        :type marker: str
        """
        self._marker = marker

    @property
    def limit(self):
        """Gets the limit of this ListObsObjectRequest.

        单次查询条数

        :return: The limit of this ListObsObjectRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListObsObjectRequest.

        单次查询条数

        :param limit: The limit of this ListObsObjectRequest.
        :type limit: int
        """
        self._limit = limit

    @property
    def prefix(self):
        """Gets the prefix of this ListObsObjectRequest.

        搜索前缀

        :return: The prefix of this ListObsObjectRequest.
        :rtype: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """Sets the prefix of this ListObsObjectRequest.

        搜索前缀

        :param prefix: The prefix of this ListObsObjectRequest.
        :type prefix: str
        """
        self._prefix = prefix

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
        if not isinstance(other, ListObsObjectRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
