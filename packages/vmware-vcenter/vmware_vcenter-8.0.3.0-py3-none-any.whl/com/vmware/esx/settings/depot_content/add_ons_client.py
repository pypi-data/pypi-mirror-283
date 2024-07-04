# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.depot_content.add_ons.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.depot_content.add_ons_client`` module provides
classes to retrieve OEM specific add-on versions from the depot.

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
    The ``Versions`` class provides methods to get OEM add-on versions from the
    sync'ed and imported depots.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.depot_content.add_ons.versions'
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
        for a OEM add-on.

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
        'com.vmware.esx.settings.depot_content.add_ons.versions.category_type',
        CategoryType))


    class RemovedComponentInfo(VapiStruct):
        """
        The ``Versions.RemovedComponentInfo`` class defines the information
        regarding a component removed by the OEM add-on.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     display_name=None,
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
            """
            self.name = name
            self.display_name = display_name
            VapiStruct.__init__(self)


    RemovedComponentInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.depot_content.add_ons.versions.removed_component_info', {
            'name': type.IdType(resource_types='com.vmware.esx.settings.component'),
            'display_name': type.StringType(),
        },
        RemovedComponentInfo,
        False,
        None))


    class ComponentInfo(VapiStruct):
        """
        The ``Versions.ComponentInfo`` class defines the information regarding a
        component present in OEM add-on.

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
            :param display_version: Human readable version of the OEM add-on.
            """
            self.name = name
            self.display_name = display_name
            self.version = version
            self.display_version = display_version
            VapiStruct.__init__(self)


    ComponentInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.depot_content.add_ons.versions.component_info', {
            'name': type.IdType(resource_types='com.vmware.esx.settings.component'),
            'display_name': type.StringType(),
            'version': type.StringType(),
            'display_version': type.StringType(),
        },
        ComponentInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Versions.Info`` class defines the information regarding a OEM add-on
        version.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     display_name=None,
                     vendor=None,
                     display_version=None,
                     summary=None,
                     description=None,
                     category=None,
                     kb=None,
                     release_date=None,
                     components=None,
                     removed_components=None,
                    ):
            """
            :type  display_name: :class:`str`
            :param display_name: Display name of the OEM add-on.
            :type  vendor: :class:`str`
            :param vendor: Vendor of the OEM add-on.
            :type  display_version: :class:`str`
            :param display_version: Human readable version of the OEM add-on.
            :type  summary: :class:`str`
            :param summary: Summary of the OEM add-on.
            :type  description: :class:`str`
            :param description: Discription of the OEM add-on.
            :type  category: :class:`Versions.CategoryType`
            :param category: Category of the OEM add-on.
            :type  kb: :class:`str`
            :param kb: Link to kb article related to this the OEM add-on.
            :type  release_date: :class:`datetime.datetime`
            :param release_date: Release date of the OEM add-on.
            :type  components: :class:`list` of :class:`Versions.ComponentInfo`
            :param components: List of components in this OEM add-on.
            :type  removed_components: :class:`list` of :class:`Versions.RemovedComponentInfo`
            :param removed_components: List of components removed by this OEM add-on.
            """
            self.display_name = display_name
            self.vendor = vendor
            self.display_version = display_version
            self.summary = summary
            self.description = description
            self.category = category
            self.kb = kb
            self.release_date = release_date
            self.components = components
            self.removed_components = removed_components
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.depot_content.add_ons.versions.info', {
            'display_name': type.StringType(),
            'vendor': type.StringType(),
            'display_version': type.StringType(),
            'summary': type.StringType(),
            'description': type.StringType(),
            'category': type.ReferenceType(__name__, 'Versions.CategoryType'),
            'kb': type.URIType(),
            'release_date': type.DateTimeType(),
            'components': type.ListType(type.ReferenceType(__name__, 'Versions.ComponentInfo')),
            'removed_components': type.ListType(type.ReferenceType(__name__, 'Versions.RemovedComponentInfo')),
        },
        Info,
        False,
        None))



    def get(self,
            name,
            version,
            ):
        """
        Returns information about a given OEM add-on version in the depot.

        :type  name: :class:`str`
        :param name: Name of the OEM add-on
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.add_on``.
        :type  version: :class:`str`
        :param version: Version of the OEM add-on
        :rtype: :class:`Versions.Info`
        :return: Information about the given OEM add-on
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if OEM add-on with given version is not found.
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
                            'name': name,
                            'version': version,
                            })
class _VersionsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'name': type.IdType(resource_types='com.vmware.esx.settings.add_on'),
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
            url_template='/esx/settings/depot-content/add-ons/{name}/versions/{version}',
            path_variables={
                'name': 'name',
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
            self, iface_name='com.vmware.esx.settings.depot_content.add_ons.versions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Versions': Versions,
    }

