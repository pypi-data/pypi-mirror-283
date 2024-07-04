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


class SchemaFieldMetadata(object):
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
        'dimension': 'bool',
        'metric': 'bool',
        'table': 'str'
    }

    attribute_map = {
        'dimension': 'dimension',
        'metric': 'metric',
        'table': 'table'
    }

    def __init__(self, dimension=None, metric=None, table=None):  # noqa: E501
        """SchemaFieldMetadata - a model defined in OpenAPI"""  # noqa: E501

        self._dimension = None
        self._metric = None
        self._table = None
        self.discriminator = None

        if dimension is not None:
            self.dimension = dimension
        if metric is not None:
            self.metric = metric
        if table is not None:
            self.table = table

    @property
    def dimension(self):
        """Gets the dimension of this SchemaFieldMetadata.  # noqa: E501


        :return: The dimension of this SchemaFieldMetadata.  # noqa: E501
        :rtype: bool
        """
        return self._dimension

    @dimension.setter
    def dimension(self, dimension):
        """Sets the dimension of this SchemaFieldMetadata.


        :param dimension: The dimension of this SchemaFieldMetadata.  # noqa: E501
        :type: bool
        """

        self._dimension = dimension

    @property
    def metric(self):
        """Gets the metric of this SchemaFieldMetadata.  # noqa: E501


        :return: The metric of this SchemaFieldMetadata.  # noqa: E501
        :rtype: bool
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """Sets the metric of this SchemaFieldMetadata.


        :param metric: The metric of this SchemaFieldMetadata.  # noqa: E501
        :type: bool
        """

        self._metric = metric

    @property
    def table(self):
        """Gets the table of this SchemaFieldMetadata.  # noqa: E501


        :return: The table of this SchemaFieldMetadata.  # noqa: E501
        :rtype: str
        """
        return self._table

    @table.setter
    def table(self, table):
        """Sets the table of this SchemaFieldMetadata.


        :param table: The table of this SchemaFieldMetadata.  # noqa: E501
        :type: str
        """

        self._table = table

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
        if not isinstance(other, SchemaFieldMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
