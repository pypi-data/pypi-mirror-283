# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.kms.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.trusted_infrastructure.kms_client`` module provides
classes for configuring Key Provider Services for Trusted vCenter.

"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

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


class Services(VapiInterface):
    """
    The ``Services`` class contains information about the registered instances
    of the Key Provider Service in vCenter. This class was added in vSphere API
    7.0.0.0.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.trusted_infrastructure.kms.Service"
    """
    The resource type for the Key Provider Service instance. This class attribute
    was added in vSphere API 7.0.0.0.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.kms.services'
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

    class Summary(VapiStruct):
        """
        The ``Services.Summary`` class contains basic information about a
        registered Key Provider Service instance. This class was added in vSphere
        API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     service=None,
                     address=None,
                     group=None,
                     trust_authority_cluster=None,
                    ):
            """
            :type  service: :class:`str`
            :param service: The service's unique identifier. This attribute was added in
                vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.kms.Service``. When
                methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.kms.Service``.
            :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
            :param address: The service's address. This attribute was added in vSphere API
                7.0.0.0.
            :type  group: :class:`str`
            :param group: The group determines the Attestation Service instances this Key
                Provider Service can accept reports from. This attribute was added
                in vSphere API 7.0.0.0.
            :type  trust_authority_cluster: :class:`str`
            :param trust_authority_cluster: The cluster specifies the Trust Authority Cluster this Key Provider
                service belongs to. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.service = service
            self.address = address
            self.group = group
            self.trust_authority_cluster = trust_authority_cluster
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.kms.services.summary', {
            'service': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.kms.Service'),
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
            'group': type.StringType(),
            'trust_authority_cluster': type.StringType(),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Services.Info`` class contains all the stored information about a
        registered Key Provider Service instance. This class was added in vSphere
        API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'trusted_CA': 'trusted_ca',
                                }

        def __init__(self,
                     address=None,
                     trusted_ca=None,
                     group=None,
                     trust_authority_cluster=None,
                    ):
            """
            :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
            :param address: The service's address. This attribute was added in vSphere API
                7.0.0.0.
            :type  trusted_ca: :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain`
            :param trusted_ca: The service's TLS certificate chain. This attribute was added in
                vSphere API 7.0.0.0.
            :type  group: :class:`str`
            :param group: The group determines the Attestation Service instances this Key
                Provider Service can accept reports from. This attribute was added
                in vSphere API 7.0.0.0.
            :type  trust_authority_cluster: :class:`str`
            :param trust_authority_cluster: The cluster specifies the Trust Authority Cluster this Key Provider
                Service belongs to. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.address = address
            self.trusted_ca = trusted_ca
            self.group = group
            self.trust_authority_cluster = trust_authority_cluster
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.kms.services.info', {
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
            'trusted_CA': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain'),
            'group': type.StringType(),
            'trust_authority_cluster': type.StringType(),
        },
        Info,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Services.CreateSpec`` class contains the data necessary for
        registering a Key Provider Service instance to the environment. This class
        was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'trusted_CA': 'trusted_ca',
                                }

        def __init__(self,
                     address=None,
                     trusted_ca=None,
                     group=None,
                     trust_authority_cluster=None,
                    ):
            """
            :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
            :param address: The service's address. This attribute was added in vSphere API
                7.0.0.0.
            :type  trusted_ca: :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain`
            :param trusted_ca: The service's TLS certificate chain. This attribute was added in
                vSphere API 7.0.0.0.
            :type  group: :class:`str`
            :param group: The group determines the Attestation Service instances this Key
                Provider service can accept reports from. This attribute was added
                in vSphere API 7.0.0.0.
            :type  trust_authority_cluster: :class:`str`
            :param trust_authority_cluster: The cluster specifies the Trust Authority Cluster this Key Provider
                Service belongs to. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.address = address
            self.trusted_ca = trusted_ca
            self.group = group
            self.trust_authority_cluster = trust_authority_cluster
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.kms.services.create_spec', {
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
            'trusted_CA': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain'),
            'group': type.StringType(),
            'trust_authority_cluster': type.StringType(),
        },
        CreateSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Services.FilterSpec`` class contains the data necessary for
        identifying a Key Provider Service instance. This class was added in
        vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     services=None,
                     address=None,
                     group=None,
                     trust_authority_cluster=None,
                    ):
            """
            :type  services: :class:`set` of :class:`str` or ``None``
            :param services: A set of IDs by which to filter the services. This attribute was
                added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.kms.Service``. When
                methods return a value of this class as a return value, the
                attribute will contain identifiers for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.kms.Service``.
                If None, the services will not be filtered by ID.
            :type  address: :class:`list` of :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress` or ``None``
            :param address: A set of address by which to filter. This attribute was added in
                vSphere API 7.0.0.0.
                If None, the services will not be filtered by address.
            :type  group: :class:`set` of :class:`str` or ``None``
            :param group: The group determines the Attestation Service instances this Key
                Provider Service can accept reports from. This attribute was added
                in vSphere API 7.0.0.0.
                If None, the Services will not be filtered by group.
            :type  trust_authority_cluster: :class:`set` of :class:`str` or ``None``
            :param trust_authority_cluster: The cluster specifies the Trust Authority Cluster this Key Provider
                Service belongs to. This attribute was added in vSphere API
                7.0.0.0.
                If None, the Services will not be filtered by
                trustAuthorityCluster.
            """
            self.services = services
            self.address = address
            self.group = group
            self.trust_authority_cluster = trust_authority_cluster
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.kms.services.filter_spec', {
            'services': type.OptionalType(type.SetType(type.IdType())),
            'address': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'))),
            'group': type.OptionalType(type.SetType(type.StringType())),
            'trust_authority_cluster': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             spec=None,
             ):
        """
        Returns basic information about all registered Key Provider Service
        instances in this vCenter. This method was added in vSphere API
        7.0.0.0.

        :type  spec: :class:`Services.FilterSpec` or ``None``
        :param spec: Return only services matching the specified filters.
            If None return all services.
        :rtype: :class:`list` of :class:`Services.Summary`
        :return: Basic information about all registered Key Provider Service
            instances in this vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while getting the data.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ReadTrustedHosts``.
        """
        return self._invoke('list',
                            {
                            'spec': spec,
                            })

    def get(self,
            service,
            ):
        """
        Returns the detailed information about a registered Key Provider
        Service instance in this vCenter. This method was added in vSphere API
        7.0.0.0.

        :type  service: :class:`str`
        :param service: the Key Provider Service instance unique identifier.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.kms.Service``.
        :rtype: :class:`Services.Info`
        :return: Detailed information about the specified Key Provider Service
            instance.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while getting the data.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no Key Provider Service instance with the specified ID.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ReadTrustedHosts``.
        """
        return self._invoke('get',
                            {
                            'service': service,
                            })

    def create(self,
               spec,
               ):
        """
        Registers a Key Provider Service instance in this vCenter. This method
        was added in vSphere API 7.0.0.0.

        :type  spec: :class:`Services.CreateSpec`
        :param spec: The CreateSpec for the new service.
        :rtype: :class:`str`
        :return: ID of the newly registered Key Provider Service instance.
            The return value will be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.kms.Service``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if there is already a Key Provider Service instance with the same
            Address.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the CreateSpec contains invalid data.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ManageTrustedHosts``.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def delete(self,
               service,
               ):
        """
        Removes a currently registered Key Provider Service instance from this
        vCenter. This method was added in vSphere API 7.0.0.0.

        :type  service: :class:`str`
        :param service: the Key Provider Service instance unique identifier.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.kms.Service``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while deleting the service.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the Key Provider Service instance is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the Key Provider Service instance is used by a configuration on
            a cluster level.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ManageTrustedHosts``.
        """
        return self._invoke('delete',
                            {
                            'service': service,
                            })
class _ServicesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'spec': type.OptionalType(type.ReferenceType(__name__, 'Services.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/trusted-infrastructure/kms/services',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'query',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'service': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.kms.Service'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/vcenter/trusted-infrastructure/kms/services/{service}',
            path_variables={
                'service': 'service',
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
            'spec': type.ReferenceType(__name__, 'Services.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/trusted-infrastructure/kms/services',
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
            'service': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.kms.Service'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/vcenter/trusted-infrastructure/kms/services/{service}',
            path_variables={
                'service': 'service',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'Services.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
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
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.kms.Service'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
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
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.kms.services',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Services': Services,
    }

