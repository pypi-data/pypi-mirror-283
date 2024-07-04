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


class StringToDatetimeTransform(object):
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
        'column': 'str',
        'format': 'str',
        'output_column': 'str'
    }

    attribute_map = {
        'column': 'column',
        'format': 'format',
        'output_column': 'output_column'
    }

    def __init__(self, column=None, format=None, output_column=None):  # noqa: E501
        """StringToDatetimeTransform - a model defined in OpenAPI"""  # noqa: E501

        self._column = None
        self._format = None
        self._output_column = None
        self.discriminator = None

        self.column = column
        self.format = format
        self.output_column = output_column

    @property
    def column(self):
        """Gets the column of this StringToDatetimeTransform.  # noqa: E501


        :return: The column of this StringToDatetimeTransform.  # noqa: E501
        :rtype: str
        """
        return self._column

    @column.setter
    def column(self, column):
        """Sets the column of this StringToDatetimeTransform.


        :param column: The column of this StringToDatetimeTransform.  # noqa: E501
        :type: str
        """
        if column is None:
            raise ValueError("Invalid value for `column`, must not be `None`")  # noqa: E501

        self._column = column

    @property
    def format(self):
        """Gets the format of this StringToDatetimeTransform.  # noqa: E501


        :return: The format of this StringToDatetimeTransform.  # noqa: E501
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this StringToDatetimeTransform.


        :param format: The format of this StringToDatetimeTransform.  # noqa: E501
        :type: str
        """
        if format is None:
            raise ValueError("Invalid value for `format`, must not be `None`")  # noqa: E501

        self._format = format

    @property
    def output_column(self):
        """Gets the output_column of this StringToDatetimeTransform.  # noqa: E501


        :return: The output_column of this StringToDatetimeTransform.  # noqa: E501
        :rtype: str
        """
        return self._output_column

    @output_column.setter
    def output_column(self, output_column):
        """Sets the output_column of this StringToDatetimeTransform.


        :param output_column: The output_column of this StringToDatetimeTransform.  # noqa: E501
        :type: str
        """
        if output_column is None:
            raise ValueError("Invalid value for `output_column`, must not be `None`")  # noqa: E501

        self._output_column = output_column

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
        if not isinstance(other, StringToDatetimeTransform):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
