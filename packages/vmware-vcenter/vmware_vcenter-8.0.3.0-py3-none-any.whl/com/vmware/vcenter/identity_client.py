# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.identity.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.identity_client`` module provides classes to manage
VcIdentity.

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

class FederationType(Enum):
    """
    The ``FederationType`` class contains the possible types of federation
    paths for, vCenter Server identity providers configuration. This
    enumeration was added in vSphere API 8.0.1.0.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    DIRECT_FEDERATION = None
    """
    vCenter Server federated directly to the external identity provider. This
    class attribute was added in vSphere API 8.0.1.0.

    """
    INDIRECT_FEDERATION = None
    """
    vCenter Server federated indirectly to the external identity provider, by
    means of an intermediary federation broker. This class attribute was added
    in vSphere API 8.0.1.0.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`FederationType` instance.
        """
        Enum.__init__(string)

FederationType._set_values({
    'DIRECT_FEDERATION': FederationType('DIRECT_FEDERATION'),
    'INDIRECT_FEDERATION': FederationType('INDIRECT_FEDERATION'),
})
FederationType._set_binding_type(type.EnumType(
    'com.vmware.vcenter.identity.federation_type',
    FederationType))




class Providers(VapiInterface):
    """
    The ``Providers`` interface provides methods to list, read and modify
    vCenter Server identity providers. This class was added in vSphere API
    7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.identity.providers'
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

    class ConfigType(Enum):
        """
        The ``Providers.ConfigType`` class contains the possible types of vCenter
        Server identity providers. This enumeration was added in vSphere API
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
        Oauth2 = None
        """
        Config for OAuth2. This class attribute was added in vSphere API 7.0.0.0.

        """
        Oidc = None
        """
        Config for OIDC. This class attribute was added in vSphere API 7.0.0.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ConfigType` instance.
            """
            Enum.__init__(string)

    ConfigType._set_values({
        'Oauth2': ConfigType('Oauth2'),
        'Oidc': ConfigType('Oidc'),
    })
    ConfigType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.identity.providers.config_type',
        ConfigType))


    class IdmProtocol(Enum):
        """
        The ``Providers.IdmProtocol`` class contains the possible types of
        communication protocols to the identity management endpoints. This
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
        REST = None
        """
        REST protocol based identity management endpoints. This class attribute was
        added in vSphere API 7.0.0.0.

        """
        SCIM = None
        """
        SCIM V1.1 protocol based identity management endpoints. This class
        attribute was added in vSphere API 7.0.0.0.

        """
        SCIM2_0 = None
        """
        SCIM V2.0 protocol based identity management endpoints. This class
        attribute was added in vSphere API 7.0.0.0.

        """
        LDAP = None
        """
        LDAP protocol based identity management endpoints. This class attribute was
        added in vSphere API 7.0.0.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`IdmProtocol` instance.
            """
            Enum.__init__(string)

    IdmProtocol._set_values({
        'REST': IdmProtocol('REST'),
        'SCIM': IdmProtocol('SCIM'),
        'SCIM2_0': IdmProtocol('SCIM2_0'),
        'LDAP': IdmProtocol('LDAP'),
    })
    IdmProtocol._set_binding_type(type.EnumType(
        'com.vmware.vcenter.identity.providers.idm_protocol',
        IdmProtocol))


    class Oauth2AuthenticationMethod(Enum):
        """
        The ``Providers.Oauth2AuthenticationMethod`` class contains the possible
        types of OAuth2 authentication methods. This enumeration was added in
        vSphere API 7.0.0.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        CLIENT_SECRET_BASIC = None
        """
        Clients that have received a client_secret value from the Authorization
        Server, authenticate with the Authorization Server in accordance with
        Section 3.2.1 of OAuth 2.0 [RFC6749] using the HTTP Basic authentication
        scheme. This class attribute was added in vSphere API 7.0.0.0.

        """
        CLIENT_SECRET_POST = None
        """
        Clients that have received a client_secret value from the Authorization
        Server, authenticate with the Authorization Server in accordance with
        Section 3.2.1 of OAuth 2.0 [RFC6749] by including the Client Credentials in
        the request body. This class attribute was added in vSphere API 7.0.0.0.

        """
        CLIENT_SECRET_JWT = None
        """
        Clients that have received a client_secret value from the Authorization
        Server, create a JWT using an HMAC SHA algorithm, such as HMAC SHA-256. The
        HMAC (Hash-based Message Authentication Code) is calculated using the
        octets of the UTF-8 representation of the client_secret as the shared key.
        This class attribute was added in vSphere API 7.0.0.0.

        """
        PRIVATE_KEY_JWT = None
        """
        Clients that have registered a public key sign a JWT using that key. The
        client authenticates in accordance with JSON Web Token (JWT) Profile for
        OAuth 2.0 Client Authentication and Authorization Grants [OAuth.JWT] and
        Assertion Framework for OAuth 2.0 Client Authentication and Authorization
        Grants [OAuth.Assertions]. This class attribute was added in vSphere API
        7.0.0.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Oauth2AuthenticationMethod` instance.
            """
            Enum.__init__(string)

    Oauth2AuthenticationMethod._set_values({
        'CLIENT_SECRET_BASIC': Oauth2AuthenticationMethod('CLIENT_SECRET_BASIC'),
        'CLIENT_SECRET_POST': Oauth2AuthenticationMethod('CLIENT_SECRET_POST'),
        'CLIENT_SECRET_JWT': Oauth2AuthenticationMethod('CLIENT_SECRET_JWT'),
        'PRIVATE_KEY_JWT': Oauth2AuthenticationMethod('PRIVATE_KEY_JWT'),
    })
    Oauth2AuthenticationMethod._set_binding_type(type.EnumType(
        'com.vmware.vcenter.identity.providers.oauth2_authentication_method',
        Oauth2AuthenticationMethod))


    class Summary(VapiStruct):
        """
        The ``Providers.Summary`` class contains commonly used information about an
        identity provider. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'config_tag',
                {
                    'Oauth2' : [('oauth2', True)],
                    'Oidc' : [('oidc', True)],
                }
            ),
        ]



        def __init__(self,
                     provider=None,
                     name=None,
                     config_tag=None,
                     oauth2=None,
                     oidc=None,
                     is_default=None,
                     domain_names=None,
                     auth_query_params=None,
                     federation_type=None,
                    ):
            """
            :type  provider: :class:`str`
            :param provider: The identifier of the provider. This attribute was added in vSphere
                API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.identity.Providers``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.identity.Providers``.
            :type  name: :class:`str`
            :param name: The user friendly name for the provider. This attribute was added
                in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  config_tag: :class:`Providers.ConfigType`
            :param config_tag: The config type of the identity provider. This attribute was added
                in vSphere API 7.0.0.0.
            :type  oauth2: :class:`Providers.Oauth2Summary`
            :param oauth2: OAuth2 Summary. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``configTag`` is :attr:`Providers.ConfigType.Oauth2`.
            :type  oidc: :class:`Providers.OidcSummary`
            :param oidc: OIDC Summary. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``configTag`` is :attr:`Providers.ConfigType.Oidc`.
            :type  is_default: :class:`bool`
            :param is_default: Specifies whether the provider is the default provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  domain_names: :class:`set` of :class:`str`
            :param domain_names: Set of fully qualified domain names to trust when federating with
                this identity provider. Tokens from this identity provider will
                only be validated if the user belongs to one of these domains, and
                any domain-qualified groups in the tokens will be filtered to
                include only those groups that belong to one of these domains. If
                domainNames is an empty set, domain validation behavior at login
                with this identity provider will be as follows: the user's domain
                will be parsed from the User Principal Name (UPN) value that is
                found in the tokens returned by the identity provider. This domain
                will then be implicitly trusted and used to filter any groups that
                are also provided in the tokens. This attribute was added in
                vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  auth_query_params: :class:`dict` of :class:`str` and :class:`list` of :class:`str`
            :param auth_query_params: 
                
                key/value pairs that are to be appended to the authEndpoint
                request. 
                
                How to append to authEndpoint request: If the map is not empty, a
                "?" is added to the endpoint URL, and combination of each k and
                each string in the v is added with an "&" delimiter. Details:
                
                * If the value contains only one string, then the key is added with
                  "k=v".
                * If the value is an empty list, then the key is added without a
                  "=v".
                * If the value contains multiple strings, then the key is repeated
                  in the query-string for each string in the value.
                
                . This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  federation_type: :class:`FederationType` or ``None``
            :param federation_type: The type of the identity provider. This attribute was added in
                vSphere API 8.0.1.0.
                If no federation type value set earlier.
            """
            self.provider = provider
            self.name = name
            self.config_tag = config_tag
            self.oauth2 = oauth2
            self.oidc = oidc
            self.is_default = is_default
            self.domain_names = domain_names
            self.auth_query_params = auth_query_params
            self.federation_type = federation_type
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.summary', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.identity.Providers'),
            'name': type.OptionalType(type.StringType()),
            'config_tag': type.ReferenceType(__name__, 'Providers.ConfigType'),
            'oauth2': type.OptionalType(type.ReferenceType(__name__, 'Providers.Oauth2Summary')),
            'oidc': type.OptionalType(type.ReferenceType(__name__, 'Providers.OidcSummary')),
            'is_default': type.BooleanType(),
            'domain_names': type.OptionalType(type.SetType(type.StringType())),
            'auth_query_params': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.StringType()))),
            'federation_type': type.OptionalType(type.ReferenceType(__name__, 'FederationType')),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Providers.Info`` class contains the information about an identity
        provider. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'config_tag',
                {
                    'Oauth2' : [('oauth2', True)],
                    'Oidc' : [('oidc', True)],
                }
            ),
            UnionValidator(
                'idm_protocol',
                {
                    'REST' : [('idm_endpoints', True)],
                    'SCIM' : [('idm_endpoints', True)],
                    'SCIM2_0' : [('idm_endpoints', True)],
                    'LDAP' : [('active_directory_over_ldap', True)],
                }
            ),
        ]



        def __init__(self,
                     name=None,
                     org_ids=None,
                     config_tag=None,
                     oauth2=None,
                     oidc=None,
                     is_default=None,
                     domain_names=None,
                     auth_query_params=None,
                     idm_protocol=None,
                     idm_endpoints=None,
                     active_directory_over_ldap=None,
                     upn_claim=None,
                     groups_claim=None,
                     federation_type=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The user friendly name for the provider. This attribute was added
                in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  org_ids: :class:`set` of :class:`str`
            :param org_ids: The set of orgIds as part of SDDC creation which provides the basis
                for tenancy. This attribute was added in vSphere API 7.0.0.0.
            :type  config_tag: :class:`Providers.ConfigType`
            :param config_tag: The config type of the identity provider. This attribute was added
                in vSphere API 7.0.0.0.
            :type  oauth2: :class:`Providers.Oauth2Info`
            :param oauth2: OAuth2 Info. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``configTag`` is :attr:`Providers.ConfigType.Oauth2`.
            :type  oidc: :class:`Providers.OidcInfo`
            :param oidc: OIDC Info. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``configTag`` is :attr:`Providers.ConfigType.Oidc`.
            :type  is_default: :class:`bool`
            :param is_default: Specifies whether the provider is the default provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  domain_names: :class:`set` of :class:`str`
            :param domain_names: Set of fully qualified domain names to trust when federating with
                this identity provider. Tokens from this identity provider will
                only be validated if the user belongs to one of these domains, and
                any domain-qualified groups in the tokens will be filtered to
                include only those groups that belong to one of these domains. If
                domainNames is an empty set, domain validation behavior at login
                with this identity provider will be as follows: the user's domain
                will be parsed from the User Principal Name (UPN) value that is
                found in the tokens returned by the identity provider. This domain
                will then be implicitly trusted and used to filter any groups that
                are also provided in the tokens. This attribute was added in
                vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  auth_query_params: :class:`dict` of :class:`str` and :class:`list` of :class:`str`
            :param auth_query_params: 
                
                key/value pairs that are to be appended to the authEndpoint
                request. 
                
                How to append to authEndpoint request: If the map is not empty, a
                "?" is added to the endpoint URL, and combination of each k and
                each string in the v is added with an "&" delimiter. Details:
                
                * If the value contains only one string, then the key is added with
                  "k=v".
                * If the value is an empty list, then the key is added without a
                  "=v".
                * If the value contains multiple strings, then the key is repeated
                  in the query-string for each string in the value.
                
                . This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  idm_protocol: :class:`Providers.IdmProtocol` or ``None``
            :param idm_protocol: Communication protocol to the identity management endpoints. This
                attribute was added in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  idm_endpoints: :class:`list` of :class:`str`
            :param idm_endpoints: Identity management endpoints. This attribute was added in vSphere
                API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``idmProtocol`` is one of :attr:`Providers.IdmProtocol.REST`,
                :attr:`Providers.IdmProtocol.SCIM`, or
                :attr:`Providers.IdmProtocol.SCIM2_0`.
            :type  active_directory_over_ldap: :class:`Providers.ActiveDirectoryOverLdap`
            :param active_directory_over_ldap: Identity management configuration. This attribute was added in
                vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``idmProtocol`` is :attr:`Providers.IdmProtocol.LDAP`.
            :type  upn_claim: :class:`str`
            :param upn_claim: Specifies which claim provides the user principal name (UPN) for
                the user. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  groups_claim: :class:`str`
            :param groups_claim: Specifies which claim provides the group membership for the token
                subject. If empty, the default behavior for CSP is used. In this
                case, the groups for the subject will be comprised of the groups in
                'group_names' and 'group_ids' claims. This attribute was added in
                vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  federation_type: :class:`FederationType` or ``None``
            :param federation_type: The type of the identity provider. This attribute was added in
                vSphere API 8.0.1.0.
                If no federation type value set earlier.
            """
            self.name = name
            self.org_ids = org_ids
            self.config_tag = config_tag
            self.oauth2 = oauth2
            self.oidc = oidc
            self.is_default = is_default
            self.domain_names = domain_names
            self.auth_query_params = auth_query_params
            self.idm_protocol = idm_protocol
            self.idm_endpoints = idm_endpoints
            self.active_directory_over_ldap = active_directory_over_ldap
            self.upn_claim = upn_claim
            self.groups_claim = groups_claim
            self.federation_type = federation_type
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.info', {
            'name': type.OptionalType(type.StringType()),
            'org_ids': type.SetType(type.StringType()),
            'config_tag': type.ReferenceType(__name__, 'Providers.ConfigType'),
            'oauth2': type.OptionalType(type.ReferenceType(__name__, 'Providers.Oauth2Info')),
            'oidc': type.OptionalType(type.ReferenceType(__name__, 'Providers.OidcInfo')),
            'is_default': type.BooleanType(),
            'domain_names': type.OptionalType(type.SetType(type.StringType())),
            'auth_query_params': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.StringType()))),
            'idm_protocol': type.OptionalType(type.ReferenceType(__name__, 'Providers.IdmProtocol')),
            'idm_endpoints': type.OptionalType(type.ListType(type.URIType())),
            'active_directory_over_ldap': type.OptionalType(type.ReferenceType(__name__, 'Providers.ActiveDirectoryOverLdap')),
            'upn_claim': type.OptionalType(type.StringType()),
            'groups_claim': type.OptionalType(type.StringType()),
            'federation_type': type.OptionalType(type.ReferenceType(__name__, 'FederationType')),
        },
        Info,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Providers.CreateSpec`` class contains the information used to create
        an identity provider. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'config_tag',
                {
                    'Oauth2' : [('oauth2', True)],
                    'Oidc' : [('oidc', True)],
                }
            ),
            UnionValidator(
                'idm_protocol',
                {
                    'REST' : [('idm_endpoints', True)],
                    'SCIM' : [('idm_endpoints', True)],
                    'SCIM2_0' : [('idm_endpoints', True)],
                    'LDAP' : [('active_directory_over_ldap', True)],
                }
            ),
        ]



        def __init__(self,
                     config_tag=None,
                     oauth2=None,
                     oidc=None,
                     org_ids=None,
                     is_default=None,
                     name=None,
                     domain_names=None,
                     auth_query_params=None,
                     idm_protocol=None,
                     idm_endpoints=None,
                     active_directory_over_ldap=None,
                     upn_claim=None,
                     groups_claim=None,
                     federation_type=None,
                    ):
            """
            :type  config_tag: :class:`Providers.ConfigType`
            :param config_tag: The config type of the identity provider. This attribute was added
                in vSphere API 7.0.0.0.
            :type  oauth2: :class:`Providers.Oauth2CreateSpec`
            :param oauth2: OAuth2 CreateSpec. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``configTag`` is :attr:`Providers.ConfigType.Oauth2`.
            :type  oidc: :class:`Providers.OidcCreateSpec`
            :param oidc: OIDC CreateSpec. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``configTag`` is :attr:`Providers.ConfigType.Oidc`.
            :type  org_ids: :class:`set` of :class:`str` or ``None``
            :param org_ids: The set of orgIds as part of SDDC creation which provides the basis
                for tenancy. This attribute was added in vSphere API 7.0.0.0.
                If None, the set will be empty.
            :type  is_default: :class:`bool` or ``None``
            :param is_default: Specifies whether the provider is the default provider. Setting
                ``isDefault`` of current provider to True makes all other providers
                non-default. If no other providers created in this vCenter Server
                before, this parameter will be disregarded, and the provider will
                always be set to the default. This attribute was added in vSphere
                API 7.0.0.0.
                If None the provider will be the default provider if it is the
                first provider that is created, and will not be the default
                provider otherwise.
            :type  name: :class:`str` or ``None``
            :param name: The user friendly name for the provider. This name can be used for
                human-readable identification purposes, but it does not have to be
                unique, as the system will use internal UUIDs to differentiate
                providers. This attribute was added in vSphere API 7.0.0.0.
                If None, the name will be the empty string
            :type  domain_names: :class:`set` of :class:`str` or ``None``
            :param domain_names: Set of fully qualified domain names to trust when federating with
                this identity provider. Tokens from this identity provider will
                only be validated if the user belongs to one of these domains, and
                any domain-qualified groups in the tokens will be filtered to
                include only those groups that belong to one of these domains. This
                attribute was added in vSphere API 7.0.0.0.
                If None, domainNames will be the empty set and the domain
                validation behavior at login with this identity provider will be as
                follows: the user's domain will be parsed from the User Principal
                Name (UPN) value that is found in the tokens returned by the
                identity provider. This domain will then be implicitly trusted and
                used to filter any groups that are also provided in the tokens.
            :type  auth_query_params: (:class:`dict` of :class:`str` and :class:`list` of :class:`str`) or ``None``
            :param auth_query_params: 
                
                key/value pairs that are to be appended to the authEndpoint
                request. 
                
                How to append to authEndpoint request: If the map is not empty, a
                "?" is added to the endpoint URL, and combination of each k and
                each string in the v is added with an "&" delimiter. Details:
                
                * If the value contains only one string, then the key is added with
                  "k=v".
                * If the value is an empty list, then the key is added without a
                  "=v".
                * If the value contains multiple strings, then the key is repeated
                  in the query-string for each string in the value.
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, the map will be empty.
            :type  idm_protocol: :class:`Providers.IdmProtocol` or ``None``
            :param idm_protocol: Communication protocol to the identity management endpoints. This
                attribute was added in vSphere API 7.0.0.0.
                If None, no communication protocol will be configured for the
                identity provider.
            :type  idm_endpoints: :class:`list` of :class:`str`
            :param idm_endpoints: Identity management endpoints. When specified, at least one
                endpoint must be provided. This attribute was added in vSphere API
                7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``idmProtocol`` is one of :attr:`Providers.IdmProtocol.REST`,
                :attr:`Providers.IdmProtocol.SCIM`, or
                :attr:`Providers.IdmProtocol.SCIM2_0`.
            :type  active_directory_over_ldap: :class:`Providers.ActiveDirectoryOverLdap`
            :param active_directory_over_ldap: Identity management configuration. If the protocol is LDAP, the
                configuration must be set, else InvalidArgument is thrown. This
                attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``idmProtocol`` is :attr:`Providers.IdmProtocol.LDAP`.
            :type  upn_claim: :class:`str` or ``None``
            :param upn_claim: Specifies which claim provides the user principal name (UPN) for
                the user. This attribute was added in vSphere API 7.0.0.0.
                If None, the claim named 'acct' will be used to provide backwards
                compatibility with CSP.
            :type  groups_claim: :class:`str` or ``None``
            :param groups_claim: Specifies which claim provides the group membership for the token
                subject. These groups will be used for mapping to local groups per
                the claim map. This attribute was added in vSphere API 7.0.0.0.
                If None, the default behavior will be CSP backwards compatiblility.
                The groups for the subject will be comprised of the groups in
                'group_names' and 'group_ids' claims.
            :type  federation_type: :class:`FederationType` or ``None``
            :param federation_type: The type of the identity provider. This attribute was added in
                vSphere API 8.0.1.0.
                If None, the federation type value will not be set.
            """
            self.config_tag = config_tag
            self.oauth2 = oauth2
            self.oidc = oidc
            self.org_ids = org_ids
            self.is_default = is_default
            self.name = name
            self.domain_names = domain_names
            self.auth_query_params = auth_query_params
            self.idm_protocol = idm_protocol
            self.idm_endpoints = idm_endpoints
            self.active_directory_over_ldap = active_directory_over_ldap
            self.upn_claim = upn_claim
            self.groups_claim = groups_claim
            self.federation_type = federation_type
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.create_spec', {
            'config_tag': type.ReferenceType(__name__, 'Providers.ConfigType'),
            'oauth2': type.OptionalType(type.ReferenceType(__name__, 'Providers.Oauth2CreateSpec')),
            'oidc': type.OptionalType(type.ReferenceType(__name__, 'Providers.OidcCreateSpec')),
            'org_ids': type.OptionalType(type.SetType(type.StringType())),
            'is_default': type.OptionalType(type.BooleanType()),
            'name': type.OptionalType(type.StringType()),
            'domain_names': type.OptionalType(type.SetType(type.StringType())),
            'auth_query_params': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.StringType()))),
            'idm_protocol': type.OptionalType(type.ReferenceType(__name__, 'Providers.IdmProtocol')),
            'idm_endpoints': type.OptionalType(type.ListType(type.URIType())),
            'active_directory_over_ldap': type.OptionalType(type.ReferenceType(__name__, 'Providers.ActiveDirectoryOverLdap')),
            'upn_claim': type.OptionalType(type.StringType()),
            'groups_claim': type.OptionalType(type.StringType()),
            'federation_type': type.OptionalType(type.ReferenceType(__name__, 'FederationType')),
        },
        CreateSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Providers.UpdateSpec`` class contains the information used to update
        the identity provider. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'config_tag',
                {
                    'Oauth2' : [('oauth2', True)],
                    'Oidc' : [('oidc', True)],
                }
            ),
            UnionValidator(
                'idm_protocol',
                {
                    'REST' : [('idm_endpoints', True)],
                    'SCIM' : [('idm_endpoints', True)],
                    'SCIM2_0' : [('idm_endpoints', True)],
                    'LDAP' : [('active_directory_over_ldap', True)],
                }
            ),
        ]



        def __init__(self,
                     config_tag=None,
                     oauth2=None,
                     oidc=None,
                     org_ids=None,
                     make_default=None,
                     name=None,
                     domain_names=None,
                     auth_query_params=None,
                     idm_protocol=None,
                     idm_endpoints=None,
                     active_directory_over_ldap=None,
                     upn_claim=None,
                     reset_upn_claim=None,
                     groups_claim=None,
                     reset_groups_claim=None,
                     federation_type=None,
                    ):
            """
            :type  config_tag: :class:`Providers.ConfigType`
            :param config_tag: The config type of the identity provider. This attribute was added
                in vSphere API 7.0.0.0.
            :type  oauth2: :class:`Providers.Oauth2UpdateSpec`
            :param oauth2: OAuth2 UpdateSpec. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``configTag`` is :attr:`Providers.ConfigType.Oauth2`.
            :type  oidc: :class:`Providers.OidcUpdateSpec`
            :param oidc: OIDC UpdateSpec. This attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``configTag`` is :attr:`Providers.ConfigType.Oidc`.
            :type  org_ids: :class:`set` of :class:`str` or ``None``
            :param org_ids: The set orgIds as part of SDDC creation which provides the basis
                for tenancy. This attribute was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  make_default: :class:`bool` or ``None``
            :param make_default: Specifies whether to make this the default provider. If
                ``makeDefault`` is set to true, this provider will be flagged as
                the default provider and any other providers that had previously
                been flagged as the default will be made non-default. If
                ``makeDefault`` is set to false, this provider's default flag will
                not be modified. This attribute was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  name: :class:`str` or ``None``
            :param name: The user friendly name for the provider. This name can be used for
                human-readable identification purposes, but it does not have to be
                unique, as the system will use internal UUIDs to differentiate
                providers. This attribute was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  domain_names: :class:`set` of :class:`str` or ``None``
            :param domain_names: Set of fully qualified domain names to trust when federating with
                this identity provider. Tokens from this identity provider will
                only be validated if the user belongs to one of these domains, and
                any domain-qualified groups in the tokens will be filtered to
                include only those groups that belong to one of these domains. This
                attribute was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged. If domainNames is an empty set,
                domain validation behavior at login with this identity provider
                will be as follows: the user's domain will be parsed from the User
                Principal Name (UPN) value that is found in the tokens returned by
                the identity provider. This domain will then be implicitly trusted
                and used to filter any groups that are also provided in the tokens.
            :type  auth_query_params: (:class:`dict` of :class:`str` and :class:`list` of :class:`str`) or ``None``
            :param auth_query_params: key/value pairs that are to be appended to the authEndpoint
                request. How to append to authEndpoint request: If the map is not
                empty, a "?" is added to the endpoint URL, and combination of each
                k and each string in the v is added with an "&" delimiter. Details:
                If the value contains only one string, then the key is added with
                "k=v". If the value is an empty list, then the key is added without
                a "=v". If the value contains multiple strings, then the key is
                repeated in the query-string for each string in the value. If the
                map is empty, deletes all params. This attribute was added in
                vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  idm_protocol: :class:`Providers.IdmProtocol` or ``None``
            :param idm_protocol: The protocol to communicate to the identity management endpoints.
                This attribute was added in vSphere API 7.0.0.0.
                If None, leave value unchanged.
            :type  idm_endpoints: :class:`list` of :class:`str`
            :param idm_endpoints: Identity management endpoints. When specified, at least one
                endpoint must be provided. This attribute was added in vSphere API
                7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``idmProtocol`` is one of :attr:`Providers.IdmProtocol.REST`,
                :attr:`Providers.IdmProtocol.SCIM`, or
                :attr:`Providers.IdmProtocol.SCIM2_0`.
            :type  active_directory_over_ldap: :class:`Providers.ActiveDirectoryOverLdap`
            :param active_directory_over_ldap: Identity management configuration. If the protocol is LDAP, the
                configuration must be set, else InvalidArgument is thrown. This
                attribute was added in vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``idmProtocol`` is :attr:`Providers.IdmProtocol.LDAP`.
            :type  upn_claim: :class:`str` or ``None``
            :param upn_claim: Specifies which claim provides the user principal name (UPN) for
                the subject of the token. This attribute was added in vSphere API
                7.0.0.0.
                If None, leaves value unchanged.
            :type  reset_upn_claim: :class:`bool` or ``None``
            :param reset_upn_claim: Flag indicating whether the user principal name (UPN) claim should
                be set back to its default value. If this field is set to ``true``,
                the user principal name (UPN) claim will be set to 'acct', which is
                used for backwards compatibility with CSP. If this field is set to
                ``false``, the existing user principal name (UPN) claim will be
                changed to the value specified in
                :attr:`Providers.UpdateSpec.upn_claim`, if any. This attribute was
                added in vSphere API 7.0.0.0.
                If None, the existing user principal name (UPN) claim will be
                changed to the value specified in
                :attr:`Providers.UpdateSpec.upn_claim`, if any.
            :type  groups_claim: :class:`str` or ``None``
            :param groups_claim: Specifies which claim provides the group membership for the token
                subject. This attribute was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  reset_groups_claim: :class:`bool` or ``None``
            :param reset_groups_claim: Flag indicating whether any existing groups claim value should be
                removed. If this field is set to ``true``, the existing groups
                claim value is removed which defaults to backwards compatibility
                with CSP. In this case, the groups for the subject will be
                comprised of the groups in 'group_names' and 'group_ids' claims. If
                this field is set to ``false``, the existing groups claim will be
                changed to the value specified in
                :attr:`Providers.UpdateSpec.groups_claim`, if any. This attribute
                was added in vSphere API 7.0.0.0.
                If None, the existing groups claim will be changed to the value
                specified in :attr:`Providers.UpdateSpec.groups_claim`, if any.
            :type  federation_type: :class:`FederationType` or ``None``
            :param federation_type: The type of the identity provider. This attribute was added in
                vSphere API 8.0.1.0.
                If None, leaves value unchanged.
            """
            self.config_tag = config_tag
            self.oauth2 = oauth2
            self.oidc = oidc
            self.org_ids = org_ids
            self.make_default = make_default
            self.name = name
            self.domain_names = domain_names
            self.auth_query_params = auth_query_params
            self.idm_protocol = idm_protocol
            self.idm_endpoints = idm_endpoints
            self.active_directory_over_ldap = active_directory_over_ldap
            self.upn_claim = upn_claim
            self.reset_upn_claim = reset_upn_claim
            self.groups_claim = groups_claim
            self.reset_groups_claim = reset_groups_claim
            self.federation_type = federation_type
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.update_spec', {
            'config_tag': type.ReferenceType(__name__, 'Providers.ConfigType'),
            'oauth2': type.OptionalType(type.ReferenceType(__name__, 'Providers.Oauth2UpdateSpec')),
            'oidc': type.OptionalType(type.ReferenceType(__name__, 'Providers.OidcUpdateSpec')),
            'org_ids': type.OptionalType(type.SetType(type.StringType())),
            'make_default': type.OptionalType(type.BooleanType()),
            'name': type.OptionalType(type.StringType()),
            'domain_names': type.OptionalType(type.SetType(type.StringType())),
            'auth_query_params': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.StringType()))),
            'idm_protocol': type.OptionalType(type.ReferenceType(__name__, 'Providers.IdmProtocol')),
            'idm_endpoints': type.OptionalType(type.ListType(type.URIType())),
            'active_directory_over_ldap': type.OptionalType(type.ReferenceType(__name__, 'Providers.ActiveDirectoryOverLdap')),
            'upn_claim': type.OptionalType(type.StringType()),
            'reset_upn_claim': type.OptionalType(type.BooleanType()),
            'groups_claim': type.OptionalType(type.StringType()),
            'reset_groups_claim': type.OptionalType(type.BooleanType()),
            'federation_type': type.OptionalType(type.ReferenceType(__name__, 'FederationType')),
        },
        UpdateSpec,
        False,
        None))


    class Oauth2Summary(VapiStruct):
        """
        The ``Providers.Oauth2Summary`` class contains commonly used information
        about an OAuth2 identity provider. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     auth_endpoint=None,
                     token_endpoint=None,
                     client_id=None,
                     authentication_header=None,
                     auth_query_params=None,
                    ):
            """
            :type  auth_endpoint: :class:`str`
            :param auth_endpoint: Authentication/authorization endpoint of the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  token_endpoint: :class:`str`
            :param token_endpoint: Token endpoint of the provider. This attribute was added in vSphere
                API 7.0.0.0.
            :type  client_id: :class:`str`
            :param client_id: Client identifier to connect to the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  authentication_header: :class:`str`
            :param authentication_header: The authentication data used as part of request header to acquire
                or refresh an OAuth2 token. The data format depends on the
                authentication method used. Example of basic authentication format:
                Authorization: Basic [base64Encode(clientId + ":" + secret)]. This
                attribute was added in vSphere API 7.0.0.0.
            :type  auth_query_params: :class:`dict` of :class:`str` and :class:`list` of :class:`str`
            :param auth_query_params: 
                
                key/value pairs that are to be appended to the authEndpoint
                request. 
                
                How to append to authEndpoint request: If the map is not empty, a
                "?" is added to the endpoint URL, and combination of each k and
                each string in the v is added with an "&" delimiter. Details:
                
                * If the value contains only one string, then the key is added with
                  "k=v".
                * If the value is an empty list, then the key is added without a
                  "=v".
                * If the value contains multiple strings, then the key is repeated
                  in the query-string for each string in the value.
                
                . This attribute was added in vSphere API 7.0.0.0.
            """
            self.auth_endpoint = auth_endpoint
            self.token_endpoint = token_endpoint
            self.client_id = client_id
            self.authentication_header = authentication_header
            self.auth_query_params = auth_query_params
            VapiStruct.__init__(self)


    Oauth2Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.oauth2_summary', {
            'auth_endpoint': type.URIType(),
            'token_endpoint': type.URIType(),
            'client_id': type.StringType(),
            'authentication_header': type.StringType(),
            'auth_query_params': type.MapType(type.StringType(), type.ListType(type.StringType())),
        },
        Oauth2Summary,
        False,
        None))


    class Oauth2Info(VapiStruct):
        """
        The ``Providers.Oauth2Info`` class contains the information about an OAuth2
        identity provider. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     auth_endpoint=None,
                     token_endpoint=None,
                     public_key_uri=None,
                     client_id=None,
                     client_secret=None,
                     claim_map=None,
                     issuer=None,
                     authentication_method=None,
                     auth_query_params=None,
                    ):
            """
            :type  auth_endpoint: :class:`str`
            :param auth_endpoint: Authentication/authorization endpoint of the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  token_endpoint: :class:`str`
            :param token_endpoint: Token endpoint of the provider. This attribute was added in vSphere
                API 7.0.0.0.
            :type  public_key_uri: :class:`str`
            :param public_key_uri: Endpoint to retrieve the provider public key for validation. This
                attribute was added in vSphere API 7.0.0.0.
            :type  client_id: :class:`str`
            :param client_id: Client identifier to connect to the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  client_secret: :class:`str`
            :param client_secret: The secret shared between the client and the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  claim_map: :class:`dict` of :class:`str` and (:class:`dict` of :class:`str` and :class:`list` of :class:`str`)
            :param claim_map: The map used to transform an OAuth2 claim to a corresponding claim
                that vCenter Server understands. Currently only the key "perms" is
                supported. The key "perms" is used for mapping the "perms" claim of
                incoming JWT. The value is another map with an external group as
                the key and a vCenter Server group as value. This attribute was
                added in vSphere API 7.0.0.0.
            :type  issuer: :class:`str`
            :param issuer: The identity provider namespace. It is used to validate the issuer
                in the acquired OAuth2 token. This attribute was added in vSphere
                API 7.0.0.0.
            :type  authentication_method: :class:`Providers.Oauth2AuthenticationMethod`
            :param authentication_method: Authentication method used by the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  auth_query_params: :class:`dict` of :class:`str` and :class:`list` of :class:`str`
            :param auth_query_params: 
                
                key/value pairs that are to be appended to the authEndpoint
                request. 
                
                How to append to authEndpoint request: If the map is not empty, a
                "?" is added to the endpoint URL, and combination of each k and
                each string in the v is added with an "&" delimiter. Details:
                
                * If the value contains only one string, then the key is added with
                  "k=v".
                * If the value is an empty list, then the key is added without a
                  "=v".
                * If the value contains multiple strings, then the key is repeated
                  in the query-string for each string in the value.
                
                . This attribute was added in vSphere API 7.0.0.0.
            """
            self.auth_endpoint = auth_endpoint
            self.token_endpoint = token_endpoint
            self.public_key_uri = public_key_uri
            self.client_id = client_id
            self.client_secret = client_secret
            self.claim_map = claim_map
            self.issuer = issuer
            self.authentication_method = authentication_method
            self.auth_query_params = auth_query_params
            VapiStruct.__init__(self)


    Oauth2Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.oauth2_info', {
            'auth_endpoint': type.URIType(),
            'token_endpoint': type.URIType(),
            'public_key_uri': type.URIType(),
            'client_id': type.StringType(),
            'client_secret': type.StringType(),
            'claim_map': type.MapType(type.StringType(), type.MapType(type.StringType(), type.ListType(type.StringType()))),
            'issuer': type.StringType(),
            'authentication_method': type.ReferenceType(__name__, 'Providers.Oauth2AuthenticationMethod'),
            'auth_query_params': type.MapType(type.StringType(), type.ListType(type.StringType())),
        },
        Oauth2Info,
        False,
        None))


    class Oauth2CreateSpec(VapiStruct):
        """
        The ``Providers.Oauth2CreateSpec`` class contains the information used to
        create an OAuth2 identity provider. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     auth_endpoint=None,
                     token_endpoint=None,
                     public_key_uri=None,
                     client_id=None,
                     client_secret=None,
                     claim_map=None,
                     issuer=None,
                     authentication_method=None,
                     auth_query_params=None,
                    ):
            """
            :type  auth_endpoint: :class:`str`
            :param auth_endpoint: Authentication/authorization endpoint of the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  token_endpoint: :class:`str`
            :param token_endpoint: Token endpoint of the provider. This attribute was added in vSphere
                API 7.0.0.0.
            :type  public_key_uri: :class:`str`
            :param public_key_uri: Endpoint to retrieve the provider public key for validation. This
                attribute was added in vSphere API 7.0.0.0.
            :type  client_id: :class:`str`
            :param client_id: Client identifier to connect to the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  client_secret: :class:`str`
            :param client_secret: The secret shared between the client and the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  claim_map: :class:`dict` of :class:`str` and (:class:`dict` of :class:`str` and :class:`list` of :class:`str`)
            :param claim_map: The map used to transform an OAuth2 claim to a corresponding claim
                that vCenter Server understands. Currently only the key "perms" is
                supported. The key "perms" is used for mapping the "perms" claim of
                incoming JWT. The value is another map with an external group as
                the key and a vCenter Server group as value. This attribute was
                added in vSphere API 7.0.0.0.
            :type  issuer: :class:`str`
            :param issuer: The identity provider namespace. It is used to validate the issuer
                in the acquired OAuth2 token. This attribute was added in vSphere
                API 7.0.0.0.
            :type  authentication_method: :class:`Providers.Oauth2AuthenticationMethod`
            :param authentication_method: Authentication method used by the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  auth_query_params: (:class:`dict` of :class:`str` and :class:`list` of :class:`str`) or ``None``
            :param auth_query_params: 
                
                key/value pairs that are to be appended to the authEndpoint
                request. 
                
                How to append to authEndpoint request: If the map is not empty, a
                "?" is added to the endpoint URL, and combination of each k and
                each string in the v is added with an "&" delimiter. Details:
                
                * If the value contains only one string, then the key is added with
                  "k=v".
                * If the value is an empty list, then the key is added without a
                  "=v".
                * If the value contains multiple strings, then the key is repeated
                  in the query-string for each string in the value.
                
                . This attribute was added in vSphere API 7.0.0.0.
                If None, the map will be empty.
            """
            self.auth_endpoint = auth_endpoint
            self.token_endpoint = token_endpoint
            self.public_key_uri = public_key_uri
            self.client_id = client_id
            self.client_secret = client_secret
            self.claim_map = claim_map
            self.issuer = issuer
            self.authentication_method = authentication_method
            self.auth_query_params = auth_query_params
            VapiStruct.__init__(self)


    Oauth2CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.oauth2_create_spec', {
            'auth_endpoint': type.URIType(),
            'token_endpoint': type.URIType(),
            'public_key_uri': type.URIType(),
            'client_id': type.StringType(),
            'client_secret': type.StringType(),
            'claim_map': type.MapType(type.StringType(), type.MapType(type.StringType(), type.ListType(type.StringType()))),
            'issuer': type.StringType(),
            'authentication_method': type.ReferenceType(__name__, 'Providers.Oauth2AuthenticationMethod'),
            'auth_query_params': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.StringType()))),
        },
        Oauth2CreateSpec,
        False,
        None))


    class Oauth2UpdateSpec(VapiStruct):
        """
        The ``Providers.Oauth2UpdateSpec`` class contains the information used to
        update the OAuth2 identity provider. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     auth_endpoint=None,
                     token_endpoint=None,
                     public_key_uri=None,
                     client_id=None,
                     client_secret=None,
                     claim_map=None,
                     issuer=None,
                     authentication_method=None,
                     auth_query_params=None,
                    ):
            """
            :type  auth_endpoint: :class:`str` or ``None``
            :param auth_endpoint: Authentication/authorization endpoint of the provider. This
                attribute was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  token_endpoint: :class:`str` or ``None``
            :param token_endpoint: Token endpoint of the provider. This attribute was added in vSphere
                API 7.0.0.0.
                If None, leaves value unchanged.
            :type  public_key_uri: :class:`str` or ``None``
            :param public_key_uri: Endpoint to retrieve the provider public key for validation. This
                attribute was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  client_id: :class:`str` or ``None``
            :param client_id: Client identifier to connect to the provider. This attribute was
                added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  client_secret: :class:`str` or ``None``
            :param client_secret: Shared secret between identity provider and client. This attribute
                was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  claim_map: (:class:`dict` of :class:`str` and (:class:`dict` of :class:`str` and :class:`list` of :class:`str`)) or ``None``
            :param claim_map: The map used to transform an OAuth2 claim to a corresponding claim
                that vCenter Server understands. Currently only the key "perms" is
                supported. The key "perms" is used for mapping the "perms" claim of
                incoming JWT. The value is another map with an external group as
                the key and a vCenter Server group as value. This attribute was
                added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  issuer: :class:`str` or ``None``
            :param issuer: The identity provider namespace. It is used to validate the issuer
                in the acquired OAuth2 token. This attribute was added in vSphere
                API 7.0.0.0.
                If None, leaves value unchanged.
            :type  authentication_method: :class:`Providers.Oauth2AuthenticationMethod` or ``None``
            :param authentication_method: Authentication method used by the provider. This attribute was
                added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  auth_query_params: (:class:`dict` of :class:`str` and :class:`list` of :class:`str`) or ``None``
            :param auth_query_params: key/value pairs that are to be appended to the authEndpoint
                request. How to append to authEndpoint request: If the map is not
                empty, a "?" is added to the endpoint URL, and combination of each
                k and each string in the v is added with an "&" delimiter. Details:
                If the value contains only one string, then the key is added with
                "k=v". If the value is an empty list, then the key is added without
                a "=v". If the value contains multiple strings, then the key is
                repeated in the query-string for each string in the value. If the
                map is empty, deletes all params. This attribute was added in
                vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            """
            self.auth_endpoint = auth_endpoint
            self.token_endpoint = token_endpoint
            self.public_key_uri = public_key_uri
            self.client_id = client_id
            self.client_secret = client_secret
            self.claim_map = claim_map
            self.issuer = issuer
            self.authentication_method = authentication_method
            self.auth_query_params = auth_query_params
            VapiStruct.__init__(self)


    Oauth2UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.oauth2_update_spec', {
            'auth_endpoint': type.OptionalType(type.URIType()),
            'token_endpoint': type.OptionalType(type.URIType()),
            'public_key_uri': type.OptionalType(type.URIType()),
            'client_id': type.OptionalType(type.StringType()),
            'client_secret': type.OptionalType(type.StringType()),
            'claim_map': type.OptionalType(type.MapType(type.StringType(), type.MapType(type.StringType(), type.ListType(type.StringType())))),
            'issuer': type.OptionalType(type.StringType()),
            'authentication_method': type.OptionalType(type.ReferenceType(__name__, 'Providers.Oauth2AuthenticationMethod')),
            'auth_query_params': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.StringType()))),
        },
        Oauth2UpdateSpec,
        False,
        None))


    class OidcSummary(VapiStruct):
        """
        The ``Providers.OidcSummary`` class contains commonly used information
        about an OIDC identity provider. OIDC is a discovery protocol for OAuth2
        configuration metadata, so ``Providers.OidcSummary`` contains discovered
        OAuth2 metadata. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     discovery_endpoint=None,
                     logout_endpoint=None,
                     auth_endpoint=None,
                     token_endpoint=None,
                     client_id=None,
                     authentication_header=None,
                     auth_query_params=None,
                    ):
            """
            :type  discovery_endpoint: :class:`str`
            :param discovery_endpoint: Endpoint to retrieve the provider metadata. This attribute was
                added in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  logout_endpoint: :class:`str`
            :param logout_endpoint: The endpoint to use for terminating the user's session at the
                identity provider. This value is automatically derived from the
                metadata information provided by the OIDC discovery endpoint. This
                attribute was added in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  auth_endpoint: :class:`str`
            :param auth_endpoint: Authentication/authorization endpoint of the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  token_endpoint: :class:`str`
            :param token_endpoint: Token endpoint of the provider. This attribute was added in vSphere
                API 7.0.0.0.
            :type  client_id: :class:`str`
            :param client_id: Client identifier to connect to the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  authentication_header: :class:`str`
            :param authentication_header: The authentication data used as part of request header to acquire
                or refresh an OAuth2 token. The data format depends on the
                authentication method used. Example of basic authentication format:
                Authorization: Basic [base64Encode(clientId + ":" + secret)]. This
                attribute was added in vSphere API 7.0.0.0.
            :type  auth_query_params: :class:`dict` of :class:`str` and :class:`list` of :class:`str`
            :param auth_query_params: 
                
                key/value pairs that are to be appended to the authEndpoint
                request. 
                
                How to append to authEndpoint request: If the map is not empty, a
                "?" is added to the endpoint URL, and combination of each k and
                each string in the v is added with an "&" delimiter. Details:
                
                * If the value contains only one string, then the key is added with
                  "k=v".
                * If the value is an empty list, then the key is added without a
                  "=v".
                * If the value contains multiple strings, then the key is repeated
                  in the query-string for each string in the value.
                
                . This attribute was added in vSphere API 7.0.0.0.
            """
            self.discovery_endpoint = discovery_endpoint
            self.logout_endpoint = logout_endpoint
            self.auth_endpoint = auth_endpoint
            self.token_endpoint = token_endpoint
            self.client_id = client_id
            self.authentication_header = authentication_header
            self.auth_query_params = auth_query_params
            VapiStruct.__init__(self)


    OidcSummary._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.oidc_summary', {
            'discovery_endpoint': type.OptionalType(type.URIType()),
            'logout_endpoint': type.OptionalType(type.URIType()),
            'auth_endpoint': type.URIType(),
            'token_endpoint': type.URIType(),
            'client_id': type.StringType(),
            'authentication_header': type.StringType(),
            'auth_query_params': type.MapType(type.StringType(), type.ListType(type.StringType())),
        },
        OidcSummary,
        False,
        None))


    class OidcInfo(VapiStruct):
        """
        The ``Providers.OidcInfo`` class contains information about an OIDC
        identity provider. OIDC is a discovery protocol for OAuth2 configuration
        metadata, so ``Providers.OidcInfo`` contains additional discovered OAuth2
        metadata. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     discovery_endpoint=None,
                     logout_endpoint=None,
                     auth_endpoint=None,
                     token_endpoint=None,
                     public_key_uri=None,
                     client_id=None,
                     client_secret=None,
                     claim_map=None,
                     issuer=None,
                     authentication_method=None,
                     auth_query_params=None,
                    ):
            """
            :type  discovery_endpoint: :class:`str`
            :param discovery_endpoint: Endpoint to retrieve the provider metadata. This attribute was
                added in vSphere API 7.0.0.0.
            :type  logout_endpoint: :class:`str`
            :param logout_endpoint: The endpoint to use for terminating the user's session at the
                identity provider. This value is automatically derived from the
                metadata information provided by the OIDC discovery endpoint. This
                attribute was added in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  auth_endpoint: :class:`str`
            :param auth_endpoint: Authentication/authorization endpoint of the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  token_endpoint: :class:`str`
            :param token_endpoint: Token endpoint of the provider. This attribute was added in vSphere
                API 7.0.0.0.
            :type  public_key_uri: :class:`str`
            :param public_key_uri: Endpoint to retrieve the provider public key for validation. This
                attribute was added in vSphere API 7.0.0.0.
            :type  client_id: :class:`str`
            :param client_id: Client identifier to connect to the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  client_secret: :class:`str`
            :param client_secret: The secret shared between the client and the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  claim_map: :class:`dict` of :class:`str` and (:class:`dict` of :class:`str` and :class:`list` of :class:`str`)
            :param claim_map: The map used to transform an OAuth2 claim to a corresponding claim
                that vCenter Server understands. Currently only the key "perms" is
                supported. The key "perms" is used for mapping the "perms" claim of
                incoming JWT. The value is another map with an external group as
                the key and a vCenter Server group as value. This attribute was
                added in vSphere API 7.0.0.0.
            :type  issuer: :class:`str`
            :param issuer: The identity provider namespace. It is used to validate the issuer
                in the acquired OAuth2 token. This attribute was added in vSphere
                API 7.0.0.0.
            :type  authentication_method: :class:`Providers.Oauth2AuthenticationMethod`
            :param authentication_method: Authentication method used by the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  auth_query_params: :class:`dict` of :class:`str` and :class:`list` of :class:`str`
            :param auth_query_params: 
                
                key/value pairs that are to be appended to the authEndpoint
                request. 
                
                How to append to authEndpoint request: If the map is not empty, a
                "?" is added to the endpoint URL, and combination of each k and
                each string in the v is added with an "&" delimiter. Details:
                
                * If the value contains only one string, then the key is added with
                  "k=v".
                * If the value is an empty list, then the key is added without a
                  "=v".
                * If the value contains multiple strings, then the key is repeated
                  in the query-string for each string in the value.
                
                . This attribute was added in vSphere API 7.0.0.0.
            """
            self.discovery_endpoint = discovery_endpoint
            self.logout_endpoint = logout_endpoint
            self.auth_endpoint = auth_endpoint
            self.token_endpoint = token_endpoint
            self.public_key_uri = public_key_uri
            self.client_id = client_id
            self.client_secret = client_secret
            self.claim_map = claim_map
            self.issuer = issuer
            self.authentication_method = authentication_method
            self.auth_query_params = auth_query_params
            VapiStruct.__init__(self)


    OidcInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.oidc_info', {
            'discovery_endpoint': type.URIType(),
            'logout_endpoint': type.OptionalType(type.URIType()),
            'auth_endpoint': type.URIType(),
            'token_endpoint': type.URIType(),
            'public_key_uri': type.URIType(),
            'client_id': type.StringType(),
            'client_secret': type.StringType(),
            'claim_map': type.MapType(type.StringType(), type.MapType(type.StringType(), type.ListType(type.StringType()))),
            'issuer': type.StringType(),
            'authentication_method': type.ReferenceType(__name__, 'Providers.Oauth2AuthenticationMethod'),
            'auth_query_params': type.MapType(type.StringType(), type.ListType(type.StringType())),
        },
        OidcInfo,
        False,
        None))


    class OidcCreateSpec(VapiStruct):
        """
        The ``Providers.OidcCreateSpec`` class contains the information used to
        create an OIDC identity provider. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     discovery_endpoint=None,
                     client_id=None,
                     client_secret=None,
                     claim_map=None,
                    ):
            """
            :type  discovery_endpoint: :class:`str`
            :param discovery_endpoint: Endpoint to retrieve the provider metadata. This attribute was
                added in vSphere API 7.0.0.0.
            :type  client_id: :class:`str`
            :param client_id: Client identifier to connect to the provider. This attribute was
                added in vSphere API 7.0.0.0.
            :type  client_secret: :class:`str`
            :param client_secret: The secret shared between the client and the provider. This
                attribute was added in vSphere API 7.0.0.0.
            :type  claim_map: :class:`dict` of :class:`str` and (:class:`dict` of :class:`str` and :class:`list` of :class:`str`)
            :param claim_map: The map used to transform an OAuth2 claim to a corresponding claim
                that vCenter Server understands. Currently only the key "perms" is
                supported. The key "perms" is used for mapping the "perms" claim of
                incoming JWT. The value is another map with an external group as
                the key and a vCenter Server group as value. This attribute was
                added in vSphere API 7.0.0.0.
            """
            self.discovery_endpoint = discovery_endpoint
            self.client_id = client_id
            self.client_secret = client_secret
            self.claim_map = claim_map
            VapiStruct.__init__(self)


    OidcCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.oidc_create_spec', {
            'discovery_endpoint': type.URIType(),
            'client_id': type.StringType(),
            'client_secret': type.StringType(),
            'claim_map': type.MapType(type.StringType(), type.MapType(type.StringType(), type.ListType(type.StringType()))),
        },
        OidcCreateSpec,
        False,
        None))


    class OidcUpdateSpec(VapiStruct):
        """
        The ``Providers.OidcUpdateSpec`` class contains the information used to
        update the OIDC identity provider. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     discovery_endpoint=None,
                     client_id=None,
                     client_secret=None,
                     claim_map=None,
                    ):
            """
            :type  discovery_endpoint: :class:`str` or ``None``
            :param discovery_endpoint: Endpoint to retrieve the provider metadata. This attribute was
                added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  client_id: :class:`str` or ``None``
            :param client_id: Client identifier to connect to the provider. This attribute was
                added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  client_secret: :class:`str` or ``None``
            :param client_secret: The secret shared between the client and the provider. This
                attribute was added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            :type  claim_map: (:class:`dict` of :class:`str` and (:class:`dict` of :class:`str` and :class:`list` of :class:`str`)) or ``None``
            :param claim_map: The map used to transform an OAuth2 claim to a corresponding claim
                that vCenter Server understands. Currently only the key "perms" is
                supported. The key "perms" is used for mapping the "perms" claim of
                incoming JWT. The value is another map with an external group as
                the key and a vCenter Server group as value. This attribute was
                added in vSphere API 7.0.0.0.
                If None, leaves value unchanged.
            """
            self.discovery_endpoint = discovery_endpoint
            self.client_id = client_id
            self.client_secret = client_secret
            self.claim_map = claim_map
            VapiStruct.__init__(self)


    OidcUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.oidc_update_spec', {
            'discovery_endpoint': type.OptionalType(type.URIType()),
            'client_id': type.OptionalType(type.StringType()),
            'client_secret': type.OptionalType(type.StringType()),
            'claim_map': type.OptionalType(type.MapType(type.StringType(), type.MapType(type.StringType(), type.ListType(type.StringType())))),
        },
        OidcUpdateSpec,
        False,
        None))


    class ActiveDirectoryOverLdap(VapiStruct):
        """
        The ``Providers.ActiveDirectoryOverLdap`` class contains the information
        about to how to use an Active Directory over LDAP connection to allow
        searching for users and groups if the identity provider is an On-Prem
        service. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     user_name=None,
                     password=None,
                     users_base_dn=None,
                     groups_base_dn=None,
                     server_endpoints=None,
                     cert_chain=None,
                    ):
            """
            :type  user_name: :class:`str`
            :param user_name: User name to connect to the active directory server. This attribute
                was added in vSphere API 7.0.0.0.
            :type  password: :class:`str`
            :param password: Password to connect to the active directory server. This attribute
                was added in vSphere API 7.0.0.0.
            :type  users_base_dn: :class:`str`
            :param users_base_dn: Base distinguished name for users. This attribute was added in
                vSphere API 7.0.0.0.
            :type  groups_base_dn: :class:`str`
            :param groups_base_dn: Base distinguished name for groups. This attribute was added in
                vSphere API 7.0.0.0.
            :type  server_endpoints: :class:`list` of :class:`str`
            :param server_endpoints: Active directory server endpoints. At least one active directory
                server endpoint must be set. This attribute was added in vSphere
                API 7.0.0.0.
            :type  cert_chain: :class:`com.vmware.vcenter.certificate_management_client.X509CertChain` or ``None``
            :param cert_chain: SSL certificate chain in base64 encoding. This attribute was added
                in vSphere API 7.0.0.0.
                This attribute can be None only, if all the active directory server
                endpoints use the LDAP (not LDAPS) protocol.
            """
            self.user_name = user_name
            self.password = password
            self.users_base_dn = users_base_dn
            self.groups_base_dn = groups_base_dn
            self.server_endpoints = server_endpoints
            self.cert_chain = cert_chain
            VapiStruct.__init__(self)


    ActiveDirectoryOverLdap._set_binding_type(type.StructType(
        'com.vmware.vcenter.identity.providers.active_directory_over_ldap', {
            'user_name': type.StringType(),
            'password': type.SecretType(),
            'users_base_dn': type.StringType(),
            'groups_base_dn': type.StringType(),
            'server_endpoints': type.ListType(type.URIType()),
            'cert_chain': type.OptionalType(type.ReferenceType('com.vmware.vcenter.certificate_management_client', 'X509CertChain')),
        },
        ActiveDirectoryOverLdap,
        False,
        None))



    def list(self):
        """
        Retrieve all identity providers. This method was added in vSphere API
        7.0.0.0.


        :rtype: :class:`list` of :class:`Providers.Summary`
        :return: Commonly used information about the identity providers.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if authorization is not given to caller.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIdentityProviders.Read`` and
              ``VcIdentityProviders.Manage``.
        """
        return self._invoke('list', None)

    def get(self,
            provider,
            ):
        """
        Retrieve detailed information of the specified identity provider. This
        method was added in vSphere API 7.0.0.0.

        :type  provider: :class:`str`
        :param provider: the identifier of the provider
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.identity.Providers``.
        :rtype: :class:`Providers.Info`
        :return: Detailed information of the specified identity provider.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if authorization is not given to caller.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no provider found with the given provider identifier.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIdentityProviders.Read`` and
              ``VcIdentityProviders.Manage``.
        """
        return self._invoke('get',
                            {
                            'provider': provider,
                            })

    def create(self,
               spec,
               ):
        """
        Create a vCenter Server identity provider. This method was added in
        vSphere API 7.0.0.0.

        :type  spec: :class:`Providers.CreateSpec`
        :param spec: the CreateSpec contains the information used to create the provider
        :rtype: :class:`str`
        :return: The identifier of the created identity provider.
            The return value will be an identifier for the resource type:
            ``com.vmware.vcenter.identity.Providers``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if authorization is not given to caller.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if invalid arguments are provided in createSpec.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if provider exists for provider ID in given spec.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIdentityProviders.Create`` and
              ``VcIdentityProviders.Manage``.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def update(self,
               provider,
               spec,
               ):
        """
        Update a vCenter Server identity provider. This method was added in
        vSphere API 7.0.0.0.

        :type  provider: :class:`str`
        :param provider: the identifier of the provider to update
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.identity.Providers``.
        :type  spec: :class:`Providers.UpdateSpec`
        :param spec: the UpdateSpec contains the information used to update the provider
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if authorization is not given to caller.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if invalid arguments are provided in updateSpec.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no provider found with the given provider identifier.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIdentityProviders.Manage``.
        """
        return self._invoke('update',
                            {
                            'provider': provider,
                            'spec': spec,
                            })

    def delete(self,
               provider,
               ):
        """
        Delete a vCenter Server identity provider. This method was added in
        vSphere API 7.0.0.0.

        :type  provider: :class:`str`
        :param provider: the identifier of the provider to delete
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.identity.Providers``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if authorization is not given to caller.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no provider found with the given provider identifier.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIdentityProviders.Manage``.
        """
        return self._invoke('delete',
                            {
                            'provider': provider,
                            })
class _ProvidersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/identity/providers',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.identity.Providers'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/identity/providers/{providerid}',
            path_variables={
                'provider': 'providerid',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Providers.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/identity/providers',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.identity.Providers'),
            'spec': type.ReferenceType(__name__, 'Providers.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/identity/providers/{providerid}',
            path_variables={
                'provider': 'providerid',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.identity.Providers'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/identity/providers/{providerid}',
            path_variables={
                'provider': 'providerid',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Providers.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Providers.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.vcenter.identity.Providers'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
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
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.identity.providers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Providers': Providers,
        'broker': 'com.vmware.vcenter.identity.broker_client.StubFactory',
    }

