# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.clusters.enablement.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.clusters.enablement_client`` module provides
classes to manage enablement of the feature that allows to collectively manage
hosts within the cluster with a single software specification.

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


class Configuration(VapiInterface):
    """
    The ``Configuration`` class provides methods to control whether the cluster
    is managed using desired configuration platform semantics. This class was
    added in vSphere API 8.0.1.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.enablement.configuration'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ConfigurationStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Configuration.Info`` class contains information describing whether
        the feature is enabled. This class was added in vSphere API 8.0.1.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     enabled=None,
                    ):
            """
            :type  enabled: :class:`bool`
            :param enabled: Status of the feature enablement True if feature is enabled, false
                otherwise. This attribute was added in vSphere API 8.0.1.0.
            """
            self.enabled = enabled
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.enablement.configuration.info', {
            'enabled': type.BooleanType(),
        },
        Info,
        False,
        None))



    def get(self,
            cluster,
            ):
        """
        Returns whether the given cluster is managed using a desired
        configuration plaftorm. This method was added in vSphere API 8.0.1.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:`Configuration.Info`
        :return: Information about the feature enablement.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.ClusterConfiguration.View``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires
              ``VcIntegrity.ClusterConfiguration.View``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            })
class Software(VapiInterface):
    """
    The ``Software`` class provides methods to control whether the cluster is
    managed with a single software specification.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.enablement.software'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SoftwareStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'check_task': 'check$task'})
        self._VAPI_OPERATION_IDS.update({'enable_task': 'enable$task'})

    class CheckType(Enum):
        """
        The ``Software.CheckType`` class contains various checks to identify the
        possibility to enable the feature that manages the cluster with a single
        software specification.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        SOFTWARE = None
        """
        Perform host software check. This check is to report standalone VIBs (VIBs
        which are not part of any component) and the features on the given cluster
        that cannot coexist with the feature which manages the cluster with a
        single software specification.

        """
        VERSION = None
        """
        Perform host version check. This feature does not support hosts with
        version less than XYZ.

        """
        STATELESSNESS = None
        """
        Perform host statelessness check. This feature does not support stateless
        hosts.

        """
        VUM_REMEDIATION = None
        """
        Perform VUM active remediation check.

        """
        SOFTWARE_SPECIFICATION_EXISTENCE = None
        """
        Perform cluster's software specification existence check.

        """
        VSAN_WITNESS_ELIGIBILITY = None
        """
        Checks to verify if the cluster software specification can be used to
        manage any vSAN witness hosts in the cluster. This class attribute was
        added in vSphere API 7.0.2.1.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`CheckType` instance.
            """
            Enum.__init__(string)

    CheckType._set_values({
        'SOFTWARE': CheckType('SOFTWARE'),
        'VERSION': CheckType('VERSION'),
        'STATELESSNESS': CheckType('STATELESSNESS'),
        'VUM_REMEDIATION': CheckType('VUM_REMEDIATION'),
        'SOFTWARE_SPECIFICATION_EXISTENCE': CheckType('SOFTWARE_SPECIFICATION_EXISTENCE'),
        'VSAN_WITNESS_ELIGIBILITY': CheckType('VSAN_WITNESS_ELIGIBILITY'),
    })
    CheckType._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.clusters.enablement.software.check_type',
        CheckType))


    class Info(VapiStruct):
        """
        The ``Software.Info`` class contains information describing whether the
        feature is enabled.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     enabled=None,
                    ):
            """
            :type  enabled: :class:`bool`
            :param enabled: Status of the feature enablement True if feature is enabled, false
                otherwise
            """
            self.enabled = enabled
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.enablement.software.info', {
            'enabled': type.BooleanType(),
        },
        Info,
        False,
        None))


    class CheckSpec(VapiStruct):
        """
        The ``Software.CheckSpec`` class contains information describing what
        checks should be performed.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     checks_to_skip=None,
                    ):
            """
            :type  checks_to_skip: :class:`set` of :class:`Software.CheckType`
            :param checks_to_skip: Specifies the checks that should be skipped. If the :class:`set` is
                empty, all checks will be performed.
            """
            self.checks_to_skip = checks_to_skip
            VapiStruct.__init__(self)


    CheckSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.enablement.software.check_spec', {
            'checks_to_skip': type.SetType(type.ReferenceType(__name__, 'Software.CheckType')),
        },
        CheckSpec,
        False,
        None))


    class CheckResult(VapiStruct):
        """
        The ``Software.CheckResult`` class contains information that describes the
        results of the checks.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     notifications=None,
                    ):
            """
            :type  notifications: :class:`dict` of :class:`Software.CheckType` and :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications containing check results grouped by
                :class:`Software.CheckType` type.
            """
            self.notifications = notifications
            VapiStruct.__init__(self)


    CheckResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.enablement.software.check_result', {
            'notifications': type.MapType(type.ReferenceType(__name__, 'Software.CheckType'), type.ReferenceType('com.vmware.esx.settings_client', 'Notifications')),
        },
        CheckResult,
        False,
        None))


    class EnableSpec(VapiStruct):
        """
        The ``Software.EnableSpec`` class contains information describing checks
        that should be skipped during enablement. Currently only
        :attr:`Software.CheckType.SOFTWARE` check can be skipped.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     skip_software_check=None,
                    ):
            """
            :type  skip_software_check: :class:`bool`
            :param skip_software_check: Skip :attr:`Software.CheckType.SOFTWARE` check during feature
                enablement.
            """
            self.skip_software_check = skip_software_check
            VapiStruct.__init__(self)


    EnableSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.enablement.software.enable_spec', {
            'skip_software_check': type.BooleanType(),
        },
        EnableSpec,
        False,
        None))



    def get(self,
            cluster,
            ):
        """
        Returns whether the given cluster is managed with a single software
        specification.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:`Software.Info`
        :return: Information about the feature enablement.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.lifecycleSettings.Read``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires
              ``VcIntegrity.lifecycleSettings.Read``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            })


    def check_task(self,
              cluster,
              spec=None,
              ):
        """
        Checks the possibility to manage the cluster with a single software
        specification.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`Software.CheckSpec` or ``None``
        :param spec: Check specification.
            If None, all checks are performed.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown error. The accompanying error message will
            give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the feature is already enabled for the given cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        """
        task_id = self._invoke('check$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Software.CheckResult'))
        return task_instance


    def enable_task(self,
               cluster,
               spec=None,
               ):
        """
        Enables the feature which manages the cluster with a single software
        specification.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`Software.EnableSpec` or ``None``
        :param spec: Enablement specification.
            If None, all checks are performed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If feature enablement failed for the given cluster. The value of
            the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` will be a class
            that contains all the attributes defined in
            :class:`Software.CheckResult`.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the feature is already enabled for the given cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        """
        task_id = self._invoke('enable$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class _ConfigurationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/clusters/{cluster}/enablement/configuration',
            path_variables={
                'cluster': 'cluster',
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
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Configuration.Info'),
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
            self, iface_name='com.vmware.esx.settings.clusters.enablement.configuration',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SoftwareStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/clusters/{cluster}/enablement/software',
            path_variables={
                'cluster': 'cluster',
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

        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'Software.CheckSpec')),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/clusters/{cluster}/enablement/software',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'check',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for enable operation
        enable_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'Software.EnableSpec')),
        })
        enable_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        enable_input_value_validator_list = [
        ]
        enable_output_validator_list = [
        ]
        enable_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/esx/settings/clusters/{cluster}/enablement/software',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
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
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Software.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check$task': {
                'input_type': check_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': check_error_dict,
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'enable$task': {
                'input_type': enable_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': enable_error_dict,
                'input_value_validator_list': enable_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'check': check_rest_metadata,
            'enable': enable_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.clusters.enablement.software',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Configuration': Configuration,
        'Software': Software,
        'configuration': 'com.vmware.esx.settings.clusters.enablement.configuration_client.StubFactory',
    }

