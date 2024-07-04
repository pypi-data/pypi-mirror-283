# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters_client``
module provides the Trust Authority Components.

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


class ConsumerPrincipals(VapiInterface):
    """
    The ``ConsumerPrincipals`` class configures the token policies and STS
    trust necessary for the workload vCenter to query the trusted services for
    their status. This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.consumer_principals'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ConsumerPrincipalsStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})
        self._VAPI_OPERATION_IDS.update({'list_task': 'list$task'})

    class Health(Enum):
        """
        The ``ConsumerPrincipals.Health`` class defines the possible health states.
        This enumeration was added in vSphere API 7.0.0.0.

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
        None. No status available. This class attribute was added in vSphere API
        7.0.0.0.

        """
        OK = None
        """
        OK. Health is normal. This class attribute was added in vSphere API
        7.0.0.0.

        """
        WARNING = None
        """
        Warning. Health is normal, however there is an issue that requires
        attention. This class attribute was added in vSphere API 7.0.0.0.

        """
        ERROR = None
        """
        Error. Not healthy. This class attribute was added in vSphere API 7.0.0.0.

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
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.consumer_principals.health',
        Health))


    class CreateSpec(VapiStruct):
        """
        The ``ConsumerPrincipals.CreateSpec`` class contains the information
        necessary to establish trust between a workload vCenter and a Trust
        Authority Host. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     certificates=None,
                     issuer_alias=None,
                     issuer=None,
                     principal=None,
                    ):
            """
            :type  certificates: :class:`list` of :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain`
            :param certificates: The certificates used by the vCenter STS to sign tokens. This
                attribute was added in vSphere API 7.0.0.0.
            :type  issuer_alias: :class:`str`
            :param issuer_alias: A user-friendly alias of the service which created and signed the
                security token. This attribute was added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.authentication.trust.security-token-issuer``. When
                methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.esx.authentication.trust.security-token-issuer``.
            :type  issuer: :class:`str`
            :param issuer: The service which created and signed the security token. This
                attribute was added in vSphere API 7.0.0.0.
            :type  principal: :class:`com.vmware.vcenter.trusted_infrastructure_client.StsPrincipal`
            :param principal: The principal used by the vCenter to retrieve tokens. This
                attribute was added in vSphere API 7.0.0.0.
            """
            self.certificates = certificates
            self.issuer_alias = issuer_alias
            self.issuer = issuer
            self.principal = principal
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.consumer_principals.create_spec', {
            'certificates': type.ListType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain')),
            'issuer_alias': type.IdType(resource_types='com.vmware.esx.authentication.trust.security-token-issuer'),
            'issuer': type.StringType(),
            'principal': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'StsPrincipal'),
        },
        CreateSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``ConsumerPrincipals.FilterSpec`` class contains data which identifies
        a connection profile on the trusted vCenter. This class was added in
        vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     principals=None,
                     issuer=None,
                    ):
            """
            :type  id: :class:`set` of :class:`str` or ``None``
            :param id: The unqiue identifier of a connection profile. This attribute was
                added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.authentication.clientprofile``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.esx.authentication.clientprofile``.
                If None, no filtration will be performed by ID.
            :type  principals: :class:`list` of :class:`com.vmware.vcenter.trusted_infrastructure_client.StsPrincipal` or ``None``
            :param principals: The principal used by the vCenter to retrieve tokens. This
                attribute was added in vSphere API 7.0.0.0.
                If None, no filtration will be performed by principals.
            :type  issuer: :class:`set` of :class:`str` or ``None``
            :param issuer: The service which created and signed the security token. This
                attribute was added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.authentication.trust.security-token-issuer``. When
                methods return a value of this class as a return value, the
                attribute will contain identifiers for the resource type:
                ``com.vmware.esx.authentication.trust.security-token-issuer``.
                If None, no filtration will be performed by issuer.
            """
            self.id = id
            self.principals = principals
            self.issuer = issuer
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.consumer_principals.filter_spec', {
            'id': type.OptionalType(type.SetType(type.IdType())),
            'principals': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'StsPrincipal'))),
            'issuer': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``ConsumerPrincipals.Info`` class contains the information necessary to
        establish trust between a workload vCenter and a Trust Authority Host. This
        class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     principal=None,
                     issuer_alias=None,
                     issuer=None,
                     certificates=None,
                     health=None,
                     message=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: The unqiue identifier of a connection profile. This attribute was
                added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.authentication.clientprofile``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.authentication.clientprofile``.
            :type  principal: :class:`com.vmware.vcenter.trusted_infrastructure_client.StsPrincipal`
            :param principal: The principal used by the vCenter to retrieve tokens. Currently
                this is the vCenter solution user. This attribute was added in
                vSphere API 7.0.0.0.
            :type  issuer_alias: :class:`str`
            :param issuer_alias: A user-friendly alias of the service which created and signed the
                security token. This attribute was added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.authentication.trust.security-token-issuer``. When
                methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.esx.authentication.trust.security-token-issuer``.
            :type  issuer: :class:`str`
            :param issuer: The service which created and signed the security token. This
                attribute was added in vSphere API 7.0.0.0.
            :type  certificates: :class:`list` of :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain`
            :param certificates: The certificates used by the vCenter STS to sign tokens. This
                attribute was added in vSphere API 7.0.0.0.
            :type  health: :class:`ConsumerPrincipals.Health`
            :param health: The consistency of the profile across the hosts in the cluster.
                This attribute was added in vSphere API 7.0.0.0.
            :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
            :param message: A localizable message describing the health of the profile. This
                attribute was added in vSphere API 7.0.0.0.
                If None, the certificates won't be updated.
            """
            self.id = id
            self.principal = principal
            self.issuer_alias = issuer_alias
            self.issuer = issuer
            self.certificates = certificates
            self.health = health
            self.message = message
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.consumer_principals.info', {
            'id': type.IdType(resource_types='com.vmware.esx.authentication.clientprofile'),
            'principal': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'StsPrincipal'),
            'issuer_alias': type.IdType(resource_types='com.vmware.esx.authentication.trust.security-token-issuer'),
            'issuer': type.StringType(),
            'certificates': type.ListType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain')),
            'health': type.ReferenceType(__name__, 'ConsumerPrincipals.Health'),
            'message': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Info,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``ConsumerPrincipals.Summary`` class contains a summary of the
        information necessary to establish trust between a workload vCenter and a
        Trust Authority Host. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     principal=None,
                     issuer_alias=None,
                     issuer=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: The unqiue identifier of a connection profile. This attribute was
                added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.authentication.clientprofile``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.authentication.clientprofile``.
            :type  principal: :class:`com.vmware.vcenter.trusted_infrastructure_client.StsPrincipal`
            :param principal: The principal used by the vCenter to retrieve tokens. Currently
                this is the vCenter solution user. This attribute was added in
                vSphere API 7.0.0.0.
            :type  issuer_alias: :class:`str`
            :param issuer_alias: A user-friendly alias of the service which created and signed the
                security token. This attribute was added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.authentication.trust.security-token-issuer``. When
                methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.esx.authentication.trust.security-token-issuer``.
            :type  issuer: :class:`str`
            :param issuer: The service which created and signed the security token. This
                attribute was added in vSphere API 7.0.0.0.
            """
            self.id = id
            self.principal = principal
            self.issuer_alias = issuer_alias
            self.issuer = issuer
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.consumer_principals.summary', {
            'id': type.IdType(resource_types='com.vmware.esx.authentication.clientprofile'),
            'principal': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'StsPrincipal'),
            'issuer_alias': type.IdType(resource_types='com.vmware.esx.authentication.trust.security-token-issuer'),
            'issuer': type.StringType(),
        },
        Summary,
        False,
        None))




    def create_task(self,
               cluster,
               spec,
               ):
        """
        Creates a profile with the specified connection information on all
        hosts from a Trust Authority Cluster. This method was added in vSphere
        API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the Trust Authority Cluster to configure.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`ConsumerPrincipals.CreateSpec`
        :param spec: The CreateSpec specifying the connection information.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a profile for the issuer already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no such cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        task_id = self._invoke('create$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='com.vmware.esx.authentication.clientprofile'))
        return task_instance


    def delete_task(self,
               cluster,
               profile,
               ):
        """
        Removes the read-only policy configured on ESX for a specific
        principal. This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the Trust Authority Cluster to configure.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  profile: :class:`str`
        :param profile: The ID of the connection profile to modify.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.authentication.clientprofile``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no profile configured with that ID.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cluster': cluster,
                                'profile': profile,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def get_task(self,
            cluster,
            profile,
            ):
        """
        Retrieve information for a specific profile. This method was added in
        vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the Trust Authority Cluster on which the profile is
            configured.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  profile: :class:`str`
        :param profile: The ID of the profile.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.authentication.clientprofile``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no profile configured with that ID.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                'profile': profile,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'ConsumerPrincipals.Info'))
        return task_instance


    def list_task(self,
             cluster,
             spec=None,
             ):
        """
        Lists all policies configured on a specific cluster. This method was
        added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the Trust Authority Cluster on which the profile is
            configured.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`ConsumerPrincipals.FilterSpec` or ``None``
        :param spec: A FilterSpec specifying the profiles to be listed.
            If None return all policies.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no profile configured with that ID.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        task_id = self._invoke('list$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ListType(type.ReferenceType(__name__, 'ConsumerPrincipals.Summary')))
        return task_instance
class _ConsumerPrincipalsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'ConsumerPrincipals.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/consumer-principals',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'profile': type.IdType(resource_types='com.vmware.esx.authentication.clientprofile'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/consumer-principals/{profile}',
            path_variables={
                'cluster': 'cluster',
                'profile': 'profile',
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
            'profile': type.IdType(resource_types='com.vmware.esx.authentication.clientprofile'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/consumer-principals/{profile}',
            path_variables={
                'cluster': 'cluster',
                'profile': 'profile',
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

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'ConsumerPrincipals.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/consumer-principals',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
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

        operations = {
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
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
            'get$task': {
                'input_type': get_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'list$task': {
                'input_type': list_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.consumer_principals',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ConsumerPrincipals': ConsumerPrincipals,
        'attestation': 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation_client.StubFactory',
        'kms': 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms_client.StubFactory',
    }

