# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2_client``
module provides classes to manage remote attestation configuration for TPM
trust.

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


class CaCertificates(VapiInterface):
    """
    The ``CaCertificates`` class provides methods to manage Trusted Platform
    Module (TPM) CA certificates. 
    
    Endorsement Keys are typically packaged in a certificate that is signed by
    a certificate authority (CA). This class allows the CA certificate to be
    registered with the Attestation Service in order to validate TPM EK
    certificates when presented at attestation time.. This class was added in
    vSphere API 7.0.0.0.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate"
    """
    Resource type for TPM 2.0 CA certificates. This class attribute was added in
    vSphere API 7.0.0.0.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.ca_certificates'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CaCertificatesStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'list_task': 'list$task'})
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})

    class Health(Enum):
        """
        The ``CaCertificates.Health`` class is indicator for the consistency of the
        hosts status in the cluster. This enumeration was added in vSphere API
        7.0.0.0.

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
        Each host in the cluster is in consistent state with the rest hosts in the
        cluster. This class attribute was added in vSphere API 7.0.0.0.

        """
        WARNING = None
        """
        Attestation is funtioning, however there is an issue that requires
        attention. This class attribute was added in vSphere API 7.0.0.0.

        """
        ERROR = None
        """
        Not all hosts in the cluster are in consistent state. This class attribute
        was added in vSphere API 7.0.0.0.

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
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.ca_certificates.health',
        Health))


    class Summary(VapiStruct):
        """
        The ``CaCertificates.Summary`` class contains information that summarizes a
        TPM CA certificate. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     health=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: A unique name for the TPM CA certificate. This attribute was added
                in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate``.
            :type  health: :class:`CaCertificates.Health`
            :param health: A health indicator which indicates whether each host in the cluster
                has the same CA certs. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.name = name
            self.health = health
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.ca_certificates.summary', {
            'name': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate'),
            'health': type.ReferenceType(__name__, 'CaCertificates.Health'),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``CaCertificates.Info`` class contains information that describes a TPM
        CA certificate. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cert_chain=None,
                     health=None,
                     details=None,
                    ):
            """
            :type  cert_chain: :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain`
            :param cert_chain: The CA certificate chain. This attribute was added in vSphere API
                7.0.0.0.
            :type  health: :class:`CaCertificates.Health`
            :param health: A health indicator which indicates whether each host in the cluster
                has the same CA certs. This attribute was added in vSphere API
                7.0.0.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health. 
                
                When the ``CaCertificates.Health`` is not
                :attr:`CaCertificates.Health.OK` or
                :attr:`CaCertificates.Health.NONE`, this member will provide an
                actionable description of the issues present.. This attribute was
                added in vSphere API 7.0.0.0.
            """
            self.cert_chain = cert_chain
            self.health = health
            self.details = details
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.ca_certificates.info', {
            'cert_chain': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain'),
            'health': type.ReferenceType(__name__, 'CaCertificates.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Info,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``CaCertificates.CreateSpec`` class contains information that describes
        a TPM CA certificate. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     cert_chain=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: A unique name for the TPM CA certificate. This attribute was added
                in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate``.
            :type  cert_chain: :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain` or ``None``
            :param cert_chain: The CA certificate chain. 
                
                Certificates may either be added one at a time, or as a chain.
                Adding the certificates as a chain allows the group to be managed
                as a whole. For example, an entire chain can be deleted in one
                :func:`CaCertificates.delete` operation. 
                
                When certificates are added one at a time, the order must be root
                first, followed by any intermediates. The intermediates
                certificates must also be ordered in the direction from root to
                leaf. 
                
                Similarly, when added as a chain the list must be ordered in the
                direction from root to leaf.. This attribute was added in vSphere
                API 7.0.0.0.
                If None creation will fail.
            """
            self.name = name
            self.cert_chain = cert_chain
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.ca_certificates.create_spec', {
            'name': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate'),
            'cert_chain': type.OptionalType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain')),
        },
        CreateSpec,
        False,
        None))




    def list_task(self,
             cluster,
             ):
        """
        Return a list of configured TPM CA certificates on a cluster. This
        method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the ``cluster`` doesn't match to any cluster in the vCenter or
            given name is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('list$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ListType(type.ReferenceType(__name__, 'CaCertificates.Summary')))
        return task_instance


    def create_task(self,
               cluster,
               spec,
               ):
        """
        Add a new TPM CA certificate on a cluster. This method was added in
        vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`CaCertificates.CreateSpec`
        :param spec: The new CA certificate details.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if the certificate name exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the configuration is invalid or the cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``cluster`` doesn't match to any cluster in the vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('create$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def delete_task(self,
               cluster,
               name,
               ):
        """
        Remove a TPM CA certificate on a cluster. This method was added in
        vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  name: :class:`str`
        :param name: The CA certificate name.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the name is invalid or cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the ``cluster`` doesn't match to any cluster in the vCenter or
            given name is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cluster': cluster,
                                'name': name,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def get_task(self,
            cluster,
            name,
            ):
        """
        Get the TPM CA certificate details on a cluster. This method was added
        in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  name: :class:`str`
        :param name: The CA certificate name.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the name is invalid or cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the CA certificate is not found or ``cluster`` doesn't match to
            any cluster in the vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                'name': name,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'CaCertificates.Info'))
        return task_instance
class EndorsementKeys(VapiInterface):
    """
    The ``EndorsementKeys`` class provides methods to manage Trusted Platform
    Module (TPM) Endorsement Keys (EK) on a cluster level. This class was added
    in vSphere API 7.0.0.0.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey"
    """
    Resource type for TPM 2.0 endorsement keys. This class attribute was added in
    vSphere API 7.0.0.0.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.endorsement_keys'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EndorsementKeysStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'list_task': 'list$task'})
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})

    class Health(Enum):
        """
        The ``EndorsementKeys.Health`` class is indicator for the consistency of
        the hosts status in the cluster. This enumeration was added in vSphere API
        7.0.0.0.

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
        Each host in the cluster is in consistent state with the rest hosts in the
        cluster. This class attribute was added in vSphere API 7.0.0.0.

        """
        WARNING = None
        """
        Attestation is functioning, however there is an issue that requires
        attention. This class attribute was added in vSphere API 7.0.0.0.

        """
        ERROR = None
        """
        Not all hosts in the cluster are in consistent state. This class attribute
        was added in vSphere API 7.0.0.0.

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
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.endorsement_keys.health',
        Health))


    class Summary(VapiStruct):
        """
        The ``EndorsementKeys.Summary`` class contains information that summarizes
        a TPM endorsement key. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     health=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: A unique name for the TPM endorsement key. This attribute was added
                in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey``.
            :type  health: :class:`EndorsementKeys.Health`
            :param health: A health indicator which indicates whether each host in the cluster
                has the same endorsement key. This attribute was added in vSphere
                API 7.0.0.0.
            """
            self.name = name
            self.health = health
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.endorsement_keys.summary', {
            'name': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey'),
            'health': type.ReferenceType(__name__, 'EndorsementKeys.Health'),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``EndorsementKeys.Info`` class contains information that describes a
        TPM endorsement key. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     public_key=None,
                     health=None,
                     details=None,
                    ):
            """
            :type  public_key: :class:`str`
            :param public_key: TPM public endorsement key in PEM format. This attribute was added
                in vSphere API 7.0.0.0.
            :type  health: :class:`EndorsementKeys.Health`
            :param health: A health indicator which indicates whether each host in the cluster
                has the same endorsement key. This attribute was added in vSphere
                API 7.0.0.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health. 
                
                When the ``EndorsementKeys.Health`` is not
                :attr:`EndorsementKeys.Health.OK` or
                :attr:`EndorsementKeys.Health.NONE`, this member will provide an
                actionable description of the issues present.. This attribute was
                added in vSphere API 7.0.0.0.
            """
            self.public_key = public_key
            self.health = health
            self.details = details
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.endorsement_keys.info', {
            'public_key': type.StringType(),
            'health': type.ReferenceType(__name__, 'EndorsementKeys.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Info,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``EndorsementKeys.CreateSpec`` class contains information that
        describes a TPM endorsement key. 
        
        Only one of :attr:`EndorsementKeys.CreateSpec.public_key` or
        :attr:`EndorsementKeys.CreateSpec.certificate` must be specified.. This
        class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     public_key=None,
                     certificate=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: A unique name for the TPM endorsement key. 
                
                The unique name should be something that an administrator can use
                to easily identify the remote system. For example, the hostname, or
                hardware UUID.. This attribute was added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey``.
            :type  public_key: :class:`str` or ``None``
            :param public_key: TPM public endorsement key in PEM format. This attribute was added
                in vSphere API 7.0.0.0.
                If None :attr:`EndorsementKeys.CreateSpec.certificate` must be
                :class:`set`.
            :type  certificate: :class:`str` or ``None``
            :param certificate: TPM endorsement key certificate in PEM format. 
                
                When a endorsement key certificate is provided, it will be verified
                against the CA certificate list. Endorsement key certificates that
                are not signed by one of the CA certificates will be rejected. 
                
                Using this format allows for failures to be caught during
                configuration rather than later during attestation.. This attribute
                was added in vSphere API 7.0.0.0.
                If None :attr:`EndorsementKeys.CreateSpec.public_key` must be
                :class:`set`.
            """
            self.name = name
            self.public_key = public_key
            self.certificate = certificate
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.endorsement_keys.create_spec', {
            'name': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey'),
            'public_key': type.OptionalType(type.StringType()),
            'certificate': type.OptionalType(type.StringType()),
        },
        CreateSpec,
        False,
        None))




    def list_task(self,
             cluster,
             ):
        """
        Return a list of configured TPM endorsement keys in a cluster. This
        method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('list$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ListType(type.ReferenceType(__name__, 'EndorsementKeys.Summary')))
        return task_instance


    def create_task(self,
               cluster,
               spec,
               ):
        """
        Add a new TPM endorsement key on a cluster. This method was added in
        vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`EndorsementKeys.CreateSpec`
        :param spec: The configuration.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if the endorsement key name exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the configuration is invalid or cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``cluster`` doesn't match to any cluster in the vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('create$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def delete_task(self,
               cluster,
               name,
               ):
        """
        Remove a TPM endorsement key on a cluster. This method was added in
        vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  name: :class:`str`
        :param name: The endorsement key name.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the name is invalid or cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the name is not found or ``cluster`` doesn't match to any
            cluster in the vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cluster': cluster,
                                'name': name,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def get_task(self,
            cluster,
            name,
            ):
        """
        Get the TPM endorsement key details on a cluster. This method was added
        in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  name: :class:`str`
        :param name: The endorsement key name.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the name is invalid or cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the endorsement key is not found or ``cluster`` doesn't match to
            any cluster in the vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                'name': name,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'EndorsementKeys.Info'))
        return task_instance
class Settings(VapiInterface):
    """
    The ``Settings`` interface provides methods to get or update settings
    related to the TPM 2.0 attestation protocol behavior. This class was added
    in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.settings'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SettingsStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})

    class Health(Enum):
        """
        The ``Settings.Health`` class is indicator for the consistency of the hosts
        status in the cluster. This enumeration was added in vSphere API 7.0.0.0.

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
        Each host in the cluster is in consistent state with the rest hosts in the
        cluster. This class attribute was added in vSphere API 7.0.0.0.

        """
        WARNING = None
        """
        Attestation is functioning, however there is an issue that requires
        attention. This class attribute was added in vSphere API 7.0.0.0.

        """
        ERROR = None
        """
        Not all hosts in the cluster are in consistent state. This class attribute
        was added in vSphere API 7.0.0.0.

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
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.settings.health',
        Health))


    class Info(VapiStruct):
        """
        The ``Settings.Info`` class contains information that describes the TPM 2.0
        protocol settings. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     require_endorsement_keys=None,
                     require_certificate_validation=None,
                     health=None,
                     details=None,
                    ):
            """
            :type  require_endorsement_keys: :class:`bool`
            :param require_endorsement_keys: Require registered TPM endorsement keys. 
                
                During attestation, the attested host will always send its
                endorsement key to the Attestation Service. With this option is
                set, the Attestation Service will only proceed with attestation if
                the endorsement key has been added to the list of configured
                trusted endorsement keys.. This attribute was added in vSphere API
                7.0.0.0.
            :type  require_certificate_validation: :class:`bool`
            :param require_certificate_validation: Require TPM endorsement key certificate validation. 
                
                During attestation, the attested host will send its endorsement key
                certificate if one is available. With this option set, the
                Attestation Service will validate the endorsement key certificate
                against the list of configured trusted TPM CA certificates. Only
                endorsement key certificates that are signed by a trusted TPM CA
                certificate will be able to successfully attest.. This attribute
                was added in vSphere API 7.0.0.0.
            :type  health: :class:`Settings.Health`
            :param health: A health indicator which indicates whether each host in the cluster
                has the same attestation settings. This attribute was added in
                vSphere API 7.0.0.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health. 
                
                When the ``Settings.Health`` is not :attr:`Settings.Health.OK` or
                :attr:`Settings.Health.NONE`, this member will provide an
                actionable description of the issues present.. This attribute was
                added in vSphere API 7.0.0.0.
            """
            self.require_endorsement_keys = require_endorsement_keys
            self.require_certificate_validation = require_certificate_validation
            self.health = health
            self.details = details
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.settings.info', {
            'require_endorsement_keys': type.BooleanType(),
            'require_certificate_validation': type.BooleanType(),
            'health': type.ReferenceType(__name__, 'Settings.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Info,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Settings.UpdateSpec`` class contains information that describes
        changes to the TPM 2.0 protocol settings. This class was added in vSphere
        API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     require_endorsement_keys=None,
                     require_certificate_validation=None,
                    ):
            """
            :type  require_endorsement_keys: :class:`bool` or ``None``
            :param require_endorsement_keys: Require registered TPM endorsement keys. This attribute was added
                in vSphere API 7.0.0.0.
                If None the current state will remain unchanged.
            :type  require_certificate_validation: :class:`bool` or ``None``
            :param require_certificate_validation: Require TPM endorsement key certificate validation. This attribute
                was added in vSphere API 7.0.0.0.
                If None the current state will remain unchanged.
            """
            self.require_endorsement_keys = require_endorsement_keys
            self.require_certificate_validation = require_certificate_validation
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.settings.update_spec', {
            'require_endorsement_keys': type.OptionalType(type.BooleanType()),
            'require_certificate_validation': type.OptionalType(type.BooleanType()),
        },
        UpdateSpec,
        False,
        None))




    def get_task(self,
            cluster,
            ):
        """
        Return the TPM 2.0 protocol settings. This method was added in vSphere
        API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``cluster`` doesn't match to any cluster in the vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Settings.Info'))
        return task_instance


    def update_task(self,
               cluster,
               spec,
               ):
        """
        Set the TPM 2.0 protocol settings. This method was added in vSphere API
        7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The id of the cluster on which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`Settings.UpdateSpec`
        :param spec: The settings.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the spec is invalid or cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``cluster`` doesn't match to any cluster in the vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('update$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class _CaCertificatesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/ca-certificates',
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

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'CaCertificates.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/ca-certificates',
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
            'name': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/ca-certificates/{name}',
            path_variables={
                'cluster': 'cluster',
                'name': 'name',
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
            'name': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.CaCertificate'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/ca-certificates/{name}',
            path_variables={
                'cluster': 'cluster',
                'name': 'name',
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
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.ca_certificates',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _EndorsementKeysStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/endorsement-keys',
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

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'EndorsementKeys.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/endorsement-keys',
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
            'name': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/endorsement-keys/{name}',
            path_variables={
                'cluster': 'cluster',
                'name': 'name',
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
            'name': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.EndorsementKey'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/endorsement-keys/{name}',
            path_variables={
                'cluster': 'cluster',
                'name': 'name',
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
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.endorsement_keys',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SettingsStub(ApiInterfaceStub):
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/settings',
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
            'spec': type.ReferenceType(__name__, 'Settings.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/tpm2/settings',
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
            'get': get_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.attestation.tpm2.settings',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'CaCertificates': CaCertificates,
        'EndorsementKeys': EndorsementKeys,
        'Settings': Settings,
    }

