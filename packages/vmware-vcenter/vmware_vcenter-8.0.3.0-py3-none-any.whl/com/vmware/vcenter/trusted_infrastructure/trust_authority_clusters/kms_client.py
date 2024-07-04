# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms_client``
module provides the interfaces for configuring the Key Provider Service. It
encapsulates one or more key servers and exposes Trusted Key Providers.

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


class Providers(VapiInterface):
    """
    The ``Providers`` interface provides methods to create, update and delete
    Key Providers that handoff to key servers. This class was added in vSphere
    API 7.0.0.0.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider"
    """
    Resource type for a Key Provider. This class attribute was added in vSphere API
    7.0.0.0.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProvidersStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'list_task': 'list$task'})
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})

    class Health(Enum):
        """
        The ``Providers.Health`` class defines the possible health states. This
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
        NONE = None
        """
        No status available. This class attribute was added in vSphere API 7.0.0.0.

        """
        OK = None
        """
        Health is normal. This class attribute was added in vSphere API 7.0.0.0.

        """
        WARNING = None
        """
        Health is normal, however there is an issue that requires attention. This
        class attribute was added in vSphere API 7.0.0.0.

        """
        ERROR = None
        """
        Not healthy. This class attribute was added in vSphere API 7.0.0.0.

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
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.health',
        Health))


    class ServerInfo(VapiStruct):
        """
        The ``Providers.ServerInfo`` class contains attributes that describe the
        status of a key server. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     health=None,
                     details=None,
                     client_trust_server=None,
                     server_trust_client=None,
                     name=None,
                    ):
            """
            :type  health: :class:`Providers.Health`
            :param health: The connection status health of the server. This attribute was
                added in vSphere API 7.0.0.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health of the server connection. 
                
                When the service ``Providers.Health`` is not
                :attr:`Providers.Health.OK`, this attribute will provide an
                actionable description of the issue.. This attribute was added in
                vSphere API 7.0.0.0.
            :type  client_trust_server: :class:`bool`
            :param client_trust_server: Whether this client trusts the server. This attribute was added in
                vSphere API 7.0.0.0.
            :type  server_trust_client: :class:`bool`
            :param server_trust_client: Whether the server trusts this client. This attribute was added in
                vSphere API 7.0.0.0.
            :type  name: :class:`str`
            :param name: Name of the server. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.health = health
            self.details = details
            self.client_trust_server = client_trust_server
            self.server_trust_client = server_trust_client
            self.name = name
            VapiStruct.__init__(self)


    ServerInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.server_info', {
            'health': type.ReferenceType(__name__, 'Providers.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'client_trust_server': type.BooleanType(),
            'server_trust_client': type.BooleanType(),
            'name': type.StringType(),
        },
        ServerInfo,
        False,
        None))


    class Status(VapiStruct):
        """
        The ``Providers.Status`` class contains attributes that describe the status
        of the Key Provider. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     health=None,
                     details=None,
                     servers=None,
                    ):
            """
            :type  health: :class:`Providers.Health`
            :param health: The health of the provider. This attribute was added in vSphere API
                7.0.0.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health of the provider. 
                
                When the service ``Providers.Health`` is not
                :attr:`Providers.Health.OK`, this attribute will provide an
                actionable description of the issue.. This attribute was added in
                vSphere API 7.0.0.0.
            :type  servers: :class:`list` of :class:`Providers.ServerInfo`
            :param servers: Health of the key servers. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.health = health
            self.details = details
            self.servers = servers
            VapiStruct.__init__(self)


    Status._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.status', {
            'health': type.ReferenceType(__name__, 'Providers.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'servers': type.ListType(type.ReferenceType(__name__, 'Providers.ServerInfo')),
        },
        Status,
        False,
        None))


    class Server(VapiStruct):
        """
        The ``Providers.Server`` class contains attributes that describe a
        connection endpoint. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     address=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the server. 
                
                A unique string chosen by the client.. This attribute was added in
                vSphere API 7.0.0.0.
            :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
            :param address: The server's address. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.name = name
            self.address = address
            VapiStruct.__init__(self)


    Server._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.server', {
            'name': type.StringType(),
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
        },
        Server,
        False,
        None))


    class KmipServerCreateSpec(VapiStruct):
        """
        The ``Providers.KmipServerCreateSpec`` class contains attributes that
        describe Key Management Interoperability Protocol (KMIP) desired key server
        configuration. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     servers=None,
                     username=None,
                    ):
            """
            :type  servers: :class:`list` of :class:`Providers.Server`
            :param servers: List of Key Management Interoperability Protocol (KMIP) compliant
                key servers. 
                
                Key servers must be configured for active-active replication. If
                the server port is None, a default value for KMIP's port will be
                used.. This attribute was added in vSphere API 7.0.0.0.
            :type  username: :class:`str` or ``None``
            :param username: Username for authentication. This attribute was added in vSphere
                API 7.0.0.0.
                If None, no username will be added.
            """
            self.servers = servers
            self.username = username
            VapiStruct.__init__(self)


    KmipServerCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.kmip_server_create_spec', {
            'servers': type.ListType(type.ReferenceType(__name__, 'Providers.Server')),
            'username': type.OptionalType(type.StringType()),
        },
        KmipServerCreateSpec,
        False,
        None))


    class KeyServerCreateSpec(VapiStruct):
        """
        The ``Providers.KeyServerCreateSpec`` class contains attributes that
        describe the desired configuration for the key server. This class was added
        in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'KMIP' : [('kmip_server', True)],
                }
            ),
        ]



        def __init__(self,
                     type=None,
                     description=None,
                     proxy_server=None,
                     connection_timeout=None,
                     kmip_server=None,
                    ):
            """
            :type  type: :class:`Providers.KeyServerCreateSpec.Type`
            :param type: Type of the key server. This attribute was added in vSphere API
                7.0.0.0.
            :type  description: :class:`str` or ``None``
            :param description: Description of the key server. This attribute was added in vSphere
                API 7.0.0.0.
                If None, description will not be added.
            :type  proxy_server: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress` or ``None``
            :param proxy_server: Proxy server configuration. This attribute was added in vSphere API
                7.0.0.0.
                If None, the key server will not use a proxy server.
            :type  connection_timeout: :class:`long` or ``None``
            :param connection_timeout: Connection timeout in seconds. This attribute was added in vSphere
                API 7.0.0.0.
                If None, connection timeout will not be set.
            :type  kmip_server: :class:`Providers.KmipServerCreateSpec`
            :param kmip_server: Configuration information for Key Management Interoperability
                Protocol (KMIP) based key server. This attribute was added in
                vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Providers.KeyServerCreateSpec.Type.KMIP`.
            """
            self.type = type
            self.description = description
            self.proxy_server = proxy_server
            self.connection_timeout = connection_timeout
            self.kmip_server = kmip_server
            VapiStruct.__init__(self)


        class Type(Enum):
            """
            The ``Providers.KeyServerCreateSpec.Type`` class lists the key server
            types. This enumeration was added in vSphere API 7.0.0.0.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            KMIP = None
            """
            Key Management Interoperability Protocol (KMIP) based key management
            server. This class attribute was added in vSphere API 7.0.0.0.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Type` instance.
                """
                Enum.__init__(string)

        Type._set_values({
            'KMIP': Type('KMIP'),
        })
        Type._set_binding_type(type.EnumType(
            'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.key_server_create_spec.type',
            Type))

    KeyServerCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.key_server_create_spec', {
            'type': type.ReferenceType(__name__, 'Providers.KeyServerCreateSpec.Type'),
            'description': type.OptionalType(type.StringType()),
            'proxy_server': type.OptionalType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress')),
            'connection_timeout': type.OptionalType(type.IntegerType()),
            'kmip_server': type.OptionalType(type.ReferenceType(__name__, 'Providers.KmipServerCreateSpec')),
        },
        KeyServerCreateSpec,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Providers.CreateSpec`` class contains attributes that describe the
        desired configuration for a new Key Provider. This class was added in
        vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     provider=None,
                     master_key_id=None,
                     key_server=None,
                    ):
            """
            :type  provider: :class:`str`
            :param provider: Name of the provider. 
                
                A unique string chosen by the client.. This attribute was added in
                vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
            :type  master_key_id: :class:`str`
            :param master_key_id: Master key ID created for the provider. 
                
                A unique Key ID.. This attribute was added in vSphere API 7.0.0.0.
            :type  key_server: :class:`Providers.KeyServerCreateSpec`
            :param key_server: Key server associated with this Provider. This attribute was added
                in vSphere API 7.0.0.0.
            """
            self.provider = provider
            self.master_key_id = master_key_id
            self.key_server = key_server
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.create_spec', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
            'master_key_id': type.StringType(),
            'key_server': type.ReferenceType(__name__, 'Providers.KeyServerCreateSpec'),
        },
        CreateSpec,
        False,
        None))


    class KmipServerUpdateSpec(VapiStruct):
        """
        The ``Providers.KmipServerUpdateSpec`` class contains attributes that
        describe new configuration for KMIP based key server. This class was added
        in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     servers=None,
                     username=None,
                    ):
            """
            :type  servers: :class:`list` of :class:`Providers.Server` or ``None``
            :param servers: List of KMIP compliant key servers. 
                
                Key servers must be configured for active-active replication. If
                the server port is None, a default value for KMIP's port will be
                used. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, server configuration will remain unchanged.
            :type  username: :class:`str` or ``None``
            :param username: Username for authentication. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, username will remain unchanged.
            """
            self.servers = servers
            self.username = username
            VapiStruct.__init__(self)


    KmipServerUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.kmip_server_update_spec', {
            'servers': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Providers.Server'))),
            'username': type.OptionalType(type.StringType()),
        },
        KmipServerUpdateSpec,
        False,
        None))


    class KeyServerUpdateSpec(VapiStruct):
        """
        The ``Providers.KeyServerUpdateSpec`` class contains attributes that
        describe new configuration for an existing key server. This class was added
        in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'KMIP' : [('kmip_server', False)],
                }
            ),
        ]



        def __init__(self,
                     type=None,
                     description=None,
                     proxy_server=None,
                     connection_timeout=None,
                     kmip_server=None,
                    ):
            """
            :type  type: :class:`Providers.KeyServerUpdateSpec.Type` or ``None``
            :param type: Type of the key server. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, key server type and configuration information will remain
                unchanged. In this case all key server configuration information
                fields (e.g KMIP) should be unset.
            :type  description: :class:`str` or ``None``
            :param description: Description of the key server. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, description will remain unchanged.
            :type  proxy_server: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress` or ``None``
            :param proxy_server: Proxy server configuration. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, proxy server configuration will remain unchanged.
            :type  connection_timeout: :class:`long` or ``None``
            :param connection_timeout: Connection timeout in seconds. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, connection timeout will remain unchanged.
            :type  kmip_server: :class:`Providers.KmipServerUpdateSpec` or ``None``
            :param kmip_server: Configuration information for KMIP based key server. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, kmip server configuration will remain unchanged.
            """
            self.type = type
            self.description = description
            self.proxy_server = proxy_server
            self.connection_timeout = connection_timeout
            self.kmip_server = kmip_server
            VapiStruct.__init__(self)


        class Type(Enum):
            """
            The ``Providers.KeyServerUpdateSpec.Type`` class list the key server types.
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
            KMIP = None
            """
            Key Management Interoperability Protocol (KMIP) based key management
            server. This class attribute was added in vSphere API 7.0.0.0.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Type` instance.
                """
                Enum.__init__(string)

        Type._set_values({
            'KMIP': Type('KMIP'),
        })
        Type._set_binding_type(type.EnumType(
            'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.key_server_update_spec.type',
            Type))

    KeyServerUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.key_server_update_spec', {
            'type': type.OptionalType(type.ReferenceType(__name__, 'Providers.KeyServerUpdateSpec.Type')),
            'description': type.OptionalType(type.StringType()),
            'proxy_server': type.OptionalType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress')),
            'connection_timeout': type.OptionalType(type.IntegerType()),
            'kmip_server': type.OptionalType(type.ReferenceType(__name__, 'Providers.KmipServerUpdateSpec')),
        },
        KeyServerUpdateSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Providers.UpdateSpec`` class contains attributes that describe the
        new configuration for an existing provider. This class was added in vSphere
        API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     master_key_id=None,
                     key_server=None,
                    ):
            """
            :type  master_key_id: :class:`str` or ``None``
            :param master_key_id: Master key identifier created for the provider. 
                
                A unique Key identifier. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, masterKeyId will remain unchanged.
            :type  key_server: :class:`Providers.KeyServerUpdateSpec` or ``None``
            :param key_server: Key server associated with this provider. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, key server configuration will remain unchanged.
            """
            self.master_key_id = master_key_id
            self.key_server = key_server
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.update_spec', {
            'master_key_id': type.OptionalType(type.StringType()),
            'key_server': type.OptionalType(type.ReferenceType(__name__, 'Providers.KeyServerUpdateSpec')),
        },
        UpdateSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Providers.Summary`` class contains attributes that summarize a
        provider. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     provider=None,
                     health=None,
                    ):
            """
            :type  provider: :class:`str`
            :param provider: Name of the provider. 
                
                A unique string chosen by the client.. This attribute was added in
                vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
            :type  health: :class:`Providers.Health`
            :param health: Health of the provider in the cluster. This attribute was added in
                vSphere API 7.0.0.0.
            """
            self.provider = provider
            self.health = health
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.summary', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
            'health': type.ReferenceType(__name__, 'Providers.Health'),
        },
        Summary,
        False,
        None))


    class KmipServerInfo(VapiStruct):
        """
        The ``Providers.KmipServerInfo`` class contains attributes that describe
        the current configuration of a KMIP based key server. This class was added
        in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     servers=None,
                     username=None,
                    ):
            """
            :type  servers: :class:`list` of :class:`Providers.Server`
            :param servers: List of KMIP compliant key servers. This attribute was added in
                vSphere API 7.0.0.0.
            :type  username: :class:`str` or ``None``
            :param username: Username for authentication. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, username will not be set.
            """
            self.servers = servers
            self.username = username
            VapiStruct.__init__(self)


    KmipServerInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.kmip_server_info', {
            'servers': type.ListType(type.ReferenceType(__name__, 'Providers.Server')),
            'username': type.OptionalType(type.StringType()),
        },
        KmipServerInfo,
        False,
        None))


    class KeyServerInfo(VapiStruct):
        """
        The ``Providers.KeyServerInfo`` class contains attributes that describe the
        current configuration of a key server. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'KMIP' : [('kmip_server', True)],
                }
            ),
        ]



        def __init__(self,
                     type=None,
                     description=None,
                     proxy_server=None,
                     connection_timeout=None,
                     kmip_server=None,
                    ):
            """
            :type  type: :class:`Providers.KeyServerInfo.Type`
            :param type: Type of the key server. This attribute was added in vSphere API
                7.0.0.0.
            :type  description: :class:`str`
            :param description: Description of the key server. This attribute was added in vSphere
                API 7.0.0.0.
            :type  proxy_server: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress` or ``None``
            :param proxy_server: Proxy server configuration. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, proxy server configuration will not be set.
            :type  connection_timeout: :class:`long` or ``None``
            :param connection_timeout: Connection timeout in seconds. 
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, connection timeout will be unset.
            :type  kmip_server: :class:`Providers.KmipServerInfo`
            :param kmip_server: Configuration information for KMIP based key server. This attribute
                was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Providers.KeyServerInfo.Type.KMIP`.
            """
            self.type = type
            self.description = description
            self.proxy_server = proxy_server
            self.connection_timeout = connection_timeout
            self.kmip_server = kmip_server
            VapiStruct.__init__(self)


        class Type(Enum):
            """
            The ``Providers.KeyServerInfo.Type`` class list the key server types. This
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
            KMIP = None
            """
            Key Management Interoperability Protocol (KMIP) based key management
            server. This class attribute was added in vSphere API 7.0.0.0.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Type` instance.
                """
                Enum.__init__(string)

        Type._set_values({
            'KMIP': Type('KMIP'),
        })
        Type._set_binding_type(type.EnumType(
            'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.key_server_info.type',
            Type))

    KeyServerInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.key_server_info', {
            'type': type.ReferenceType(__name__, 'Providers.KeyServerInfo.Type'),
            'description': type.StringType(),
            'proxy_server': type.OptionalType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress')),
            'connection_timeout': type.OptionalType(type.IntegerType()),
            'kmip_server': type.OptionalType(type.ReferenceType(__name__, 'Providers.KmipServerInfo')),
        },
        KeyServerInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Providers.Info`` class contains attributes that describe the current
        configuration of a provider. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     master_key_id=None,
                     key_server=None,
                     status=None,
                    ):
            """
            :type  master_key_id: :class:`str`
            :param master_key_id: Master key identifier created for the provider. 
                
                A unique Key identifier.. This attribute was added in vSphere API
                7.0.0.0.
            :type  key_server: :class:`Providers.KeyServerInfo`
            :param key_server: Key server associated with this provider. This attribute was added
                in vSphere API 7.0.0.0.
            :type  status: :class:`Providers.Status`
            :param status: Status of the provider in the cluster. This attribute was added in
                vSphere API 7.0.0.0.
            """
            self.master_key_id = master_key_id
            self.key_server = key_server
            self.status = status
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers.info', {
            'master_key_id': type.StringType(),
            'key_server': type.ReferenceType(__name__, 'Providers.KeyServerInfo'),
            'status': type.ReferenceType(__name__, 'Providers.Status'),
        },
        Info,
        False,
        None))




    def list_task(self,
             cluster,
             ):
        """
        Return a list of summary of Key Providers. This method was added in
        vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            For any other error.
        """
        task_id = self._invoke('list$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ListType(type.ReferenceType(__name__, 'Providers.Summary')))
        return task_instance


    def create_task(self,
               cluster,
               spec,
               ):
        """
        Add a new Key Provider. This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`Providers.CreateSpec`
        :param spec: Provider information.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If the provider already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the spec is invalid or cluster id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            For any other error.
        """
        task_id = self._invoke('create$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def update_task(self,
               cluster,
               provider,
               spec,
               ):
        """
        Update an existing Key Provider. This method was added in vSphere API
        7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :type  spec: :class:`Providers.UpdateSpec`
        :param spec: Provider information.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the cluster or provider id is empty, or the spec is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster or provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            For any other error.
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


    def delete_task(self,
               cluster,
               provider,
               ):
        """
        Remove a Key Provider. This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider``.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the cluster or provider id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster or provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            For any other error.
        """
        task_id = self._invoke('delete$task',
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
        Return information about a Key Provider. This method was added in
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
            If the cluster or provider id is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the cluster or provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            For any other error.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                'provider': provider,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Providers.Info'))
        return task_instance
class ServiceStatus(VapiInterface):
    """
    The ``ServiceStatus`` class provides methods to get the Key Provider
    Service health status. This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.service_status'
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
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.service_status.health',
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
        'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.service_status.info', {
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
        Return the Key Provider Service health in the given cluster. This
        method was added in vSphere API 7.0.0.0.

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
class _ProvidersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers',
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
            'spec': type.ReferenceType(__name__, 'Providers.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
            'spec': type.ReferenceType(__name__, 'Providers.UpdateSpec'),
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}',
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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}',
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
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
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
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

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
            url_template='/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/service-status',
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
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.service_status',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Providers': Providers,
        'ServiceStatus': ServiceStatus,
        'providers': 'com.vmware.vcenter.trusted_infrastructure.trust_authority_clusters.kms.providers_client.StubFactory',
    }

