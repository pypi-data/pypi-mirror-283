# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.oauth2.
#---------------------------------------------------------------------------

"""
The ``com.vmware.oauth2_client`` module contains classes for reuse by OAuth2
API definitions.

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


class Constants(VapiStruct):
    """
    Constants defined in `RFC 6749
    <https://tools.ietf.org/html/rfc6749#section-5>`_ and `RFC 8693
    <https://tools.ietf.org/html/rfc8693#section-2.2.1>`_.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """
    TOKEN_EXCHANGE_GRANT = "urn:ietf:params:oauth:grant-type:token-exchange"
    """
    Token exchange grant type for OAuth 2.0

    """
    PASSWORD_GRANT = "password"
    """
    Resource Owner Password Credentials grant type for OAuth 2.0. This class
    attribute was added in vSphere API 8.0.3.0.

    """
    ACCESS_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:access_token"
    """
    Token type URI for an OAuth 2.0 access token

    """
    REFRESH_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:refresh_token"
    """
    Token type URI for an OAuth 2.0 refresh token

    """
    ID_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:id_token"
    """
    Token type URI for an ID Token

    """
    SAML2_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:saml2"
    """
    Token type URI for a base64url-encoded SAML 2.0

    """




    def __init__(self,
                ):
        """
        """
        VapiStruct.__init__(self)


Constants._set_binding_type(type.StructType(
    'com.vmware.oauth2.constants', {
    },
    Constants,
    False,
    None))



class TokenInfo(VapiStruct):
    """
    The ``TokenInfo`` class contains data that represents successful
    access-token response as defined in `RFC 6749
    <https://tools.ietf.org/html/rfc6749#section-5>`_ and extended in `RFC 8693
    <https://tools.ietf.org/html/rfc8693#section-2.2.1>`_.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """
    BEARER_TOKEN_METHOD_TYPE = "Bearer"
    """
    Class attribute indicating that the security token is a bearer token.

    """




    def __init__(self,
                 access_token=None,
                 token_type=None,
                 expires_in=None,
                 scope=None,
                 refresh_token=None,
                 issued_token_type=None,
                ):
        """
        :type  access_token: :class:`str`
        :param access_token: The access token issued by the authorization server.
        :type  token_type: :class:`str`
        :param token_type: A case-insensitive value specifying the method of using the access
            token issued.
        :type  expires_in: :class:`long` or ``None``
        :param expires_in: The validity lifetime, in seconds, of the token issued by the
            server.
            None if not applicable for issued token.
        :type  scope: :class:`str` or ``None``
        :param scope: Scope of the issued access token. The value of the scope parameter
            is expressed as a list of space- delimited, case-sensitive strings.
            The strings are defined by the authorization server. If the value
            contains multiple space-delimited strings, their order does not
            matter, and each string adds an additional access range to the
            requested scope.
            None if the scope of the issued security token is identical to the
            scope requested by the client.
        :type  refresh_token: :class:`str` or ``None``
        :param refresh_token: The refresh token, which can be used to obtain new access tokens.
            None if not applicable to the specific request.
        :type  issued_token_type: :class:`str` or ``None``
        :param issued_token_type: An identifier which indicates the type of the access token in the
            :attr:`TokenInfo.access_token` attribute.
            None if not the result of a token-exchange invocation; otherwise,
            required.
        """
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope
        self.refresh_token = refresh_token
        self.issued_token_type = issued_token_type
        VapiStruct.__init__(self)


TokenInfo._set_binding_type(type.StructType(
    'com.vmware.oauth2.token_info', {
        'access_token': type.StringType(),
        'token_type': type.StringType(),
        'expires_in': type.OptionalType(type.IntegerType()),
        'scope': type.OptionalType(type.StringType()),
        'refresh_token': type.OptionalType(type.StringType()),
        'issued_token_type': type.OptionalType(type.StringType()),
    },
    TokenInfo,
    False,
    None))



class TokenResult(VapiStruct):
    """
    The ``TokenResult`` class contains data that represents successful
    access-token response as defined in `RFC 6749
    <https://tools.ietf.org/html/rfc6749#section-5>`_ and extended in `RFC 8693
    <https://tools.ietf.org/html/rfc8693#section-2.2.1>`_. This class was added
    in vSphere API 8.0.3.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """
    BEARER_TOKEN_METHOD_TYPE = "Bearer"
    """
    Class attribute indicating that the security token is a bearer token. This
    class attribute was added in vSphere API 8.0.3.0.

    """




    def __init__(self,
                 access_token=None,
                 token_type=None,
                 expires_in=None,
                 scope=None,
                 refresh_token=None,
                 issued_token_type=None,
                ):
        """
        :type  access_token: :class:`str`
        :param access_token: The access token issued by the authorization server. This attribute
            was added in vSphere API 8.0.3.0.
        :type  token_type: :class:`str`
        :param token_type: A case-insensitive value specifying the method of using the access
            token issued. This attribute was added in vSphere API 8.0.3.0.
        :type  expires_in: :class:`long` or ``None``
        :param expires_in: The validity lifetime, in seconds, of the token issued by the
            server. This attribute was added in vSphere API 8.0.3.0.
            None if not applicable for issued token.
        :type  scope: :class:`str` or ``None``
        :param scope: Scope of the issued access token. 
            
            The value of the scope parameter is expressed as a list of space-
            delimited, case-sensitive strings. The strings are defined by the
            authorization server. If the value contains multiple
            space-delimited strings, their order does not matter, and each
            string adds an additional access range to the requested scope..
            This attribute was added in vSphere API 8.0.3.0.
            None if the scope of the issued security token is identical to the
            scope requested by the client.
        :type  refresh_token: :class:`str` or ``None``
        :param refresh_token: The refresh token, which can be used to obtain new access tokens.
            This attribute was added in vSphere API 8.0.3.0.
            None if not applicable to the specific request.
        :type  issued_token_type: :class:`str` or ``None``
        :param issued_token_type: An identifier which indicates the type of the access token in the
            :attr:`TokenResult.access_token` attribute. This attribute was
            added in vSphere API 8.0.3.0.
            None if not the result of a token-exchange invocation; otherwise,
            required.
        """
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope
        self.refresh_token = refresh_token
        self.issued_token_type = issued_token_type
        VapiStruct.__init__(self)


TokenResult._set_binding_type(type.StructType(
    'com.vmware.oauth2.token_result', {
        'access_token': type.SecretType(),
        'token_type': type.StringType(),
        'expires_in': type.OptionalType(type.IntegerType()),
        'scope': type.OptionalType(type.StringType()),
        'refresh_token': type.OptionalType(type.SecretType()),
        'issued_token_type': type.OptionalType(type.StringType()),
    },
    TokenResult,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
        'errors': 'com.vmware.oauth2.errors_client.StubFactory',
    }

