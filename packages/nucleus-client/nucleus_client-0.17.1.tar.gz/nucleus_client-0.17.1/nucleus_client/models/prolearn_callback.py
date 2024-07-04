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


class ProlearnCallback(object):
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
        'course': 'ProlearnCourse',
        'event_type': 'str',
        'registration': 'ProlearnRegistration',
        'user': 'ProlearnUser',
        'owner_org': 'str'
    }

    attribute_map = {
        'course': 'Course',
        'event_type': 'EventType',
        'registration': 'Registration',
        'user': 'User',
        'owner_org': 'ownerOrg'
    }

    def __init__(self, course=None, event_type=None, registration=None, user=None, owner_org=None):  # noqa: E501
        """ProlearnCallback - a model defined in OpenAPI"""  # noqa: E501

        self._course = None
        self._event_type = None
        self._registration = None
        self._user = None
        self._owner_org = None
        self.discriminator = None

        if course is not None:
            self.course = course
        if event_type is not None:
            self.event_type = event_type
        if registration is not None:
            self.registration = registration
        if user is not None:
            self.user = user
        if owner_org is not None:
            self.owner_org = owner_org

    @property
    def course(self):
        """Gets the course of this ProlearnCallback.  # noqa: E501


        :return: The course of this ProlearnCallback.  # noqa: E501
        :rtype: ProlearnCourse
        """
        return self._course

    @course.setter
    def course(self, course):
        """Sets the course of this ProlearnCallback.


        :param course: The course of this ProlearnCallback.  # noqa: E501
        :type: ProlearnCourse
        """

        self._course = course

    @property
    def event_type(self):
        """Gets the event_type of this ProlearnCallback.  # noqa: E501


        :return: The event_type of this ProlearnCallback.  # noqa: E501
        :rtype: str
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """Sets the event_type of this ProlearnCallback.


        :param event_type: The event_type of this ProlearnCallback.  # noqa: E501
        :type: str
        """

        self._event_type = event_type

    @property
    def registration(self):
        """Gets the registration of this ProlearnCallback.  # noqa: E501


        :return: The registration of this ProlearnCallback.  # noqa: E501
        :rtype: ProlearnRegistration
        """
        return self._registration

    @registration.setter
    def registration(self, registration):
        """Sets the registration of this ProlearnCallback.


        :param registration: The registration of this ProlearnCallback.  # noqa: E501
        :type: ProlearnRegistration
        """

        self._registration = registration

    @property
    def user(self):
        """Gets the user of this ProlearnCallback.  # noqa: E501


        :return: The user of this ProlearnCallback.  # noqa: E501
        :rtype: ProlearnUser
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this ProlearnCallback.


        :param user: The user of this ProlearnCallback.  # noqa: E501
        :type: ProlearnUser
        """

        self._user = user

    @property
    def owner_org(self):
        """Gets the owner_org of this ProlearnCallback.  # noqa: E501


        :return: The owner_org of this ProlearnCallback.  # noqa: E501
        :rtype: str
        """
        return self._owner_org

    @owner_org.setter
    def owner_org(self, owner_org):
        """Sets the owner_org of this ProlearnCallback.


        :param owner_org: The owner_org of this ProlearnCallback.  # noqa: E501
        :type: str
        """

        self._owner_org = owner_org

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
        if not isinstance(other, ProlearnCallback):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
