# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers_client``
module provides the classes for configuring the Key Providers of a Trust
Authority Cluster.

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


class ClientCertificate(VapiInterface):
    """
    The ``ClientCertificate`` interface provides methods to add and retrieve
    client certificate. This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ClientCertificateStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})

    class Info(VapiStruct):
        """
        The ``ClientCertificate.Info`` class contains the client certificate used
        by the hosts in a cluster for authenticating with the Provider. This class
        was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     certificate=None,
                    ):
            """
            :type  certificate: :class:`str`
            :param certificate: Public certificate. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.certificate = certificate
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate.info', {
            'certificate': type.StringType(),
        },
        Info,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``ClientCertificate.UpdateSpec`` class contains attributes that
        describe the client certificate update for a Key Provider. This class was
        added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     certificate=None,
                     private_key=None,
                    ):
            """
            :type  certificate: :class:`str`
            :param certificate: Public certificate used by every host in the cluster. This
                attribute was added in vSphere API 7.0.0.0.
            :type  private_key: :class:`str` or ``None``
            :param private_key: Private part of the certificate. This attribute was added in
                vSphere API 7.0.0.0.
                If None, the update request is for a public/private client
                certificate pair, not for a signed CSR.
            """
            self.certificate = certificate
            self.private_key = private_key
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate.update_spec', {
            'certificate': type.StringType(),
            'private_key': type.OptionalType(type.SecretType()),
        },
        UpdateSpec,
        False,
        None))




    def create_task(self,
               cluster,
               provider,
               ):
        """
        Generate a new self signed client certificate. Existing client
        certificate is overwritten. The key server will use this certificate to
        validate the client connection. This method was added in vSphere API
        7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If cluster or provider id are empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster or provider is not found.
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
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def get_task(self,
            cluster,
            provider,
            ):
        """
        Return the existing client certificate. This method was added in
        vSphere API 7.0.0.0.

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
            If the cluster or provider is not found.
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
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'ClientCertificate.Info'))
        return task_instance


    def update_task(self,
               cluster,
               provider,
               spec,
               ):
        """
        Update the client certificate. 
        
        The key server will use this certificate to validate the client
        connection. If a client certificate already exists, it will be
        replaced. 
        
        An optional private key can be specified if the certificate has already
        been provisioned.. This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :type  spec: :class:`ClientCertificate.UpdateSpec`
        :param spec: The update spec.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the certificate or private key is invalid or cluster/provider id
            are empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster or provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        task_id = self._invoke('update$task',
                                {
                                'cluster': cluster,
                                'provider': provider,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class Credential(VapiInterface):
    """
    The ``Credential`` interface provides methods to add a credential for
    external key management service(s). This class was added in vSphere API
    7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.credential'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CredentialStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'set_task': 'set$task'})



    def set_task(self,
            cluster,
            provider,
            credential,
            ):
        """
        Set the key server credential. This method was added in vSphere API
        7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :type  credential: :class:`str`
        :param credential: KMIP KMS password or AWS access key.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If cluster or provider id are empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the provider or cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        task_id = self._invoke('set$task',
                                {
                                'cluster': cluster,
                                'provider': provider,
                                'credential': credential,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class CurrentPeerCertificates(VapiInterface):
    """
    Retrieves the list of TLS certificates used by peer key servers. Those are
    meant for review. Following approval these certificates should be added as
    trusted certificates in the :class:`TrustedPeerCertificates` class. This
    class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.current_peer_certificates'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CurrentPeerCertificatesStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'list_task': 'list$task'})

    class Summary(VapiStruct):
        """
        The ``CurrentPeerCertificates.Summary`` class contains a summary of the
        current key server certificates. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     server_name=None,
                     certificate=None,
                     error_messages=None,
                     trusted=None,
                    ):
            """
            :type  server_name: :class:`str`
            :param server_name: Name of the server. This attribute was added in vSphere API
                7.0.0.0.
            :type  certificate: :class:`str` or ``None``
            :param certificate: Server certificate. This attribute was added in vSphere API
                7.0.0.0.
                If None, the certificate cannot be retrieved from the remote
                system, and :attr:`CurrentPeerCertificates.Summary.trusted` is
                undefined. See
                :attr:`CurrentPeerCertificates.Summary.error_messages` for details.
            :type  error_messages: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param error_messages: Server certificate retrieval errors. 
                
                Specifies error details when retrieving the remote server
                certificate fails. This list will be empty when
                :attr:`CurrentPeerCertificates.Summary.certificate` is
                :class:`set`.. This attribute was added in vSphere API 7.0.0.0.
            :type  trusted: :class:`bool`
            :param trusted: whether server certificate is already trusted . This attribute was
                added in vSphere API 7.0.0.0.
            """
            self.server_name = server_name
            self.certificate = certificate
            self.error_messages = error_messages
            self.trusted = trusted
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.current_peer_certificates.summary', {
            'server_name': type.StringType(),
            'certificate': type.OptionalType(type.StringType()),
            'error_messages': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'trusted': type.BooleanType(),
        },
        Summary,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``CurrentPeerCertificates.FilterSpec`` class contains attributes used
        to filter the results when listing remote server certificates. This class
        was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     server_names=None,
                     trusted=None,
                    ):
            """
            :type  server_names: :class:`set` of :class:`str` or ``None``
            :param server_names: Names that key server must have to match the filter (see
                :attr:`CurrentPeerCertificates.Summary.server_name`). This
                attribute was added in vSphere API 7.0.0.0.
                If None or empty, key servers with any name match the filter.
            :type  trusted: :class:`bool` or ``None``
            :param trusted: Trust status that server certificates must have to match the filter
                (see :attr:`CurrentPeerCertificates.Summary.trusted`). This
                attribute was added in vSphere API 7.0.0.0.
                If None, trusted and untrusted server certificates match the
                filter.
            """
            self.server_names = server_names
            self.trusted = trusted
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.current_peer_certificates.filter_spec', {
            'server_names': type.OptionalType(type.SetType(type.StringType())),
            'trusted': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))




    def list_task(self,
             cluster,
             provider,
             spec=None,
             ):
        """
        Return the remote server certificates. 
        
        Contacts the configured key servers and attempts to retrieve their
        certificates. These certificates might not yet be trusted. 
        
        If the returned certificates are to be considered trustworthy, then it
        must be added to the list of trusted server certificates by adding to
        the certificates returned by :func:`TrustedPeerCertificates.get` and
        invoking :func:`TrustedPeerCertificates.update` with the updated
        :class:`list` of certificates.. This method was added in vSphere API
        7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :type  spec: :class:`CurrentPeerCertificates.FilterSpec` or ``None``
        :param spec: Filter spec.
            If None, the behavior is equivalent to a
            :class:`CurrentPeerCertificates.FilterSpec` with all attributes
            None
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the cluster or provider id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster or provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            For any other error.
        """
        task_id = self._invoke('list$task',
                                {
                                'cluster': cluster,
                                'provider': provider,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ListType(type.ReferenceType(__name__, 'CurrentPeerCertificates.Summary')))
        return task_instance
class TrustedPeerCertificates(VapiInterface):
    """
    Provides management operations for the TLS certificates trusted for
    communication with peer key servers. 
    
    To obtain the currently used TLS certificates use the
    :class:`CurrentPeerCertificates` class. This class was added in vSphere API
    7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.trusted_peer_certificates'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TrustedPeerCertificatesStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})

    class Info(VapiStruct):
        """
        The ``TrustedPeerCertificates.Info`` class contains x509 certificate list.
        This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     certificates=None,
                    ):
            """
            :type  certificates: :class:`list` of :class:`str`
            :param certificates: List of certificate strings, PEM format. This attribute was added
                in vSphere API 7.0.0.0.
            """
            self.certificates = certificates
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.trusted_peer_certificates.info', {
            'certificates': type.ListType(type.StringType()),
        },
        Info,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``TrustedPeerCertificates.UpdateSpec`` class contains attributes that
        describe the server certificate update for a Key Provider. This class was
        added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     certificates=None,
                    ):
            """
            :type  certificates: :class:`list` of :class:`str` or ``None``
            :param certificates: Public certificates of key server to trust. This attribute was
                added in vSphere API 7.0.0.0.
                If None, the trusted server certificates will not be updated.
            """
            self.certificates = certificates
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.trusted_peer_certificates.update_spec', {
            'certificates': type.OptionalType(type.ListType(type.StringType())),
        },
        UpdateSpec,
        False,
        None))




    def update_task(self,
               cluster,
               provider,
               spec,
               ):
        """
        Update trusted server certificate(s). 
        
        The client will use these certificates to validate the server
        connection. The existing list of trusted certificates will be
        overwritten. 
        
        The client will not trust the server connection until a server
        certificate has been set.. This method was added in vSphere API
        7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :type  spec: :class:`TrustedPeerCertificates.UpdateSpec`
        :param spec: The update spec
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If one or more certificates are invalid or the cluster/provider Id
            is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster or provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        task_id = self._invoke('update$task',
                                {
                                'cluster': cluster,
                                'provider': provider,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def get_task(self,
            cluster,
            provider,
            ):
        """
        Return the list of trusted server certificates. This method was added
        in vSphere API 7.0.0.0.

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
            If the cluster or provider is not found.
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
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'TrustedPeerCertificates.Info'))
        return task_instance
class _ClientCertificateStub(ApiInterfaceStub):
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/client-certificate',
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/client-certificate',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
            'spec': type.ReferenceType(__name__, 'ClientCertificate.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/client-certificate',
            request_body_parameter='spec',
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
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'get': get_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _CredentialStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
            'credential': type.SecretType(),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/credential',
            request_body_parameter='credential',
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
            'set$task': {
                'input_type': set_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'set': set_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.credential',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _CurrentPeerCertificatesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'CurrentPeerCertificates.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/peer-certs/current',
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
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.current_peer_certificates',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _TrustedPeerCertificatesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
            'spec': type.ReferenceType(__name__, 'TrustedPeerCertificates.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/peer-certs/trusted',
            request_body_parameter='spec',
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/peer-certs/trusted',
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
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
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
            'update': update_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.trusted_peer_certificates',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ClientCertificate': ClientCertificate,
        'Credential': Credential,
        'CurrentPeerCertificates': CurrentPeerCertificates,
        'TrustedPeerCertificates': TrustedPeerCertificates,
        'client_certificate': 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.client_certificate_client.StubFactory',
    }

