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


class CycloneClient(object):
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
        'allowed_server_names': 'list[str]',
        'allowed_servers': 'list[str]',
        'client_id': 'str',
        'code': 'str',
        'confs': 'list[CycloneConf]',
        'dt_u': 'datetime',
        'etl_list': 'list[CycloneAddClientEtlItem]',
        'integration_id': 'str',
        'last_record_count': 'int',
        'last_run_completed': 'datetime',
        'last_run_seconds': 'int',
        'last_server': 'str',
        'last_server_name': 'str',
        'queue_last_run': 'datetime',
        'queue_reset': 'bool',
        'queue_server': 'str',
        'queue_server_name': 'str',
        'queue_status': 'str',
        'queue_status_dt_u': 'datetime',
        'status': 'str',
        'status_dt_u': 'datetime'
    }

    attribute_map = {
        'id': '_id',
        'allowed_server_names': 'allowed_server_names',
        'allowed_servers': 'allowed_servers',
        'client_id': 'client_id',
        'code': 'code',
        'confs': 'confs',
        'dt_u': 'dt_u',
        'etl_list': 'etl_list',
        'integration_id': 'integration_id',
        'last_record_count': 'last_record_count',
        'last_run_completed': 'last_run_completed',
        'last_run_seconds': 'last_run_seconds',
        'last_server': 'last_server',
        'last_server_name': 'last_server_name',
        'queue_last_run': 'queue_last_run',
        'queue_reset': 'queue_reset',
        'queue_server': 'queue_server',
        'queue_server_name': 'queue_server_name',
        'queue_status': 'queue_status',
        'queue_status_dt_u': 'queue_status_dt_u',
        'status': 'status',
        'status_dt_u': 'status_dt_u'
    }

    def __init__(self, id=None, allowed_server_names=None, allowed_servers=None, client_id=None, code=None, confs=None, dt_u=None, etl_list=None, integration_id=None, last_record_count=None, last_run_completed=None, last_run_seconds=None, last_server=None, last_server_name=None, queue_last_run=None, queue_reset=None, queue_server=None, queue_server_name=None, queue_status=None, queue_status_dt_u=None, status=None, status_dt_u=None):  # noqa: E501
        """CycloneClient - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._allowed_server_names = None
        self._allowed_servers = None
        self._client_id = None
        self._code = None
        self._confs = None
        self._dt_u = None
        self._etl_list = None
        self._integration_id = None
        self._last_record_count = None
        self._last_run_completed = None
        self._last_run_seconds = None
        self._last_server = None
        self._last_server_name = None
        self._queue_last_run = None
        self._queue_reset = None
        self._queue_server = None
        self._queue_server_name = None
        self._queue_status = None
        self._queue_status_dt_u = None
        self._status = None
        self._status_dt_u = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if allowed_server_names is not None:
            self.allowed_server_names = allowed_server_names
        if allowed_servers is not None:
            self.allowed_servers = allowed_servers
        self.client_id = client_id
        self.code = code
        if confs is not None:
            self.confs = confs
        if dt_u is not None:
            self.dt_u = dt_u
        if etl_list is not None:
            self.etl_list = etl_list
        if integration_id is not None:
            self.integration_id = integration_id
        if last_record_count is not None:
            self.last_record_count = last_record_count
        if last_run_completed is not None:
            self.last_run_completed = last_run_completed
        if last_run_seconds is not None:
            self.last_run_seconds = last_run_seconds
        if last_server is not None:
            self.last_server = last_server
        if last_server_name is not None:
            self.last_server_name = last_server_name
        if queue_last_run is not None:
            self.queue_last_run = queue_last_run
        if queue_reset is not None:
            self.queue_reset = queue_reset
        if queue_server is not None:
            self.queue_server = queue_server
        if queue_server_name is not None:
            self.queue_server_name = queue_server_name
        if queue_status is not None:
            self.queue_status = queue_status
        if queue_status_dt_u is not None:
            self.queue_status_dt_u = queue_status_dt_u
        self.status = status
        if status_dt_u is not None:
            self.status_dt_u = status_dt_u

    @property
    def id(self):
        """Gets the id of this CycloneClient.  # noqa: E501


        :return: The id of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CycloneClient.


        :param id: The id of this CycloneClient.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def allowed_server_names(self):
        """Gets the allowed_server_names of this CycloneClient.  # noqa: E501


        :return: The allowed_server_names of this CycloneClient.  # noqa: E501
        :rtype: list[str]
        """
        return self._allowed_server_names

    @allowed_server_names.setter
    def allowed_server_names(self, allowed_server_names):
        """Sets the allowed_server_names of this CycloneClient.


        :param allowed_server_names: The allowed_server_names of this CycloneClient.  # noqa: E501
        :type: list[str]
        """

        self._allowed_server_names = allowed_server_names

    @property
    def allowed_servers(self):
        """Gets the allowed_servers of this CycloneClient.  # noqa: E501


        :return: The allowed_servers of this CycloneClient.  # noqa: E501
        :rtype: list[str]
        """
        return self._allowed_servers

    @allowed_servers.setter
    def allowed_servers(self, allowed_servers):
        """Sets the allowed_servers of this CycloneClient.


        :param allowed_servers: The allowed_servers of this CycloneClient.  # noqa: E501
        :type: list[str]
        """

        self._allowed_servers = allowed_servers

    @property
    def client_id(self):
        """Gets the client_id of this CycloneClient.  # noqa: E501


        :return: The client_id of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this CycloneClient.


        :param client_id: The client_id of this CycloneClient.  # noqa: E501
        :type: str
        """
        if client_id is None:
            raise ValueError("Invalid value for `client_id`, must not be `None`")  # noqa: E501

        self._client_id = client_id

    @property
    def code(self):
        """Gets the code of this CycloneClient.  # noqa: E501


        :return: The code of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this CycloneClient.


        :param code: The code of this CycloneClient.  # noqa: E501
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

    @property
    def confs(self):
        """Gets the confs of this CycloneClient.  # noqa: E501


        :return: The confs of this CycloneClient.  # noqa: E501
        :rtype: list[CycloneConf]
        """
        return self._confs

    @confs.setter
    def confs(self, confs):
        """Sets the confs of this CycloneClient.


        :param confs: The confs of this CycloneClient.  # noqa: E501
        :type: list[CycloneConf]
        """

        self._confs = confs

    @property
    def dt_u(self):
        """Gets the dt_u of this CycloneClient.  # noqa: E501


        :return: The dt_u of this CycloneClient.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_u

    @dt_u.setter
    def dt_u(self, dt_u):
        """Sets the dt_u of this CycloneClient.


        :param dt_u: The dt_u of this CycloneClient.  # noqa: E501
        :type: datetime
        """

        self._dt_u = dt_u

    @property
    def etl_list(self):
        """Gets the etl_list of this CycloneClient.  # noqa: E501


        :return: The etl_list of this CycloneClient.  # noqa: E501
        :rtype: list[CycloneAddClientEtlItem]
        """
        return self._etl_list

    @etl_list.setter
    def etl_list(self, etl_list):
        """Sets the etl_list of this CycloneClient.


        :param etl_list: The etl_list of this CycloneClient.  # noqa: E501
        :type: list[CycloneAddClientEtlItem]
        """

        self._etl_list = etl_list

    @property
    def integration_id(self):
        """Gets the integration_id of this CycloneClient.  # noqa: E501


        :return: The integration_id of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._integration_id

    @integration_id.setter
    def integration_id(self, integration_id):
        """Sets the integration_id of this CycloneClient.


        :param integration_id: The integration_id of this CycloneClient.  # noqa: E501
        :type: str
        """

        self._integration_id = integration_id

    @property
    def last_record_count(self):
        """Gets the last_record_count of this CycloneClient.  # noqa: E501


        :return: The last_record_count of this CycloneClient.  # noqa: E501
        :rtype: int
        """
        return self._last_record_count

    @last_record_count.setter
    def last_record_count(self, last_record_count):
        """Sets the last_record_count of this CycloneClient.


        :param last_record_count: The last_record_count of this CycloneClient.  # noqa: E501
        :type: int
        """

        self._last_record_count = last_record_count

    @property
    def last_run_completed(self):
        """Gets the last_run_completed of this CycloneClient.  # noqa: E501


        :return: The last_run_completed of this CycloneClient.  # noqa: E501
        :rtype: datetime
        """
        return self._last_run_completed

    @last_run_completed.setter
    def last_run_completed(self, last_run_completed):
        """Sets the last_run_completed of this CycloneClient.


        :param last_run_completed: The last_run_completed of this CycloneClient.  # noqa: E501
        :type: datetime
        """

        self._last_run_completed = last_run_completed

    @property
    def last_run_seconds(self):
        """Gets the last_run_seconds of this CycloneClient.  # noqa: E501


        :return: The last_run_seconds of this CycloneClient.  # noqa: E501
        :rtype: int
        """
        return self._last_run_seconds

    @last_run_seconds.setter
    def last_run_seconds(self, last_run_seconds):
        """Sets the last_run_seconds of this CycloneClient.


        :param last_run_seconds: The last_run_seconds of this CycloneClient.  # noqa: E501
        :type: int
        """

        self._last_run_seconds = last_run_seconds

    @property
    def last_server(self):
        """Gets the last_server of this CycloneClient.  # noqa: E501


        :return: The last_server of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._last_server

    @last_server.setter
    def last_server(self, last_server):
        """Sets the last_server of this CycloneClient.


        :param last_server: The last_server of this CycloneClient.  # noqa: E501
        :type: str
        """

        self._last_server = last_server

    @property
    def last_server_name(self):
        """Gets the last_server_name of this CycloneClient.  # noqa: E501


        :return: The last_server_name of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._last_server_name

    @last_server_name.setter
    def last_server_name(self, last_server_name):
        """Sets the last_server_name of this CycloneClient.


        :param last_server_name: The last_server_name of this CycloneClient.  # noqa: E501
        :type: str
        """

        self._last_server_name = last_server_name

    @property
    def queue_last_run(self):
        """Gets the queue_last_run of this CycloneClient.  # noqa: E501


        :return: The queue_last_run of this CycloneClient.  # noqa: E501
        :rtype: datetime
        """
        return self._queue_last_run

    @queue_last_run.setter
    def queue_last_run(self, queue_last_run):
        """Sets the queue_last_run of this CycloneClient.


        :param queue_last_run: The queue_last_run of this CycloneClient.  # noqa: E501
        :type: datetime
        """

        self._queue_last_run = queue_last_run

    @property
    def queue_reset(self):
        """Gets the queue_reset of this CycloneClient.  # noqa: E501


        :return: The queue_reset of this CycloneClient.  # noqa: E501
        :rtype: bool
        """
        return self._queue_reset

    @queue_reset.setter
    def queue_reset(self, queue_reset):
        """Sets the queue_reset of this CycloneClient.


        :param queue_reset: The queue_reset of this CycloneClient.  # noqa: E501
        :type: bool
        """

        self._queue_reset = queue_reset

    @property
    def queue_server(self):
        """Gets the queue_server of this CycloneClient.  # noqa: E501


        :return: The queue_server of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._queue_server

    @queue_server.setter
    def queue_server(self, queue_server):
        """Sets the queue_server of this CycloneClient.


        :param queue_server: The queue_server of this CycloneClient.  # noqa: E501
        :type: str
        """

        self._queue_server = queue_server

    @property
    def queue_server_name(self):
        """Gets the queue_server_name of this CycloneClient.  # noqa: E501


        :return: The queue_server_name of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._queue_server_name

    @queue_server_name.setter
    def queue_server_name(self, queue_server_name):
        """Sets the queue_server_name of this CycloneClient.


        :param queue_server_name: The queue_server_name of this CycloneClient.  # noqa: E501
        :type: str
        """

        self._queue_server_name = queue_server_name

    @property
    def queue_status(self):
        """Gets the queue_status of this CycloneClient.  # noqa: E501


        :return: The queue_status of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._queue_status

    @queue_status.setter
    def queue_status(self, queue_status):
        """Sets the queue_status of this CycloneClient.


        :param queue_status: The queue_status of this CycloneClient.  # noqa: E501
        :type: str
        """

        self._queue_status = queue_status

    @property
    def queue_status_dt_u(self):
        """Gets the queue_status_dt_u of this CycloneClient.  # noqa: E501


        :return: The queue_status_dt_u of this CycloneClient.  # noqa: E501
        :rtype: datetime
        """
        return self._queue_status_dt_u

    @queue_status_dt_u.setter
    def queue_status_dt_u(self, queue_status_dt_u):
        """Sets the queue_status_dt_u of this CycloneClient.


        :param queue_status_dt_u: The queue_status_dt_u of this CycloneClient.  # noqa: E501
        :type: datetime
        """

        self._queue_status_dt_u = queue_status_dt_u

    @property
    def status(self):
        """Gets the status of this CycloneClient.  # noqa: E501


        :return: The status of this CycloneClient.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this CycloneClient.


        :param status: The status of this CycloneClient.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def status_dt_u(self):
        """Gets the status_dt_u of this CycloneClient.  # noqa: E501


        :return: The status_dt_u of this CycloneClient.  # noqa: E501
        :rtype: datetime
        """
        return self._status_dt_u

    @status_dt_u.setter
    def status_dt_u(self, status_dt_u):
        """Sets the status_dt_u of this CycloneClient.


        :param status_dt_u: The status_dt_u of this CycloneClient.  # noqa: E501
        :type: datetime
        """

        self._status_dt_u = status_dt_u

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
        if not isinstance(other, CycloneClient):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
