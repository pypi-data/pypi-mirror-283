# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.trusted_clusters.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.trusted_infrastructure.trusted_clusters_client``
module provides classes for configuring Trusted Clusters.

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


class ServicesAppliedConfig(VapiInterface):
    """
    The ``ServicesAppliedConfig`` class provides information about the
    aggregate health of the applied Trust Authority Component configurations on
    the Trusted Clusters. The desired state of the Trust Authority Component
    configurations is stored within vCenter, while the applied configuration is
    stored on the hosts in the cluster and is a copy of the desired state. The
    ``ServicesAppliedConfig`` class is available for all clusters, not only
    Trusted Clusters. When an applied Trust Authority Component configuration
    is found outside of a Trusted Cluster it is considered an
    :attr:`ServicesAppliedConfig.Health.ERROR`. The ``ServicesAppliedConfig``
    class is able to make the applied Trust Authority Component configuration
    consistent with the desired state when individual host configurations have
    diverged from the desired state. This class was added in vSphere API
    7.0.1.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.services_applied_config'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ServicesAppliedConfigStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})

    class Health(Enum):
        """
        The ``ServicesAppliedConfig.Health`` class is an indicator for the
        consistency of all applied Trust Authority Component configurations in a
        cluster with respect to the desired state. This enumeration was added in
        vSphere API 7.0.1.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        NONE = None
        """
        The consistency of some applied configurations is unknown. This class
        attribute was added in vSphere API 7.0.1.0.

        """
        OK = None
        """
        All the applied Trust Authority Component configurations are consistent
        with the desired state. This class attribute was added in vSphere API
        7.0.1.0.

        """
        ERROR = None
        """
        Some applied Trust Authority Component configurations have diverged from
        the desired state. This class attribute was added in vSphere API 7.0.1.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Health` instance.
            """
            Enum.__init__(string)

    Health._set_values({
        'NONE': Health('NONE'),
        'OK': Health('OK'),
        'ERROR': Health('ERROR'),
    })
    Health._set_binding_type(type.EnumType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.services_applied_config.health',
        Health))


    class Info(VapiStruct):
        """
        The ``ServicesAppliedConfig.Info`` class contains detailed information
        about the health of the applied Trust Authority Component configurations in
        a cluster. This class was added in vSphere API 7.0.1.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     health=None,
                     details=None,
                    ):
            """
            :type  health: :class:`ServicesAppliedConfig.Health`
            :param health: The health value which indicates whether the configuration applied
                to the cluster differs from the desired state. This attribute was
                added in vSphere API 7.0.1.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health. When the
                ``ServicesAppliedConfig.Health`` is not
                :attr:`ServicesAppliedConfig.Health.OK`, this member will provide a
                detailed description of the issues present. This attribute was
                added in vSphere API 7.0.1.0.
            """
            self.health = health
            self.details = details
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.services_applied_config.info', {
            'health': type.ReferenceType(__name__, 'ServicesAppliedConfig.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Info,
        False,
        None))




    def get_task(self,
            cluster,
            ):
        """
        Returns detailed information about the health of the applied Trust
        Authority Component configurations in the given cluster. This method
        was added in vSphere API 7.0.1.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster against which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster ID is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no cluster corresponding to the given ID is found within this
            vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if there are ongoing mutating operations.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'ServicesAppliedConfig.Info'))
        return task_instance


    def update_task(self,
               cluster,
               ):
        """
        Update all applied Trust Authority Component configuration on the given
        cluster to be consistent with the desired state. This method has no
        affect on the desired state, apart from it being used as a reference
        point for the remediation. If the cluster is not a Trusted Cluster, the
        method will remove all Trust Authority Component configuration from the
        Trusted Hosts in the cluster, if such hosts are found. This method was
        added in vSphere API 7.0.1.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster against which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster ID is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no cluster corresponding to the given ID is found within this
            vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if there are ongoing mutating operations.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('update$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def delete_task(self,
               cluster,
               ):
        """
        Delete all Trust Authority Components configuration that has been
        applied to the given cluster. This method has no affect on the desired
        state, it only removes applied Trust Authority Component configurations
        from any Trusted Hosts within the given cluster. This method was added
        in vSphere API 7.0.1.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster against which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster ID is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no cluster corresponding to the given ID is found within this
            vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if there are ongoing mutating operations.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class _ServicesAppliedConfigStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/services-applied-config',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/services-applied-config',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/services-applied-config',
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
            'get$task': {
                'input_type': get_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'delete$task': {
                'input_type': delete_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trusted_clusters.services_applied_config',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ServicesAppliedConfig': ServicesAppliedConfig,
        'attestation': 'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation_client.StubFactory',
        'kms': 'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.kms_client.StubFactory',
    }

