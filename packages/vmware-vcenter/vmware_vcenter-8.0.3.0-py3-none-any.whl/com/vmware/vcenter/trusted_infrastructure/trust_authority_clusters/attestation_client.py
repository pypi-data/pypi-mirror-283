# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation_client``
module provides classes for configuring the Attestation Service. It attests the
state of a remote infrastructure node.

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


class ServiceStatus(VapiInterface):
    """
    The ``ServiceStatus`` class provides methods to get the Attestation Service
    health status. This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.service_status'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ServiceStatusStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})

    class Health(Enum):
        """
        The ``ServiceStatus.Health`` class defines the possible service health
        states. This enumeration was added in vSphere API 7.0.0.0.

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
        No status available. This class attribute was added in vSphere API 7.0.0.0.

        """
        OK = None
        """
        Service is functioning normally. This class attribute was added in vSphere
        API 7.0.0.0.

        """
        WARNING = None
        """
        Service is functioning, however there is an issue that requires attention.
        This class attribute was added in vSphere API 7.0.0.0.

        """
        ERROR = None
        """
        Service is not functioning. This class attribute was added in vSphere API
        7.0.0.0.

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
        'WARNING': Health('WARNING'),
        'ERROR': Health('ERROR'),
    })
    Health._set_binding_type(type.EnumType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.service_status.health',
        Health))


    class Info(VapiStruct):
        """
        The ``ServiceStatus.Info`` class contains information that describes the
        status of the service. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     health=None,
                     details=None,
                    ):
            """
            :type  health: :class:`ServiceStatus.Health`
            :param health: The service health status. This attribute was added in vSphere API
                7.0.0.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health of the service. 
                
                When the service ``ServiceStatus.Health`` is not
                :attr:`ServiceStatus.Health.OK` or
                :attr:`ServiceStatus.Health.NONE`, this member will provide an
                actionable description of the issues present.. This attribute was
                added in vSphere API 7.0.0.0.
            """
            self.health = health
            self.details = details
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.service_status.info', {
            'health': type.ReferenceType(__name__, 'ServiceStatus.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Info,
        False,
        None))




    def get_task(self,
            cluster,
            ):
        """
        Return the Attestation service health in the given cluster. This method
        was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            For any other error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'ServiceStatus.Info'))
        return task_instance
class _ServiceStatusStub(ApiInterfaceStub):
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
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/service-status',
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
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.service_status',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ServiceStatus': ServiceStatus,
        'tpm2': 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2_client.StubFactory',
    }

