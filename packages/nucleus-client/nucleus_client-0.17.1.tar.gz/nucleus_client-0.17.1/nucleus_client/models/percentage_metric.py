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


class PercentageMetric(object):
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
        'exclude_column': 'str',
        'include_column': 'str',
        'include_columns': 'list[str]',
        'output_column': 'str',
        'population_dataset': 'str',
        'population_dimension': 'str',
        'population_id_field': 'str'
    }

    attribute_map = {
        'column': 'column',
        'exclude_column': 'exclude_column',
        'include_column': 'include_column',
        'include_columns': 'include_columns',
        'output_column': 'output_column',
        'population_dataset': 'population_dataset',
        'population_dimension': 'population_dimension',
        'population_id_field': 'population_id_field'
    }

    def __init__(self, column=None, exclude_column=None, include_column=None, include_columns=None, output_column=None, population_dataset=None, population_dimension=None, population_id_field=None):  # noqa: E501
        """PercentageMetric - a model defined in OpenAPI"""  # noqa: E501

        self._column = None
        self._exclude_column = None
        self._include_column = None
        self._include_columns = None
        self._output_column = None
        self._population_dataset = None
        self._population_dimension = None
        self._population_id_field = None
        self.discriminator = None

        self.column = column
        if exclude_column is not None:
            self.exclude_column = exclude_column
        if include_column is not None:
            self.include_column = include_column
        if include_columns is not None:
            self.include_columns = include_columns
        self.output_column = output_column
        self.population_dataset = population_dataset
        if population_dimension is not None:
            self.population_dimension = population_dimension
        if population_id_field is not None:
            self.population_id_field = population_id_field

    @property
    def column(self):
        """Gets the column of this PercentageMetric.  # noqa: E501


        :return: The column of this PercentageMetric.  # noqa: E501
        :rtype: str
        """
        return self._column

    @column.setter
    def column(self, column):
        """Sets the column of this PercentageMetric.


        :param column: The column of this PercentageMetric.  # noqa: E501
        :type: str
        """
        if column is None:
            raise ValueError("Invalid value for `column`, must not be `None`")  # noqa: E501

        self._column = column

    @property
    def exclude_column(self):
        """Gets the exclude_column of this PercentageMetric.  # noqa: E501


        :return: The exclude_column of this PercentageMetric.  # noqa: E501
        :rtype: str
        """
        return self._exclude_column

    @exclude_column.setter
    def exclude_column(self, exclude_column):
        """Sets the exclude_column of this PercentageMetric.


        :param exclude_column: The exclude_column of this PercentageMetric.  # noqa: E501
        :type: str
        """

        self._exclude_column = exclude_column

    @property
    def include_column(self):
        """Gets the include_column of this PercentageMetric.  # noqa: E501


        :return: The include_column of this PercentageMetric.  # noqa: E501
        :rtype: str
        """
        return self._include_column

    @include_column.setter
    def include_column(self, include_column):
        """Sets the include_column of this PercentageMetric.


        :param include_column: The include_column of this PercentageMetric.  # noqa: E501
        :type: str
        """

        self._include_column = include_column

    @property
    def include_columns(self):
        """Gets the include_columns of this PercentageMetric.  # noqa: E501


        :return: The include_columns of this PercentageMetric.  # noqa: E501
        :rtype: list[str]
        """
        return self._include_columns

    @include_columns.setter
    def include_columns(self, include_columns):
        """Sets the include_columns of this PercentageMetric.


        :param include_columns: The include_columns of this PercentageMetric.  # noqa: E501
        :type: list[str]
        """

        self._include_columns = include_columns

    @property
    def output_column(self):
        """Gets the output_column of this PercentageMetric.  # noqa: E501


        :return: The output_column of this PercentageMetric.  # noqa: E501
        :rtype: str
        """
        return self._output_column

    @output_column.setter
    def output_column(self, output_column):
        """Sets the output_column of this PercentageMetric.


        :param output_column: The output_column of this PercentageMetric.  # noqa: E501
        :type: str
        """
        if output_column is None:
            raise ValueError("Invalid value for `output_column`, must not be `None`")  # noqa: E501

        self._output_column = output_column

    @property
    def population_dataset(self):
        """Gets the population_dataset of this PercentageMetric.  # noqa: E501


        :return: The population_dataset of this PercentageMetric.  # noqa: E501
        :rtype: str
        """
        return self._population_dataset

    @population_dataset.setter
    def population_dataset(self, population_dataset):
        """Sets the population_dataset of this PercentageMetric.


        :param population_dataset: The population_dataset of this PercentageMetric.  # noqa: E501
        :type: str
        """
        if population_dataset is None:
            raise ValueError("Invalid value for `population_dataset`, must not be `None`")  # noqa: E501

        self._population_dataset = population_dataset

    @property
    def population_dimension(self):
        """Gets the population_dimension of this PercentageMetric.  # noqa: E501


        :return: The population_dimension of this PercentageMetric.  # noqa: E501
        :rtype: str
        """
        return self._population_dimension

    @population_dimension.setter
    def population_dimension(self, population_dimension):
        """Sets the population_dimension of this PercentageMetric.


        :param population_dimension: The population_dimension of this PercentageMetric.  # noqa: E501
        :type: str
        """

        self._population_dimension = population_dimension

    @property
    def population_id_field(self):
        """Gets the population_id_field of this PercentageMetric.  # noqa: E501


        :return: The population_id_field of this PercentageMetric.  # noqa: E501
        :rtype: str
        """
        return self._population_id_field

    @population_id_field.setter
    def population_id_field(self, population_id_field):
        """Sets the population_id_field of this PercentageMetric.


        :param population_id_field: The population_id_field of this PercentageMetric.  # noqa: E501
        :type: str
        """

        self._population_id_field = population_id_field

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
        if not isinstance(other, PercentageMetric):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
