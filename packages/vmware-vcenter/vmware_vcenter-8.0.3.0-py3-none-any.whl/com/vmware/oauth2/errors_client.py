# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.oauth2.errors.
#---------------------------------------------------------------------------

"""
The ``com.vmware.oauth2.errors_client`` module provides the OAuth 2.0
exceptions that can be included in the list of exceptions in the specification
of OAuth 2.0 methods to indicate that the method might report those exceptions.

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


class Error(VapiError):
    """
    The OAuth2 ``Error`` describes the attributes common to standard OAuth 2.0
    exceptions.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'Error'

    def __init__(self,
                 error=None,
                 error_description=None,
                 error_uri=None,
                ):
        """
        :type  error: :class:`Error.Type`
        :param error: Discriminator field to help API consumers identify the structure
            type.
        :type  error_description: :class:`str` or ``None``
        :param error_description: Human-readable ASCII text providing additional information, used to
            assist the client developer in understanding the error that
            occurred. Values for the "error_description" parameter MUST NOT
            include characters outside the set %x20-21 / %x23-5B / %x5D-7E.
            if no additional information is available.
        :type  error_uri: :class:`str` or ``None``
        :param error_uri: A URI identifying a human-readable web page with information about
            the error, used to provide the client developer with additional
            information about the error.
            if no such web-page is available.
        """

        self.error = error
        self.error_description = error_description
        self.error_uri = error_uri
        VapiError.__init__(self)

    class Type(Enum):
        """
        Enumeration of OAuth 2.0 exceptions.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        invalid_request = None
        """
        Discriminator for the :class:`InvalidRequest` type.

        """
        invalid_scope = None
        """
        Discriminator for the :class:`InvalidScope` type.

        """
        invalid_grant = None
        """
        Discriminator for the :class:`InvalidGrant` type.

        """
        invalid_client = None
        """
        Discriminator for the :class:`InvalidClient` type. This class attribute was
        added in vSphere API 8.0.3.0.

        """
        unauthorized_client = None
        """
        Discriminator for the :class:`UnauthorizedClient` type. This class
        attribute was added in vSphere API 8.0.3.0.

        """
        unsupported_grant_type = None
        """
        Discriminator for the :class:`UnsupportedGrantType` type. This class
        attribute was added in vSphere API 8.0.3.0.

        """
        invalid_target = None
        """
        Discriminator for the :class:`InvalidTarget` type. This class attribute was
        added in vSphere API 8.0.3.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'invalid_request': Type('invalid_request'),
        'invalid_scope': Type('invalid_scope'),
        'invalid_grant': Type('invalid_grant'),
        'invalid_client': Type('invalid_client'),
        'unauthorized_client': Type('unauthorized_client'),
        'unsupported_grant_type': Type('unsupported_grant_type'),
        'invalid_target': Type('invalid_target'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.oauth2.errors.error.type',
        Type))

Error._set_binding_type(type.ErrorType(
    'com.vmware.oauth2.errors.error', {
        'error': type.ReferenceType(__name__, 'Error.Type'),
        'error_description': type.OptionalType(type.StringType()),
        'error_uri': type.OptionalType(type.URIType()),
    },
    Error))



class UnsupportedGrantType(Error):
    """
    Indicates that the authorization grant type is not supported by the
    authorization server. This class was added in vSphere API 8.0.3.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'UnsupportedGrantType'

    def __init__(self,
                 error='UNSUPPORTED_GRANT_TYPE',
                 error_description=None,
                 error_uri=None,
                ):
        """
        :type  error: :class:`Error.Type`
        :param error: Discriminator field to help API consumers identify the structure
            type.
        :type  error_description: :class:`str` or ``None``
        :param error_description: Human-readable ASCII text providing additional information, used to
            assist the client developer in understanding the error that
            occurred. Values for the "error_description" parameter MUST NOT
            include characters outside the set %x20-21 / %x23-5B / %x5D-7E.
            if no additional information is available.
        :type  error_uri: :class:`str` or ``None``
        :param error_uri: A URI identifying a human-readable web page with information about
            the error, used to provide the client developer with additional
            information about the error.
            if no such web-page is available.
        """

        Error.__init__(
            self,
            error=error,
            error_description=error_description,
            error_uri=error_uri,
        )

UnsupportedGrantType._set_binding_type(type.ErrorType(
    'com.vmware.oauth2.errors.unsupported_grant_type', {
        'error': type.ReferenceType(__name__, 'Error.Type'),
        'error_description': type.OptionalType(type.StringType()),
        'error_uri': type.OptionalType(type.URIType()),
    },
    UnsupportedGrantType))



class UnauthorizedClient(Error):
    """
    Indicates that the authenticated client is not authorized to use this
    authorization grant type. This class was added in vSphere API 8.0.3.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'UnauthorizedClient'

    def __init__(self,
                 error='UNAUTHORIZED_CLIENT',
                 error_description=None,
                 error_uri=None,
                ):
        """
        :type  error: :class:`Error.Type`
        :param error: Discriminator field to help API consumers identify the structure
            type.
        :type  error_description: :class:`str` or ``None``
        :param error_description: Human-readable ASCII text providing additional information, used to
            assist the client developer in understanding the error that
            occurred. Values for the "error_description" parameter MUST NOT
            include characters outside the set %x20-21 / %x23-5B / %x5D-7E.
            if no additional information is available.
        :type  error_uri: :class:`str` or ``None``
        :param error_uri: A URI identifying a human-readable web page with information about
            the error, used to provide the client developer with additional
            information about the error.
            if no such web-page is available.
        """

        Error.__init__(
            self,
            error=error,
            error_description=error_description,
            error_uri=error_uri,
        )

UnauthorizedClient._set_binding_type(type.ErrorType(
    'com.vmware.oauth2.errors.unauthorized_client', {
        'error': type.ReferenceType(__name__, 'Error.Type'),
        'error_description': type.OptionalType(type.StringType()),
        'error_uri': type.OptionalType(type.URIType()),
    },
    UnauthorizedClient))



class InvalidTarget(Error):
    """
    Indicates that the authorization server is unwilling or unable to issue a
    token for any target service. This class was added in vSphere API 8.0.3.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'InvalidTarget'

    def __init__(self,
                 error='INVALID_TARGET',
                 error_description=None,
                 error_uri=None,
                ):
        """
        :type  error: :class:`Error.Type`
        :param error: Discriminator field to help API consumers identify the structure
            type.
        :type  error_description: :class:`str` or ``None``
        :param error_description: Human-readable ASCII text providing additional information, used to
            assist the client developer in understanding the error that
            occurred. Values for the "error_description" parameter MUST NOT
            include characters outside the set %x20-21 / %x23-5B / %x5D-7E.
            if no additional information is available.
        :type  error_uri: :class:`str` or ``None``
        :param error_uri: A URI identifying a human-readable web page with information about
            the error, used to provide the client developer with additional
            information about the error.
            if no such web-page is available.
        """

        Error.__init__(
            self,
            error=error,
            error_description=error_description,
            error_uri=error_uri,
        )

InvalidTarget._set_binding_type(type.ErrorType(
    'com.vmware.oauth2.errors.invalid_target', {
        'error': type.ReferenceType(__name__, 'Error.Type'),
        'error_description': type.OptionalType(type.StringType()),
        'error_uri': type.OptionalType(type.URIType()),
    },
    InvalidTarget))



class InvalidScope(Error):
    """
    Indicates that the requested scope is invalid, unknown, malformed, or
    exceeds the scope granted by the resource owner.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'InvalidScope'

    def __init__(self,
                 error='INVALID_SCOPE',
                 error_description=None,
                 error_uri=None,
                ):
        """
        :type  error: :class:`Error.Type`
        :param error: Discriminator field to help API consumers identify the structure
            type.
        :type  error_description: :class:`str` or ``None``
        :param error_description: Human-readable ASCII text providing additional information, used to
            assist the client developer in understanding the error that
            occurred. Values for the "error_description" parameter MUST NOT
            include characters outside the set %x20-21 / %x23-5B / %x5D-7E.
            if no additional information is available.
        :type  error_uri: :class:`str` or ``None``
        :param error_uri: A URI identifying a human-readable web page with information about
            the error, used to provide the client developer with additional
            information about the error.
            if no such web-page is available.
        """

        Error.__init__(
            self,
            error=error,
            error_description=error_description,
            error_uri=error_uri,
        )

InvalidScope._set_binding_type(type.ErrorType(
    'com.vmware.oauth2.errors.invalid_scope', {
        'error': type.ReferenceType(__name__, 'Error.Type'),
        'error_description': type.OptionalType(type.StringType()),
        'error_uri': type.OptionalType(type.URIType()),
    },
    InvalidScope))



class InvalidRequest(Error):
    """
    Indicates that the request is missing a required parameter, includes an
    unsupported parameter value (other than grant type), repeats a parameter,
    includes multiple credentials, utilizes more than one mechanism for
    authenticating the client, or is otherwise malformed

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'InvalidRequest'

    def __init__(self,
                 error='INVALID_REQUEST',
                 error_description=None,
                 error_uri=None,
                ):
        """
        :type  error: :class:`Error.Type`
        :param error: Discriminator field to help API consumers identify the structure
            type.
        :type  error_description: :class:`str` or ``None``
        :param error_description: Human-readable ASCII text providing additional information, used to
            assist the client developer in understanding the error that
            occurred. Values for the "error_description" parameter MUST NOT
            include characters outside the set %x20-21 / %x23-5B / %x5D-7E.
            if no additional information is available.
        :type  error_uri: :class:`str` or ``None``
        :param error_uri: A URI identifying a human-readable web page with information about
            the error, used to provide the client developer with additional
            information about the error.
            if no such web-page is available.
        """

        Error.__init__(
            self,
            error=error,
            error_description=error_description,
            error_uri=error_uri,
        )

InvalidRequest._set_binding_type(type.ErrorType(
    'com.vmware.oauth2.errors.invalid_request', {
        'error': type.ReferenceType(__name__, 'Error.Type'),
        'error_description': type.OptionalType(type.StringType()),
        'error_uri': type.OptionalType(type.URIType()),
    },
    InvalidRequest))



class InvalidGrant(Error):
    """
    Indicates that the provided authorization grant (e.g., authorization code,
    resource owner credentials) or refresh token is invalid, expired, revoked,
    does not match the redirection URI used in the authorization request, or
    was issued to another client.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'InvalidGrant'

    def __init__(self,
                 error='INVALID_GRANT',
                 error_description=None,
                 error_uri=None,
                ):
        """
        :type  error: :class:`Error.Type`
        :param error: Discriminator field to help API consumers identify the structure
            type.
        :type  error_description: :class:`str` or ``None``
        :param error_description: Human-readable ASCII text providing additional information, used to
            assist the client developer in understanding the error that
            occurred. Values for the "error_description" parameter MUST NOT
            include characters outside the set %x20-21 / %x23-5B / %x5D-7E.
            if no additional information is available.
        :type  error_uri: :class:`str` or ``None``
        :param error_uri: A URI identifying a human-readable web page with information about
            the error, used to provide the client developer with additional
            information about the error.
            if no such web-page is available.
        """

        Error.__init__(
            self,
            error=error,
            error_description=error_description,
            error_uri=error_uri,
        )

InvalidGrant._set_binding_type(type.ErrorType(
    'com.vmware.oauth2.errors.invalid_grant', {
        'error': type.ReferenceType(__name__, 'Error.Type'),
        'error_description': type.OptionalType(type.StringType()),
        'error_uri': type.OptionalType(type.URIType()),
    },
    InvalidGrant))



class InvalidClient(Error):
    """
    Indicates that the client authentication failed (e.g., unknown client, no
    client authentication included, or unsupported authentication method). This
    class was added in vSphere API 8.0.3.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'InvalidClient'

    def __init__(self,
                 error='INVALID_CLIENT',
                 error_description=None,
                 error_uri=None,
                 challenge=None,
                ):
        """
        :type  error: :class:`Error.Type`
        :param error: Discriminator field to help API consumers identify the structure
            type.
        :type  error_description: :class:`str` or ``None``
        :param error_description: Human-readable ASCII text providing additional information, used to
            assist the client developer in understanding the error that
            occurred. Values for the "error_description" parameter MUST NOT
            include characters outside the set %x20-21 / %x23-5B / %x5D-7E.
            if no additional information is available.
        :type  error_uri: :class:`str` or ``None``
        :param error_uri: A URI identifying a human-readable web page with information about
            the error, used to provide the client developer with additional
            information about the error.
            if no such web-page is available.
        :type  challenge: :class:`str`
        :param challenge: Authentication header as defined in `RFC 9110, Section 11.6.1 -
            WWW-Authenticate
            <https://tools.ietf.org/html/rfc9110#name-www-authenticate>`_. The
            "WWW-Authenticate" response header field indicates the
            authentication scheme(s) and parameters applicable to the target
            resource. This attribute was added in vSphere API 8.0.3.0.
        """

        self.challenge = challenge
        Error.__init__(
            self,
            error=error,
            error_description=error_description,
            error_uri=error_uri,
        )

InvalidClient._set_binding_type(type.ErrorType(
    'com.vmware.oauth2.errors.invalid_client', {
        'error': type.ReferenceType(__name__, 'Error.Type'),
        'error_description': type.OptionalType(type.StringType()),
        'error_uri': type.OptionalType(type.URIType()),
        'challenge': type.StringType(),
    },
    InvalidClient))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

