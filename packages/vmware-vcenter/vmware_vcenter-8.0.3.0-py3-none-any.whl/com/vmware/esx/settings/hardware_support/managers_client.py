# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.hardware_support.managers.
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


class Packages(VapiInterface):
    """
    The ``Packages`` class provides methods to manage a host's Hardware Support
    Package (HSP) configuration.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hardware_support.managers.packages'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PackagesStub)
        self._VAPI_OPERATION_IDS = {}

    class HardwareSupportPackageInfo(VapiStruct):
        """
        The ``Packages.HardwareSupportPackageInfo`` class contains attributes that
        describe a particular 3rd party Hardware Support Package (HSP)

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     pkg=None,
                     version=None,
                     description=None,
                     supported_releases=None,
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
            """
            self.pkg = pkg
            self.version = version
            self.description = description
            self.supported_releases = supported_releases
            VapiStruct.__init__(self)


    HardwareSupportPackageInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hardware_support.managers.packages.hardware_support_package_info', {
            'pkg': type.IdType(resource_types='com.vmware.esx.setting.hardware_support.package'),
            'version': type.StringType(),
            'description': type.StringType(),
            'supported_releases': type.SetType(type.StringType()),
        },
        HardwareSupportPackageInfo,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Packages.FilterSpec`` class contains attributes used to filter the
        results when listing OEM Hardware Support Packages (HSPs), see
        :func:`Packages.list`).

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     base_image_version=None,
                    ):
            """
            :type  base_image_version: :class:`str` or ``None``
            :param base_image_version: vSphere release version the Hardware Support Package (HSP) must
                support to match the filter. Only Hardware Support Packages (HSPs)
                compatible with the vSphere release version specified in
                'baseImageVersion' will be returned. The 'baseImageVersion'
                parameter should be a full numeric base image version string (e.g.
                "7.1.0-2.3.436234"). Future implementations may support version
                specification by prefix (e.g. "7.1" to specify all updates and
                builds of 7.1) or other forms of specification (e.g. ">=7.0").
                Hardware Support Pacakges (HSPs) may be advertised as supporting
                truncated version strings to indicate the remainder is wildcarded.
                Matching is on the specified substring only, so a bundle supporting
                "7.1.0-2" would match a 'release' parameter of "7.1.0-2.3.436234"
                as well as "7.1.0-2.1.4133564" and "7.1.0-1.0.355667" but not
                "7.1.0-3.0.63445" or any base image version starting with "7.2".
                Note that we require compatible base image versions be specified at
                least down to the update version (i.e. "7.0" is insufficiently
                constrained)
                If None, all packages will be returned, regardless of base image
                version.
            """
            self.base_image_version = base_image_version
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hardware_support.managers.packages.filter_spec', {
            'base_image_version': type.OptionalType(type.StringType()),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             manager,
             filter=None,
             ):
        """
        Returns the list of available Hardware Support Packages (HSPs) for a
        particular host, as specified by its Hardware Support Manager (HSM)

        :type  manager: :class:`str`
        :param manager: Identifier for the Hardware Support Manager (HSM).
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.setting.hardware_support.manager``.
        :type  filter: :class:`Packages.FilterSpec` or ``None``
        :param filter: Specification of Hardware Support Packages (HSPs) to be returned
            If None, the behavior is equivalent to a
            :class:`Packages.FilterSpec` with all attributes None, which means
            all HSPs match the filter.
        :rtype: :class:`list` of :class:`Packages.HardwareSupportPackageInfo`
        :return: List of available Hardware Support Packages (HSPs) for given
            manager
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no Hardware Support Manager (HSM) with the specified
            name
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated. named ``manager`` in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.lifecycleSettings.Read``.
        """
        return self._invoke('list',
                            {
                            'manager': manager,
                            'filter': filter,
                            })
class _PackagesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'manager': type.IdType(resource_types='com.vmware.esx.setting.hardware_support.manager'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Packages.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/hardware-support/managers/{manager}/packages',
            path_variables={
                'manager': 'manager',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'Packages.HardwareSupportPackageInfo')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.hardware_support.managers.packages',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Packages': Packages,
        'packages': 'com.vmware.esx.settings.hardware_support.managers.packages_client.StubFactory',
    }

