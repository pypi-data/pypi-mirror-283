# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.crypto_manager.kms.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.crypto_manager.kms_client`` module provides classes
for managing key providers and cryptographic keys.

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
    The ``Providers`` class provides methods to create, retrieve, update,
    delete, export and import providers. This class was added in vSphere API
    7.0.2.0.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.crypto_manager.kms.provider"
    """
    Resource type for a provider. This class attribute was added in vSphere API
    7.0.2.0.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.crypto_manager.kms.providers'
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

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'NATIVE': Type('NATIVE'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.crypto_manager.kms.providers.type',
        Type))


    class Health(Enum):
        """
        The ``Providers.Health`` class describes the health status of a provider.
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
        'com.vmware.vcenter.crypto_manager.kms.providers.health',
        Health))


    class ExportType(Enum):
        """
        The ``Providers.ExportType`` class identifies the type of result that is
        returned when a provider is exported. This enumeration was added in vSphere
        API 7.0.2.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        LOCATION = None
        """
        Result returned as a URL from which the provider configuration can be
        downloaded. This class attribute was added in vSphere API 7.0.2.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ExportType` instance.
            """
            Enum.__init__(string)

    ExportType._set_values({
        'LOCATION': ExportType('LOCATION'),
    })
    ExportType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.crypto_manager.kms.providers.export_type',
        ExportType))


    class Constraints(VapiStruct):
        """
        The ``Providers.Constraints`` class contains constraints on a provider.
        This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     tpm_required=None,
                    ):
            """
            :type  tpm_required: :class:`bool`
            :param tpm_required: Determines if a provider is restricted to hosts with TPM 2.0
                capability. This attribute was added in vSphere API 7.0.2.0.
            """
            self.tpm_required = tpm_required
            VapiStruct.__init__(self)


    Constraints._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.constraints', {
            'tpm_required': type.BooleanType(),
        },
        Constraints,
        False,
        None))


    class ConstraintsSpec(VapiStruct):
        """
        The ``Providers.ConstraintsSpec`` class contains constraints to be imposed
        on a provider. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     tpm_required=None,
                    ):
            """
            :type  tpm_required: :class:`bool` or ``None``
            :param tpm_required: Determines if a provider is restricted to hosts with TPM 2.0
                capability. This attribute was added in vSphere API 7.0.2.0.
                If None, the constraint does not apply to the provider.
            """
            self.tpm_required = tpm_required
            VapiStruct.__init__(self)


    ConstraintsSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.constraints_spec', {
            'tpm_required': type.OptionalType(type.BooleanType()),
        },
        ConstraintsSpec,
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
            :param provider: Provider identifier. This attribute was added in vSphere API
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
        'com.vmware.vcenter.crypto_manager.kms.providers.summary', {
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
        'com.vmware.vcenter.crypto_manager.kms.providers.native_provider_info', {
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
                }
            ),
        ]



        def __init__(self,
                     health=None,
                     details=None,
                     constraints=None,
                     type=None,
                     native_info=None,
                    ):
            """
            :type  health: :class:`Providers.Health`
            :param health: Health status of the provider. This attribute was added in vSphere
                API 7.0.2.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health status of the provider. 
                
                When the provider ``Providers.Health`` is not
                :attr:`Providers.Health.NONE` or :attr:`Providers.Health.OK`, this
                attribute will provide actionable descriptions of the issues.. This
                attribute was added in vSphere API 7.0.2.0.
            :type  constraints: :class:`Providers.Constraints` or ``None``
            :param constraints: The constraints on the provider. This attribute was added in
                vSphere API 7.0.2.0.
                If None, there are no constraints on the provider.
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
            self.constraints = constraints
            self.type = type
            self.native_info = native_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.info', {
            'health': type.ReferenceType(__name__, 'Providers.Health'),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'constraints': type.OptionalType(type.ReferenceType(__name__, 'Providers.Constraints')),
            'type': type.ReferenceType(__name__, 'Providers.Type'),
            'native_info': type.OptionalType(type.ReferenceType(__name__, 'Providers.NativeProviderInfo')),
        },
        Info,
        False,
        None))


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
            """
            self.providers = providers
            self.health = health
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.filter_spec', {
            'providers': type.OptionalType(type.SetType(type.IdType())),
            'health': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'Providers.Health'))),
        },
        FilterSpec,
        False,
        None))


    class NativeProviderCreateSpec(VapiStruct):
        """
        The ``Providers.NativeProviderCreateSpec`` class contains attributes that
        describe the desired configuration for a :attr:`Providers.Type.NATIVE`
        provider. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     key_id=None,
                     key_derivation_key=None,
                    ):
            """
            :type  key_id: :class:`str` or ``None``
            :param key_id: Key identifier for the provider. 
                
                The key identifier is required to be a 128-bit UUID represented as
                a hexadecimal string in "12345678-abcd-1234-cdef-123456789abc"
                format.. This attribute was added in vSphere API 7.0.2.0.
                If None, the key identifier will be generated automatically.
            :type  key_derivation_key: :class:`str` or ``None``
            :param key_derivation_key: Key used to derive data encryption keys. Base64 encoded. This
                attribute was added in vSphere API 7.0.2.0.
                If None, the key derivation key will be generated automatically.
            """
            self.key_id = key_id
            self.key_derivation_key = key_derivation_key
            VapiStruct.__init__(self)


    NativeProviderCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.native_provider_create_spec', {
            'key_id': type.OptionalType(type.StringType()),
            'key_derivation_key': type.OptionalType(type.SecretType()),
        },
        NativeProviderCreateSpec,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Providers.CreateSpec`` class contains attributes that describe the
        desired configuration for a new provider. This class was added in vSphere
        API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     provider=None,
                     constraints=None,
                     native_spec=None,
                    ):
            """
            :type  provider: :class:`str`
            :param provider: Provider identifier. 
                
                A unique string provided by the client.. This attribute was added
                in vSphere API 7.0.2.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``.
            :type  constraints: :class:`Providers.ConstraintsSpec` or ``None``
            :param constraints: The constraints on the provider. This attribute was added in
                vSphere API 7.0.2.0.
                If None there are no constraints on the provider.
            :type  native_spec: :class:`Providers.NativeProviderCreateSpec` or ``None``
            :param native_spec: Native provider create spec. This attribute was added in vSphere
                API 7.0.2.0.
                This attribute is required when creating a
                :attr:`Providers.Type.NATIVE` provider.
            """
            self.provider = provider
            self.constraints = constraints
            self.native_spec = native_spec
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.create_spec', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.crypto_manager.kms.provider'),
            'constraints': type.OptionalType(type.ReferenceType(__name__, 'Providers.ConstraintsSpec')),
            'native_spec': type.OptionalType(type.ReferenceType(__name__, 'Providers.NativeProviderCreateSpec')),
        },
        CreateSpec,
        False,
        None))


    class NativeProviderUpdateSpec(VapiStruct):
        """
        The ``Providers.NativeProviderUpdateSpec`` class contains attributes that
        describe the desired configuration for :attr:`Providers.Type.NATIVE`
        provider. Exporting a :attr:`Providers.Type.NATIVE` provider to create a
        new back-up is suggested after any update. This class was added in vSphere
        API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     key_id=None,
                    ):
            """
            :type  key_id: :class:`str` or ``None``
            :param key_id: Key identifier for the provider. 
                
                The key identifier is required to be a 128-bit UUID represented as
                a hexadecimal string in "12345678-abcd-1234-cdef-123456789abc"
                format.. This attribute was added in vSphere API 7.0.2.0.
                If None, the key identifier will remain unchanged.
            """
            self.key_id = key_id
            VapiStruct.__init__(self)


    NativeProviderUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.native_provider_update_spec', {
            'key_id': type.OptionalType(type.StringType()),
        },
        NativeProviderUpdateSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Providers.UpdateSpec`` class contains attributes that describe the
        new configuration for an existing provider. This class was added in vSphere
        API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     native_spec=None,
                    ):
            """
            :type  native_spec: :class:`Providers.NativeProviderUpdateSpec` or ``None``
            :param native_spec: New Configuration for :attr:`Providers.Type.NATIVE` provider. 
                
                . This attribute was added in vSphere API 7.0.2.0.
                If None, provider configuration will remain unchanged.
            """
            self.native_spec = native_spec
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.update_spec', {
            'native_spec': type.OptionalType(type.ReferenceType(__name__, 'Providers.NativeProviderUpdateSpec')),
        },
        UpdateSpec,
        False,
        None))


    class ExportSpec(VapiStruct):
        """
        The ``Providers.ExportSpec`` class contains attributes that are needed to
        export a provider. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     provider=None,
                     password=None,
                    ):
            """
            :type  provider: :class:`str`
            :param provider: Provider identifier. This attribute was added in vSphere API
                7.0.2.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``.
            :type  password: :class:`str` or ``None``
            :param password: Password used to encrypt the exported configuration. This attribute
                was added in vSphere API 7.0.2.0.
                If None or empty, the configuration will not be encrypted.
            """
            self.provider = provider
            self.password = password
            VapiStruct.__init__(self)


    ExportSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.export_spec', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.crypto_manager.kms.provider'),
            'password': type.OptionalType(type.SecretType()),
        },
        ExportSpec,
        False,
        None))


    class Token(VapiStruct):
        """
        The ``Providers.Token`` class contains information about the token required
        to be passed in the HTTP header in the HTTP GET request to download the
        provider configuration. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     token=None,
                     expiry=None,
                    ):
            """
            :type  token: :class:`str`
            :param token: A one-time, short-lived token required in "Authorization" field of
                the HTTP header of the request to the url. 
                
                After the token expires, any attempt to download the configuration
                with said token will fail.. This attribute was added in vSphere API
                7.0.2.0.
            :type  expiry: :class:`datetime.datetime`
            :param expiry: Expiry time of the token. This attribute was added in vSphere API
                7.0.2.0.
            """
            self.token = token
            self.expiry = expiry
            VapiStruct.__init__(self)


    Token._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.token', {
            'token': type.SecretType(),
            'expiry': type.DateTimeType(),
        },
        Token,
        False,
        None))


    class Location(VapiStruct):
        """
        The ``Providers.Location`` class contains the location as well as a token
        required (as a header in the HTTP GET request) to download the
        configuration. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     url=None,
                     download_token=None,
                    ):
            """
            :type  url: :class:`str`
            :param url: Provider configuration download URL. This attribute was added in
                vSphere API 7.0.2.0.
            :type  download_token: :class:`Providers.Token`
            :param download_token: Information about the token required in the HTTP GET request to
                download the provider configuration. This attribute was added in
                vSphere API 7.0.2.0.
            """
            self.url = url
            self.download_token = download_token
            VapiStruct.__init__(self)


    Location._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.location', {
            'url': type.URIType(),
            'download_token': type.ReferenceType(__name__, 'Providers.Token'),
        },
        Location,
        False,
        None))


    class ExportResult(VapiStruct):
        """
        The ``Providers.ExportResult`` class contains result of
        :func:`Providers.export` operation. This class was added in vSphere API
        7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'LOCATION' : [('location', True)],
                }
            ),
        ]



        def __init__(self,
                     type=None,
                     location=None,
                    ):
            """
            :type  type: :class:`Providers.ExportType`
            :param type: Type of provider export result. This attribute was added in vSphere
                API 7.0.2.0.
            :type  location: :class:`Providers.Location`
            :param location: Location of the exported configuration. This attribute was added in
                vSphere API 7.0.2.0.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Providers.ExportType.LOCATION`.
            """
            self.type = type
            self.location = location
            VapiStruct.__init__(self)


    ExportResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.export_result', {
            'type': type.ReferenceType(__name__, 'Providers.ExportType'),
            'location': type.OptionalType(type.ReferenceType(__name__, 'Providers.Location')),
        },
        ExportResult,
        False,
        None))


    class ImportSpec(VapiStruct):
        """
        The ``Providers.ImportSpec`` class contains attributes that are needed to
        import a provider. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     config=None,
                     password=None,
                     constraints=None,
                     dry_run=None,
                    ):
            """
            :type  config: :class:`str` or ``None``
            :param config: Configuration to import. This attribute was added in vSphere API
                7.0.2.0.
                Currently this is required. Other import methods may be supported
                in the future.
            :type  password: :class:`str` or ``None``
            :param password: Password to decrypt the configuration to import. This attribute was
                added in vSphere API 7.0.2.0.
                If None or empty, configuration to import must be unencrypted.
            :type  constraints: :class:`Providers.ConstraintsSpec` or ``None``
            :param constraints: Constraints to impose on the imported provider. This attribute was
                added in vSphere API 7.0.2.0.
                If None, the imported provider constraints will match the exported
                provider constraints.
            :type  dry_run: :class:`bool` or ``None``
            :param dry_run: Whether to perform a trial import without actuallly creating a
                provider. This attribute was added in vSphere API 7.0.2.0.
                If None, a new provider will be created.
            """
            self.config = config
            self.password = password
            self.constraints = constraints
            self.dry_run = dry_run
            VapiStruct.__init__(self)


    ImportSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.import_spec', {
            'config': type.OptionalType(type.BlobType()),
            'password': type.OptionalType(type.SecretType()),
            'constraints': type.OptionalType(type.ReferenceType(__name__, 'Providers.ConstraintsSpec')),
            'dry_run': type.OptionalType(type.BooleanType()),
        },
        ImportSpec,
        False,
        None))


    class ImportResult(VapiStruct):
        """
        The ``Providers.ImportResult`` class contains result of the
        :func:`Providers.import_provider` operation. This class was added in
        vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'NATIVE' : [('native_info', True)],
                }
            ),
        ]



        def __init__(self,
                     provider=None,
                     type=None,
                     native_info=None,
                     export_time=None,
                     constraints=None,
                    ):
            """
            :type  provider: :class:`str`
            :param provider: Provider identifier. This attribute was added in vSphere API
                7.0.2.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.crypto_manager.kms.provider``.
            :type  type: :class:`Providers.Type`
            :param type: Provider type. This attribute was added in vSphere API 7.0.2.0.
            :type  native_info: :class:`Providers.NativeProviderInfo`
            :param native_info: Native provider information. This attribute was added in vSphere
                API 7.0.2.0.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Providers.Type.NATIVE`.
            :type  export_time: :class:`datetime.datetime`
            :param export_time: Time when the provider was exported. This attribute was added in
                vSphere API 7.0.2.0.
            :type  constraints: :class:`Providers.Constraints` or ``None``
            :param constraints: The constraints on the provider. This attribute was added in
                vSphere API 7.0.2.0.
                If None, there are no constraints on the provider.
            """
            self.provider = provider
            self.type = type
            self.native_info = native_info
            self.export_time = export_time
            self.constraints = constraints
            VapiStruct.__init__(self)


    ImportResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.crypto_manager.kms.providers.import_result', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.crypto_manager.kms.provider'),
            'type': type.ReferenceType(__name__, 'Providers.Type'),
            'native_info': type.OptionalType(type.ReferenceType(__name__, 'Providers.NativeProviderInfo')),
            'export_time': type.DateTimeType(),
            'constraints': type.OptionalType(type.ReferenceType(__name__, 'Providers.Constraints')),
        },
        ImportResult,
        False,
        None))



    def list(self,
             filter_spec=None,
             ):
        """
        Return a list of providers. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  filter_spec: :class:`Providers.FilterSpec` or ``None``
        :param filter_spec: Filter for the providers list.
            If None, the behavior is equivalent to a
            :class:`Providers.FilterSpec` with all attributes None.
        :rtype: :class:`list` of :class:`Providers.Summary`
        :return: Summary of providers.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the spec is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Cryptographer.ReadKeyServersInfo``.
        """
        return self._invoke('list',
                            {
                            'filter_spec': filter_spec,
                            })

    def create(self,
               spec,
               ):
        """
        Add a new provider. This method was added in vSphere API 7.0.2.0.

        :type  spec: :class:`Providers.CreateSpec`
        :param spec: Provider information.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a provider with the same identifier already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the spec is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if creating a provider of the type is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Cryptographer.ManageKeyServers``.
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
        Update an existing provider. This method was added in vSphere API
        7.0.2.0.

        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.crypto_manager.kms.provider``.
        :type  spec: :class:`Providers.UpdateSpec`
        :param spec: Provider information.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the spec is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the provider's type does not allow updates.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Cryptographer.ManageKeyServers``.
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
        Remove a provider. This method was added in vSphere API 7.0.2.0.

        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.crypto_manager.kms.provider``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the provider identifier is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the provider's type does not allow deletion.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Cryptographer.ManageKeyServers``.
        """
        return self._invoke('delete',
                            {
                            'provider': provider,
                            })

    def get(self,
            provider,
            ):
        """
        Return information about a provider. This method was added in vSphere
        API 7.0.2.0.

        :type  provider: :class:`str`
        :param provider: Identifier of the provider.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.crypto_manager.kms.provider``.
        :rtype: :class:`Providers.Info`
        :return: Information of the provider.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the provider identifier is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the provider is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Cryptographer.ReadKeyServersInfo``.
        """
        return self._invoke('get',
                            {
                            'provider': provider,
                            })

    def export(self,
               spec,
               ):
        """
        Export provider configuration. This method was added in vSphere API
        7.0.2.0.

        :type  spec: :class:`Providers.ExportSpec`
        :param spec: ExportSpec needed to export a provider.
        :rtype: :class:`Providers.ExportResult`
        :return: ExportResult.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the provider identifier is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the provider with the identifier is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the provider's type does not allow export.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Cryptographer.ManageKeyServers``.
        """
        return self._invoke('export',
                            {
                            'spec': spec,
                            })

    def import_provider(self,
                        spec,
                        ):
        """
        Import provider configuration. This method was added in vSphere API
        7.0.2.0.

        :type  spec: :class:`Providers.ImportSpec`
        :param spec: ImportSpec needed to import a provider.
        :rtype: :class:`Providers.ImportResult`
        :return: importResult ImportResult.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a provider with the same identifier already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the config or the password is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Cryptographer.ManageKeyServers``.
        """
        return self._invoke('import_provider',
                            {
                            'spec': spec,
                            })
class _ProvidersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter_spec': type.OptionalType(type.ReferenceType(__name__, 'Providers.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/crypto-manager/kms/providers',
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

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Providers.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/crypto-manager/kms/providers',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'provider': type.IdType(resource_types='com.vmware.vcenter.crypto_manager.kms.provider'),
            'spec': type.ReferenceType(__name__, 'Providers.UpdateSpec'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/crypto-manager/kms/providers/{provider}',
            request_body_parameter='spec',
            path_variables={
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
            'provider': type.IdType(resource_types='com.vmware.vcenter.crypto_manager.kms.provider'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/crypto-manager/kms/providers/{provider}',
            path_variables={
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
            url_template='/vcenter/crypto-manager/kms/providers/{provider}',
            path_variables={
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

        # properties for export operation
        export_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Providers.ExportSpec'),
        })
        export_error_dict = {
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        export_input_value_validator_list = [
        ]
        export_output_validator_list = [
        ]
        export_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/crypto-manager/kms/providers',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'export',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for import_provider operation
        import_provider_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Providers.ImportSpec'),
        })
        import_provider_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        import_provider_input_value_validator_list = [
        ]
        import_provider_output_validator_list = [
        ]
        import_provider_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/crypto-manager/kms/providers',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'import',
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
            'create': {
                'input_type': create_input_type,
                'output_type': type.VoidType(),
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
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Providers.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'export': {
                'input_type': export_input_type,
                'output_type': type.ReferenceType(__name__, 'Providers.ExportResult'),
                'errors': export_error_dict,
                'input_value_validator_list': export_input_value_validator_list,
                'output_validator_list': export_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'import_provider': {
                'input_type': import_provider_input_type,
                'output_type': type.ReferenceType(__name__, 'Providers.ImportResult'),
                'errors': import_provider_error_dict,
                'input_value_validator_list': import_provider_input_value_validator_list,
                'output_validator_list': import_provider_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
            'export': export_rest_metadata,
            'import_provider': import_provider_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.crypto_manager.kms.providers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Providers': Providers,
    }

