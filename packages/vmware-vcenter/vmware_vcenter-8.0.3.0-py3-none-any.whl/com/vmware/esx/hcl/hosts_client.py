# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.hcl.hosts.
#---------------------------------------------------------------------------

"""


"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from com.vmware.cis_client import Tasks
from vmware.vapi.stdlib.client.task import Task
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


class CompatibilityReleases(VapiInterface):
    """
    This class provides methods to list available releases for generating
    compatibility report for a specific ESXi host.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.hcl.hosts.compatibility_releases'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CompatibilityReleasesStub)
        self._VAPI_OPERATION_IDS = {}

    class EsxiCompatibilityReleases(VapiStruct):
        """
        This ``CompatibilityReleases.EsxiCompatibilityReleases`` class contains
        attributes that describe available releases for generating compatibility
        report for a specific ESXi host.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     current_compatibility_release=None,
                     newer_compatibility_releases=None,
                     notifications=None,
                    ):
            """
            :type  current_compatibility_release: :class:`str`
            :param current_compatibility_release: The current release of the ESXi, which also can be checked for
                compatibility. 
                
                The information for the release does not include patch information.
            :type  newer_compatibility_releases: :class:`list` of :class:`str`
            :param newer_compatibility_releases: The available ESXi releases, greater than the current one, than can
                be checked for compatibility.
            :type  notifications: :class:`com.vmware.esx.hcl_client.Notifications`
            :param notifications: Notifications returned by the operation.
            """
            self.current_compatibility_release = current_compatibility_release
            self.newer_compatibility_releases = newer_compatibility_releases
            self.notifications = notifications
            VapiStruct.__init__(self)


    EsxiCompatibilityReleases._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_releases.esxi_compatibility_releases', {
            'current_compatibility_release': type.StringType(),
            'newer_compatibility_releases': type.ListType(type.StringType()),
            'notifications': type.ReferenceType('com.vmware.esx.hcl_client', 'Notifications'),
        },
        EsxiCompatibilityReleases,
        False,
        None))



    def list(self,
             host,
             ):
        """
        Lists the locally available ESXi releases for a given host that can be
        used to generate a compatiblity report. Each host has its own list of
        supported releases depending on its current release.

        :type  host: :class:`str`
        :param host: Contains the MoID identifying the ESXi host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :rtype: :class:`CompatibilityReleases.EsxiCompatibilityReleases`
        :return: Available releases for compatibility for a specified host.
        :raise: :class:`com.vmware.vapi.std.errors_client.InternalServerError` 
            If there is some internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if there is no compatibility data on the vCenter executing the
            operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no host with the given MoID can be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the provided host is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the vCenter this API is executed on is not part of the Customer
            Experience Improvement Program (CEIP).
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown error. The accompanying error message will
            give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.HardwareCompatibility.Read``.
        """
        return self._invoke('list',
                            {
                            'host': host,
                            })
class CompatibilityReport(VapiInterface):
    """
    This class provides methods to generate hardware compatibility report for a
    given ESXi host against a specific ESXi release.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.hcl.hosts.compatibility_report'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CompatibilityReportStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})

    class BiosConstraint(VapiStruct):
        """
        This ``CompatibilityReport.BiosConstraint`` class contains attributes that
        describe the BIOS that is supported for the given server and ESXi release.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     bios=None,
                     notes=None,
                    ):
            """
            :type  bios: :class:`com.vmware.esx.hcl_client.Firmware`
            :param bios: The BIOS information about the constraint.
            :type  notes: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param notes: Any information that should be taken into account when reviewing
                the BIOS constraint.
            """
            self.bios = bios
            self.notes = notes
            VapiStruct.__init__(self)


    BiosConstraint._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_report.bios_constraint', {
            'bios': type.ReferenceType('com.vmware.esx.hcl_client', 'Firmware'),
            'notes': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        BiosConstraint,
        False,
        None))


    class ServerCompatibility(VapiStruct):
        """
        This ``CompatibilityReport.ServerCompatibility`` class contains attributes
        that provide the compatibility information for a server model, cpu and
        BIOS.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     bios_constraints=None,
                     cpu_series=None,
                     supported_releases=None,
                     vcg_link=None,
                     notes=None,
                    ):
            """
            :type  bios_constraints: :class:`list` of :class:`CompatibilityReport.BiosConstraint` or ``None``
            :param bios_constraints: Lists the BIOS constraints that the target ESXi release has for
                this server.
                If None no constraints are present as server is either not
                compatible or compatibility information is not found.
            :type  cpu_series: :class:`str`
            :param cpu_series: The CPU series name.
            :type  supported_releases: :class:`list` of :class:`str` or ``None``
            :param supported_releases: Provides information about supported releases for this entry.
                If None server is compatible with the given target release.
            :type  vcg_link: :class:`str`
            :param vcg_link: Provides link to the VMware Compatibility Guide for further
                information on the compatibility.
            :type  notes: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
            :param notes: Information that needs to be taken into account when considering
                this server hardware compatibility.
                Only :class:`set` if there is any information reported.
            """
            self.bios_constraints = bios_constraints
            self.cpu_series = cpu_series
            self.supported_releases = supported_releases
            self.vcg_link = vcg_link
            self.notes = notes
            VapiStruct.__init__(self)


    ServerCompatibility._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_report.server_compatibility', {
            'bios_constraints': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'CompatibilityReport.BiosConstraint'))),
            'cpu_series': type.StringType(),
            'supported_releases': type.OptionalType(type.ListType(type.StringType())),
            'vcg_link': type.URIType(),
            'notes': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'))),
        },
        ServerCompatibility,
        False,
        None))


    class ServerHclInfo(VapiStruct):
        """
        This ``CompatibilityReport.ServerHclInfo`` class contains attributes that
        describe the server of a ESXi host and its compatibility information.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     server=None,
                     matches=None,
                     model_compatibility=None,
                    ):
            """
            :type  server: :class:`com.vmware.esx.hcl_client.Server`
            :param server: Information about the server.
            :type  matches: :class:`list` of :class:`CompatibilityReport.ServerCompatibility`
            :param matches: Provides information about possible compatibility matches for the
                given server. 
                
                There could be multiple matches returned as there are several
                possible matches in the Compatibility data.
            :type  model_compatibility: :class:`com.vmware.esx.hcl_client.CompatibilityStatus`
            :param model_compatibility: Shows if the server model is compatible with given target ESXi
                release.
            """
            self.server = server
            self.matches = matches
            self.model_compatibility = model_compatibility
            VapiStruct.__init__(self)


    ServerHclInfo._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_report.server_hcl_info', {
            'server': type.ReferenceType('com.vmware.esx.hcl_client', 'Server'),
            'matches': type.ListType(type.ReferenceType(__name__, 'CompatibilityReport.ServerCompatibility')),
            'model_compatibility': type.ReferenceType('com.vmware.esx.hcl_client', 'CompatibilityStatus'),
        },
        ServerHclInfo,
        False,
        None))


    class DeviceConstraint(VapiStruct):
        """
        This ``CompatibilityReport.DeviceConstraint`` class contains attributes
        that describe pair of driver and firmware that are supported for a given
        PCI device and ESXi release.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     driver=None,
                     firmware=None,
                     notes=None,
                    ):
            """
            :type  driver: :class:`com.vmware.esx.hcl_client.Driver`
            :param driver: The driver information about the constraint.
            :type  firmware: :class:`com.vmware.esx.hcl_client.Firmware` or ``None``
            :param firmware: The firmware information about the constraint.
                If None there is no firmware restriction on the driver to work with
                that release.
            :type  notes: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param notes: Any information that should be taken into account when reviewing
                the device constraint.
            """
            self.driver = driver
            self.firmware = firmware
            self.notes = notes
            VapiStruct.__init__(self)


    DeviceConstraint._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_report.device_constraint', {
            'driver': type.ReferenceType('com.vmware.esx.hcl_client', 'Driver'),
            'firmware': type.OptionalType(type.ReferenceType('com.vmware.esx.hcl_client', 'Firmware')),
            'notes': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        DeviceConstraint,
        False,
        None))


    class DeviceHclInfo(VapiStruct):
        """
        This ``CompatibilityReport.DeviceHclInfo`` class contains attributes that
        describe a PCI device of a given ESXi host and its compatibility
        information. 
        
        If there are multiple PCI devices of the same type on the host each one
        will be listed in separate instance of this class.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     compatibility=None,
                     device=None,
                     device_constraints=None,
                     supported_releases=None,
                     vcg_link=None,
                     notes=None,
                    ):
            """
            :type  compatibility: :class:`com.vmware.esx.hcl_client.CompatibilityStatus`
            :param compatibility: Indicates compatibility status of the PCI device.
            :type  device: :class:`com.vmware.esx.hcl_client.PCIDevice`
            :param device: Information about the PCI device.
            :type  device_constraints: :class:`list` of :class:`CompatibilityReport.DeviceConstraint` or ``None``
            :param device_constraints: Lists the constraints the target ESXi release has for this PCI
                device
                If None no constraints are present as PCI device is either not
                compatible or compatibility information is not found.
            :type  supported_releases: :class:`list` of :class:`str` or ``None``
            :param supported_releases: Provides information about supported releases for this device.
                If None device is compatible with the given target release.
            :type  vcg_link: :class:`str` or ``None``
            :param vcg_link: Provides link to the VMware Compatibility Guide for further
                information on the compatibility.
                If None there is no VMware Compatibility link available as this is
                device used by VSAN.
            :type  notes: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
            :param notes: Information that needs to be taken into account when considering
                this device hcl.
                Only :class:`set` if there is any information reported.
            """
            self.compatibility = compatibility
            self.device = device
            self.device_constraints = device_constraints
            self.supported_releases = supported_releases
            self.vcg_link = vcg_link
            self.notes = notes
            VapiStruct.__init__(self)


    DeviceHclInfo._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_report.device_hcl_info', {
            'compatibility': type.ReferenceType('com.vmware.esx.hcl_client', 'CompatibilityStatus'),
            'device': type.ReferenceType('com.vmware.esx.hcl_client', 'PCIDevice'),
            'device_constraints': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'CompatibilityReport.DeviceConstraint'))),
            'supported_releases': type.OptionalType(type.ListType(type.StringType())),
            'vcg_link': type.OptionalType(type.URIType()),
            'notes': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'))),
        },
        DeviceHclInfo,
        False,
        None))


    class HclReport(VapiStruct):
        """
        This ``CompatibilityReport.HclReport`` represents the hardware
        compatibility report generated for a specific host and target ESXi release.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     host=None,
                     target_release=None,
                     server_hcl=None,
                     devices_hcl=None,
                     generated_at=None,
                     notifications=None,
                    ):
            """
            :type  host: :class:`str`
            :param host: FQDN identifying the ESXi host that the report refers to.
            :type  target_release: :class:`str`
            :param target_release: Indicates for which ESXi release the report is generated.
            :type  server_hcl: :class:`CompatibilityReport.ServerHclInfo`
            :param server_hcl: Lists compatibility information for the ESXi's server part.
            :type  devices_hcl: :class:`list` of :class:`CompatibilityReport.DeviceHclInfo` or ``None``
            :param devices_hcl: Lists compatibility information for discoverable PCI devices of the
                host.
                If None the server is not compatible with the requested release and
                the PCI devices cannot be checked.
            :type  generated_at: :class:`datetime.datetime`
            :param generated_at: Specifies the time the report was generated.
            :type  notifications: :class:`com.vmware.esx.hcl_client.Notifications`
            :param notifications: Notifications returned by the operation.
            """
            self.host = host
            self.target_release = target_release
            self.server_hcl = server_hcl
            self.devices_hcl = devices_hcl
            self.generated_at = generated_at
            self.notifications = notifications
            VapiStruct.__init__(self)


    HclReport._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_report.hcl_report', {
            'host': type.URIType(),
            'target_release': type.StringType(),
            'server_hcl': type.ReferenceType(__name__, 'CompatibilityReport.ServerHclInfo'),
            'devices_hcl': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'CompatibilityReport.DeviceHclInfo'))),
            'generated_at': type.DateTimeType(),
            'notifications': type.ReferenceType('com.vmware.esx.hcl_client', 'Notifications'),
        },
        HclReport,
        False,
        None))


    class Result(VapiStruct):
        """
        The ``CompatibilityReport.Result`` class contains the result of hardware
        compatibility report creation operation.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     report=None,
                     identifier=None,
                    ):
            """
            :type  report: :class:`CompatibilityReport.HclReport`
            :param report: The hardware compatibility report.
            :type  identifier: :class:`str` or ``None``
            :param identifier: The identifier of the compatibility report. 
                
                :func:`com.vmware.esx.hcl_client.Reports.get` provides location
                where a file based report based on the
                ``CompatibilityReport.HclReport`` can be downloaded using this
                identifier.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.hcl.resources.CompatibilityReport``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.hcl.resources.CompatibilityReport``.
                None in case of error reported in
                :attr:`CompatibilityReport.HclReport.notifications`.
            """
            self.report = report
            self.identifier = identifier
            VapiStruct.__init__(self)


    Result._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_report.result', {
            'report': type.ReferenceType(__name__, 'CompatibilityReport.HclReport'),
            'identifier': type.OptionalType(type.IdType()),
        },
        Result,
        False,
        None))


    class Spec(VapiStruct):
        """
        The ``CompatibilityReport.Spec`` class contains attributes to describe the
        input configuration for an ESXi's compatibility report generation.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     release=None,
                    ):
            """
            :type  release: :class:`str`
            :param release: A target ESXi release which will be used to generate a
                compatibility report. Releases that can be used to generate report
                can be found using :func:`CompatibilityReleases.list`
            """
            self.release = release
            VapiStruct.__init__(self)


    Spec._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.hosts.compatibility_report.spec', {
            'release': type.StringType(),
        },
        Spec,
        False,
        None))




    def create_task(self,
               host,
               spec=None,
               ):
        """
        Generates hardware compatibility report for a specified ESXi host
        against specific ESXi release.
        
        The result of this operation can be queried by calling the
        cis/tasks/{task-id} where the task-id is the response of this
        operation.

        :type  host: :class:`str`
        :param host: Contains the MoID identifying the ESXi host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  spec: :class:`CompatibilityReport.Spec` or ``None``
        :param spec: Specifies the input parameters for generating compatibility report.
            If None host compatibility will be checked against the current
            release of the ESXi.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no host with the given MoID can be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the provided host is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the vCenter this API is executed on is not part of the Customer
            Experience Improvement Program (CEIP).
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if there is no compatibility data on the vCenter executing the
            operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown error. The accompanying error message will
            give more details about the failure.
        """
        task_id = self._invoke('create$task',
                                {
                                'host': host,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'CompatibilityReport.Result'))
        return task_instance

    def get(self,
            host,
            ):
        """
        Returns the last generated hardware compatibility report for the given
        host.

        :type  host: :class:`str`
        :param host: 
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :rtype: :class:`CompatibilityReport.Result`
        :return: 
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no report generated for the given host. This operation
            does not check if the host id is valid or it exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the vCenter this API is executed on is not part of the Customer
            Experience Improvement Program (CEIP).
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown error. The accompanying error message will
            give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.HardwareCompatibility.Read``.
        """
        return self._invoke('get',
                            {
                            'host': host,
                            })
class _CompatibilityReleasesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.internal_server_error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InternalServerError'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/hcl/hosts/{host}/compatibility-releases',
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

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'CompatibilityReleases.EsxiCompatibilityReleases'),
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
            self, iface_name='com.vmware.esx.hcl.hosts.compatibility_releases',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _CompatibilityReportStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'CompatibilityReport.Spec')),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/hcl/hosts/{host}/compatibility-report',
            request_body_parameter='spec',
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
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/hcl/hosts/{host}/compatibility-report',
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

        operations = {
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'CompatibilityReport.Result'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.hcl.hosts.compatibility_report',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'CompatibilityReleases': CompatibilityReleases,
        'CompatibilityReport': CompatibilityReport,
    }

