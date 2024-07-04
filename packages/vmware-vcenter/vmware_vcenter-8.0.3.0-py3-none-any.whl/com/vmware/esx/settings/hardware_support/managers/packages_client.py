# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.hardware_support.managers.packages.
#---------------------------------------------------------------------------

"""


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
    The ``Versions`` class provides methods to inspect a Hardware Support
    Package (HSP)'s detailed information.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hardware_support.managers.packages.versions'
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

    class RemovedComponentInfo(VapiStruct):
        """
        The ``Versions.RemovedComponentInfo`` class defines the information
        regarding a component removed by the HSP manifest.

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
        'com.vmware.esx.settings.hardware_support.managers.packages.versions.removed_component_info', {
            'name': type.IdType(resource_types='com.vmware.esx.settings.component'),
            'display_name': type.StringType(),
        },
        RemovedComponentInfo,
        False,
        None))


    class ComponentInfo(VapiStruct):
        """
        The ``Versions.ComponentInfo`` class defines the information regarding a
        component present in HSP manifest.

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
            :param display_version: Human readable version of the HSP manifest.
            """
            self.name = name
            self.display_name = display_name
            self.version = version
            self.display_version = display_version
            VapiStruct.__init__(self)


    ComponentInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hardware_support.managers.packages.versions.component_info', {
            'name': type.IdType(resource_types='com.vmware.esx.settings.component'),
            'display_name': type.StringType(),
            'version': type.StringType(),
            'display_version': type.StringType(),
        },
        ComponentInfo,
        False,
        None))


    class PackageInfo(VapiStruct):
        """
        The ``Versions.PackageInfo`` class contains attributes that describe a
        particular 3rd party Hardware Support Package (HSP)

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     pkg=None,
                     version=None,
                     description=None,
                     supported_releases=None,
                     components=None,
                     removed_components=None,
                    ):
            """
            :type  pkg: :class:`str`
            :param pkg: Name of the Hardware Support Package (e.g. "Jan. 2018 Release" or
                "Latest Hardware Support Package for Frobozz GenX hardware")
                selected
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.setting.hardware_support.package``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.setting.hardware_support.package``.
            :type  version: :class:`str`
            :param version: Version of the Hardware Support Package (e.g. "20180128.1" or
                "v42") selected
            :type  description: :class:`str`
            :param description: Description of the Hardware Support Package (HSP) (e.g. for use in
                help bubble)
            :type  supported_releases: :class:`set` of :class:`str`
            :param supported_releases: Supported vSphere releases
            :type  components: :class:`list` of :class:`Versions.ComponentInfo`
            :param components: List of components in this HSP manifest.
            :type  removed_components: :class:`list` of :class:`Versions.RemovedComponentInfo`
            :param removed_components: List of components removed by this HSP manifest.
            """
            self.pkg = pkg
            self.version = version
            self.description = description
            self.supported_releases = supported_releases
            self.components = components
            self.removed_components = removed_components
            VapiStruct.__init__(self)


    PackageInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hardware_support.managers.packages.versions.package_info', {
            'pkg': type.IdType(resource_types='com.vmware.esx.setting.hardware_support.package'),
            'version': type.StringType(),
            'description': type.StringType(),
            'supported_releases': type.SetType(type.StringType()),
            'components': type.ListType(type.ReferenceType(__name__, 'Versions.ComponentInfo')),
            'removed_components': type.ListType(type.ReferenceType(__name__, 'Versions.RemovedComponentInfo')),
        },
        PackageInfo,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Versions.FilterSpec`` class contains attributes used to filter the
        results when retrieving Hardware Support Packages (HSPs) information.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     base_image_version=None,
                    ):
            """
            :type  base_image_version: :class:`str` or ``None``
            :param base_image_version: vSphere release version for the component information in the
                Hardware Support Package (HSP). Only Hardware Support Packages
                (HSPs) compatible with the vSphere release version specified in
                'baseImageVersion' will be returned. The 'baseImageVersion'
                parameter should be a full numeric base image version string (e.g.
                "7.1.0-2.3.436234"). Future implementations may support version
                specification by prefix (e.g. "7.1" to specify all updates and
                builds of 7.1) or other forms of specification (e.g. ">=7.0").
                Hardware Support Pacakges (HSPs) may be advertised as supporting
                truncated version strings to indicate the remainder is wildcarded.
                Matching is on the specified substring only, so a bundle supporting
                "7.1.0-2" would match a 'release' parameter of "7.1.0-2.3.436234"
                as well as "7.1.0-2.1.4133564" and "7.1.0-2.0.355667" but not
                "7.1.0-3.0.63445" or any base image version starting with "7.2".
                Note that we require compatible base image versions be specified at
                least down to the update version (i.e. "7.0" is insufficiently
                constrained)
                If None, all supported releases will be returned but no specific
                component information (added or deleted) will be included.
            """
            self.base_image_version = base_image_version
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hardware_support.managers.packages.versions.filter_spec', {
            'base_image_version': type.OptionalType(type.StringType()),
        },
        FilterSpec,
        False,
        None))



    def get(self,
            manager,
            pkg,
            version,
            filter=None,
            ):
        """
        Returns the detailed information for a specific version of an available
        Hardware Support Packages (HSPs) as specified by the Hardware Support
        Manager (HSM)

        :type  manager: :class:`str`
        :param manager: Identifier for the Hardware Support Manager (HSM).
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.setting.hardware_support.manager``.
        :type  pkg: :class:`str`
        :param pkg: The name of the Hardware Support Package (HSP)
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.setting.hardware_support.package``.
        :type  version: :class:`str`
        :param version: The version of the Hardware Support Package (HSP)
        :type  filter: :class:`Versions.FilterSpec` or ``None``
        :param filter: Specification of detailed information to be returned
            If None, the behavior is equivalent to a
            :class:`Versions.FilterSpec` with all attributes None, which means
            all releases supported are returned but no component information
            for any particular release is included.
        :rtype: :class:`Versions.PackageInfo`
        :return: detailed information on Hardware Support Packages (HSPs)
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If any of the specified parameters are Invalid (e.g. if the release
            version specified in the query parameter is not, in fact, among
            those supported by the Hardware Support Package (HSP).
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no Hardware Support Manager (HSM) with the specified
            name, or no Hardware Support Package (HSP) with the specified name
            and version.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated. named ``manager`` in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have the required privilege to perform the
            operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.lifecycleSettings.Read``.
        """
        return self._invoke('get',
                            {
                            'manager': manager,
                            'pkg': pkg,
                            'version': version,
                            'filter': filter,
                            })
class _VersionsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'manager': type.IdType(resource_types='com.vmware.esx.setting.hardware_support.manager'),
            'pkg': type.IdType(resource_types='com.vmware.esx.setting.hardware_support.package'),
            'version': type.StringType(),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Versions.FilterSpec')),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
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
            url_template='/esx/settings/hardware-support/managers/{manager}/packages/{pkg}/versions/{version}',
            path_variables={
                'manager': 'manager',
                'pkg': 'pkg',
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
                'output_type': type.ReferenceType(__name__, 'Versions.PackageInfo'),
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
            self, iface_name='com.vmware.esx.settings.hardware_support.managers.packages.versions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Versions': Versions,
    }

