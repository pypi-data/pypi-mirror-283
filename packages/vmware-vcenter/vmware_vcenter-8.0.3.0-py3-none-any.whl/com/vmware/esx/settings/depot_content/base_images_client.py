# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.depot_content.base_images.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.depot_content.base_images_client`` module
provides classes to retrieve base_images from the depot.

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


class Versions(VapiInterface):
    """
    The ``Versions`` class provides methods to get versions of base images from
    the sync'ed and imported depots.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.depot_content.base_images.versions'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VersionsStub)
        self._VAPI_OPERATION_IDS = {}

    class CategoryType(Enum):
        """
        The ``Versions.CategoryType`` class defines possible values of categories
        for a base image.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        SECURITY = None
        """
        Security

        """
        ENHANCEMENT = None
        """
        Enhancement

        """
        BUGFIX = None
        """
        Bugfix

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`CategoryType` instance.
            """
            Enum.__init__(string)

    CategoryType._set_values({
        'SECURITY': CategoryType('SECURITY'),
        'ENHANCEMENT': CategoryType('ENHANCEMENT'),
        'BUGFIX': CategoryType('BUGFIX'),
    })
    CategoryType._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.depot_content.base_images.versions.category_type',
        CategoryType))


    class ComponentVersionInfo(VapiStruct):
        """
        The ``Versions.ComponentVersionInfo`` class defines the information
        regarding a component present in base image.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     display_name=None,
                     version=None,
                     display_version=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Identifier of the component.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.settings.component``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.esx.settings.component``.
            :type  display_name: :class:`str`
            :param display_name: Display name of the component.
            :type  version: :class:`str`
            :param version: Version of the component.
            :type  display_version: :class:`str`
            :param display_version: Human readable version of the base image.
            """
            self.name = name
            self.display_name = display_name
            self.version = version
            self.display_version = display_version
            VapiStruct.__init__(self)


    ComponentVersionInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.depot_content.base_images.versions.component_version_info', {
            'name': type.IdType(resource_types='com.vmware.esx.settings.component'),
            'display_name': type.StringType(),
            'version': type.StringType(),
            'display_version': type.StringType(),
        },
        ComponentVersionInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Versions.Info`` class defines the information regarding a base image.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     display_name=None,
                     version=None,
                     display_version=None,
                     summary=None,
                     description=None,
                     category=None,
                     kb=None,
                     release_date=None,
                     components=None,
                     quick_patch_compatible_versions=None,
                    ):
            """
            :type  display_name: :class:`str`
            :param display_name: Display name of the base image.
            :type  version: :class:`str`
            :param version: Version of the base image.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.settings.base_image``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.esx.settings.base_image``.
            :type  display_version: :class:`str`
            :param display_version: Human readable version of the base image.
            :type  summary: :class:`str`
            :param summary: Summary of the base image.
            :type  description: :class:`str`
            :param description: Discription of the base image.
            :type  category: :class:`Versions.CategoryType`
            :param category: Category of the base image.
            :type  kb: :class:`str`
            :param kb: Link to kb article related to this the base image.
            :type  release_date: :class:`datetime.datetime`
            :param release_date: Release date of the base image.
            :type  components: :class:`list` of :class:`Versions.ComponentVersionInfo`
            :param components: List of components in this base image.
            :type  quick_patch_compatible_versions: (:class:`dict` of :class:`str` and :class:`str`) or ``None``
            :param quick_patch_compatible_versions: For base images this base image can quick patch from, map their
                full versions to display versions. This attribute was added in
                vSphere API 8.0.3.0.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.base_image``. When methods return a
                value of this class as a return value, the key in the attribute
                :class:`dict` will be an identifier for the resource type:
                ``com.vmware.esx.settings.base_image``.
                If None this base image does not support quick patch.
            """
            self.display_name = display_name
            self.version = version
            self.display_version = display_version
            self.summary = summary
            self.description = description
            self.category = category
            self.kb = kb
            self.release_date = release_date
            self.components = components
            self.quick_patch_compatible_versions = quick_patch_compatible_versions
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.depot_content.base_images.versions.info', {
            'display_name': type.StringType(),
            'version': type.IdType(resource_types='com.vmware.esx.settings.base_image'),
            'display_version': type.StringType(),
            'summary': type.StringType(),
            'description': type.StringType(),
            'category': type.ReferenceType(__name__, 'Versions.CategoryType'),
            'kb': type.URIType(),
            'release_date': type.DateTimeType(),
            'components': type.ListType(type.ReferenceType(__name__, 'Versions.ComponentVersionInfo')),
            'quick_patch_compatible_versions': type.OptionalType(type.MapType(type.IdType(), type.StringType())),
        },
        Info,
        False,
        None))



    def get(self,
            version,
            ):
        """
        Returns information about a given base image version in the depot.

        :type  version: :class:`str`
        :param version: Version of the base image
        :rtype: :class:`Versions.Info`
        :return: Information about the given base image
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if base image with given version is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.lifecycleSettings.Read``.
        """
        return self._invoke('get',
                            {
                            'version': version,
                            })
class _VersionsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'version': type.StringType(),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/depot-content/base-images/versions/{version}',
            path_variables={
                'version': 'version',
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
                'output_type': type.ReferenceType(__name__, 'Versions.Info'),
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
            self, iface_name='com.vmware.esx.settings.depot_content.base_images.versions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Versions': Versions,
    }

