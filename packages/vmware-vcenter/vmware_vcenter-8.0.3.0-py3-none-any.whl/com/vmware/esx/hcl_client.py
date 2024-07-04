# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.hcl.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.hcl_client`` module provides classes to query the hardware
compatibility for an ESXi or a cluster.

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

class CompatibilityStatus(Enum):
    """
    The ``CompatibilityStatus`` class defines compatibility status of a given
    server or PCI device against a specific release of ESXi.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    COMPATIBLE = None
    """
    When given hardware is certified for the specified ESXi release but no
    validation of the software of this hardware is performed.

    """
    INCOMPATIBLE = None
    """
    When given hardware is not certified for the specified ESXi release.

    """
    UNAVAILABLE = None
    """
    When there is no information about specified hardware.

    """
    CERTIFIED = None
    """
    When given hardware is certified for the specified ESXi release. Its
    software is also validated and it is also certified.

    """
    NOT_CERTIFIED = None
    """
    When given hardware is certified for the specified ESXi release. Its
    software is also validated and it is not certified.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`CompatibilityStatus` instance.
        """
        Enum.__init__(string)

CompatibilityStatus._set_values({
    'COMPATIBLE': CompatibilityStatus('COMPATIBLE'),
    'INCOMPATIBLE': CompatibilityStatus('INCOMPATIBLE'),
    'UNAVAILABLE': CompatibilityStatus('UNAVAILABLE'),
    'CERTIFIED': CompatibilityStatus('CERTIFIED'),
    'NOT_CERTIFIED': CompatibilityStatus('NOT_CERTIFIED'),
})
CompatibilityStatus._set_binding_type(type.EnumType(
    'com.vmware.esx.hcl.compatibility_status',
    CompatibilityStatus))




class Driver(VapiStruct):
    """
    The ``Driver`` class contains attributes describing information about a
    driver.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 version=None,
                 vendor=None,
                ):
        """
        :type  name: :class:`str`
        :param name: The name of the driver.
        :type  version: :class:`str`
        :param version: The version of the driver.
        :type  vendor: :class:`str` or ``None``
        :param vendor: The vendor that produced the driver.
            If None vendor is unknown.
        """
        self.name = name
        self.version = version
        self.vendor = vendor
        VapiStruct.__init__(self)


Driver._set_binding_type(type.StructType(
    'com.vmware.esx.hcl.driver', {
        'name': type.StringType(),
        'version': type.StringType(),
        'vendor': type.OptionalType(type.StringType()),
    },
    Driver,
    False,
    None))



class Firmware(VapiStruct):
    """
    The ``Firmware`` class contains attributes describing information about a
    firmware.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 version=None,
                 vendor=None,
                ):
        """
        :type  version: :class:`str`
        :param version: The version of the firmware.
        :type  vendor: :class:`str` or ``None``
        :param vendor: The vendor that produced the firmware.
            If None vendor is unknown.
        """
        self.version = version
        self.vendor = vendor
        VapiStruct.__init__(self)


Firmware._set_binding_type(type.StructType(
    'com.vmware.esx.hcl.firmware', {
        'version': type.StringType(),
        'vendor': type.OptionalType(type.StringType()),
    },
    Firmware,
    False,
    None))



class PCIDevice(VapiStruct):
    """
    The ``PCIDevice`` class contains attributes describing information about a
    single PCI device on a host.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 pci_address=None,
                 vid=None,
                 did=None,
                 svid=None,
                 ssid=None,
                 vendor=None,
                 model_name=None,
                 class_code=None,
                 sub_class_code=None,
                 driver=None,
                 firmware=None,
                 used_by_vsan=None,
                ):
        """
        :type  pci_address: :class:`str`
        :param pci_address: The device's address in a given ESXi host.
        :type  vid: :class:`str`
        :param vid: A unique number assigned to each computer hardware device that
            helps to identify the chipset manufacturer. For example, Dell,
            Broadcom, etc.
        :type  did: :class:`str`
        :param did: A unique number that identifies the specific device of the Vendor
            (VID).
        :type  svid: :class:`str`
        :param svid: A unique number that identifies the card manufacturer.
        :type  ssid: :class:`str`
        :param ssid: A unique number that identifies the specific device of Subsystem
            Vendor (SVID).
        :type  vendor: :class:`str`
        :param vendor: The name of the vendor.
        :type  model_name: :class:`str`
        :param model_name: The name of the device model.
        :type  class_code: :class:`str`
        :param class_code: Register that specifies the type of function the device performs.
        :type  sub_class_code: :class:`str`
        :param sub_class_code: Register that specifies the specific function the device performs.
        :type  driver: :class:`Driver`
        :param driver: Currently installed driver used by the device.
        :type  firmware: :class:`Firmware` or ``None``
        :param firmware: Currently installed firmware used by the device.
            If None firmware is unknown.
        :type  used_by_vsan: :class:`bool`
        :param used_by_vsan: Shows whether the device is part of VSAN cluster or not.
        """
        self.pci_address = pci_address
        self.vid = vid
        self.did = did
        self.svid = svid
        self.ssid = ssid
        self.vendor = vendor
        self.model_name = model_name
        self.class_code = class_code
        self.sub_class_code = sub_class_code
        self.driver = driver
        self.firmware = firmware
        self.used_by_vsan = used_by_vsan
        VapiStruct.__init__(self)


PCIDevice._set_binding_type(type.StructType(
    'com.vmware.esx.hcl.PCI_device', {
        'pci_address': type.StringType(),
        'vid': type.StringType(),
        'did': type.StringType(),
        'svid': type.StringType(),
        'ssid': type.StringType(),
        'vendor': type.StringType(),
        'model_name': type.StringType(),
        'class_code': type.StringType(),
        'sub_class_code': type.StringType(),
        'driver': type.ReferenceType(__name__, 'Driver'),
        'firmware': type.OptionalType(type.ReferenceType(__name__, 'Firmware')),
        'used_by_vsan': type.BooleanType(),
    },
    PCIDevice,
    False,
    None))



class Server(VapiStruct):
    """
    The ``Server`` class contains attributes describing information about a
    server.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 model_name=None,
                 vendor=None,
                 cpu_series=None,
                 cpu_features=None,
                 bios=None,
                ):
        """
        :type  model_name: :class:`str`
        :param model_name: The name of the server model (for example, "PowerEdge R740xd").
        :type  vendor: :class:`str`
        :param vendor: The name of the vendor (for example, "Dell").
        :type  cpu_series: :class:`str`
        :param cpu_series: The CPU series name (for example, "Intel Xeon Gold 6100/5100,
            Silver 4100, Bronze 3100 (Skylake-SP) Series"). 
            
            **Note**: This attribute is initialized with the CPU *model* name;
            it's updated to the actual CPU series later, based on recognizing
            one of the CPU series the server hardware is certified with in the
            VCG.s
        :type  cpu_features: :class:`str`
        :param cpu_features: The current CPU features.
        :type  bios: :class:`Firmware`
        :param bios: Currently installed BIOS of the server.
        """
        self.model_name = model_name
        self.vendor = vendor
        self.cpu_series = cpu_series
        self.cpu_features = cpu_features
        self.bios = bios
        VapiStruct.__init__(self)


Server._set_binding_type(type.StructType(
    'com.vmware.esx.hcl.server', {
        'model_name': type.StringType(),
        'vendor': type.StringType(),
        'cpu_series': type.StringType(),
        'cpu_features': type.StringType(),
        'bios': type.ReferenceType(__name__, 'Firmware'),
    },
    Server,
    False,
    None))



class Notification(VapiStruct):
    """
    The ``Notification`` class contains attributes to describe any
    info/warning/error messages that Tasks can raise.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 id=None,
                 time=None,
                 message=None,
                 resolution=None,
                ):
        """
        :type  id: :class:`str`
        :param id: The notification id.
        :type  time: :class:`datetime.datetime`
        :param time: The time the notification was raised/found.
        :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param message: The notification message.
        :type  resolution: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
        :param resolution: The resolution message, if any.
            Only :class:`set` if there is a resolution available for this
            notification.
        """
        self.id = id
        self.time = time
        self.message = message
        self.resolution = resolution
        VapiStruct.__init__(self)


Notification._set_binding_type(type.StructType(
    'com.vmware.esx.hcl.notification', {
        'id': type.StringType(),
        'time': type.DateTimeType(),
        'message': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'resolution': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
    },
    Notification,
    False,
    None))



class Notifications(VapiStruct):
    """
    The ``Notifications`` class contains info/warning/error messages that can
    be reported be the task.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 info=None,
                 warnings=None,
                 errors=None,
                ):
        """
        :type  info: :class:`list` of :class:`Notification` or ``None``
        :param info: Info notification messages reported.
            Only :class:`set` if an info was reported by the task.
        :type  warnings: :class:`list` of :class:`Notification` or ``None``
        :param warnings: Warning notification messages reported.
            Only :class:`set` if an warning was reported by the task.
        :type  errors: :class:`list` of :class:`Notification` or ``None``
        :param errors: Error notification messages reported.
            Only :class:`set` if an error was reported by the task.
        """
        self.info = info
        self.warnings = warnings
        self.errors = errors
        VapiStruct.__init__(self)


Notifications._set_binding_type(type.StructType(
    'com.vmware.esx.hcl.notifications', {
        'info': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'warnings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
    },
    Notifications,
    False,
    None))



class CompatibilityData(VapiInterface):
    """
    This class provides methods to update the local compatibility data residing
    on the vCenter Appliance or to get information about the said data. The
    information in the data is generic VMware compatibility information for
    servers and devices.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.hcl.compatibility_data'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CompatibilityDataStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})

    class Status(VapiStruct):
        """
        The ``CompatibilityData.Status`` class contains attributes to describe the
        information available for the compatibility data.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     updated_at=None,
                     notifications=None,
                    ):
            """
            :type  updated_at: :class:`datetime.datetime`
            :param updated_at: Indicates when the data was last updated.
            :type  notifications: :class:`Notifications`
            :param notifications: Notifications returned by the operation.
            """
            self.updated_at = updated_at
            self.notifications = notifications
            VapiStruct.__init__(self)


    Status._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.compatibility_data.status', {
            'updated_at': type.DateTimeType(),
            'notifications': type.ReferenceType(__name__, 'Notifications'),
        },
        Status,
        False,
        None))



    def get(self):
        """
        Provides information about the compatibility data located on the
        vCenter Appliance.


        :rtype: :class:`CompatibilityData.Status`
        :return: Information about the compatibility data.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if there is no compatibility data on the vCenter executing the
            operation.
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
        return self._invoke('get', None)


    def update_task(self):
        """
        Replaces the local compatibility data with the latest version found
        from VMware official source.


        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if there is compatibility data update in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the vCenter this API is executed on is not part of the Customer
            Experience Improvement Program (CEIP).
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown error. The accompanying error message will
            give more details about the failure.
        """
        task_id = self._invoke('update$task',
                                None)
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class Reports(VapiInterface):
    """
    This class provides methods to download information generated from the
    hardware compatibility feature residing on the vCenter Appliance.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.hcl.reports'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ReportsStub)
        self._VAPI_OPERATION_IDS = {}

    class Token(VapiStruct):
        """
        The ``Reports.Token`` class contains information about the token required
        to be passed in the HTTP header in the HTTP GET request to generate the
        report.

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
            :param token: A one-time, short-lived token required in the HTTP header of the
                request to the url. This token needs to be passed in as a header
                with the name "session-id".
            :type  expiry: :class:`datetime.datetime`
            :param expiry: Expiry time of the token
            """
            self.token = token
            self.expiry = expiry
            VapiStruct.__init__(self)


    Token._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.reports.token', {
            'token': type.SecretType(),
            'expiry': type.DateTimeType(),
        },
        Token,
        False,
        None))


    class Location(VapiStruct):
        """
        The ``Reports.Location`` class contains the URI location to download
        generated compatibility report, as well as a token required (as a header on
        the HTTP GET request) to get the report. The validity of the token is 5
        minutes. After the token expires, any attempt to call the URI with said
        token will fail.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     url=None,
                     report_token=None,
                    ):
            """
            :type  url: :class:`str`
            :param url: Compatibility report download URL.
            :type  report_token: :class:`Reports.Token`
            :param report_token: Information about the token required in the HTTP GET request to
                download the compatibility report.
            """
            self.url = url
            self.report_token = report_token
            VapiStruct.__init__(self)


    Location._set_binding_type(type.StructType(
        'com.vmware.esx.hcl.reports.location', {
            'url': type.URIType(),
            'report_token': type.ReferenceType(__name__, 'Reports.Token'),
        },
        Location,
        False,
        None))



    def get(self,
            report,
            ):
        """
        Returns the location :class:`Reports.Location` information for
        downloading a compatibility report.

        :type  report: :class:`str`
        :param report: identifier of hardware compatiblity report to be downloaded.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.hcl.resources.CompatibilityReport``.
        :rtype: :class:`Reports.Location`
        :return: ``Reports.Location`` class which includes the URI to file, short
            lived token and expiry of the token in the
            :class:`Reports.Location` object.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no report for the given id.
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
                            'report': report,
                            })
class _CompatibilityDataStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
            url_template='/esx/hcl/compatibility-data/status',
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
        update_input_type = type.StructType('operation-input', {})
        update_error_dict = {
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/hcl/compatibility-data',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'download',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'CompatibilityData.Status'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.hcl.compatibility_data',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ReportsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'report': type.IdType(resource_types='com.vmware.esx.hcl.resources.CompatibilityReport'),
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
            url_template='/esx/hcl/reports/{report}',
            path_variables={
                'report': 'report',
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
                'output_type': type.ReferenceType(__name__, 'Reports.Location'),
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
            self, iface_name='com.vmware.esx.hcl.reports',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'CompatibilityData': CompatibilityData,
        'Reports': Reports,
        'hosts': 'com.vmware.esx.hcl.hosts_client.StubFactory',
    }

