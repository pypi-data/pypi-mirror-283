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


class ComplexDataset(object):
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
        'activity_type': 'str',
        'filters': 'list[dict(str, object)]',
        'partner_id': 'str'
    }

    attribute_map = {
        'activity_type': 'activity_type',
        'filters': 'filters',
        'partner_id': 'partner_id'
    }

    def __init__(self, activity_type=None, filters=None, partner_id=None):  # noqa: E501
        """ComplexDataset - a model defined in OpenAPI"""  # noqa: E501

        self._activity_type = None
        self._filters = None
        self._partner_id = None
        self.discriminator = None

        self.activity_type = activity_type
        if filters is not None:
            self.filters = filters
        if partner_id is not None:
            self.partner_id = partner_id

    @property
    def activity_type(self):
        """Gets the activity_type of this ComplexDataset.  # noqa: E501


        :return: The activity_type of this ComplexDataset.  # noqa: E501
        :rtype: str
        """
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        """Sets the activity_type of this ComplexDataset.


        :param activity_type: The activity_type of this ComplexDataset.  # noqa: E501
        :type: str
        """
        if activity_type is None:
            raise ValueError("Invalid value for `activity_type`, must not be `None`")  # noqa: E501

        self._activity_type = activity_type

    @property
    def filters(self):
        """Gets the filters of this ComplexDataset.  # noqa: E501


        :return: The filters of this ComplexDataset.  # noqa: E501
        :rtype: list[dict(str, object)]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this ComplexDataset.


        :param filters: The filters of this ComplexDataset.  # noqa: E501
        :type: list[dict(str, object)]
        """

        self._filters = filters

    @property
    def partner_id(self):
        """Gets the partner_id of this ComplexDataset.  # noqa: E501


        :return: The partner_id of this ComplexDataset.  # noqa: E501
        :rtype: str
        """
        return self._partner_id

    @partner_id.setter
    def partner_id(self, partner_id):
        """Sets the partner_id of this ComplexDataset.


        :param partner_id: The partner_id of this ComplexDataset.  # noqa: E501
        :type: str
        """

        self._partner_id = partner_id

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
        if not isinstance(other, ComplexDataset):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
