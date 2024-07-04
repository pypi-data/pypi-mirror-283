# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate_client``
module provides the interfaces for configuring the Client Certificate used by
the Key Provider Service to authenticate against the Key Servers.

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


class Csr(VapiInterface):
    """
    The ``Csr`` interface provides methods to create a certificate signing
    request(CSR). This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate.csr'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CsrStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})

    class Info(VapiStruct):
        """
        The ``Csr.Info`` class contains the certificate signing request. This class
        was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     csr=None,
                    ):
            """
            :type  csr: :class:`str`
            :param csr: Certificate signing request. This attribute was added in vSphere
                API 7.0.0.0.
            """
            self.csr = csr
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate.csr.info', {
            'csr': type.StringType(),
        },
        Info,
        False,
        None))




    def create_task(self,
               cluster,
               provider,
               ):
        """
        Generate a certificate signing request (CSR) for the client
        certificate. This overwrites any existing CSR. 
        
        The CSR will allow the certificate to be signed by a third party. Once
        the CSR is signed, certificate may be added as a client certificate. 
        
        Calling the API repeatedly will result in a generating a new CSR each
        time.. This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If cluster or provider id are empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the provider or cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        task_id = self._invoke('create$task',
                                {
                                'cluster': cluster,
                                'provider': provider,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Csr.Info'))
        return task_instance


    def get_task(self,
            cluster,
            provider,
            ):
        """
        Get existing certificate signing request (CSR) for the client
        certificate. 
        
        The CSR will allow the certificate to be signed by a third party. Once
        the CSR is signed, certificate may be added as a client certificate. 
        
        . This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If cluster or provider id are empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the provider or cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                'provider': provider,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Csr.Info'))
        return task_instance
class _CsrStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/client-certificate/csr',
            path_variables={
                'cluster': 'cluster',
                'provider': 'provider',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/client-certificate/csr',
            path_variables={
                'cluster': 'cluster',
                'provider': 'provider',
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
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
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
            'create': create_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate.csr',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Csr': Csr,
    }

