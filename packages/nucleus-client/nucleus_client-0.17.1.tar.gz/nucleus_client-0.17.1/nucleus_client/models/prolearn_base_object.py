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


class ProlearnBaseObject(object):
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
        'created': 'datetime',
        'name': 'str',
        'updated': 'datetime',
        'id': 'str'
    }

    attribute_map = {
        'created': 'Created',
        'name': 'Name',
        'updated': 'Updated',
        'id': 'id'
    }

    def __init__(self, created=None, name=None, updated=None, id=None):  # noqa: E501
        """ProlearnBaseObject - a model defined in OpenAPI"""  # noqa: E501

        self._created = None
        self._name = None
        self._updated = None
        self._id = None
        self.discriminator = None

        if created is not None:
            self.created = created
        if name is not None:
            self.name = name
        self.updated = updated
        self.id = id

    @property
    def created(self):
        """Gets the created of this ProlearnBaseObject.  # noqa: E501


        :return: The created of this ProlearnBaseObject.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this ProlearnBaseObject.


        :param created: The created of this ProlearnBaseObject.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def name(self):
        """Gets the name of this ProlearnBaseObject.  # noqa: E501


        :return: The name of this ProlearnBaseObject.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ProlearnBaseObject.


        :param name: The name of this ProlearnBaseObject.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def updated(self):
        """Gets the updated of this ProlearnBaseObject.  # noqa: E501


        :return: The updated of this ProlearnBaseObject.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this ProlearnBaseObject.


        :param updated: The updated of this ProlearnBaseObject.  # noqa: E501
        :type: datetime
        """
        if updated is None:
            raise ValueError("Invalid value for `updated`, must not be `None`")  # noqa: E501

        self._updated = updated

    @property
    def id(self):
        """Gets the id of this ProlearnBaseObject.  # noqa: E501


        :return: The id of this ProlearnBaseObject.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ProlearnBaseObject.


        :param id: The id of this ProlearnBaseObject.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

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
        if not isinstance(other, ProlearnBaseObject):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
