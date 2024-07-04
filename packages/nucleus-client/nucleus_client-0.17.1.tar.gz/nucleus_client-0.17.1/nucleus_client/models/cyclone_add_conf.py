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


class CycloneAddConf(object):
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
        'description': 'str',
        'destinations': 'list[CycloneConfDestination]',
        'is_etl': 'bool',
        'name': 'str',
        'old_name': 'str',
        'run_once': 'bool',
        'run_once_complete': 'bool',
        'schedule': 'str',
        'source': 'CycloneConfSource',
        'status': 'str'
    }

    attribute_map = {
        'description': 'description',
        'destinations': 'destinations',
        'is_etl': 'is_etl',
        'name': 'name',
        'old_name': 'old_name',
        'run_once': 'run_once',
        'run_once_complete': 'run_once_complete',
        'schedule': 'schedule',
        'source': 'source',
        'status': 'status'
    }

    def __init__(self, description=None, destinations=None, is_etl=None, name=None, old_name=None, run_once=None, run_once_complete=None, schedule=None, source=None, status=None):  # noqa: E501
        """CycloneAddConf - a model defined in OpenAPI"""  # noqa: E501

        self._description = None
        self._destinations = None
        self._is_etl = None
        self._name = None
        self._old_name = None
        self._run_once = None
        self._run_once_complete = None
        self._schedule = None
        self._source = None
        self._status = None
        self.discriminator = None

        if description is not None:
            self.description = description
        self.destinations = destinations
        if is_etl is not None:
            self.is_etl = is_etl
        self.name = name
        if old_name is not None:
            self.old_name = old_name
        if run_once is not None:
            self.run_once = run_once
        if run_once_complete is not None:
            self.run_once_complete = run_once_complete
        if schedule is not None:
            self.schedule = schedule
        self.source = source
        self.status = status

    @property
    def description(self):
        """Gets the description of this CycloneAddConf.  # noqa: E501


        :return: The description of this CycloneAddConf.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CycloneAddConf.


        :param description: The description of this CycloneAddConf.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def destinations(self):
        """Gets the destinations of this CycloneAddConf.  # noqa: E501


        :return: The destinations of this CycloneAddConf.  # noqa: E501
        :rtype: list[CycloneConfDestination]
        """
        return self._destinations

    @destinations.setter
    def destinations(self, destinations):
        """Sets the destinations of this CycloneAddConf.


        :param destinations: The destinations of this CycloneAddConf.  # noqa: E501
        :type: list[CycloneConfDestination]
        """
        if destinations is None:
            raise ValueError("Invalid value for `destinations`, must not be `None`")  # noqa: E501

        self._destinations = destinations

    @property
    def is_etl(self):
        """Gets the is_etl of this CycloneAddConf.  # noqa: E501


        :return: The is_etl of this CycloneAddConf.  # noqa: E501
        :rtype: bool
        """
        return self._is_etl

    @is_etl.setter
    def is_etl(self, is_etl):
        """Sets the is_etl of this CycloneAddConf.


        :param is_etl: The is_etl of this CycloneAddConf.  # noqa: E501
        :type: bool
        """

        self._is_etl = is_etl

    @property
    def name(self):
        """Gets the name of this CycloneAddConf.  # noqa: E501


        :return: The name of this CycloneAddConf.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CycloneAddConf.


        :param name: The name of this CycloneAddConf.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def old_name(self):
        """Gets the old_name of this CycloneAddConf.  # noqa: E501


        :return: The old_name of this CycloneAddConf.  # noqa: E501
        :rtype: str
        """
        return self._old_name

    @old_name.setter
    def old_name(self, old_name):
        """Sets the old_name of this CycloneAddConf.


        :param old_name: The old_name of this CycloneAddConf.  # noqa: E501
        :type: str
        """

        self._old_name = old_name

    @property
    def run_once(self):
        """Gets the run_once of this CycloneAddConf.  # noqa: E501


        :return: The run_once of this CycloneAddConf.  # noqa: E501
        :rtype: bool
        """
        return self._run_once

    @run_once.setter
    def run_once(self, run_once):
        """Sets the run_once of this CycloneAddConf.


        :param run_once: The run_once of this CycloneAddConf.  # noqa: E501
        :type: bool
        """

        self._run_once = run_once

    @property
    def run_once_complete(self):
        """Gets the run_once_complete of this CycloneAddConf.  # noqa: E501


        :return: The run_once_complete of this CycloneAddConf.  # noqa: E501
        :rtype: bool
        """
        return self._run_once_complete

    @run_once_complete.setter
    def run_once_complete(self, run_once_complete):
        """Sets the run_once_complete of this CycloneAddConf.


        :param run_once_complete: The run_once_complete of this CycloneAddConf.  # noqa: E501
        :type: bool
        """

        self._run_once_complete = run_once_complete

    @property
    def schedule(self):
        """Gets the schedule of this CycloneAddConf.  # noqa: E501


        :return: The schedule of this CycloneAddConf.  # noqa: E501
        :rtype: str
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """Sets the schedule of this CycloneAddConf.


        :param schedule: The schedule of this CycloneAddConf.  # noqa: E501
        :type: str
        """

        self._schedule = schedule

    @property
    def source(self):
        """Gets the source of this CycloneAddConf.  # noqa: E501


        :return: The source of this CycloneAddConf.  # noqa: E501
        :rtype: CycloneConfSource
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this CycloneAddConf.


        :param source: The source of this CycloneAddConf.  # noqa: E501
        :type: CycloneConfSource
        """
        if source is None:
            raise ValueError("Invalid value for `source`, must not be `None`")  # noqa: E501

        self._source = source

    @property
    def status(self):
        """Gets the status of this CycloneAddConf.  # noqa: E501


        :return: The status of this CycloneAddConf.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this CycloneAddConf.


        :param status: The status of this CycloneAddConf.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

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
        if not isinstance(other, CycloneAddConf):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
