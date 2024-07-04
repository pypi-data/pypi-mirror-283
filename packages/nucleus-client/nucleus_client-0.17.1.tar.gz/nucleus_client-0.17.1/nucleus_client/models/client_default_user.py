# coding: utf-8

"""
    Nucleus API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ClientDefaultUser(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'default_login_policy': 'str',
        'default_user_id': 'str',
        'default_user_token': 'str'
    }

    attribute_map = {
        'default_login_policy': 'default_login_policy',
        'default_user_id': 'default_user_id',
        'default_user_token': 'default_user_token'
    }

    def __init__(self, default_login_policy=None, default_user_id=None, default_user_token=None):  # noqa: E501
        """ClientDefaultUser - a model defined in OpenAPI"""  # noqa: E501

        self._default_login_policy = None
        self._default_user_id = None
        self._default_user_token = None
        self.discriminator = None

        self.default_login_policy = default_login_policy
        self.default_user_id = default_user_id
        if default_user_token is not None:
            self.default_user_token = default_user_token

    @property
    def default_login_policy(self):
        """Gets the default_login_policy of this ClientDefaultUser.  # noqa: E501


        :return: The default_login_policy of this ClientDefaultUser.  # noqa: E501
        :rtype: str
        """
        return self._default_login_policy

    @default_login_policy.setter
    def default_login_policy(self, default_login_policy):
        """Sets the default_login_policy of this ClientDefaultUser.


        :param default_login_policy: The default_login_policy of this ClientDefaultUser.  # noqa: E501
        :type: str
        """
        if default_login_policy is None:
            raise ValueError("Invalid value for `default_login_policy`, must not be `None`")  # noqa: E501

        self._default_login_policy = default_login_policy

    @property
    def default_user_id(self):
        """Gets the default_user_id of this ClientDefaultUser.  # noqa: E501


        :return: The default_user_id of this ClientDefaultUser.  # noqa: E501
        :rtype: str
        """
        return self._default_user_id

    @default_user_id.setter
    def default_user_id(self, default_user_id):
        """Sets the default_user_id of this ClientDefaultUser.


        :param default_user_id: The default_user_id of this ClientDefaultUser.  # noqa: E501
        :type: str
        """
        if default_user_id is None:
            raise ValueError("Invalid value for `default_user_id`, must not be `None`")  # noqa: E501

        self._default_user_id = default_user_id

    @property
    def default_user_token(self):
        """Gets the default_user_token of this ClientDefaultUser.  # noqa: E501


        :return: The default_user_token of this ClientDefaultUser.  # noqa: E501
        :rtype: str
        """
        return self._default_user_token

    @default_user_token.setter
    def default_user_token(self, default_user_token):
        """Sets the default_user_token of this ClientDefaultUser.


        :param default_user_token: The default_user_token of this ClientDefaultUser.  # noqa: E501
        :type: str
        """

        self._default_user_token = default_user_token

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
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ClientDefaultUser):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
