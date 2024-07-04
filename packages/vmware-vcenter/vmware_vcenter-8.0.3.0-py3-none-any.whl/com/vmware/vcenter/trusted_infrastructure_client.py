# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.trusted_infrastructure_client`` module provides
classes that enable a Trusted Infrastructure. They are responsible for ensuring
that infrastructure nodes are running trusted software and for releasing
encryption keys only to trusted infrastructure nodes.

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

class StsPrincipalType(Enum):
    """
    The ``StsPrincipalType`` enum can be either users or groups. This
    enumeration was added in vSphere API 7.0.0.0.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    STS_USER = None
    """
    The principal is a user. This class attribute was added in vSphere API
    7.0.0.0.

    """
    STS_GROUP = None
    """
    The principal is a group. This class attribute was added in vSphere API
    7.0.0.0.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`StsPrincipalType` instance.
        """
        Enum.__init__(string)

StsPrincipalType._set_values({
    'STS_USER': StsPrincipalType('STS_USER'),
    'STS_GROUP': StsPrincipalType('STS_GROUP'),
})
StsPrincipalType._set_binding_type(type.EnumType(
    'com.vmware.vcenter.trusted_infrastructure.sts_principal_type',
    StsPrincipalType))




class NetworkAddress(VapiStruct):
    """
    The ``NetworkAddress`` class contains an IP address or DNS resolvable name
    and a port on which a connection can be established. This class was added
    in vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 hostname=None,
                 port=None,
                ):
        """
        :type  hostname: :class:`str`
        :param hostname: The IP address or DNS resolvable name of the service. This
            attribute was added in vSphere API 7.0.0.0.
        :type  port: :class:`long` or ``None``
        :param port: The port of the service. This attribute was added in vSphere API
            7.0.0.0.
            If None, port 443 will be used.
        """
        self.hostname = hostname
        self.port = port
        VapiStruct.__init__(self)


NetworkAddress._set_binding_type(type.StructType(
    'com.vmware.vcenter.trusted_infrastructure.network_address', {
        'hostname': type.StringType(),
        'port': type.OptionalType(type.IntegerType()),
    },
    NetworkAddress,
    False,
    None))



class StsPrincipalId(VapiStruct):
    """
    The ``StsPrincipalId`` class contains an IDM principal ID. This class was
    added in vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 domain=None,
                ):
        """
        :type  name: :class:`str`
        :param name: The principal's username. This attribute was added in vSphere API
            7.0.0.0.
        :type  domain: :class:`str`
        :param domain: The principal's domain. This attribute was added in vSphere API
            7.0.0.0.
        """
        self.name = name
        self.domain = domain
        VapiStruct.__init__(self)


StsPrincipalId._set_binding_type(type.StructType(
    'com.vmware.vcenter.trusted_infrastructure.sts_principal_id', {
        'name': type.StringType(),
        'domain': type.StringType(),
    },
    StsPrincipalId,
    False,
    None))



class StsPrincipal(VapiStruct):
    """
    The ``StsPrincipal`` class contains a IDM principal. This class was added
    in vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 id=None,
                 type=None,
                ):
        """
        :type  id: :class:`StsPrincipalId`
        :param id: The principal's ID. This attribute was added in vSphere API
            7.0.0.0.
        :type  type: :class:`StsPrincipalType`
        :param type: The type of the principal (user or group). This attribute was added
            in vSphere API 7.0.0.0.
        """
        self.id = id
        self.type = type
        VapiStruct.__init__(self)


StsPrincipal._set_binding_type(type.StructType(
    'com.vmware.vcenter.trusted_infrastructure.sts_principal', {
        'id': type.ReferenceType(__name__, 'StsPrincipalId'),
        'type': type.ReferenceType(__name__, 'StsPrincipalType'),
    },
    StsPrincipal,
    False,
    None))



class X509CertChain(VapiStruct):
    """
    The ``X509CertChain`` class contains x509 certificate chain. This class was
    added in vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 cert_chain=None,
                ):
        """
        :type  cert_chain: :class:`list` of :class:`str`
        :param cert_chain: Certificate chain in base64 format. This attribute was added in
            vSphere API 7.0.0.0.
        """
        self.cert_chain = cert_chain
        VapiStruct.__init__(self)


X509CertChain._set_binding_type(type.StructType(
    'com.vmware.vcenter.trusted_infrastructure.x509_cert_chain', {
        'cert_chain': type.ListType(type.StringType()),
    },
    X509CertChain,
    False,
    None))



class TrustAuthorityClusters(VapiInterface):
    """
    The ``TrustAuthorityClusters`` class manages all the Trust Authority
    Components on each Trust Authority Host in the cluster. The
    ``TrustAuthorityClusters`` class transforms a ClusterComputeResource into
    Trust Authority Cluster and vice versa. This class was added in vSphere API
    7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TrustAuthorityClustersStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})

    class State(Enum):
        """
        The ``TrustAuthorityClusters.State`` class defines the states of the
        :class:`TrustAuthorityClusters`. This enumeration was added in vSphere API
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
        ENABLE = None
        """
        The :class:`TrustAuthorityClusters` is enabled. This class attribute was
        added in vSphere API 7.0.0.0.

        """
        DISABLE = None
        """
        The :class:`TrustAuthorityClusters` is disabled. This class attribute was
        added in vSphere API 7.0.0.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`State` instance.
            """
            Enum.__init__(string)

    State._set_values({
        'ENABLE': State('ENABLE'),
        'DISABLE': State('DISABLE'),
    })
    State._set_binding_type(type.EnumType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.state',
        State))


    class Summary(VapiStruct):
        """
        The ``TrustAuthorityClusters.Summary`` class contains information about
        :class:`TrustAuthorityClusters` id and state. This class was added in
        vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     state=None,
                    ):
            """
            :type  cluster: :class:`str`
            :param cluster: Identifies the cluster. This attribute was added in vSphere API
                7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            :type  state: :class:`TrustAuthorityClusters.State`
            :param state: The state of the :class:`TrustAuthorityClusters`. This attribute
                was added in vSphere API 7.0.0.0.
            """
            self.cluster = cluster
            self.state = state
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.summary', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'state': type.ReferenceType(__name__, 'TrustAuthorityClusters.State'),
        },
        Summary,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``TrustAuthorityClusters.FilterSpec`` class contains the data necessary
        for identifying a :class:`TrustAuthorityClusters`. This class was added in
        vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     state=None,
                    ):
            """
            :type  cluster: :class:`set` of :class:`str` or ``None``
            :param cluster: Identifies the cluster. This attribute was added in vSphere API
                7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                cluster If None return all Trust Authority Clusters.
            :type  state: :class:`set` of :class:`TrustAuthorityClusters.State` or ``None``
            :param state: The state of the :class:`TrustAuthorityClusters`. This attribute
                was added in vSphere API 7.0.0.0.
                state If None return all Trust Authority Clusters.
            """
            self.cluster = cluster
            self.state = state
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.filter_spec', {
            'cluster': type.OptionalType(type.SetType(type.IdType())),
            'state': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'TrustAuthorityClusters.State'))),
        },
        FilterSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``TrustAuthorityClusters.UpdateSpec`` class contains the data necessary
        for update of a :class:`TrustAuthorityClusters`. This class was added in
        vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     state=None,
                    ):
            """
            :type  state: :class:`TrustAuthorityClusters.State` or ``None``
            :param state: The state of the :class:`TrustAuthorityClusters`. This attribute
                was added in vSphere API 7.0.0.0.
                state If None no operation is performed.
            """
            self.state = state
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.update_spec', {
            'state': type.OptionalType(type.ReferenceType(__name__, 'TrustAuthorityClusters.State')),
        },
        UpdateSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``TrustAuthorityClusters.Info`` class contains the data necessary for
        retrieving the :class:`TrustAuthorityClusters` info. This class was added
        in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     state=None,
                    ):
            """
            :type  cluster: :class:`str`
            :param cluster: Identifies the cluster. This attribute was added in vSphere API
                7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            :type  state: :class:`TrustAuthorityClusters.State`
            :param state: The state of the cluster. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.cluster = cluster
            self.state = state
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.info', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'state': type.ReferenceType(__name__, 'TrustAuthorityClusters.State'),
        },
        Info,
        False,
        None))




    def update_task(self,
               cluster,
               spec,
               ):
        """
        Updates the state of a cluster. This method was added in vSphere API
        7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Cluster id.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`TrustAuthorityClusters.UpdateSpec`
        :param spec: The specification for update of a cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``spec`` doesn't match to any cluster compute resource.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        task_id = self._invoke('update$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance

    def get(self,
            cluster,
            ):
        """
        Get the result of the last Update operation which matches the cluster
        id. This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Cluster id.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:`TrustAuthorityClusters.Info`
        :return: The :class:`TrustAuthorityClusters.Info` instance which contains
            information about the state of the cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``cluster`` doesn't match to any ClusterComputeResource.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ReadTrustedHosts``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires ``System.View``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            })

    def list(self,
             spec=None,
             ):
        """
        Returns a list of clusters for this vCenter instance which matches the
        :class:`TrustAuthorityClusters.FilterSpec`. This method was added in
        vSphere API 7.0.0.0.

        :type  spec: :class:`TrustAuthorityClusters.FilterSpec` or ``None``
        :param spec: Return only clusters matching the specified filters.
            If None return all clusters.
        :rtype: :class:`list` of :class:`TrustAuthorityClusters.Summary`
        :return: List of :class:`TrustAuthorityClusters.Summary` for a
            :class:`TrustAuthorityClusters`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ReadTrustedHosts``.
            * The resource ``ClusterComputeResource`` referenced by the
              attribute :attr:`TrustAuthorityClusters.FilterSpec.cluster`
              requires ``System.View``.
        """
        return self._invoke('list',
                            {
                            'spec': spec,
                            })
class Principal(VapiInterface):
    """
    The ``Principal`` class contains information about the certificates which
    sign the tokens used by vCenter for authentication. This class was added in
    vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.principal'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PrincipalStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Principal.Info`` class contains the information about the principal
        and certificates used by this vCenter to retrieve tokens. This class was
        added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     certificates=None,
                     issuer=None,
                     principal=None,
                     name=None,
                    ):
            """
            :type  certificates: :class:`list` of :class:`X509CertChain`
            :param certificates: The certificates used by the STS to sign tokens for this vCenter.
                This attribute was added in vSphere API 7.0.0.0.
            :type  issuer: :class:`str`
            :param issuer: The service which created and signed the security token. This
                attribute was added in vSphere API 7.0.0.0.
            :type  principal: :class:`StsPrincipal`
            :param principal: The principal used by this vCenter instance to retrieve tokens.
                Currently this is the vCenter solution user. This attribute was
                added in vSphere API 7.0.0.0.
            :type  name: :class:`str`
            :param name: The user-friednly name of the vCenter. This attribute was added in
                vSphere API 7.0.0.0.
            """
            self.certificates = certificates
            self.issuer = issuer
            self.principal = principal
            self.name = name
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.principal.info', {
            'certificates': type.ListType(type.ReferenceType(__name__, 'X509CertChain')),
            'issuer': type.StringType(),
            'principal': type.ReferenceType(__name__, 'StsPrincipal'),
            'name': type.StringType(),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Returns information about the STS used by this vCenter instance. This
        method was added in vSphere API 7.0.0.0.


        :rtype: :class:`Principal.Info`
        :return: :class:`Principal.Info` a summary containing the certificates used
            to sign tokens and the solution user used to retrieve them.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ReadStsInfo``.
        """
        return self._invoke('get', None)
class _TrustAuthorityClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'TrustAuthorityClusters.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}',
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

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'spec': type.OptionalType(type.ReferenceType(__name__, 'TrustAuthorityClusters.FilterSpec')),
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
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters',
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
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'TrustAuthorityClusters.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'TrustAuthorityClusters.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'update': update_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _PrincipalStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/principal',
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
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Principal.Info'),
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
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.principal',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'TrustAuthorityClusters': TrustAuthorityClusters,
        'Principal': Principal,
        'attestation': 'com.vmware.vcenter.trusted_infrastructure.attestation_client.StubFactory',
        'hosts': 'com.vmware.vcenter.trusted_infrastructure.hosts_client.StubFactory',
        'kms': 'com.vmware.vcenter.trusted_infrastructure.kms_client.StubFactory',
        'trust_authority_clusters': 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters_client.StubFactory',
        'trust_authority_hosts': 'com.vmware.vcenter.trusted_infrastructure.trust_authority_hosts_client.StubFactory',
        'trusted_clusters': 'com.vmware.vcenter.trusted_infrastructure.trusted_clusters_client.StubFactory',
    }

