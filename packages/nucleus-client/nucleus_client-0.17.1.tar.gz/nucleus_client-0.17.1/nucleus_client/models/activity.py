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


class Activity(object):
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
        'id': 'str',
        'activity_type': 'str',
        'client_id': 'str',
        'data': 'dict(str, object)',
        'dt_activity': 'datetime',
        'dt_u': 'datetime',
        'existing_entity_external_key': 'list[str]',
        'external_key': 'list[str]',
        'integration_id': 'str'
    }

    attribute_map = {
        'id': '_id',
        'activity_type': 'activity_type',
        'client_id': 'client_id',
        'data': 'data',
        'dt_activity': 'dt_activity',
        'dt_u': 'dt_u',
        'existing_entity_external_key': 'existing_entity_external_key',
        'external_key': 'external_key',
        'integration_id': 'integration_id'
    }

    def __init__(self, id=None, activity_type=None, client_id=None, data=None, dt_activity=None, dt_u=None, existing_entity_external_key=None, external_key=None, integration_id=None):  # noqa: E501
        """Activity - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._activity_type = None
        self._client_id = None
        self._data = None
        self._dt_activity = None
        self._dt_u = None
        self._existing_entity_external_key = None
        self._external_key = None
        self._integration_id = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if activity_type is not None:
            self.activity_type = activity_type
        if client_id is not None:
            self.client_id = client_id
        if data is not None:
            self.data = data
        if dt_activity is not None:
            self.dt_activity = dt_activity
        if dt_u is not None:
            self.dt_u = dt_u
        if existing_entity_external_key is not None:
            self.existing_entity_external_key = existing_entity_external_key
        if external_key is not None:
            self.external_key = external_key
        if integration_id is not None:
            self.integration_id = integration_id

    @property
    def id(self):
        """Gets the id of this Activity.  # noqa: E501


        :return: The id of this Activity.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Activity.


        :param id: The id of this Activity.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def activity_type(self):
        """Gets the activity_type of this Activity.  # noqa: E501


        :return: The activity_type of this Activity.  # noqa: E501
        :rtype: str
        """
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        """Sets the activity_type of this Activity.


        :param activity_type: The activity_type of this Activity.  # noqa: E501
        :type: str
        """

        self._activity_type = activity_type

    @property
    def client_id(self):
        """Gets the client_id of this Activity.  # noqa: E501


        :return: The client_id of this Activity.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this Activity.


        :param client_id: The client_id of this Activity.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def data(self):
        """Gets the data of this Activity.  # noqa: E501


        :return: The data of this Activity.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this Activity.


        :param data: The data of this Activity.  # noqa: E501
        :type: dict(str, object)
        """

        self._data = data

    @property
    def dt_activity(self):
        """Gets the dt_activity of this Activity.  # noqa: E501


        :return: The dt_activity of this Activity.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_activity

    @dt_activity.setter
    def dt_activity(self, dt_activity):
        """Sets the dt_activity of this Activity.


        :param dt_activity: The dt_activity of this Activity.  # noqa: E501
        :type: datetime
        """

        self._dt_activity = dt_activity

    @property
    def dt_u(self):
        """Gets the dt_u of this Activity.  # noqa: E501


        :return: The dt_u of this Activity.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_u

    @dt_u.setter
    def dt_u(self, dt_u):
        """Sets the dt_u of this Activity.


        :param dt_u: The dt_u of this Activity.  # noqa: E501
        :type: datetime
        """

        self._dt_u = dt_u

    @property
    def existing_entity_external_key(self):
        """Gets the existing_entity_external_key of this Activity.  # noqa: E501


        :return: The existing_entity_external_key of this Activity.  # noqa: E501
        :rtype: list[str]
        """
        return self._existing_entity_external_key

    @existing_entity_external_key.setter
    def existing_entity_external_key(self, existing_entity_external_key):
        """Sets the existing_entity_external_key of this Activity.


        :param existing_entity_external_key: The existing_entity_external_key of this Activity.  # noqa: E501
        :type: list[str]
        """

        self._existing_entity_external_key = existing_entity_external_key

    @property
    def external_key(self):
        """Gets the external_key of this Activity.  # noqa: E501


        :return: The external_key of this Activity.  # noqa: E501
        :rtype: list[str]
        """
        return self._external_key

    @external_key.setter
    def external_key(self, external_key):
        """Sets the external_key of this Activity.


        :param external_key: The external_key of this Activity.  # noqa: E501
        :type: list[str]
        """

        self._external_key = external_key

    @property
    def integration_id(self):
        """Gets the integration_id of this Activity.  # noqa: E501


        :return: The integration_id of this Activity.  # noqa: E501
        :rtype: str
        """
        return self._integration_id

    @integration_id.setter
    def integration_id(self, integration_id):
        """Sets the integration_id of this Activity.


        :param integration_id: The integration_id of this Activity.  # noqa: E501
        :type: str
        """

        self._integration_id = integration_id

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
        if not isinstance(other, Activity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
