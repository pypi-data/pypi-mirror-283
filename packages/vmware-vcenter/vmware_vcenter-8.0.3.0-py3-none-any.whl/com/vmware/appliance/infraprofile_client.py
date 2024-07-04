# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.infraprofile.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.infraprofile_client`` module provides classes to
manage profile spec for the appliance

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
    The ``Notification`` class contains attributes to describe any
    info/warning/error messages that Tasks can raise.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 notification=None,
                 time=None,
                 message=None,
                 resolution=None,
                ):
        """
        :type  notification: :class:`str`
        :param notification: The notification id.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.infraprofile.notification``. When methods return a
            value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.infraprofile.notification``.
        :type  time: :class:`datetime.datetime` or ``None``
        :param time: The time the notification was raised/found.
            Only :class:`set` if the time information is available.
        :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param message: The notification message.
        :type  resolution: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
        :param resolution: The resolution message, if any.
            Only :class:`set` for warnings and errors.
        """
        self.notification = notification
        self.time = time
        self.message = message
        self.resolution = resolution
        VapiStruct.__init__(self)


Notification._set_binding_type(type.StructType(
    'com.vmware.appliance.infraprofile.notification', {
        'notification': type.IdType(resource_types='com.vmware.infraprofile.notification'),
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
    be reported be the task.

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
        :param info: Info notification messages reported.
            Only :class:`set` if an info was reported by the task.
        :type  warnings: :class:`list` of :class:`Notification` or ``None``
        :param warnings: Warning notification messages reported.
            Only :class:`set` if an warning was reported by the task.
        :type  errors: :class:`list` of :class:`Notification` or ``None``
        :param errors: Error notification messages reported.
            Only :class:`set` if an error was reported by the task.
        """
        self.info = info
        self.warnings = warnings
        self.errors = errors
        VapiStruct.__init__(self)


Notifications._set_binding_type(type.StructType(
    'com.vmware.appliance.infraprofile.notifications', {
        'info': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'warnings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
    },
    Notifications,
    False,
    None))



class TaskInfo(VapiStruct):
    """
    The ``TaskInfo`` class contains information about a task.

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
                 notifications=None,
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
        :param progress: Progress of the operation.
            This attribute is optional and it is only relevant when the value
            of ``status`` is one of
            :attr:`com.vmware.cis.task_client.Status.RUNNING`,
            :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
            :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
            :attr:`com.vmware.cis.task_client.Status.FAILED`.
        :type  notifications: :class:`Notifications` or ``None``
        :param notifications: Notifications to the user
            Only :class:`set` if the notifications were reported by this
            particular task.
        :type  result: :class:`DataValue` or ``None``
        :param result: Task result.
            This attribute will be None if the task has no result.
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
        self.notifications = notifications
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


TaskInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.infraprofile.task_info', {
        'progress': type.OptionalType(type.ReferenceType('com.vmware.cis.task_client', 'Progress')),
        'notifications': type.OptionalType(type.ReferenceType(__name__, 'Notifications')),
        'result': type.OptionalType(type.OpaqueType()),
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



class Configs(VapiInterface):
    """
    ``Configs`` class provides methods to manage desired configuration
    specification of an appliance.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.infraprofile.configs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ConfigsStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'validate_task': 'validate$task'})
        self._VAPI_OPERATION_IDS.update({'import_profile_task': 'import_profile$task'})

    class ValidationStatus(Enum):
        """
        The ``Configs.ValidationStatus`` class defines possible values of status of
        profile spec.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        VALID = None
        """
        Profile spec is valid.

        """
        INVALID = None
        """
        Profile spec is invalid.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ValidationStatus` instance.
            """
            Enum.__init__(string)

    ValidationStatus._set_values({
        'VALID': ValidationStatus('VALID'),
        'INVALID': ValidationStatus('INVALID'),
    })
    ValidationStatus._set_binding_type(type.EnumType(
        'com.vmware.appliance.infraprofile.configs.validation_status',
        ValidationStatus))


    class ProfileInfo(VapiStruct):
        """
        The ``Configs.ProfileInfo`` class defines the information about profile.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     info=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the profile which is also a profile identifier.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.infraprofile.profile``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.infraprofile.profile``.
            :type  info: :class:`str`
            :param info: Description of the profile.
            """
            self.name = name
            self.info = info
            VapiStruct.__init__(self)


    ProfileInfo._set_binding_type(type.StructType(
        'com.vmware.appliance.infraprofile.configs.profile_info', {
            'name': type.IdType(resource_types='com.vmware.infraprofile.profile'),
            'info': type.StringType(),
        },
        ProfileInfo,
        False,
        None))


    class ProfilesSpec(VapiStruct):
        """
        The ``Configs.ProfilesSpec`` class represents a spec information for export
        operation.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     encryption_key=None,
                     description=None,
                     profiles=None,
                    ):
            """
            :type  encryption_key: :class:`str` or ``None``
            :param encryption_key: Encryption Key to encrypt/decrypt profiles.
                If None encryption will not be used for the profile.
            :type  description: :class:`str` or ``None``
            :param description: Custom description provided by the user.
                If None description will be empty.
            :type  profiles: :class:`set` of :class:`str` or ``None``
            :param profiles: Profiles to be exported/imported.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.infraprofile.profile``. When methods return a value of
                this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.infraprofile.profile``.
                If None or empty, all profiles will be returned.
            """
            self.encryption_key = encryption_key
            self.description = description
            self.profiles = profiles
            VapiStruct.__init__(self)


    ProfilesSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.infraprofile.configs.profiles_spec', {
            'encryption_key': type.OptionalType(type.SecretType()),
            'description': type.OptionalType(type.StringType()),
            'profiles': type.OptionalType(type.SetType(type.IdType())),
        },
        ProfilesSpec,
        False,
        None))


    class ImportProfileSpec(VapiStruct):
        """
        The ``Configs.ImportProfileSpec`` class represents a spec information for
        import and validate.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     config_spec=None,
                     profile_spec=None,
                    ):
            """
            :type  config_spec: :class:`str`
            :param config_spec: The JSON string representing the desired config specification.
            :type  profile_spec: :class:`Configs.ProfilesSpec` or ``None``
            :param profile_spec: The profile specification, if any
                only :class:`set` if there is a profilespec avaliable for this
                import profilespec.
            """
            self.config_spec = config_spec
            self.profile_spec = profile_spec
            VapiStruct.__init__(self)


    ImportProfileSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.infraprofile.configs.import_profile_spec', {
            'config_spec': type.StringType(),
            'profile_spec': type.OptionalType(type.ReferenceType(__name__, 'Configs.ProfilesSpec')),
        },
        ImportProfileSpec,
        False,
        None))


    class ValidationResult(VapiStruct):
        """
        The ``Configs.ValidationResult`` class contains attributes to describe
        result of validation of profile specification.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     notifications=None,
                    ):
            """
            :type  status: :class:`Configs.ValidationStatus`
            :param status: Status of the Profile spec.
            :type  notifications: :class:`Notifications` or ``None``
            :param notifications: Notifications to the user
                Only :class:`set` if the notifications were reported by this
                particular validation.
            """
            self.status = status
            self.notifications = notifications
            VapiStruct.__init__(self)


    ValidationResult._set_binding_type(type.StructType(
        'com.vmware.appliance.infraprofile.configs.validation_result', {
            'status': type.ReferenceType(__name__, 'Configs.ValidationStatus'),
            'notifications': type.OptionalType(type.ReferenceType(__name__, 'Notifications')),
        },
        ValidationResult,
        False,
        None))



    def list(self):
        """
        List all the profiles which are registered.


        :rtype: :class:`list` of :class:`Configs.ProfileInfo`
        :return: List of profiles with description are registered.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Infraprofile.Read``.
        """
        return self._invoke('list', None)

    def export(self,
               spec=None,
               ):
        """
        Exports the desired profile specification.

        :type  spec: :class:`Configs.ProfilesSpec` or ``None``
        :param spec: 
            information to export the profile.
        :rtype: :class:`str`
        :return: Configuration specification JSON in string format.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no profile associated.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Infraprofile.Read``.
        """
        return self._invoke('export',
                            {
                            'spec': spec,
                            })


    def validate_task(self,
                 spec,
                 ):
        """
        Validates the desired profile specification.

        :type  spec: :class:`Configs.ImportProfileSpec`
        :param spec: information to validate the profile.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no profile associated.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        """
        task_id = self._invoke('validate$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Configs.ValidationResult'))
        return task_instance


    def import_profile_task(self,
                       spec,
                       ):
        """
        Imports the desired profile specification.

        :type  spec: :class:`Configs.ImportProfileSpec`
        :param spec: information to import the profile.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no profile associated.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If there is another operation in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        """
        task_id = self._invoke('import_profile$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.StringType())
        return task_instance
class _ConfigsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/infraprofile/configs',
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

        # properties for export operation
        export_input_type = type.StructType('operation-input', {
            'spec': type.OptionalType(type.ReferenceType(__name__, 'Configs.ProfilesSpec')),
        })
        export_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        export_input_value_validator_list = [
        ]
        export_output_validator_list = [
        ]
        export_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/infraprofile/configs',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'export',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for validate operation
        validate_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Configs.ImportProfileSpec'),
        })
        validate_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        validate_input_value_validator_list = [
        ]
        validate_output_validator_list = [
        ]
        validate_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/infraprofile/configs',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'validate',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for import_profile operation
        import_profile_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Configs.ImportProfileSpec'),
        })
        import_profile_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        import_profile_input_value_validator_list = [
        ]
        import_profile_output_validator_list = [
        ]
        import_profile_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/infraprofile/configs',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'import',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Configs.ProfileInfo')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'export': {
                'input_type': export_input_type,
                'output_type': type.StringType(),
                'errors': export_error_dict,
                'input_value_validator_list': export_input_value_validator_list,
                'output_validator_list': export_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'validate$task': {
                'input_type': validate_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': validate_error_dict,
                'input_value_validator_list': validate_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'import_profile$task': {
                'input_type': import_profile_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': import_profile_error_dict,
                'input_value_validator_list': import_profile_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'export': export_rest_metadata,
            'validate': validate_rest_metadata,
            'import_profile': import_profile_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.infraprofile.configs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Configs': Configs,
    }

