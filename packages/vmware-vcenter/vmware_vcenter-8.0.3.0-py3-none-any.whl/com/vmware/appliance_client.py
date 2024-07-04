# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance_client`` module provides classes for managing
vCenter Appliance configuration. The module is available starting in vSphere
6.5.

"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from com.vmware.cis_client import Tasks
from vmware.vapi.stdlib.client.task import Task
from vmware.vapi.bindings import type
from vmware.vapi.bindings.converter import TypeConverter
from vmware.vapi.bindings.enum import Enum
from vmware.vapi.bindings.error import VapiError
from vmware.vapi.bindings.struct import VapiStruct
from vmware.vapi.bindings.stub import (
    ApiInterfaceStub, StubFactoryBase, VapiInterface)
from vmware.vapi.bindings.common import raise_core_exception
from vmware.vapi.data.validator import (UnionValidator, HasFieldsOfValidator)
from vmware.vapi.exception import CoreException
from vmware.vapi.lib.constants import TaskType
from vmware.vapi.lib.rest import OperationRestMetadata


class Notification(VapiStruct):
    """
    The ``Notification`` class describes a notification that can be reported by
    the appliance task. This class was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 id=None,
                 time=None,
                 message=None,
                 resolution=None,
                ):
        """
        :type  id: :class:`str`
        :param id: The notification id. This attribute was added in vSphere API 6.7.
        :type  time: :class:`datetime.datetime` or ``None``
        :param time: The time the notification was raised/found. This attribute was
            added in vSphere API 6.7.
            Only if the time information is available.
        :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param message: The notification message. This attribute was added in vSphere API
            6.7.
        :type  resolution: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
        :param resolution: The resolution message, if any. This attribute was added in vSphere
            API 6.7.
            Only :class:`set` for warnings and errors.
        """
        self.id = id
        self.time = time
        self.message = message
        self.resolution = resolution
        VapiStruct.__init__(self)


Notification._set_binding_type(type.StructType(
    'com.vmware.appliance.notification', {
        'id': type.StringType(),
        'time': type.OptionalType(type.DateTimeType()),
        'message': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'resolution': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
    },
    Notification,
    False,
    None))



class Notifications(VapiStruct):
    """
    The ``Notifications`` class contains info/warning/error messages that can
    be reported be the appliance task. This class was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 info=None,
                 warnings=None,
                 errors=None,
                ):
        """
        :type  info: :class:`list` of :class:`Notification` or ``None``
        :param info: Info notification messages reported. This attribute was added in
            vSphere API 6.7.
            Only :class:`set` if an info was reported by the appliance task.
        :type  warnings: :class:`list` of :class:`Notification` or ``None``
        :param warnings: Warning notification messages reported. This attribute was added in
            vSphere API 6.7.
            Only :class:`set` if an warning was reported by the appliance task.
        :type  errors: :class:`list` of :class:`Notification` or ``None``
        :param errors: Error notification messages reported. This attribute was added in
            vSphere API 6.7.
            Only :class:`set` if an error was reported by the appliance task.
        """
        self.info = info
        self.warnings = warnings
        self.errors = errors
        VapiStruct.__init__(self)


Notifications._set_binding_type(type.StructType(
    'com.vmware.appliance.notifications', {
        'info': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'warnings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
    },
    Notifications,
    False,
    None))



class SubtaskInfo(VapiStruct):
    """
    The ``SubtaskInfo`` class contains information about one of the subtasks
    that makes up an appliance task. This class was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'status',
            {
                'RUNNING' : [('progress', True), ('result', False), ('start_time', True)],
                'BLOCKED' : [('progress', True), ('result', False), ('start_time', True)],
                'SUCCEEDED' : [('progress', True), ('result', False), ('start_time', True), ('end_time', True)],
                'FAILED' : [('progress', True), ('result', False), ('error', False), ('start_time', True), ('end_time', True)],
                'PENDING' : [],
            }
        ),
    ]



    def __init__(self,
                 progress=None,
                 result=None,
                 description=None,
                 service=None,
                 operation=None,
                 parent=None,
                 target=None,
                 status=None,
                 cancelable=None,
                 error=None,
                 start_time=None,
                 end_time=None,
                 user=None,
                ):
        """
        :type  progress: :class:`com.vmware.cis.task_client.Progress`
        :param progress: Progress of the operation. This attribute was added in vSphere API
            6.7.
            This attribute is optional and it is only relevant when the value
            of ``CommonInfo#status`` is one of
            :attr:`com.vmware.cis.task_client.Status.RUNNING`,
            :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
            :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
            :attr:`com.vmware.cis.task_client.Status.FAILED`.
        :type  result: :class:`Notifications` or ``None``
        :param result: Result of the operation. If an operation reports partial results
            before it completes, this attribute could be :class:`set` before
            the :attr:`com.vmware.cis.task_client.CommonInfo.status` has the
            value :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`. The
            value could change as the operation progresses. This attribute was
            added in vSphere API 6.7.
            This attribute will be None if result is not available at the
            current step of the operation.
        :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param description: Description of the operation associated with the task.
        :type  service: :class:`str`
        :param service: Identifier of the service containing the operation.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vapi.service``. When methods return a value of this
            class as a return value, the attribute will be an identifier for
            the resource type: ``com.vmware.vapi.service``.
        :type  operation: :class:`str`
        :param operation: Identifier of the operation associated with the task.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vapi.operation``. When methods return a value of this
            class as a return value, the attribute will be an identifier for
            the resource type: ``com.vmware.vapi.operation``.
        :type  parent: :class:`str` or ``None``
        :param parent: Parent of the current task.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.task``. When methods return a value of this class
            as a return value, the attribute will be an identifier for the
            resource type: ``com.vmware.cis.task``.
            This attribute will be None if the task has no parent.
        :type  target: :class:`com.vmware.vapi.std_client.DynamicID` or ``None``
        :param target: Identifier of the target created by the operation or an existing
            one the operation performed on.
            This attribute will be None if the operation has no target or
            multiple targets.
        :type  status: :class:`com.vmware.cis.task_client.Status`
        :param status: Status of the operation associated with the task.
        :type  cancelable: :class:`bool`
        :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
            value may change as the operation progresses.
        :type  error: :class:`Exception` or ``None``
        :param error: Description of the error if the operation status is "FAILED".
            If None the description of why the operation failed will be
            included in the result of the operation (see
            :attr:`com.vmware.cis.task_client.Info.result`).
        :type  start_time: :class:`datetime.datetime`
        :param start_time: Time when the operation is started.
            This attribute is optional and it is only relevant when the value
            of ``status`` is one of
            :attr:`com.vmware.cis.task_client.Status.RUNNING`,
            :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
            :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
            :attr:`com.vmware.cis.task_client.Status.FAILED`.
        :type  end_time: :class:`datetime.datetime`
        :param end_time: Time when the operation is completed.
            This attribute is optional and it is only relevant when the value
            of ``status`` is one of
            :attr:`com.vmware.cis.task_client.Status.SUCCEEDED` or
            :attr:`com.vmware.cis.task_client.Status.FAILED`.
        :type  user: :class:`str` or ``None``
        :param user: Name of the user who performed the operation.
            This attribute will be None if the operation is performed by the
            system.
        """
        self.progress = progress
        self.result = result
        self.description = description
        self.service = service
        self.operation = operation
        self.parent = parent
        self.target = target
        self.status = status
        self.cancelable = cancelable
        self.error = error
        self.start_time = start_time
        self.end_time = end_time
        self.user = user
        VapiStruct.__init__(self)


SubtaskInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.subtask_info', {
        'progress': type.OptionalType(type.ReferenceType('com.vmware.cis.task_client', 'Progress')),
        'result': type.OptionalType(type.ReferenceType(__name__, 'Notifications')),
        'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'service': type.IdType(resource_types='com.vmware.vapi.service'),
        'operation': type.IdType(resource_types='com.vmware.vapi.operation'),
        'parent': type.OptionalType(type.IdType()),
        'target': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID')),
        'status': type.ReferenceType('com.vmware.cis.task_client', 'Status'),
        'cancelable': type.BooleanType(),
        'error': type.OptionalType(type.AnyErrorType()),
        'start_time': type.OptionalType(type.DateTimeType()),
        'end_time': type.OptionalType(type.DateTimeType()),
        'user': type.OptionalType(type.StringType()),
    },
    SubtaskInfo,
    False,
    None))



class TaskInfo(VapiStruct):
    """
    The ``TaskInfo`` class contains information about an appliance task and the
    subtasks of which it consists. This class was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'status',
            {
                'RUNNING' : [('progress', True), ('start_time', True)],
                'BLOCKED' : [('progress', True), ('start_time', True)],
                'SUCCEEDED' : [('progress', True), ('start_time', True), ('end_time', True)],
                'FAILED' : [('progress', True), ('error', False), ('start_time', True), ('end_time', True)],
                'PENDING' : [],
            }
        ),
    ]



    def __init__(self,
                 progress=None,
                 subtask_order=None,
                 subtasks=None,
                 description=None,
                 service=None,
                 operation=None,
                 parent=None,
                 target=None,
                 status=None,
                 cancelable=None,
                 error=None,
                 start_time=None,
                 end_time=None,
                 user=None,
                ):
        """
        :type  progress: :class:`com.vmware.cis.task_client.Progress`
        :param progress: Progress of the task. This attribute was added in vSphere API 6.7.
            This attribute is optional and it is only relevant when the value
            of ``CommonInfo#status`` is one of
            :attr:`com.vmware.cis.task_client.Status.RUNNING`,
            :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
            :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
            :attr:`com.vmware.cis.task_client.Status.FAILED`.
        :type  subtask_order: :class:`list` of :class:`str`
        :param subtask_order: List of tasks that make up this appliance task in the order they
            are being run. This attribute was added in vSphere API 6.7.
        :type  subtasks: :class:`dict` of :class:`str` and :class:`SubtaskInfo`
        :param subtasks: Information about the subtasks that this appliance task consists
            of. This attribute was added in vSphere API 6.7.
        :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param description: Description of the operation associated with the task.
        :type  service: :class:`str`
        :param service: Identifier of the service containing the operation.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vapi.service``. When methods return a value of this
            class as a return value, the attribute will be an identifier for
            the resource type: ``com.vmware.vapi.service``.
        :type  operation: :class:`str`
        :param operation: Identifier of the operation associated with the task.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vapi.operation``. When methods return a value of this
            class as a return value, the attribute will be an identifier for
            the resource type: ``com.vmware.vapi.operation``.
        :type  parent: :class:`str` or ``None``
        :param parent: Parent of the current task.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.task``. When methods return a value of this class
            as a return value, the attribute will be an identifier for the
            resource type: ``com.vmware.cis.task``.
            This attribute will be None if the task has no parent.
        :type  target: :class:`com.vmware.vapi.std_client.DynamicID` or ``None``
        :param target: Identifier of the target created by the operation or an existing
            one the operation performed on.
            This attribute will be None if the operation has no target or
            multiple targets.
        :type  status: :class:`com.vmware.cis.task_client.Status`
        :param status: Status of the operation associated with the task.
        :type  cancelable: :class:`bool`
        :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
            value may change as the operation progresses.
        :type  error: :class:`Exception` or ``None``
        :param error: Description of the error if the operation status is "FAILED".
            If None the description of why the operation failed will be
            included in the result of the operation (see
            :attr:`com.vmware.cis.task_client.Info.result`).
        :type  start_time: :class:`datetime.datetime`
        :param start_time: Time when the operation is started.
            This attribute is optional and it is only relevant when the value
            of ``status`` is one of
            :attr:`com.vmware.cis.task_client.Status.RUNNING`,
            :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
            :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
            :attr:`com.vmware.cis.task_client.Status.FAILED`.
        :type  end_time: :class:`datetime.datetime`
        :param end_time: Time when the operation is completed.
            This attribute is optional and it is only relevant when the value
            of ``status`` is one of
            :attr:`com.vmware.cis.task_client.Status.SUCCEEDED` or
            :attr:`com.vmware.cis.task_client.Status.FAILED`.
        :type  user: :class:`str` or ``None``
        :param user: Name of the user who performed the operation.
            This attribute will be None if the operation is performed by the
            system.
        """
        self.progress = progress
        self.subtask_order = subtask_order
        self.subtasks = subtasks
        self.description = description
        self.service = service
        self.operation = operation
        self.parent = parent
        self.target = target
        self.status = status
        self.cancelable = cancelable
        self.error = error
        self.start_time = start_time
        self.end_time = end_time
        self.user = user
        VapiStruct.__init__(self)


TaskInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.task_info', {
        'progress': type.OptionalType(type.ReferenceType('com.vmware.cis.task_client', 'Progress')),
        'subtask_order': type.ListType(type.StringType()),
        'subtasks': type.MapType(type.StringType(), type.ReferenceType(__name__, 'SubtaskInfo')),
        'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'service': type.IdType(resource_types='com.vmware.vapi.service'),
        'operation': type.IdType(resource_types='com.vmware.vapi.operation'),
        'parent': type.OptionalType(type.IdType()),
        'target': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID')),
        'status': type.ReferenceType('com.vmware.cis.task_client', 'Status'),
        'cancelable': type.BooleanType(),
        'error': type.OptionalType(type.AnyErrorType()),
        'start_time': type.OptionalType(type.DateTimeType()),
        'end_time': type.OptionalType(type.DateTimeType()),
        'user': type.OptionalType(type.StringType()),
    },
    TaskInfo,
    False,
    None))



class Health(VapiInterface):
    """
    The ``Health`` class provides methods to retrieve the appliance health
    information. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.health'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HealthStub)
        self._VAPI_OPERATION_IDS = {}


    def messages(self,
                 item,
                 ):
        """
        Get health messages. This method was added in vSphere API 6.7.

        :type  item: :class:`str`
        :param item: ID of the data item
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.health``.
        :rtype: :class:`list` of :class:`Notification`
        :return: List of the health messages
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            Unknown health item
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('messages',
                            {
                            'item': item,
                            })
class HealthCheckSettings(VapiInterface):
    """
    The ``HealthCheckSettings`` class provides methods to enable/disable health
    check settings in vCenter Server. This class was added in vSphere API
    7.0.0.1.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.health_check_settings'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HealthCheckSettingsStub)
        self._VAPI_OPERATION_IDS = {}

    class SettingSpec(VapiStruct):
        """
        ``HealthCheckSettings.SettingSpec`` class contains specification of vCenter
        Server health and its corresponding state. This class was added in vSphere
        API 7.0.0.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     db_health_check_state_manual_backup=None,
                     db_health_check_state_scheduled_backup=None,
                    ):
            """
            :type  db_health_check_state_manual_backup: :class:`bool`
            :param db_health_check_state_manual_backup: Health check state of database during manual backup with this
                option set, the health status of the particular health check will
                be reported. This attribute was added in vSphere API 7.0.0.1.
            :type  db_health_check_state_scheduled_backup: :class:`bool`
            :param db_health_check_state_scheduled_backup: Health check state of database during schedule backup with this
                option set, the health status of the particular health check will
                be reported. This attribute was added in vSphere API 7.0.0.1.
            """
            self.db_health_check_state_manual_backup = db_health_check_state_manual_backup
            self.db_health_check_state_scheduled_backup = db_health_check_state_scheduled_backup
            VapiStruct.__init__(self)


    SettingSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.health_check_settings.setting_spec', {
            'db_health_check_state_manual_backup': type.BooleanType(),
            'db_health_check_state_scheduled_backup': type.BooleanType(),
        },
        SettingSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     db_health_check_state_manual_backup=None,
                     db_health_check_state_scheduled_backup=None,
                    ):
            """
            :type  db_health_check_state_manual_backup: :class:`bool` or ``None``
            :param db_health_check_state_manual_backup: Health check state of database during manual backup with this
                option set, the health status of the particular health check will
                be enabled. This attribute was added in vSphere API 7.0.0.1.
                If None the current state will remain unchanged.
            :type  db_health_check_state_scheduled_backup: :class:`bool` or ``None``
            :param db_health_check_state_scheduled_backup: Health check state of database during schedule backup with this
                option set, the health status of the particular health check will
                be enabled. This attribute was added in vSphere API 7.0.0.1.
                If None the current state will remain unchanged.
            """
            self.db_health_check_state_manual_backup = db_health_check_state_manual_backup
            self.db_health_check_state_scheduled_backup = db_health_check_state_scheduled_backup
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.health_check_settings.update_spec', {
            'db_health_check_state_manual_backup': type.OptionalType(type.BooleanType()),
            'db_health_check_state_scheduled_backup': type.OptionalType(type.BooleanType()),
        },
        UpdateSpec,
        False,
        None))



    def get(self):
        """
        Get health settings for vCenter Server. This method was added in
        vSphere API 7.0.0.1.


        :rtype: :class:`HealthCheckSettings.SettingSpec`
        :return: health settings.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)

    def update(self,
               health_settings,
               ):
        """
        Set health settings based on provided healthSpec. This method was added
        in vSphere API 7.0.0.1.

        :type  health_settings: :class:`HealthCheckSettings.UpdateSpec`
        :param health_settings: 
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('update',
                            {
                            'health_settings': health_settings,
                            })
class LocalAccounts(VapiInterface):
    """
    The ``LocalAccounts`` class provides methods to manage local user account.
    This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.local_accounts'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LocalAccountsStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``LocalAccounts.Info`` class defines the local account properties. This
        class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     fullname=None,
                     email=None,
                     roles=None,
                     enabled=None,
                     has_password=None,
                     last_password_change=None,
                     password_expires_at=None,
                     inactive_at=None,
                     min_days_between_password_change=None,
                     max_days_between_password_change=None,
                     warn_days_before_password_expiration=None,
                    ):
            """
            :type  fullname: :class:`str` or ``None``
            :param fullname: Full name of the user. This attribute was added in vSphere API 6.7.
                If None, the value was never set.
            :type  email: :class:`str` or ``None``
            :param email: Email address of the local account. This attribute was added in
                vSphere API 6.7.
                If None, the value was never set.
            :type  roles: :class:`list` of :class:`str`
            :param roles: User roles. This attribute was added in vSphere API 6.7.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.appliance.roles``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``com.vmware.appliance.roles``.
            :type  enabled: :class:`bool`
            :param enabled: Flag indicating if the account is enabled. This attribute was added
                in vSphere API 6.7.
            :type  has_password: :class:`bool`
            :param has_password: Is the user password set. This attribute was added in vSphere API
                6.7.
            :type  last_password_change: :class:`datetime.datetime` or ``None``
            :param last_password_change: Date and time password was changed. This attribute was added in
                vSphere API 6.7.
                If None, the password was never set.
            :type  password_expires_at: :class:`datetime.datetime` or ``None``
            :param password_expires_at: Date when the account's password will expire. This attribute was
                added in vSphere API 6.7.
                If None, the password never expires.
            :type  inactive_at: :class:`datetime.datetime` or ``None``
            :param inactive_at: Date and time account will be locked after password expiration.
                This attribute was added in vSphere API 6.7.
                If None, account will not be locked.
            :type  min_days_between_password_change: :class:`long` or ``None``
            :param min_days_between_password_change: Minimum number of days between password change. This attribute was
                added in vSphere API 6.7.
                If None, pasword can be changed any time.
            :type  max_days_between_password_change: :class:`long` or ``None``
            :param max_days_between_password_change: Maximum number of days between password change. This attribute was
                added in vSphere API 6.7.
                If None, password never expires.
            :type  warn_days_before_password_expiration: :class:`long` or ``None``
            :param warn_days_before_password_expiration: Number of days of warning before password expires. This attribute
                was added in vSphere API 6.7.
                If None, a user is never warned.
            """
            self.fullname = fullname
            self.email = email
            self.roles = roles
            self.enabled = enabled
            self.has_password = has_password
            self.last_password_change = last_password_change
            self.password_expires_at = password_expires_at
            self.inactive_at = inactive_at
            self.min_days_between_password_change = min_days_between_password_change
            self.max_days_between_password_change = max_days_between_password_change
            self.warn_days_before_password_expiration = warn_days_before_password_expiration
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.local_accounts.info', {
            'fullname': type.OptionalType(type.StringType()),
            'email': type.OptionalType(type.StringType()),
            'roles': type.ListType(type.IdType()),
            'enabled': type.BooleanType(),
            'has_password': type.BooleanType(),
            'last_password_change': type.OptionalType(type.DateTimeType()),
            'password_expires_at': type.OptionalType(type.DateTimeType()),
            'inactive_at': type.OptionalType(type.DateTimeType()),
            'min_days_between_password_change': type.OptionalType(type.IntegerType()),
            'max_days_between_password_change': type.OptionalType(type.IntegerType()),
            'warn_days_before_password_expiration': type.OptionalType(type.IntegerType()),
        },
        Info,
        False,
        None))


    class Config(VapiStruct):
        """
        The ``LocalAccounts.Config`` class defines the information required for the
        account. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     password=None,
                     old_password=None,
                     full_name=None,
                     email=None,
                     roles=None,
                     enabled=None,
                     password_expires=None,
                     password_expires_at=None,
                     inactive_after_password_expiration=None,
                     days_after_password_expiration=None,
                     min_days_between_password_change=None,
                     max_days_between_password_change=None,
                     warn_days_before_password_expiration=None,
                    ):
            """
            :type  password: :class:`str`
            :param password: Password. This attribute was added in vSphere API 6.7.
            :type  old_password: :class:`str` or ``None``
            :param old_password: Old password of the user (required in case of the password change,
                not required if superAdmin user changes the password of the other
                user). This attribute was added in vSphere API 6.7.
                If None, user may not have password set.
            :type  full_name: :class:`str` or ``None``
            :param full_name: Full name of the user. This attribute was added in vSphere API 6.7.
                If None, user will have no fullname.
            :type  email: :class:`str` or ``None``
            :param email: Email address of the local account. This attribute was added in
                vSphere API 6.7.
                If None, user will have no email.
            :type  roles: :class:`list` of :class:`str`
            :param roles: User roles. This attribute was added in vSphere API 6.7.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.appliance.roles``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``com.vmware.appliance.roles``.
            :type  enabled: :class:`bool` or ``None``
            :param enabled: Flag indicating if the account is enabled. This attribute was added
                in vSphere API 6.7.
                If None, defaults to True
            :type  password_expires: :class:`bool` or ``None``
            :param password_expires: Flag indicating if the account password expires. This attribute was
                added in vSphere API 6.7.
                If None, defaults to True.
            :type  password_expires_at: :class:`datetime.datetime` or ``None``
            :param password_expires_at: Date when the account's password will expire. This attribute was
                added in vSphere API 6.7.
                If None, will be taken from system defaults (see
                local-accounts/policy).
            :type  inactive_after_password_expiration: :class:`bool` or ``None``
            :param inactive_after_password_expiration: Flag indicating if the account will be locked after password
                expiration. This attribute was added in vSphere API 6.7.
                If None, defaults to True.
            :type  days_after_password_expiration: :class:`long` or ``None``
            :param days_after_password_expiration: Number of days after password expiration before the account will be
                locked. This attribute was added in vSphere API 6.7.
                If None, will be taken from system defaults (see
                local-accounts/policy).
            :type  min_days_between_password_change: :class:`long` or ``None``
            :param min_days_between_password_change: Minimum number of days between password change. This attribute was
                added in vSphere API 6.7.
                If None, will be taken from system defaults (see
                local-accounts/policy).
            :type  max_days_between_password_change: :class:`long` or ``None``
            :param max_days_between_password_change: Maximum number of days between password change. This attribute was
                added in vSphere API 6.7.
                If None, will be taken from system defaults (see
                local-accounts/policy).
            :type  warn_days_before_password_expiration: :class:`long` or ``None``
            :param warn_days_before_password_expiration: Number of days of warning before password expires. This attribute
                was added in vSphere API 6.7.
                If None, will be taken from system defaults (see
                local-accounts/policy).
            """
            self.password = password
            self.old_password = old_password
            self.full_name = full_name
            self.email = email
            self.roles = roles
            self.enabled = enabled
            self.password_expires = password_expires
            self.password_expires_at = password_expires_at
            self.inactive_after_password_expiration = inactive_after_password_expiration
            self.days_after_password_expiration = days_after_password_expiration
            self.min_days_between_password_change = min_days_between_password_change
            self.max_days_between_password_change = max_days_between_password_change
            self.warn_days_before_password_expiration = warn_days_before_password_expiration
            VapiStruct.__init__(self)


    Config._set_binding_type(type.StructType(
        'com.vmware.appliance.local_accounts.config', {
            'password': type.SecretType(),
            'old_password': type.OptionalType(type.SecretType()),
            'full_name': type.OptionalType(type.StringType()),
            'email': type.OptionalType(type.StringType()),
            'roles': type.ListType(type.IdType()),
            'enabled': type.OptionalType(type.BooleanType()),
            'password_expires': type.OptionalType(type.BooleanType()),
            'password_expires_at': type.OptionalType(type.DateTimeType()),
            'inactive_after_password_expiration': type.OptionalType(type.BooleanType()),
            'days_after_password_expiration': type.OptionalType(type.IntegerType()),
            'min_days_between_password_change': type.OptionalType(type.IntegerType()),
            'max_days_between_password_change': type.OptionalType(type.IntegerType()),
            'warn_days_before_password_expiration': type.OptionalType(type.IntegerType()),
        },
        Config,
        False,
        None))


    class UpdateConfig(VapiStruct):
        """
        The ``LocalAccounts.UpdateConfig`` class defines the fields that might be
        updated. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     password=None,
                     old_password=None,
                     full_name=None,
                     email=None,
                     roles=None,
                     enabled=None,
                     password_expires=None,
                     password_expires_at=None,
                     inactive_after_password_expiration=None,
                     days_after_password_expiration=None,
                     min_days_between_password_change=None,
                     max_days_between_password_change=None,
                     warn_days_before_password_expiration=None,
                    ):
            """
            :type  password: :class:`str` or ``None``
            :param password: Password. This attribute was added in vSphere API 6.7.
                If None, value will not be changed
            :type  old_password: :class:`str` or ``None``
            :param old_password: Old password of the user (required in case of the password change,
                not required if superAdmin user changes the password of the other
                user). This attribute was added in vSphere API 6.7.
                If None, user may not have password set.
            :type  full_name: :class:`str` or ``None``
            :param full_name: Full name of the user. This attribute was added in vSphere API 6.7.
                If None, value will not be changed
            :type  email: :class:`str` or ``None``
            :param email: Email address of the local account. This attribute was added in
                vSphere API 6.7.
                If None, value will not be changed
            :type  roles: :class:`list` of :class:`str` or ``None``
            :param roles: User roles. This attribute was added in vSphere API 6.7.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.appliance.roles``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``com.vmware.appliance.roles``.
                If None, value will not be changed
            :type  enabled: :class:`bool` or ``None``
            :param enabled: Flag indicating if the account is enabled. This attribute was added
                in vSphere API 6.7.
                If None, value will not be changed
            :type  password_expires: :class:`bool` or ``None``
            :param password_expires: Flag indicating if the account password expires. This attribute was
                added in vSphere API 6.7.
                If None, value will not be changed
            :type  password_expires_at: :class:`datetime.datetime` or ``None``
            :param password_expires_at: Date when the account's password will expire. This attribute was
                added in vSphere API 6.7.
                If None, value will not be changed
            :type  inactive_after_password_expiration: :class:`bool` or ``None``
            :param inactive_after_password_expiration: Flag indicating if the account will be locked after password
                expiration. This attribute was added in vSphere API 6.7.
                If None, value will not be changed
            :type  days_after_password_expiration: :class:`long` or ``None``
            :param days_after_password_expiration: Number of days after password expiration before the account will be
                locked. This attribute was added in vSphere API 6.7.
                If None, value will not be changed
            :type  min_days_between_password_change: :class:`long` or ``None``
            :param min_days_between_password_change: Minimum number of days between password change. This attribute was
                added in vSphere API 6.7.
                If None, value will not be changed
            :type  max_days_between_password_change: :class:`long` or ``None``
            :param max_days_between_password_change: Maximum number of days between password change. This attribute was
                added in vSphere API 6.7.
                If None, value will not be changed
            :type  warn_days_before_password_expiration: :class:`long` or ``None``
            :param warn_days_before_password_expiration: Number of days of warning before password expires. This attribute
                was added in vSphere API 6.7.
                If None, value will not be changed
            """
            self.password = password
            self.old_password = old_password
            self.full_name = full_name
            self.email = email
            self.roles = roles
            self.enabled = enabled
            self.password_expires = password_expires
            self.password_expires_at = password_expires_at
            self.inactive_after_password_expiration = inactive_after_password_expiration
            self.days_after_password_expiration = days_after_password_expiration
            self.min_days_between_password_change = min_days_between_password_change
            self.max_days_between_password_change = max_days_between_password_change
            self.warn_days_before_password_expiration = warn_days_before_password_expiration
            VapiStruct.__init__(self)


    UpdateConfig._set_binding_type(type.StructType(
        'com.vmware.appliance.local_accounts.update_config', {
            'password': type.OptionalType(type.SecretType()),
            'old_password': type.OptionalType(type.SecretType()),
            'full_name': type.OptionalType(type.StringType()),
            'email': type.OptionalType(type.StringType()),
            'roles': type.OptionalType(type.ListType(type.IdType())),
            'enabled': type.OptionalType(type.BooleanType()),
            'password_expires': type.OptionalType(type.BooleanType()),
            'password_expires_at': type.OptionalType(type.DateTimeType()),
            'inactive_after_password_expiration': type.OptionalType(type.BooleanType()),
            'days_after_password_expiration': type.OptionalType(type.IntegerType()),
            'min_days_between_password_change': type.OptionalType(type.IntegerType()),
            'max_days_between_password_change': type.OptionalType(type.IntegerType()),
            'warn_days_before_password_expiration': type.OptionalType(type.IntegerType()),
        },
        UpdateConfig,
        False,
        None))



    def get(self,
            username,
            ):
        """
        Get the local user account information. This method was added in
        vSphere API 6.7.

        :type  username: :class:`str`
        :param username: User login name
        :rtype: :class:`LocalAccounts.Info`
        :return: Local user account information
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the account is not found
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get',
                            {
                            'username': username,
                            })

    def list(self):
        """
        Get a list of the local user accounts. This method was added in vSphere
        API 6.7.


        :rtype: :class:`list` of :class:`str`
        :return: List of identifiers
            The return value will contain identifiers for the resource type:
            ``com.vmware.appliance.local_accounts``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('list', None)

    def create(self,
               username,
               config,
               ):
        """
        Create a new local user account. This method was added in vSphere API
        6.7.

        :type  username: :class:`str`
        :param username: User login name
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.local_accounts``.
        :type  config: :class:`LocalAccounts.Config`
        :param config: User configuration
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If an account already exists
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If a username is invalid (username is validated against
            [a-zA-Z0-9][a-zA-Z0-9\-\.\\\\@]\*[a-zA-Z0-9] pattern)
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('create',
                            {
                            'username': username,
                            'config': config,
                            })

    def set(self,
            username,
            config,
            ):
        """
        Set local user account properties. This method was added in vSphere API
        6.7.

        :type  username: :class:`str`
        :param username: User login name
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.local_accounts``.
        :type  config: :class:`LocalAccounts.Config`
        :param config: User configuration
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the account is not found
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('set',
                            {
                            'username': username,
                            'config': config,
                            })

    def update(self,
               username,
               config,
               ):
        """
        Update selected fields in local user account properties. This method
        was added in vSphere API 6.7.

        :type  username: :class:`str`
        :param username: User login name
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.local_accounts``.
        :type  config: :class:`LocalAccounts.UpdateConfig`
        :param config: User configuration
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the account is not found
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('update',
                            {
                            'username': username,
                            'config': config,
                            })

    def delete(self,
               username,
               ):
        """
        Delete a local user account. This method was added in vSphere API 6.7.

        :type  username: :class:`str`
        :param username: User login name
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.local_accounts``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the account is not found
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('delete',
                            {
                            'username': username,
                            })
class Monitoring(VapiInterface):
    """
    ``Monitoring`` class provides methods Get and list monitoring data for
    requested item.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.monitoring'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _MonitoringStub)
        self._VAPI_OPERATION_IDS = {}

    class FunctionType(Enum):
        """
        ``Monitoring.FunctionType`` class Defines aggregation function

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        COUNT = None
        """
        Aggregation takes count per period (sum)

        """
        MAX = None
        """
        Aggregation takes maximums per period

        """
        AVG = None
        """
        Aggregation takes average per period

        """
        MIN = None
        """
        Aggregation takes minimums per period

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`FunctionType` instance.
            """
            Enum.__init__(string)

    FunctionType._set_values({
        'COUNT': FunctionType('COUNT'),
        'MAX': FunctionType('MAX'),
        'AVG': FunctionType('AVG'),
        'MIN': FunctionType('MIN'),
    })
    FunctionType._set_binding_type(type.EnumType(
        'com.vmware.appliance.monitoring.function_type',
        FunctionType))


    class IntervalType(Enum):
        """
        ``Monitoring.IntervalType`` class Defines interval between the values in
        hours and mins, for which aggregation will apply

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        MINUTES30 = None
        """
        Thirty minutes interval between values. One week is 336 values.

        """
        HOURS2 = None
        """
        Two hours interval between values. One month has 360 values.

        """
        MINUTES5 = None
        """
        Five minutes interval between values (finest). One day would have 288
        values, one week is 2016.

        """
        DAY1 = None
        """
        24 hours interval between values. One year has 365 values.

        """
        HOURS6 = None
        """
        Six hour interval between values. One quarter is 360 values.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`IntervalType` instance.
            """
            Enum.__init__(string)

    IntervalType._set_values({
        'MINUTES30': IntervalType('MINUTES30'),
        'HOURS2': IntervalType('HOURS2'),
        'MINUTES5': IntervalType('MINUTES5'),
        'DAY1': IntervalType('DAY1'),
        'HOURS6': IntervalType('HOURS6'),
    })
    IntervalType._set_binding_type(type.EnumType(
        'com.vmware.appliance.monitoring.interval_type',
        IntervalType))


    class MonitoredItemData(VapiStruct):
        """
        ``Monitoring.MonitoredItemData`` class Structure representing monitored
        item data.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     interval=None,
                     function=None,
                     start_time=None,
                     end_time=None,
                     data=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Monitored item IDs Ex: CPU, MEMORY, STORAGE_TOTAL
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.appliance.monitoring``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.appliance.monitoring``.
            :type  interval: :class:`Monitoring.IntervalType`
            :param interval: interval between values in hours, minutes
            :type  function: :class:`Monitoring.FunctionType`
            :param function: aggregation function
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Start time in UTC
            :type  end_time: :class:`datetime.datetime`
            :param end_time: End time in UTC
            :type  data: :class:`list` of :class:`str`
            :param data: list of values
            """
            self.name = name
            self.interval = interval
            self.function = function
            self.start_time = start_time
            self.end_time = end_time
            self.data = data
            VapiStruct.__init__(self)


    MonitoredItemData._set_binding_type(type.StructType(
        'com.vmware.appliance.monitoring.monitored_item_data', {
            'name': type.IdType(resource_types='com.vmware.appliance.monitoring'),
            'interval': type.ReferenceType(__name__, 'Monitoring.IntervalType'),
            'function': type.ReferenceType(__name__, 'Monitoring.FunctionType'),
            'start_time': type.DateTimeType(),
            'end_time': type.DateTimeType(),
            'data': type.ListType(type.StringType()),
        },
        MonitoredItemData,
        False,
        None))


    class MonitoredItemDataRequest(VapiStruct):
        """
        ``Monitoring.MonitoredItemDataRequest`` class Structure representing
        requested monitored item data.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     names=None,
                     interval=None,
                     function=None,
                     start_time=None,
                     end_time=None,
                    ):
            """
            :type  names: :class:`list` of :class:`str`
            :param names: monitored item IDs Ex: CPU, MEMORY
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.appliance.monitoring``. When methods return a value of
                this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.appliance.monitoring``.
            :type  interval: :class:`Monitoring.IntervalType`
            :param interval: interval between values in hours, minutes
            :type  function: :class:`Monitoring.FunctionType`
            :param function: aggregation function
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Start time in UTC
            :type  end_time: :class:`datetime.datetime`
            :param end_time: End time in UTC
            """
            self.names = names
            self.interval = interval
            self.function = function
            self.start_time = start_time
            self.end_time = end_time
            VapiStruct.__init__(self)


    MonitoredItemDataRequest._set_binding_type(type.StructType(
        'com.vmware.appliance.monitoring.monitored_item_data_request', {
            'names': type.ListType(type.IdType()),
            'interval': type.ReferenceType(__name__, 'Monitoring.IntervalType'),
            'function': type.ReferenceType(__name__, 'Monitoring.FunctionType'),
            'start_time': type.DateTimeType(),
            'end_time': type.DateTimeType(),
        },
        MonitoredItemDataRequest,
        False,
        None))


    class MonitoredItem(VapiStruct):
        """
        ``Monitoring.MonitoredItem`` class Structure representing requested
        monitored item data.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     name=None,
                     units=None,
                     category=None,
                     instance=None,
                     description=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: monitored item ID Ex: CPU, MEMORY
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.appliance.monitoring``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.appliance.monitoring``.
            :type  name: :class:`str`
            :param name: monitored item name Ex: "Network write speed"
            :type  units: :class:`str`
            :param units: Y-axis label EX: "Mbps", "%"
            :type  category: :class:`str`
            :param category: category Ex: network, storage etc
            :type  instance: :class:`str`
            :param instance: instance name Ex: eth0
            :type  description: :class:`str`
            :param description: monitored item description Ex:
                com.vmware.applmgmt.mon.descr.net.rx.packetRate.eth0
            """
            self.id = id
            self.name = name
            self.units = units
            self.category = category
            self.instance = instance
            self.description = description
            VapiStruct.__init__(self)


    MonitoredItem._set_binding_type(type.StructType(
        'com.vmware.appliance.monitoring.monitored_item', {
            'id': type.IdType(resource_types='com.vmware.appliance.monitoring'),
            'name': type.StringType(),
            'units': type.StringType(),
            'category': type.StringType(),
            'instance': type.StringType(),
            'description': type.StringType(),
        },
        MonitoredItem,
        False,
        None))



    def query(self,
              item,
              ):
        """
        Get monitoring data.

        :type  item: :class:`Monitoring.MonitoredItemDataRequest`
        :param item: MonitoredItemDataRequest Structure
        :rtype: :class:`list` of :class:`Monitoring.MonitoredItemData`
        :return: list of MonitoredItemData structure
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('query',
                            {
                            'item': item,
                            })

    def list(self):
        """
        Get monitored items list


        :rtype: :class:`list` of :class:`Monitoring.MonitoredItem`
        :return: list of names
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('list', None)

    def get(self,
            stat_id,
            ):
        """
        Get monitored item info

        :type  stat_id: :class:`str`
        :param stat_id: statistic item id
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.monitoring``.
        :rtype: :class:`Monitoring.MonitoredItem`
        :return: MonitoredItem structure
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get',
                            {
                            'stat_id': stat_id,
                            })
class Networking(VapiInterface):
    """
    The ``Networking`` class provides methods Get Network configurations. This
    class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.networking'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NetworkingStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'change_task': 'change$task'})

    class DNSInfo(VapiStruct):
        """
        The ``Networking.DNSInfo`` class contains information about the DNS
        configuration of a virtual appliance. This class was added in vSphere API
        6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     mode=None,
                     hostname=None,
                     servers=None,
                    ):
            """
            :type  mode: :class:`Networking.DNSInfo.DNSMode`
            :param mode: DNS mode. This attribute was added in vSphere API 6.7.
            :type  hostname: :class:`str`
            :param hostname: Hostname. This attribute was added in vSphere API 6.7.
            :type  servers: :class:`list` of :class:`str`
            :param servers: Servers. This attribute was added in vSphere API 6.7.
            """
            self.mode = mode
            self.hostname = hostname
            self.servers = servers
            VapiStruct.__init__(self)


        class DNSMode(Enum):
            """
            The ``Networking.DNSInfo.DNSMode`` class describes the source of DNS
            servers. This enumeration was added in vSphere API 6.7.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            DHCP = None
            """
            The DNS servers addresses are obtained from a DHCP server. This class
            attribute was added in vSphere API 6.7.

            """
            STATIC = None
            """
            The DNS servers addresses are specified explicitly. This class attribute
            was added in vSphere API 6.7.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`DNSMode` instance.
                """
                Enum.__init__(string)

        DNSMode._set_values({
            'DHCP': DNSMode('DHCP'),
            'STATIC': DNSMode('STATIC'),
        })
        DNSMode._set_binding_type(type.EnumType(
            'com.vmware.appliance.networking.DNS_info.DNS_mode',
            DNSMode))

    DNSInfo._set_binding_type(type.StructType(
        'com.vmware.appliance.networking.DNS_info', {
            'mode': type.ReferenceType(__name__, 'Networking.DNSInfo.DNSMode'),
            'hostname': type.StringType(),
            'servers': type.ListType(type.StringType()),
        },
        DNSInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Networking.Info`` class contains information about the network
        configuration of a virtual appliance. This class was added in vSphere API
        6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     dns=None,
                     interfaces=None,
                    ):
            """
            :type  dns: :class:`Networking.DNSInfo`
            :param dns: DNS configuration. This attribute was added in vSphere API 6.7.
            :type  interfaces: :class:`dict` of :class:`str` and :class:`com.vmware.appliance.networking_client.Interfaces.InterfaceInfo`
            :param interfaces: Interface configuration as a key-value map where key is a network
                interface name, for example, "nic0". This attribute was added in
                vSphere API 6.7.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.appliance.networking.interfaces``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.appliance.networking.interfaces``.
            """
            self.dns = dns
            self.interfaces = interfaces
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.networking.info', {
            'dns': type.ReferenceType(__name__, 'Networking.DNSInfo'),
            'interfaces': type.MapType(type.IdType(), type.ReferenceType('com.vmware.appliance.networking_client', 'Interfaces.InterfaceInfo')),
        },
        Info,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Networking.UpdateSpec`` class describes whether to enable or disable
        ipv6 on interfaces. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ipv6_enabled=None,
                    ):
            """
            :type  ipv6_enabled: :class:`bool` or ``None``
            :param ipv6_enabled: IPv6 Enabled or not. This attribute was added in vSphere API 6.7.
                If unspecified, leaves the current state of Ipv6.
            """
            self.ipv6_enabled = ipv6_enabled
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.networking.update_spec', {
            'ipv6_enabled': type.OptionalType(type.BooleanType()),
        },
        UpdateSpec,
        False,
        None))


    class ChangeSpec(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'SSO_user': 'sso_user',
                                'SSO_password': 'sso_password',
                                }

        def __init__(self,
                     hostname=None,
                     sso_user=None,
                     sso_password=None,
                     dns=None,
                     ipv4=None,
                     ipv6=None,
                    ):
            """
            :type  hostname: :class:`str`
            :param hostname: New hostname to assign to the management network of vCenter
                appliance. This attribute was added in vSphere API 6.7.3.
            :type  sso_user: :class:`str`
            :param sso_user: vCenter Server SSO administrator username. This attribute was added
                in vSphere API 6.7.3.
            :type  sso_password: :class:`str`
            :param sso_password: vCenter Server SSO administrator Password. This attribute was added
                in vSphere API 6.7.3.
            :type  dns: :class:`com.vmware.appliance.networking.dns_client.Servers.DNSServerConfig` or ``None``
            :param dns: DNS Configuration to set for the machine. This attribute was added
                in vSphere API 6.7.3.
                If None DNS settings will not be changed
            :type  ipv4: :class:`com.vmware.appliance.networking.interfaces_client.Ipv4.Config` or ``None``
            :param ipv4: IPv4 Configuration to set for the machine. This attribute was added
                in vSphere API 6.7.3.
                If None IPv4 settings will not be changed
            :type  ipv6: :class:`com.vmware.appliance.networking.interfaces_client.Ipv6.Config` or ``None``
            :param ipv6: IPv6 Configuration to set for the machine. This attribute was added
                in vSphere API 6.7.3.
                If None IPv6 settings will not be changed
            """
            self.hostname = hostname
            self.sso_user = sso_user
            self.sso_password = sso_password
            self.dns = dns
            self.ipv4 = ipv4
            self.ipv6 = ipv6
            VapiStruct.__init__(self)


    ChangeSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.networking.change_spec', {
            'hostname': type.StringType(),
            'SSO_user': type.StringType(),
            'SSO_password': type.SecretType(),
            'dns': type.OptionalType(type.ReferenceType('com.vmware.appliance.networking.dns_client', 'Servers.DNSServerConfig')),
            'ipv4': type.OptionalType(type.ReferenceType('com.vmware.appliance.networking.interfaces_client', 'Ipv4.Config')),
            'ipv6': type.OptionalType(type.ReferenceType('com.vmware.appliance.networking.interfaces_client', 'Ipv6.Config')),
        },
        ChangeSpec,
        False,
        None))



    def get(self):
        """
        Get Networking information for all configured interfaces. This method
        was added in vSphere API 6.7.


        :rtype: :class:`Networking.Info`
        :return: The Map of network configuration info for all interfaces.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('get', None)

    def update(self,
               spec,
               ):
        """
        Enable or Disable ipv6 on all interfaces. This method was added in
        vSphere API 6.7.

        :type  spec: :class:`Networking.UpdateSpec`
        :param spec: update spec with optional boolean value
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('update',
                            {
                            'spec': spec,
                            })

    def reset(self):
        """
        Reset and restarts network configuration on all interfaces, also this
        will renew the DHCP lease for DHCP IP address. This method was added in
        vSphere API 6.7.


        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('reset', None)


    def change_task(self,
               spec,
               ):
        """
        Changes the Hostname/IP of the management network of vCenter appliance.
        The Hostname/IP change invokes the PNID change process which involves
        LDAP entry modification, updating registry entries, configuration files
        modification and network configuration changes. vCenter server is
        expected to be down for few minutes during these changes. This method
        was added in vSphere API 6.7.3.

        :type  spec: :class:`Networking.ChangeSpec`
        :param spec: Information required to change the hostname.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if it's not embedded node
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if another change task is in progress
        """
        task_id = self._invoke('change$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class Ntp(VapiInterface):
    """
    ``Ntp`` class provides methods Gets NTP configuration status and tests
    connection to ntp servers. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.ntp'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NtpStub)
        self._VAPI_OPERATION_IDS = {}

    class ServerStatus(Enum):
        """
        ``Ntp.ServerStatus`` class Status of server during test. This enumeration
        was added in vSphere API 6.7.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        SERVER_REACHABLE = None
        """
        Server is reachable. This class attribute was added in vSphere API 6.7.

        """
        SERVER_UNREACHABLE = None
        """
        Server is unreachable. This class attribute was added in vSphere API 6.7.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ServerStatus` instance.
            """
            Enum.__init__(string)

    ServerStatus._set_values({
        'SERVER_REACHABLE': ServerStatus('SERVER_REACHABLE'),
        'SERVER_UNREACHABLE': ServerStatus('SERVER_UNREACHABLE'),
    })
    ServerStatus._set_binding_type(type.EnumType(
        'com.vmware.appliance.ntp.server_status',
        ServerStatus))


    class LocalizableMessage(VapiStruct):
        """
        ``Ntp.LocalizableMessage`` class Structure representing message. This class
        was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     default_message=None,
                     args=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: id in message bundle. This attribute was added in vSphere API 6.7.
            :type  default_message: :class:`str`
            :param default_message: text in english. This attribute was added in vSphere API 6.7.
            :type  args: :class:`list` of :class:`str`
            :param args: nested data. This attribute was added in vSphere API 6.7.
            """
            self.id = id
            self.default_message = default_message
            self.args = args
            VapiStruct.__init__(self)


    LocalizableMessage._set_binding_type(type.StructType(
        'com.vmware.appliance.ntp.localizable_message', {
            'id': type.StringType(),
            'default_message': type.StringType(),
            'args': type.ListType(type.StringType()),
        },
        LocalizableMessage,
        False,
        None))


    class TestRunStatus(VapiStruct):
        """
        ``Ntp.TestRunStatus`` class Status of the test. This class was added in
        vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     server=None,
                     status=None,
                     message=None,
                    ):
            """
            :type  server: :class:`str`
            :param server: Server name associated with the test run. This attribute was added
                in vSphere API 6.7.
            :type  status: :class:`Ntp.ServerStatus`
            :param status: Server status. This attribute was added in vSphere API 6.7.
            :type  message: :class:`Ntp.LocalizableMessage`
            :param message: Message associated with status. This attribute was added in vSphere
                API 6.7.
            """
            self.server = server
            self.status = status
            self.message = message
            VapiStruct.__init__(self)


    TestRunStatus._set_binding_type(type.StructType(
        'com.vmware.appliance.ntp.test_run_status', {
            'server': type.StringType(),
            'status': type.ReferenceType(__name__, 'Ntp.ServerStatus'),
            'message': type.ReferenceType(__name__, 'Ntp.LocalizableMessage'),
        },
        TestRunStatus,
        False,
        None))



    def test(self,
             servers,
             ):
        """
        Test the connection to a list of ntp servers. This method was added in
        vSphere API 6.7.

        :type  servers: :class:`list` of :class:`str`
        :param servers: List of host names or IP addresses of NTP servers.
        :rtype: :class:`list` of :class:`Ntp.TestRunStatus`
        :return: List of test run statuses.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('test',
                            {
                            'servers': servers,
                            })

    def set(self,
            servers,
            ):
        """
        Set NTP servers. This method updates old NTP servers from configuration
        and sets the input NTP servers in the configuration. If NTP based time
        synchronization is used internally, the NTP daemon will be restarted to
        reload given NTP configuration. In case NTP based time synchronization
        is not used, this method only replaces servers in the NTP
        configuration. This method was added in vSphere API 6.7.

        :type  servers: :class:`list` of :class:`str`
        :param servers: List of host names or ip addresses of ntp servers.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('set',
                            {
                            'servers': servers,
                            })

    def get(self):
        """
        Get the NTP configuration status. If you run the 'timesync.get'
        command, you can retrieve the current time synchronization method (NTP-
        or VMware Tools-based). The 'ntp' command always returns the NTP server
        information, even when the time synchronization mode is not set to NTP.
        If the time synchronization mode is not NTP-based, the NTP server
        status is displayed as down. This method was added in vSphere API 6.7.


        :rtype: :class:`list` of :class:`str`
        :return: List of NTP servers.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)
class Recovery(VapiInterface):
    """
    The ``Recovery`` class provides methods to invoke an appliance recovery
    (backup and restore). This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.recovery'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _RecoveryStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Recovery.Info`` class contains the information about the appliance
        recovery environment. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     supported=None,
                    ):
            """
            :type  supported: :class:`bool`
            :param supported: Is recovery supported in this appliance. This attribute was added
                in vSphere API 6.7.
            """
            self.supported = supported
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.recovery.info', {
            'supported': type.BooleanType(),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Gets the properties of the appliance Recovery subsystem. This method
        was added in vSphere API 6.7.


        :rtype: :class:`Recovery.Info`
        :return: Structure containing the properties of the Recovery subsystem.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if any error occurs during the execution of the operation.
        """
        return self._invoke('get', None)
class Services(VapiInterface):
    """
    The ``Service`` class provides methods to manage a single/set of appliance
    services. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.services'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ServicesStub)
        self._VAPI_OPERATION_IDS = {}

    class State(Enum):
        """
        The ``Services.State`` class defines valid Run State for services. This
        enumeration was added in vSphere API 6.7.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        STARTING = None
        """
        Service Run State is Starting, it is still not functional. This class
        attribute was added in vSphere API 6.7.

        """
        STOPPING = None
        """
        Service Run State is Stopping, it is not functional. This class attribute
        was added in vSphere API 6.7.

        """
        STARTED = None
        """
        Service Run State is Started, it is fully functional. This class attribute
        was added in vSphere API 6.7.

        """
        STOPPED = None
        """
        Service Run State is Stopped. This class attribute was added in vSphere API
        6.7.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`State` instance.
            """
            Enum.__init__(string)

    State._set_values({
        'STARTING': State('STARTING'),
        'STOPPING': State('STOPPING'),
        'STARTED': State('STARTED'),
        'STOPPED': State('STOPPED'),
    })
    State._set_binding_type(type.EnumType(
        'com.vmware.appliance.services.state',
        State))


    class Info(VapiStruct):
        """
        The ``Services.Info`` class contains information about a service. This
        class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     description=None,
                     state=None,
                    ):
            """
            :type  description: :class:`str`
            :param description: Service description. This attribute was added in vSphere API 6.7.
            :type  state: :class:`Services.State`
            :param state: Running State. This attribute was added in vSphere API 6.7.
            """
            self.description = description
            self.state = state
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.services.info', {
            'description': type.StringType(),
            'state': type.ReferenceType(__name__, 'Services.State'),
        },
        Info,
        False,
        None))



    def start(self,
              service,
              ):
        """
        Starts a service. This method was added in vSphere API 6.7.

        :type  service: :class:`str`
        :param service: identifier of the service to start
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.services``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the service associated with ``service`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the operation is denied in the current state of the service. If
            a stop or restart operation is in progress, the start operation
            will not be allowed.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if start operation is issued on a service which has startup type
            StartupType#DISABLED.
        :raise: :class:`com.vmware.vapi.std.errors_client.TimedOut` 
            if any timeout occurs during the execution of the start operation.
            Timeout occurs when the service takes longer than StartTimeout to
            start.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if any other error occurs during the execution of the operation.
        """
        return self._invoke('start',
                            {
                            'service': service,
                            })

    def stop(self,
             service,
             ):
        """
        Stops a service. This method was added in vSphere API 6.7.

        :type  service: :class:`str`
        :param service: identifier of the service to stop
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.services``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the service associated with ``service`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if any other error occurs during the execution of the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the operation is denied in the current state of the service. If
            a stop operation is in progress, issuing another stop operation
            will lead to this error.
        """
        return self._invoke('stop',
                            {
                            'service': service,
                            })

    def restart(self,
                service,
                ):
        """
        Restarts a service. This method was added in vSphere API 6.7.

        :type  service: :class:`str`
        :param service: identifier of the service to restart
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.services``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the service associated with ``service`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.TimedOut` 
            if any timeout occurs during the execution of the restart
            operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the operation is denied in the current state of the service. If
            a stop or start operation is in progress, issuing a restart
            operation will lead to this error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if a restart operation is issued on a service which has startup
            type StartupType#DISABLED
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if any other error occurs during the execution of the operation.
        """
        return self._invoke('restart',
                            {
                            'service': service,
                            })

    def get(self,
            service,
            ):
        """
        Returns the state of a service. This method was added in vSphere API
        6.7.

        :type  service: :class:`str`
        :param service: identifier of the service whose state is being queried.
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.services``.
        :rtype: :class:`Services.Info`
        :return: Service Info structure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the service associated with ``service`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if any other error occurs during the execution of the operation.
        """
        return self._invoke('get',
                            {
                            'service': service,
                            })

    def list(self):
        """
        Lists details of vCenter services. This method was added in vSphere API
        6.7.


        :rtype: :class:`dict` of :class:`str` and :class:`Services.Info`
        :return: Map of service identifiers to service Info structures.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``com.vmware.appliance.services``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if any error occurs during the execution of the operation.
        """
        return self._invoke('list', None)
class Shutdown(VapiInterface):
    """
    ``Shutdown`` class provides methods Performs reboot/shutdown operations on
    appliance. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.shutdown'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ShutdownStub)
        self._VAPI_OPERATION_IDS = {}

    class ShutdownConfig(VapiStruct):
        """
        ``Shutdown.ShutdownConfig`` class Structure that defines shutdown
        configuration returned by the Shutdown.get operation. This class was added
        in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     shutdown_time=None,
                     action=None,
                     reason=None,
                    ):
            """
            :type  shutdown_time: :class:`datetime.datetime` or ``None``
            :param shutdown_time: Shutdown time. This attribute was added in vSphere API 6.7.
                shutdownTime Optional value of pending shutdown time
            :type  action: :class:`str`
            :param action: The pending shutdown operation. The string values for pending
                operations can be 'poweroff', 'reboot' or ''. This attribute was
                added in vSphere API 6.7.
            :type  reason: :class:`str`
            :param reason: The reason behind the shutdown action. This attribute was added in
                vSphere API 6.7.
            """
            self.shutdown_time = shutdown_time
            self.action = action
            self.reason = reason
            VapiStruct.__init__(self)


    ShutdownConfig._set_binding_type(type.StructType(
        'com.vmware.appliance.shutdown.shutdown_config', {
            'shutdown_time': type.OptionalType(type.DateTimeType()),
            'action': type.StringType(),
            'reason': type.StringType(),
        },
        ShutdownConfig,
        False,
        None))



    def cancel(self):
        """
        Cancel pending shutdown action. This method was added in vSphere API
        6.7.


        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('cancel', None)

    def poweroff(self,
                 delay,
                 reason,
                 ):
        """
        Power off the appliance. This method was added in vSphere API 6.7.

        :type  delay: :class:`long`
        :param delay: Minutes after which poweroff should start. If 0 is specified,
            poweroff will start immediately.
        :type  reason: :class:`str`
        :param reason: Reason for peforming poweroff.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('poweroff',
                            {
                            'delay': delay,
                            'reason': reason,
                            })

    def reboot(self,
               delay,
               reason,
               ):
        """
        Reboot the appliance. This method was added in vSphere API 6.7.

        :type  delay: :class:`long`
        :param delay: Minutes after which reboot should start. If 0 is specified, reboot
            will start immediately.
        :type  reason: :class:`str`
        :param reason: Reason for peforming reboot.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('reboot',
                            {
                            'delay': delay,
                            'reason': reason,
                            })

    def get(self):
        """
        Get details about the pending shutdown action. This method was added in
        vSphere API 6.7.


        :rtype: :class:`Shutdown.ShutdownConfig`
        :return: Configuration of pending shutdown action.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)
class Cores(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.cores'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CoresStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     size=None,
                     creation_time=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Identifier of the core file. This attribute was added in vSphere
                API 8.0.2.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.appliance.supportbundle.cores``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.appliance.supportbundle.cores``.
            :type  size: :class:`long`
            :param size: Size of core file. This attribute was added in vSphere API 8.0.2.0.
            :type  creation_time: :class:`datetime.datetime`
            :param creation_time: Creation time of core file. This attribute was added in vSphere API
                8.0.2.0.
            """
            self.name = name
            self.size = size
            self.creation_time = creation_time
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.cores.info', {
            'name': type.IdType(resource_types='com.vmware.appliance.supportbundle.cores'),
            'size': type.IntegerType(),
            'creation_time': type.DateTimeType(),
        },
        Info,
        False,
        None))



    def list(self):
        """
        Lists all the core files exists on storage. This method was added in
        vSphere API 8.0.2.0.


        :rtype: :class:`list` of :class:`Cores.Info`
        :return: List of core files details.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('list', None)
class SupportBundle(VapiInterface):
    """
    The ``SupportBundle`` class provides methods to create support bundle, list
    and delete generated support bundle. This class was added in vSphere API
    7.0.1.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.support_bundle'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SupportBundleStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})

    class CreationStatus(Enum):
        """
        

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        SUCCEEDED = None
        """
        Support bundle creation task succeeded. This class attribute was added in
        vSphere API 7.0.1.0.

        """
        FAILED = None
        """
        Support bundle creation task Failed. This class attribute was added in
        vSphere API 7.0.1.0.

        """
        CANCELLED = None
        """
        Support bundle creation task Cancelled. This class attribute was added in
        vSphere API 7.0.1.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`CreationStatus` instance.
            """
            Enum.__init__(string)

    CreationStatus._set_values({
        'SUCCEEDED': CreationStatus('SUCCEEDED'),
        'FAILED': CreationStatus('FAILED'),
        'CANCELLED': CreationStatus('CANCELLED'),
    })
    CreationStatus._set_binding_type(type.EnumType(
        'com.vmware.appliance.support_bundle.creation_status',
        CreationStatus))


    class ContentType(Enum):
        """
        The ``SupportBundle.ContentType`` class defines the content in the support
        bundle generated. This enumeration was added in vSphere API 8.0.2.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        LOGS = None
        """
        Support bundle will contain only logs. This class attribute was added in
        vSphere API 8.0.2.0.

        """
        CORES = None
        """
        Support bundle will contain only core files. This class attribute was added
        in vSphere API 8.0.2.0.

        """
        ALL = None
        """
        Support bundle will contain logs and core files. By default logs and cores
        are collected. This class attribute was added in vSphere API 8.0.2.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ContentType` instance.
            """
            Enum.__init__(string)

    ContentType._set_values({
        'LOGS': ContentType('LOGS'),
        'CORES': ContentType('CORES'),
        'ALL': ContentType('ALL'),
    })
    ContentType._set_binding_type(type.EnumType(
        'com.vmware.appliance.support_bundle.content_type',
        ContentType))


    class IterationSpec(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     size=None,
                    ):
            """
            :type  size: :class:`long` or ``None``
            :param size: Size specifies the maximum number of results to return. This
                attribute was added in vSphere API 7.0.1.0.
                If None defaults to 50.
            """
            self.size = size
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.support_bundle.iteration_spec', {
            'size': type.OptionalType(type.IntegerType()),
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     available=None,
                     creation_status=None,
                    ):
            """
            :type  available: :class:`bool` or ``None``
            :param available: Filter only downloadable details. This attribute was added in
                vSphere API 7.0.1.0.
            :type  creation_status: :class:`SupportBundle.CreationStatus` or ``None``
            :param creation_status: Filter by task status. This attribute was added in vSphere API
                7.0.1.0.
            """
            self.available = available
            self.creation_status = creation_status
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.support_bundle.filter_spec', {
            'available': type.OptionalType(type.BooleanType()),
            'creation_status': type.OptionalType(type.ReferenceType(__name__, 'SupportBundle.CreationStatus')),
        },
        FilterSpec,
        False,
        None))


    class Info(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'SUCCEEDED' : [('generation_time', True), ('url', True), ('expiration_time', True), ('downloadable', True), ('size', True), ('checksum_value', True), ('content_type', False)],
                    'FAILED' : [('failure_reason', False)],
                    'CANCELLED' : [],
                }
            ),
        ]



        def __init__(self,
                     description=None,
                     status=None,
                     generation_time=None,
                     url=None,
                     expiration_time=None,
                     downloadable=None,
                     size=None,
                     failure_reason=None,
                     checksum_value=None,
                     id=None,
                     content_type=None,
                    ):
            """
            :type  description: :class:`str`
            :param description: Support bundle creation description. This attribute was added in
                vSphere API 7.0.1.0.
            :type  status: :class:`SupportBundle.CreationStatus`
            :param status: Status of the task. This attribute was added in vSphere API
                7.0.1.0.
            :type  generation_time: :class:`datetime.datetime`
            :param generation_time: Support bundle generation time. This attribute was added in vSphere
                API 7.0.1.0.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`SupportBundle.CreationStatus.SUCCEEDED`.
            :type  url: :class:`str`
            :param url: Support bundle downlooad URL. This attribute was added in vSphere
                API 7.0.1.0.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`SupportBundle.CreationStatus.SUCCEEDED`.
            :type  expiration_time: :class:`datetime.datetime`
            :param expiration_time: Download expiration time. This attribute was added in vSphere API
                7.0.1.0.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`SupportBundle.CreationStatus.SUCCEEDED`.
            :type  downloadable: :class:`bool`
            :param downloadable: Support bundle availability for download. This attribute was added
                in vSphere API 7.0.1.0.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`SupportBundle.CreationStatus.SUCCEEDED`.
            :type  size: :class:`long`
            :param size: Support bundle file size in KBs. This attribute was added in
                vSphere API 7.0.1.0.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`SupportBundle.CreationStatus.SUCCEEDED`.
            :type  failure_reason: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
            :param failure_reason: Reason for failure. This attribute was added in vSphere API
                7.0.1.0.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`SupportBundle.CreationStatus.FAILED`.
            :type  checksum_value: :class:`str`
            :param checksum_value: Support bundle SHA256 checksum value. This attribute was added in
                vSphere API 8.0.2.0.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`SupportBundle.CreationStatus.SUCCEEDED`.
            :type  id: :class:`str`
            :param id: Identifier of the support bundle. This attribute was added in
                vSphere API 8.0.2.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.appliance.supportbundle``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.appliance.supportbundle``.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  content_type: :class:`SupportBundle.ContentType` or ``None``
            :param content_type: Describes the content type (LOGS, CORES, ALL) collected in support
                bundle. This attribute was added in vSphere API 8.0.2.0.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`SupportBundle.CreationStatus.SUCCEEDED`.
            """
            self.description = description
            self.status = status
            self.generation_time = generation_time
            self.url = url
            self.expiration_time = expiration_time
            self.downloadable = downloadable
            self.size = size
            self.failure_reason = failure_reason
            self.checksum_value = checksum_value
            self.id = id
            self.content_type = content_type
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.support_bundle.info', {
            'description': type.StringType(),
            'status': type.ReferenceType(__name__, 'SupportBundle.CreationStatus'),
            'generation_time': type.OptionalType(type.DateTimeType()),
            'url': type.OptionalType(type.URIType()),
            'expiration_time': type.OptionalType(type.DateTimeType()),
            'downloadable': type.OptionalType(type.BooleanType()),
            'size': type.OptionalType(type.IntegerType()),
            'failure_reason': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'checksum_value': type.OptionalType(type.StringType()),
            'id': type.OptionalType(type.IdType()),
            'content_type': type.OptionalType(type.ReferenceType(__name__, 'SupportBundle.ContentType')),
        },
        Info,
        False,
        None))


    class ListResult(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     supportbundle_operations=None,
                    ):
            """
            :type  supportbundle_operations: :class:`list` of :class:`SupportBundle.Info`
            :param supportbundle_operations: Information about all support bundle requests. This attribute was
                added in vSphere API 7.0.1.0.
            """
            self.supportbundle_operations = supportbundle_operations
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.appliance.support_bundle.list_result', {
            'supportbundle_operations': type.ListType(type.ReferenceType(__name__, 'SupportBundle.Info')),
        },
        ListResult,
        False,
        None))


    class CreateSpec(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     description=None,
                     components=None,
                     content_type=None,
                     partition=None,
                    ):
            """
            :type  description: :class:`str`
            :param description: Support bundle creation description. This attribute was added in
                vSphere API 7.0.1.0.
            :type  components: (:class:`dict` of :class:`str` and :class:`list` of :class:`str`) or ``None``
            :param components: Support bundle components to be included. Map with groupName as key
                and list of components in that group as the value. This attribute
                was added in vSphere API 7.0.1.0.
            :type  content_type: :class:`SupportBundle.ContentType` or ``None``
            :param content_type: Describes the content type to be collected in support bundle. This
                attribute was added in vSphere API 8.0.2.0.
                If None, both logs and core files will be collected.
            :type  partition: :class:`str` or ``None``
            :param partition: Partition to be used for saving the support bundle. Available
                partitions can be retrieved using storage.list API. This attribute
                was added in vSphere API 7.0.1.0.
            """
            self.description = description
            self.components = components
            self.content_type = content_type
            self.partition = partition
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.support_bundle.create_spec', {
            'description': type.StringType(),
            'components': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.StringType()))),
            'content_type': type.OptionalType(type.ReferenceType(__name__, 'SupportBundle.ContentType')),
            'partition': type.OptionalType(type.StringType()),
        },
        CreateSpec,
        False,
        None))



    def list(self,
             iteration=None,
             filter=None,
             ):
        """
        Get list of support-bundles generated. This method was added in vSphere
        API 7.0.1.0.

        :type  iteration: :class:`SupportBundle.IterationSpec` or ``None``
        :param iteration: 
        :type  filter: :class:`SupportBundle.FilterSpec` or ``None``
        :param filter: 
        :rtype: :class:`SupportBundle.ListResult`
        :return: List of support bundle details.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('list',
                            {
                            'iteration': iteration,
                            'filter': filter,
                            })


    def create_task(self,
               spec,
               ):
        """
        Create a support bundle. This method was added in vSphere API 7.0.1.0.

        :type  spec: :class:`SupportBundle.CreateSpec`
        :param spec: 
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If already a support bundle task is in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        task_id = self._invoke('create$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance

    def delete(self,
               id,
               ):
        """
        Deletes the support bundle. This method was added in vSphere API
        8.0.2.0.

        :type  id: :class:`str`
        :param id: 
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.supportbundle``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If support bundle Not Found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('delete',
                            {
                            'id': id,
                            })
class Timesync(VapiInterface):
    """
    ``Timesync`` class provides methods Performs time synchronization
    configuration. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.timesync'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TimesyncStub)
        self._VAPI_OPERATION_IDS = {}

    class TimeSyncMode(Enum):
        """
        The ``Timesync.TimeSyncMode`` class defines time synchronization modes.
        This enumeration was added in vSphere API 6.7.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DISABLED = None
        """
        Time synchronization is disabled. This class attribute was added in vSphere
        API 6.7.

        """
        NTP = None
        """
        NTP-based time synchronization. This class attribute was added in vSphere
        API 6.7.

        """
        HOST = None
        """
        VMware Tool-based time synchronization. This class attribute was added in
        vSphere API 6.7.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`TimeSyncMode` instance.
            """
            Enum.__init__(string)

    TimeSyncMode._set_values({
        'DISABLED': TimeSyncMode('DISABLED'),
        'NTP': TimeSyncMode('NTP'),
        'HOST': TimeSyncMode('HOST'),
    })
    TimeSyncMode._set_binding_type(type.EnumType(
        'com.vmware.appliance.timesync.time_sync_mode',
        TimeSyncMode))



    def set(self,
            mode,
            ):
        """
        Set time synchronization mode. This method was added in vSphere API
        6.7.

        :type  mode: :class:`Timesync.TimeSyncMode`
        :param mode: Time synchronization mode.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('set',
                            {
                            'mode': mode,
                            })

    def get(self):
        """
        Get time synchronization mode. This method was added in vSphere API
        6.7.


        :rtype: :class:`Timesync.TimeSyncMode`
        :return: Time synchronization mode.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)
class Update(VapiInterface):
    """
    The ``Update`` class provides methods to get the status of the appliance
    update. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.update'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UpdateStub)
        self._VAPI_OPERATION_IDS = {}

    class State(Enum):
        """
        The ``Update.State`` class defines the various states the appliance update
        can be in. This enumeration was added in vSphere API 6.7.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        UP_TO_DATE = None
        """
        The appliance is up to date. This class attribute was added in vSphere API
        6.7.

        """
        UPDATES_PENDING = None
        """
        A new update is available. This class attribute was added in vSphere API
        6.7.

        """
        STAGE_IN_PROGRESS = None
        """
        The appliance update is in progress of downloading an update. This class
        attribute was added in vSphere API 6.7.

        """
        INSTALL_IN_PROGRESS = None
        """
        The appliance update is in progress of installing an update. This class
        attribute was added in vSphere API 6.7.

        """
        INSTALL_FAILED = None
        """
        The appliance update failed and cannot recover. This class attribute was
        added in vSphere API 6.7.

        """
        ROLLBACK_IN_PROGRESS = None
        """
        The appliance update failed and recovery is in progress. This class
        attribute was added in vSphere API 6.7.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`State` instance.
            """
            Enum.__init__(string)

    State._set_values({
        'UP_TO_DATE': State('UP_TO_DATE'),
        'UPDATES_PENDING': State('UPDATES_PENDING'),
        'STAGE_IN_PROGRESS': State('STAGE_IN_PROGRESS'),
        'INSTALL_IN_PROGRESS': State('INSTALL_IN_PROGRESS'),
        'INSTALL_FAILED': State('INSTALL_FAILED'),
        'ROLLBACK_IN_PROGRESS': State('ROLLBACK_IN_PROGRESS'),
    })
    State._set_binding_type(type.EnumType(
        'com.vmware.appliance.update.state',
        State))


    class Info(VapiStruct):
        """
        The ``Update.Info`` class describes the state of the appliance update. This
        class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'state',
                {
                    'UP_TO_DATE' : [],
                    'UPDATES_PENDING' : [],
                    'STAGE_IN_PROGRESS' : [],
                    'INSTALL_IN_PROGRESS' : [],
                    'INSTALL_FAILED' : [],
                    'ROLLBACK_IN_PROGRESS' : [],
                }
            ),
        ]



        def __init__(self,
                     state=None,
                     task=None,
                     version=None,
                     latest_query_time=None,
                    ):
            """
            :type  state: :class:`Update.State`
            :param state: State of the appliance update. This attribute was added in vSphere
                API 6.7.
            :type  task: :class:`TaskInfo` or ``None``
            :param task: The running or completed update task. This attribute was added in
                vSphere API 6.7.
            :type  version: :class:`str`
            :param version: Version of base appliance if state is UP_TO_DATE Version of update
                being staged or installed if state is INSTALL_IN_PROGRESS or
                STAGE_IN_PROGRESS Version of update staged if state is
                UPDATES_PENDING Version of update failed if state is INSTALL_FAILED
                or ROLLBACK_IN_PROGRESS. This attribute was added in vSphere API
                6.7.
            :type  latest_query_time: :class:`datetime.datetime` or ``None``
            :param latest_query_time: Timestamp of latest query to update repository. This attribute was
                added in vSphere API 6.7.
                If None the update was never queried
            """
            self.state = state
            self.task = task
            self.version = version
            self.latest_query_time = latest_query_time
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.update.info', {
            'state': type.ReferenceType(__name__, 'Update.State'),
            'task': type.OptionalType(type.ReferenceType(__name__, 'TaskInfo')),
            'version': type.StringType(),
            'latest_query_time': type.OptionalType(type.DateTimeType()),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Gets the current status of the appliance update. This method was added
        in vSphere API 6.7.


        :rtype: :class:`Update.Info`
        :return: Info structure containing the status information about the
            appliance.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            session is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            session is not authorized to perform this operation
        """
        return self._invoke('get', None)

    def cancel(self):
        """
        Request the cancellation the update operation that is currently in
        progress. This method was added in vSphere API 6.7.


        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            Current task is not cancellable
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            session is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            session is not authorized to perform this operation
        """
        return self._invoke('cancel', None)
class _HealthStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for messages operation
        messages_input_type = type.StructType('operation-input', {
            'item': type.IdType(resource_types='com.vmware.appliance.health'),
        })
        messages_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        messages_input_value_validator_list = [
        ]
        messages_output_validator_list = [
        ]
        messages_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/health/{item}/messages',
            path_variables={
                'item': 'item',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'messages': {
                'input_type': messages_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Notification')),
                'errors': messages_error_dict,
                'input_value_validator_list': messages_input_value_validator_list,
                'output_validator_list': messages_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'messages': messages_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.health',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _HealthCheckSettingsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/health/settings',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'health_settings': type.ReferenceType(__name__, 'HealthCheckSettings.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/appliance/health/settings',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'HealthCheckSettings.SettingSpec'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.health_check_settings',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _LocalAccountsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'username': type.StringType(),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/local-accounts/{username}',
            path_variables={
                'username': 'username',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/local-accounts',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'username': type.IdType(resource_types='com.vmware.appliance.local_accounts'),
            'config': type.ReferenceType(__name__, 'LocalAccounts.Config'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/local-accounts/{username}',
            path_variables={
                'username': 'username',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'username': type.IdType(resource_types='com.vmware.appliance.local_accounts'),
            'config': type.ReferenceType(__name__, 'LocalAccounts.Config'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/appliance/local-accounts/{username}',
            path_variables={
                'username': 'username',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'username': type.IdType(resource_types='com.vmware.appliance.local_accounts'),
            'config': type.ReferenceType(__name__, 'LocalAccounts.UpdateConfig'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/appliance/local-accounts/{username}',
            path_variables={
                'username': 'username',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'username': type.IdType(resource_types='com.vmware.appliance.local_accounts'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/appliance/local-accounts/{username}',
            path_variables={
                'username': 'username',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'LocalAccounts.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.IdType()),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create': {
                'input_type': create_input_type,
                'output_type': type.VoidType(),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'set': set_rest_metadata,
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.local_accounts',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _MonitoringStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for query operation
        query_input_type = type.StructType('operation-input', {
            'item': type.ReferenceType(__name__, 'Monitoring.MonitoredItemDataRequest'),
        })
        query_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        query_input_value_validator_list = [
        ]
        query_output_validator_list = [
        ]
        query_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/monitoring/query',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/monitoring',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'stat_id': type.IdType(resource_types='com.vmware.appliance.monitoring'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/monitoring/{stat_id}',
            path_variables={
                'stat_id': 'stat_id',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'query': {
                'input_type': query_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Monitoring.MonitoredItemData')),
                'errors': query_error_dict,
                'input_value_validator_list': query_input_value_validator_list,
                'output_validator_list': query_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Monitoring.MonitoredItem')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Monitoring.MonitoredItem'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'query': query_rest_metadata,
            'list': list_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.monitoring',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _NetworkingStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/networking',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Networking.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/appliance/networking',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for reset operation
        reset_input_type = type.StructType('operation-input', {})
        reset_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        reset_input_value_validator_list = [
        ]
        reset_output_validator_list = [
        ]
        reset_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/networking?action=reset',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for change operation
        change_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Networking.ChangeSpec'),
        })
        change_error_dict = {
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        change_input_value_validator_list = [
        ]
        change_output_validator_list = [
        ]
        change_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/networking?action=change',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Networking.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'reset': {
                'input_type': reset_input_type,
                'output_type': type.VoidType(),
                'errors': reset_error_dict,
                'input_value_validator_list': reset_input_value_validator_list,
                'output_validator_list': reset_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'change$task': {
                'input_type': change_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': change_error_dict,
                'input_value_validator_list': change_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'update': update_rest_metadata,
            'reset': reset_rest_metadata,
            'change': change_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.networking',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _NtpStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for test operation
        test_input_type = type.StructType('operation-input', {
            'servers': type.ListType(type.StringType()),
        })
        test_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        test_input_value_validator_list = [
        ]
        test_output_validator_list = [
        ]
        test_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/ntp/test',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'servers': type.ListType(type.StringType()),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/appliance/ntp',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/ntp',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'test': {
                'input_type': test_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Ntp.TestRunStatus')),
                'errors': test_error_dict,
                'input_value_validator_list': test_input_value_validator_list,
                'output_validator_list': test_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ListType(type.StringType()),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'test': test_rest_metadata,
            'set': set_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.ntp',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _RecoveryStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/recovery',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Recovery.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.recovery',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ServicesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for start operation
        start_input_type = type.StructType('operation-input', {
            'service': type.IdType(resource_types='com.vmware.appliance.services'),
        })
        start_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.timed_out':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'TimedOut'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        start_input_value_validator_list = [
        ]
        start_output_validator_list = [
        ]
        start_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/services/{id}/start',
            path_variables={
                'service': 'id',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for stop operation
        stop_input_type = type.StructType('operation-input', {
            'service': type.IdType(resource_types='com.vmware.appliance.services'),
        })
        stop_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        stop_input_value_validator_list = [
        ]
        stop_output_validator_list = [
        ]
        stop_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/services/{id}/stop',
            path_variables={
                'service': 'id',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for restart operation
        restart_input_type = type.StructType('operation-input', {
            'service': type.IdType(resource_types='com.vmware.appliance.services'),
        })
        restart_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.timed_out':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'TimedOut'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        restart_input_value_validator_list = [
        ]
        restart_output_validator_list = [
        ]
        restart_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/services/{id}/restart',
            path_variables={
                'service': 'id',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'service': type.IdType(resource_types='com.vmware.appliance.services'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/services/{id}',
            path_variables={
                'service': 'id',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/services',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'start': {
                'input_type': start_input_type,
                'output_type': type.VoidType(),
                'errors': start_error_dict,
                'input_value_validator_list': start_input_value_validator_list,
                'output_validator_list': start_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'stop': {
                'input_type': stop_input_type,
                'output_type': type.VoidType(),
                'errors': stop_error_dict,
                'input_value_validator_list': stop_input_value_validator_list,
                'output_validator_list': stop_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'restart': {
                'input_type': restart_input_type,
                'output_type': type.VoidType(),
                'errors': restart_error_dict,
                'input_value_validator_list': restart_input_value_validator_list,
                'output_validator_list': restart_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Services.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Services.Info')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'start': start_rest_metadata,
            'stop': stop_rest_metadata,
            'restart': restart_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.services',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ShutdownStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for cancel operation
        cancel_input_type = type.StructType('operation-input', {})
        cancel_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        cancel_input_value_validator_list = [
        ]
        cancel_output_validator_list = [
        ]
        cancel_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/shutdown/cancel',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for poweroff operation
        poweroff_input_type = type.StructType('operation-input', {
            'delay': type.IntegerType(),
            'reason': type.StringType(),
        })
        poweroff_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        poweroff_input_value_validator_list = [
        ]
        poweroff_output_validator_list = [
        ]
        poweroff_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/shutdown/poweroff',
            path_variables={
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for reboot operation
        reboot_input_type = type.StructType('operation-input', {
            'delay': type.IntegerType(),
            'reason': type.StringType(),
        })
        reboot_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        reboot_input_value_validator_list = [
        ]
        reboot_output_validator_list = [
        ]
        reboot_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/shutdown/reboot',
            path_variables={
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/shutdown',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'cancel': {
                'input_type': cancel_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_error_dict,
                'input_value_validator_list': cancel_input_value_validator_list,
                'output_validator_list': cancel_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'poweroff': {
                'input_type': poweroff_input_type,
                'output_type': type.VoidType(),
                'errors': poweroff_error_dict,
                'input_value_validator_list': poweroff_input_value_validator_list,
                'output_validator_list': poweroff_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'reboot': {
                'input_type': reboot_input_type,
                'output_type': type.VoidType(),
                'errors': reboot_error_dict,
                'input_value_validator_list': reboot_input_value_validator_list,
                'output_validator_list': reboot_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Shutdown.ShutdownConfig'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'cancel': cancel_rest_metadata,
            'poweroff': poweroff_rest_metadata,
            'reboot': reboot_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.shutdown',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _CoresStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/support-bundle/cores',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Cores.Info')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.cores',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SupportBundleStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'iteration': type.OptionalType(type.ReferenceType(__name__, 'SupportBundle.IterationSpec')),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'SupportBundle.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/support-bundle',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'SupportBundle.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/support-bundle',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'id': type.IdType(resource_types='com.vmware.appliance.supportbundle'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/appliance/support-bundle/{id}',
            path_variables={
                'id': 'id',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'SupportBundle.ListResult'),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.support_bundle',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _TimesyncStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'mode': type.ReferenceType(__name__, 'Timesync.TimeSyncMode'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/appliance/timesync',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/timesync',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Timesync.TimeSyncMode'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'set': set_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.timesync',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _UpdateStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/update',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for cancel operation
        cancel_input_type = type.StructType('operation-input', {})
        cancel_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        cancel_input_value_validator_list = [
        ]
        cancel_output_validator_list = [
        ]
        cancel_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/update?action=cancel',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Update.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel': {
                'input_type': cancel_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_error_dict,
                'input_value_validator_list': cancel_input_value_validator_list,
                'output_validator_list': cancel_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'cancel': cancel_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.update',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Health': Health,
        'HealthCheckSettings': HealthCheckSettings,
        'LocalAccounts': LocalAccounts,
        'Monitoring': Monitoring,
        'Networking': Networking,
        'Ntp': Ntp,
        'Recovery': Recovery,
        'Services': Services,
        'Shutdown': Shutdown,
        'Cores': Cores,
        'SupportBundle': SupportBundle,
        'Timesync': Timesync,
        'Update': Update,
        'access': 'com.vmware.appliance.access_client.StubFactory',
        'health': 'com.vmware.appliance.health_client.StubFactory',
        'local_accounts': 'com.vmware.appliance.local_accounts_client.StubFactory',
        'localaccounts': 'com.vmware.appliance.localaccounts_client.StubFactory',
        'logging': 'com.vmware.appliance.logging_client.StubFactory',
        'monitoring': 'com.vmware.appliance.monitoring_client.StubFactory',
        'networking': 'com.vmware.appliance.networking_client.StubFactory',
        'ntp': 'com.vmware.appliance.ntp_client.StubFactory',
        'shutdown': 'com.vmware.appliance.shutdown_client.StubFactory',
        'support_bundle': 'com.vmware.appliance.support_bundle_client.StubFactory',
        'supportbundle': 'com.vmware.appliance.supportbundle_client.StubFactory',
        'system': 'com.vmware.appliance.system_client.StubFactory',
        'tls': 'com.vmware.appliance.tls_client.StubFactory',
        'update': 'com.vmware.appliance.update_client.StubFactory',
    }

