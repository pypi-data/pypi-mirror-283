# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.crypto_manager.hosts.kms.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.crypto_manager.hosts.kms_client`` module provides
classes for managing key providers.

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


class Providers(VapiInterface):
    """
    The ``Providers`` class provides methods to retrieve providers on a host.
    This class was added in vSphere API 7.0.2.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.crypto_manager.hosts.kms.providers'
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

    class Type(Enum):
        """
        The ``Providers.Type`` class contains the types of providers. This
        enumeration was added in vSphere API 7.0.2.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        NATIVE = None
        """
        Native provider. This class attribute was added in vSphere API 7.0.2.0.

        """
        TRUST_AUTHORITY = None
        """
        Trust Authority provider. This class attribute was added in vSphere API
        7.0.2.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'NATIVE': Type('NATIVE'),
        'TRUST_AUTHORITY': Type('TRUST_AUTHORITY'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.crypto_manager.hosts.kms.providers.type',
        Type))


    class Health(Enum):
        """
        The ``Providers.Health`` class contains the health status of a provider.
        This enumeration was added in vSphere API 7.0.2.0.

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
        No health status is available. This class attribute was added in vSphere
        API 7.0.2.0.

        """
        OK = None
        """
        Operating normally. This class attribute was added in vSphere API 7.0.2.0.

        """
        WARNING = None
        """
        Operating normally, but there is an issue that requires attention. This
        class attribute was added in vSphere API 7.0.2.0.

        """
        ERROR = None
        """
        There is a critical issue that requires attention. This class attribute was
        added in vSphere API 7.0.2.0.

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
        'com.vmware.vcenter.crypto_manager.hosts.kms.providers.health',
        Health))


    class FilterSpec(VapiStruct):
        """
        The ``Providers.FilterSpec`` class contains attributes used to filter the
        results when listing providers. This class was added in vSphere API
        7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     providers=None,
                     health=None,
                     types=None,
                    ):
            """
            :type  providers: :class:`set` of :class:`str` or ``None``
            :param providers: Provider identifiers. This attribute was added in vSphere API
                7.0.2.0.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``.
                If None or empty, the result will not be filtered by provider
                identifier.
            :type  health: :class:`set` of :class:`Providers.Health` or ``None``
            :param health: Provider health status. This attribute was added in vSphere API
                7.0.2.0.
                If None or empty, the result will not be filtered by provider
                health status.
            :type  types: :class:`set` of :class:`Providers.Type` or ``None``
            :param types: Provider types. This attribute was added in vSphere API 7.0.2.0.
                If None or empty, the result will not be filtered by provider type.
            """
            self.providers = providers
            self.health = health
            self.types = types
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.hosts.kms.providers.filter_spec', {
            'providers': type.OptionalType(type.SetType(type.IdType())),
            'health': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'Providers.Health'))),
            'types': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'Providers.Type'))),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Providers.Summary`` class contains attributes that describe a
        provider. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     provider=None,
                     type=None,
                     health=None,
                    ):
            """
            :type  provider: :class:`str`
            :param provider: Identifier of the provider. This attribute was added in vSphere API
                7.0.2.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``.
            :type  type: :class:`Providers.Type`
            :param type: Provider type. This attribute was added in vSphere API 7.0.2.0.
            :type  health: :class:`Providers.Health`
            :param health: Health status of the provider. This attribute was added in vSphere
                API 7.0.2.0.
            """
            self.provider = provider
            self.type = type
            self.health = health
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.hosts.kms.providers.summary', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.crypto_manager.kms.provider'),
            'type': type.ReferenceType(__name__, 'Providers.Type'),
            'health': type.ReferenceType(__name__, 'Providers.Health'),
        },
        Summary,
        False,
        None))


    class NativeProviderInfo(VapiStruct):
        """
        The ``Providers.NativeProviderInfo`` class contains attributes that
        describe details of a native provider. This class was added in vSphere API
        7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     key_id=None,
                    ):
            """
            :type  key_id: :class:`str`
            :param key_id: Key identifier for the provider. This attribute was added in
                vSphere API 7.0.2.0.
            """
            self.key_id = key_id
            VapiStruct.__init__(self)


    NativeProviderInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.hosts.kms.providers.native_provider_info', {
            'key_id': type.StringType(),
        },
        NativeProviderInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Providers.Info`` class contains attributes that describe the details
        of a provider. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'NATIVE' : [('native_info', True)],
                    'TRUST_AUTHORITY' : [],
                }
            ),
        ]



        def __init__(self,
                     health=None,
                     details=None,
                     type=None,
                     native_info=None,
                    ):
            """
            :type  health: :class:`Providers.Health`
            :param health: Health status of the provider. This attribute was added in vSphere
                API 7.0.2.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health status of the provider. This attribute
                was added in vSphere API 7.0.2.0.
            :type  type: :class:`Providers.Type`
            :param type: Provider type. This attribute was added in vSphere API 7.0.2.0.
            :type  native_info: :class:`Providers.NativeProviderInfo`
            :param native_info: Native provider information. This attribute was added in vSphere
                API 7.0.2.0.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Providers.Type.NATIVE`.
            """
            self.health = health
            self.details = details
            self.type = type
            self.native_info = native_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.hosts.kms.providers.info', {
            'health': type.ReferenceType(__name__, 'Providers.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'type': type.ReferenceType(__name__, 'Providers.Type'),
            'native_info': type.OptionalType(type.ReferenceType(__name__, 'Providers.NativeProviderInfo')),
        },
        Info,
        False,
        None))



    def list(self,
             host,
             filter_spec=None,
             ):
        """
        List the available providers on a host. This method was added in
        vSphere API 7.0.2.0.

        :type  host: :class:`str`
        :param host: Host identifier.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  filter_spec: :class:`Providers.FilterSpec` or ``None``
        :param filter_spec: Filter spec.
            If None, the behavior is equivalent to a
            :class:`Providers.FilterSpec` with all attributes None.
        :rtype: :class:`list` of :class:`Providers.Summary`
        :return: Summary of providers.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the host identifier is empty or the FilterSpec is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the host is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``Cryptographer.ReadKeyServersInfo``.
        """
        return self._invoke('list',
                            {
                            'host': host,
                            'filter_spec': filter_spec,
                            })

    def get(self,
            host,
            provider,
            ):
        """
        Get a provider on a host. This method was added in vSphere API 7.0.2.0.

        :type  host: :class:`str`
        :param host: Host identifier.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  provider: :class:`str`
        :param provider: Provider identifier.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.crypto_manager.kms.provider``.
        :rtype: :class:`Providers.Info`
        :return: Information of the provider.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the host identifier is empty or the provider identifier is
            empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the provider or the host is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``Cryptographer.ReadKeyServersInfo``.
        """
        return self._invoke('get',
                            {
                            'host': host,
                            'provider': provider,
                            })
class _ProvidersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'filter_spec': type.OptionalType(type.ReferenceType(__name__, 'Providers.FilterSpec')),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/crypto-manager/hosts/{host}/kms/providers',
            path_variables={
                'host': 'host',
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
            'host': type.IdType(resource_types='HostSystem'),
            'provider': type.IdType(resource_types='com.vmware.vcenter.crypto_manager.kms.provider'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/crypto-manager/hosts/{host}/kms/providers/{provider}',
            path_variables={
                'host': 'host',
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
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.crypto_manager.hosts.kms.providers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Providers': Providers,
    }

