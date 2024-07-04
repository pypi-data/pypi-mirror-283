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


class CycloneSqlResource(object):
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
        'activity_name': 'str',
        'alias_columns': 'list[CycloneSqlResourceAliasColumn]',
        'cdc_ext': 'CycloneSqlResourceCDCExtended',
        'change_tracking': 'list[str]',
        'column_exclusions': 'list[str]',
        'column_inclusions': 'list[str]',
        'column_name_transforms': 'list[str]',
        'ct_ext': 'CycloneSqlResourceCTExtended',
        'dt_activity_config': 'CycloneSqlResourceDtActivity',
        'dt_tracking_fields': 'CycloneSqlResourceDtTracking',
        'exclude_binary': 'bool',
        'exclude_large_text': 'bool',
        'external_id_config': 'CycloneSqlResourceExtId',
        'read_uncommitted': 'bool',
        'schema': 'str',
        'select_limit': 'int',
        'table': 'str',
        'where_config': 'list[CycloneSqlResourceWhere]',
        'where_text': 'str'
    }

    attribute_map = {
        'activity_name': 'activity_name',
        'alias_columns': 'alias_columns',
        'cdc_ext': 'cdc_ext',
        'change_tracking': 'change_tracking',
        'column_exclusions': 'column_exclusions',
        'column_inclusions': 'column_inclusions',
        'column_name_transforms': 'column_name_transforms',
        'ct_ext': 'ct_ext',
        'dt_activity_config': 'dt_activity_config',
        'dt_tracking_fields': 'dt_tracking_fields',
        'exclude_binary': 'exclude_binary',
        'exclude_large_text': 'exclude_large_text',
        'external_id_config': 'external_id_config',
        'read_uncommitted': 'read_uncommitted',
        'schema': 'schema',
        'select_limit': 'select_limit',
        'table': 'table',
        'where_config': 'where_config',
        'where_text': 'where_text'
    }

    def __init__(self, activity_name=None, alias_columns=None, cdc_ext=None, change_tracking=None, column_exclusions=None, column_inclusions=None, column_name_transforms=None, ct_ext=None, dt_activity_config=None, dt_tracking_fields=None, exclude_binary=None, exclude_large_text=None, external_id_config=None, read_uncommitted=None, schema=None, select_limit=None, table=None, where_config=None, where_text=None):  # noqa: E501
        """CycloneSqlResource - a model defined in OpenAPI"""  # noqa: E501

        self._activity_name = None
        self._alias_columns = None
        self._cdc_ext = None
        self._change_tracking = None
        self._column_exclusions = None
        self._column_inclusions = None
        self._column_name_transforms = None
        self._ct_ext = None
        self._dt_activity_config = None
        self._dt_tracking_fields = None
        self._exclude_binary = None
        self._exclude_large_text = None
        self._external_id_config = None
        self._read_uncommitted = None
        self._schema = None
        self._select_limit = None
        self._table = None
        self._where_config = None
        self._where_text = None
        self.discriminator = None

        if activity_name is not None:
            self.activity_name = activity_name
        if alias_columns is not None:
            self.alias_columns = alias_columns
        if cdc_ext is not None:
            self.cdc_ext = cdc_ext
        self.change_tracking = change_tracking
        if column_exclusions is not None:
            self.column_exclusions = column_exclusions
        if column_inclusions is not None:
            self.column_inclusions = column_inclusions
        if column_name_transforms is not None:
            self.column_name_transforms = column_name_transforms
        if ct_ext is not None:
            self.ct_ext = ct_ext
        self.dt_activity_config = dt_activity_config
        if dt_tracking_fields is not None:
            self.dt_tracking_fields = dt_tracking_fields
        if exclude_binary is not None:
            self.exclude_binary = exclude_binary
        if exclude_large_text is not None:
            self.exclude_large_text = exclude_large_text
        if external_id_config is not None:
            self.external_id_config = external_id_config
        if read_uncommitted is not None:
            self.read_uncommitted = read_uncommitted
        self.schema = schema
        if select_limit is not None:
            self.select_limit = select_limit
        self.table = table
        if where_config is not None:
            self.where_config = where_config
        if where_text is not None:
            self.where_text = where_text

    @property
    def activity_name(self):
        """Gets the activity_name of this CycloneSqlResource.  # noqa: E501


        :return: The activity_name of this CycloneSqlResource.  # noqa: E501
        :rtype: str
        """
        return self._activity_name

    @activity_name.setter
    def activity_name(self, activity_name):
        """Sets the activity_name of this CycloneSqlResource.


        :param activity_name: The activity_name of this CycloneSqlResource.  # noqa: E501
        :type: str
        """

        self._activity_name = activity_name

    @property
    def alias_columns(self):
        """Gets the alias_columns of this CycloneSqlResource.  # noqa: E501


        :return: The alias_columns of this CycloneSqlResource.  # noqa: E501
        :rtype: list[CycloneSqlResourceAliasColumn]
        """
        return self._alias_columns

    @alias_columns.setter
    def alias_columns(self, alias_columns):
        """Sets the alias_columns of this CycloneSqlResource.


        :param alias_columns: The alias_columns of this CycloneSqlResource.  # noqa: E501
        :type: list[CycloneSqlResourceAliasColumn]
        """

        self._alias_columns = alias_columns

    @property
    def cdc_ext(self):
        """Gets the cdc_ext of this CycloneSqlResource.  # noqa: E501


        :return: The cdc_ext of this CycloneSqlResource.  # noqa: E501
        :rtype: CycloneSqlResourceCDCExtended
        """
        return self._cdc_ext

    @cdc_ext.setter
    def cdc_ext(self, cdc_ext):
        """Sets the cdc_ext of this CycloneSqlResource.


        :param cdc_ext: The cdc_ext of this CycloneSqlResource.  # noqa: E501
        :type: CycloneSqlResourceCDCExtended
        """

        self._cdc_ext = cdc_ext

    @property
    def change_tracking(self):
        """Gets the change_tracking of this CycloneSqlResource.  # noqa: E501


        :return: The change_tracking of this CycloneSqlResource.  # noqa: E501
        :rtype: list[str]
        """
        return self._change_tracking

    @change_tracking.setter
    def change_tracking(self, change_tracking):
        """Sets the change_tracking of this CycloneSqlResource.


        :param change_tracking: The change_tracking of this CycloneSqlResource.  # noqa: E501
        :type: list[str]
        """
        if change_tracking is None:
            raise ValueError("Invalid value for `change_tracking`, must not be `None`")  # noqa: E501

        self._change_tracking = change_tracking

    @property
    def column_exclusions(self):
        """Gets the column_exclusions of this CycloneSqlResource.  # noqa: E501


        :return: The column_exclusions of this CycloneSqlResource.  # noqa: E501
        :rtype: list[str]
        """
        return self._column_exclusions

    @column_exclusions.setter
    def column_exclusions(self, column_exclusions):
        """Sets the column_exclusions of this CycloneSqlResource.


        :param column_exclusions: The column_exclusions of this CycloneSqlResource.  # noqa: E501
        :type: list[str]
        """

        self._column_exclusions = column_exclusions

    @property
    def column_inclusions(self):
        """Gets the column_inclusions of this CycloneSqlResource.  # noqa: E501


        :return: The column_inclusions of this CycloneSqlResource.  # noqa: E501
        :rtype: list[str]
        """
        return self._column_inclusions

    @column_inclusions.setter
    def column_inclusions(self, column_inclusions):
        """Sets the column_inclusions of this CycloneSqlResource.


        :param column_inclusions: The column_inclusions of this CycloneSqlResource.  # noqa: E501
        :type: list[str]
        """

        self._column_inclusions = column_inclusions

    @property
    def column_name_transforms(self):
        """Gets the column_name_transforms of this CycloneSqlResource.  # noqa: E501


        :return: The column_name_transforms of this CycloneSqlResource.  # noqa: E501
        :rtype: list[str]
        """
        return self._column_name_transforms

    @column_name_transforms.setter
    def column_name_transforms(self, column_name_transforms):
        """Sets the column_name_transforms of this CycloneSqlResource.


        :param column_name_transforms: The column_name_transforms of this CycloneSqlResource.  # noqa: E501
        :type: list[str]
        """

        self._column_name_transforms = column_name_transforms

    @property
    def ct_ext(self):
        """Gets the ct_ext of this CycloneSqlResource.  # noqa: E501


        :return: The ct_ext of this CycloneSqlResource.  # noqa: E501
        :rtype: CycloneSqlResourceCTExtended
        """
        return self._ct_ext

    @ct_ext.setter
    def ct_ext(self, ct_ext):
        """Sets the ct_ext of this CycloneSqlResource.


        :param ct_ext: The ct_ext of this CycloneSqlResource.  # noqa: E501
        :type: CycloneSqlResourceCTExtended
        """

        self._ct_ext = ct_ext

    @property
    def dt_activity_config(self):
        """Gets the dt_activity_config of this CycloneSqlResource.  # noqa: E501


        :return: The dt_activity_config of this CycloneSqlResource.  # noqa: E501
        :rtype: CycloneSqlResourceDtActivity
        """
        return self._dt_activity_config

    @dt_activity_config.setter
    def dt_activity_config(self, dt_activity_config):
        """Sets the dt_activity_config of this CycloneSqlResource.


        :param dt_activity_config: The dt_activity_config of this CycloneSqlResource.  # noqa: E501
        :type: CycloneSqlResourceDtActivity
        """
        if dt_activity_config is None:
            raise ValueError("Invalid value for `dt_activity_config`, must not be `None`")  # noqa: E501

        self._dt_activity_config = dt_activity_config

    @property
    def dt_tracking_fields(self):
        """Gets the dt_tracking_fields of this CycloneSqlResource.  # noqa: E501


        :return: The dt_tracking_fields of this CycloneSqlResource.  # noqa: E501
        :rtype: CycloneSqlResourceDtTracking
        """
        return self._dt_tracking_fields

    @dt_tracking_fields.setter
    def dt_tracking_fields(self, dt_tracking_fields):
        """Sets the dt_tracking_fields of this CycloneSqlResource.


        :param dt_tracking_fields: The dt_tracking_fields of this CycloneSqlResource.  # noqa: E501
        :type: CycloneSqlResourceDtTracking
        """

        self._dt_tracking_fields = dt_tracking_fields

    @property
    def exclude_binary(self):
        """Gets the exclude_binary of this CycloneSqlResource.  # noqa: E501


        :return: The exclude_binary of this CycloneSqlResource.  # noqa: E501
        :rtype: bool
        """
        return self._exclude_binary

    @exclude_binary.setter
    def exclude_binary(self, exclude_binary):
        """Sets the exclude_binary of this CycloneSqlResource.


        :param exclude_binary: The exclude_binary of this CycloneSqlResource.  # noqa: E501
        :type: bool
        """

        self._exclude_binary = exclude_binary

    @property
    def exclude_large_text(self):
        """Gets the exclude_large_text of this CycloneSqlResource.  # noqa: E501


        :return: The exclude_large_text of this CycloneSqlResource.  # noqa: E501
        :rtype: bool
        """
        return self._exclude_large_text

    @exclude_large_text.setter
    def exclude_large_text(self, exclude_large_text):
        """Sets the exclude_large_text of this CycloneSqlResource.


        :param exclude_large_text: The exclude_large_text of this CycloneSqlResource.  # noqa: E501
        :type: bool
        """

        self._exclude_large_text = exclude_large_text

    @property
    def external_id_config(self):
        """Gets the external_id_config of this CycloneSqlResource.  # noqa: E501


        :return: The external_id_config of this CycloneSqlResource.  # noqa: E501
        :rtype: CycloneSqlResourceExtId
        """
        return self._external_id_config

    @external_id_config.setter
    def external_id_config(self, external_id_config):
        """Sets the external_id_config of this CycloneSqlResource.


        :param external_id_config: The external_id_config of this CycloneSqlResource.  # noqa: E501
        :type: CycloneSqlResourceExtId
        """

        self._external_id_config = external_id_config

    @property
    def read_uncommitted(self):
        """Gets the read_uncommitted of this CycloneSqlResource.  # noqa: E501


        :return: The read_uncommitted of this CycloneSqlResource.  # noqa: E501
        :rtype: bool
        """
        return self._read_uncommitted

    @read_uncommitted.setter
    def read_uncommitted(self, read_uncommitted):
        """Sets the read_uncommitted of this CycloneSqlResource.


        :param read_uncommitted: The read_uncommitted of this CycloneSqlResource.  # noqa: E501
        :type: bool
        """

        self._read_uncommitted = read_uncommitted

    @property
    def schema(self):
        """Gets the schema of this CycloneSqlResource.  # noqa: E501


        :return: The schema of this CycloneSqlResource.  # noqa: E501
        :rtype: str
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """Sets the schema of this CycloneSqlResource.


        :param schema: The schema of this CycloneSqlResource.  # noqa: E501
        :type: str
        """
        if schema is None:
            raise ValueError("Invalid value for `schema`, must not be `None`")  # noqa: E501

        self._schema = schema

    @property
    def select_limit(self):
        """Gets the select_limit of this CycloneSqlResource.  # noqa: E501


        :return: The select_limit of this CycloneSqlResource.  # noqa: E501
        :rtype: int
        """
        return self._select_limit

    @select_limit.setter
    def select_limit(self, select_limit):
        """Sets the select_limit of this CycloneSqlResource.


        :param select_limit: The select_limit of this CycloneSqlResource.  # noqa: E501
        :type: int
        """

        self._select_limit = select_limit

    @property
    def table(self):
        """Gets the table of this CycloneSqlResource.  # noqa: E501


        :return: The table of this CycloneSqlResource.  # noqa: E501
        :rtype: str
        """
        return self._table

    @table.setter
    def table(self, table):
        """Sets the table of this CycloneSqlResource.


        :param table: The table of this CycloneSqlResource.  # noqa: E501
        :type: str
        """
        if table is None:
            raise ValueError("Invalid value for `table`, must not be `None`")  # noqa: E501

        self._table = table

    @property
    def where_config(self):
        """Gets the where_config of this CycloneSqlResource.  # noqa: E501


        :return: The where_config of this CycloneSqlResource.  # noqa: E501
        :rtype: list[CycloneSqlResourceWhere]
        """
        return self._where_config

    @where_config.setter
    def where_config(self, where_config):
        """Sets the where_config of this CycloneSqlResource.


        :param where_config: The where_config of this CycloneSqlResource.  # noqa: E501
        :type: list[CycloneSqlResourceWhere]
        """

        self._where_config = where_config

    @property
    def where_text(self):
        """Gets the where_text of this CycloneSqlResource.  # noqa: E501


        :return: The where_text of this CycloneSqlResource.  # noqa: E501
        :rtype: str
        """
        return self._where_text

    @where_text.setter
    def where_text(self, where_text):
        """Sets the where_text of this CycloneSqlResource.


        :param where_text: The where_text of this CycloneSqlResource.  # noqa: E501
        :type: str
        """

        self._where_text = where_text

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
        if not isinstance(other, CycloneSqlResource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
