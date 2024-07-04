# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.authentication.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.authentication_client`` module provides authentication
classes specific to the com.vmware.vcenter module. The
``com.vmware.vcenter.authentication_client`` module is available starting in
vSphere 7.0 U2.

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


class Token(VapiInterface):
    """
    The ``Token`` interface provides operations for obtaining an access token.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.authentication.token'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TokenStub)
        self._VAPI_OPERATION_IDS = {}

    class IssueSpec(VapiStruct):
        """
        The ``Token.IssueSpec`` class contains arguments required for token
        exchange.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     grant_type=None,
                     resource=None,
                     audience=None,
                     scope=None,
                     requested_token_type=None,
                     subject_token=None,
                     subject_token_type=None,
                     actor_token=None,
                     actor_token_type=None,
                    ):
            """
            :type  grant_type: :class:`str`
            :param grant_type: The value of ``urn:ietf:params:oauth:grant-type:token-exchange``
                indicates that a token exchange is being performed.
                When clients pass a value of this class as a parameter, the
                attribute must be one of
                ``urn:ietf:params:oauth:grant-type:token-exchange``. When methods
                return a value of this class as a return value, the attribute will
                be one of ``urn:ietf:params:oauth:grant-type:token-exchange``.
            :type  resource: :class:`str` or ``None``
            :param resource: Indicates the location of the target service or resource where the
                client intends to use the requested security token.
                If None, it is inferred from other arguments.
            :type  audience: :class:`str` or ``None``
            :param audience: The logical name of the target service where the client intends to
                use the requested security token. This serves a purpose similar to
                the :attr:`Token.IssueSpec.resource` attribute, but with the client
                providing a logical name rather than a location.
                If None, it is inferred from other arguments.
            :type  scope: :class:`str` or ``None``
            :param scope: A list of space-delimited, case-sensitive strings, that allow the
                client to specify the desired scope of the requested security token
                in the context of the service or resource where the token will be
                used.
                If None, it is inferred from other arguments.
            :type  requested_token_type: :class:`str` or ``None``
            :param requested_token_type: An identifier for the type of the requested security token. If the
                requested type is unspecified, the issued token type is at the
                discretion of the server and may be dictated by knowledge of the
                requirements of the service or resource indicated by the
                :attr:`Token.IssueSpec.resource` or
                :attr:`Token.IssueSpec.audience` attribute.
                If None, it is inferred from other arguments.
            :type  subject_token: :class:`str` or ``None``
            :param subject_token: A security token that represents the identity of the party on
                behalf of whom exchange is being made. Typically, the subject of
                this token will be the subject of the security token issued. Token
                is base64-encoded. 
                
                The attribute is required when the value of the
                :attr:`Token.IssueSpec.grant_type` attribute is
                ``urn:ietf:params:oauth:grant-type:token-exchange``.
                This attribute is currently required. In the future, the class may
                support grant-types other than
                ``urn:ietf:params:oauth:grant-type:token-exchange`` for which the
                value may be None.
            :type  subject_token_type: :class:`str` or ``None``
            :param subject_token_type: An identifier, that indicates the type of the security token in the
                :attr:`Token.IssueSpec.subject_token` attribute. 
                
                The attribute is required when the value of the
                :attr:`Token.IssueSpec.grant_type` attribute is
                ``urn:ietf:params:oauth:grant-type:token-exchange``.
                This attribute is currently required. In the future, the class may
                support grant-types other than
                ``urn:ietf:params:oauth:grant-type:token-exchange`` for which the
                value may be None.
            :type  actor_token: :class:`str` or ``None``
            :param actor_token: A security token that represents the identity of the acting party.
                Typically, this will be the party that is authorized to use the
                requested security token and act on behalf of the subject.
                None if not needed for the specific case of exchange.
            :type  actor_token_type: :class:`str` or ``None``
            :param actor_token_type: An identifier, that indicates the type of the security token in the
                :attr:`Token.IssueSpec.actor_token` attribute.
                None if :attr:`Token.IssueSpec.actor_token` attribute is not
                present.
            """
            self.grant_type = grant_type
            self.resource = resource
            self.audience = audience
            self.scope = scope
            self.requested_token_type = requested_token_type
            self.subject_token = subject_token
            self.subject_token_type = subject_token_type
            self.actor_token = actor_token
            self.actor_token_type = actor_token_type
            VapiStruct.__init__(self)


    IssueSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authentication.token.issue_spec', {
            'grant_type': type.StringType(),
            'resource': type.OptionalType(type.StringType()),
            'audience': type.OptionalType(type.StringType()),
            'scope': type.OptionalType(type.StringType()),
            'requested_token_type': type.OptionalType(type.StringType()),
            'subject_token': type.OptionalType(type.StringType()),
            'subject_token_type': type.OptionalType(type.StringType()),
            'actor_token': type.OptionalType(type.StringType()),
            'actor_token_type': type.OptionalType(type.StringType()),
        },
        IssueSpec,
        False,
        None))



    def issue(self,
              spec,
              ):
        """
        Provides a token endpoint as defined in `RFC 6749
        <https://tools.ietf.org/html/rfc6749#section-3.2>`_. 
        
        Supported grant types: 
        
        * ` urn:ietf:params:oauth:grant-type:token-exchange
          <https://tools.ietf.org/html/rfc8693#section-2.1>`_ - Exchanges
          incoming token based on the spec and current client authorization data.
        
        
        
        This method supercedes
        ``com.vmware.vcenter.tokenservice.TokenExchange#exchange``. The REST
        rendering of the newer operation matches RFC8693's definition for both
        input and output of the method.

        :type  spec: :class:`Token.IssueSpec`
        :param spec: ``Token.IssueSpec`` class containing arguments that define the
            exchange process.
        :rtype: :class:`com.vmware.oauth2_client.TokenInfo`
        :return: :class:`com.vmware.oauth2_client.TokenInfo` class that contains a
            newly issued token.
        :raise: :class:`com.vmware.oauth2.errors_client.InvalidRequest` 
            if :class:`Token.IssueSpec` is missing a required attribute,
            includes an unsupported attribute value (other than
            :attr:`Token.IssueSpec.grant_type`).
        :raise: :class:`com.vmware.oauth2.errors_client.InvalidGrant` 
            provided authorization grant (e.g., authorization code, resource
            owner credentials) or refresh token is invalid, expired, revoked,
            does not match the redirection URI used in the authorization
            request, or was issued to another client.
        :raise: :class:`com.vmware.oauth2.errors_client.InvalidScope` 
            If the server is unwilling or unable to issue a token for all the
            target services indicated by the :attr:`Token.IssueSpec.resource`
            or :attr:`Token.IssueSpec.audience` attributes.
        """
        return self._invoke('issue',
                            {
                            'spec': spec,
                            })
class _TokenStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for issue operation
        issue_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Token.IssueSpec'),
        })
        issue_error_dict = {
            'com.vmware.oauth2.errors.invalid_request':
                type.ReferenceType('com.vmware.oauth2.errors_client', 'InvalidRequest'),
            'com.vmware.oauth2.errors.invalid_grant':
                type.ReferenceType('com.vmware.oauth2.errors_client', 'InvalidGrant'),
            'com.vmware.oauth2.errors.invalid_scope':
                type.ReferenceType('com.vmware.oauth2.errors_client', 'InvalidScope'),

        }
        issue_input_value_validator_list = [
        ]
        issue_output_validator_list = [
        ]
        issue_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/authentication/token',
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

        operations = {
            'issue': {
                'input_type': issue_input_type,
                'output_type': type.ReferenceType('com.vmware.oauth2_client', 'TokenInfo'),
                'errors': issue_error_dict,
                'input_value_validator_list': issue_input_value_validator_list,
                'output_validator_list': issue_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'issue': issue_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.authentication.token',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Token': Token,
    }

