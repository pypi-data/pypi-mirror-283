# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.hardware_support.
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


class Managers(VapiInterface):
    """
    The ``Managers`` class provides methods to list Hardware Support Manager
    (HSM) for a given vCenter.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hardware_support.managers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ManagersStub)
        self._VAPI_OPERATION_IDS = {}

    class HardwareSupportManagerInfo(VapiStruct):
        """
        The ``Managers.HardwareSupportManagerInfo`` class contains attributes that
        describe a particular 3rd party Hardware Support Manager (HSM)

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     manager=None,
                     description=None,
                     display_name=None,
                     vendor=None,
                    ):
            """
            :type  manager: :class:`str`
            :param manager: Name of the Hardware Support Manager (HSM) (e.g. "Frobozz Hardware
                Support Manager")
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.setting.hardware_support.manager``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.setting.hardware_support.manager``.
            :type  description: :class:`str`
            :param description: User-intelligible description of the HSM (e.g. "Front end for
                Frobozz so-and-so management system")
            :type  display_name: :class:`str`
            :param display_name: UI label for HSM, derived from HSM extension's description's
                'label' field. (e.g. "Frobozz Free Management System")
            :type  vendor: :class:`str`
            :param vendor: Company providing the Hardware Support Manager (HSM) (e.g. "Frobozz
                Magic Software Company")
            """
            self.manager = manager
            self.description = description
            self.display_name = display_name
            self.vendor = vendor
            VapiStruct.__init__(self)


    HardwareSupportManagerInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hardware_support.managers.hardware_support_manager_info', {
            'manager': type.IdType(resource_types='com.vmware.esx.setting.hardware_support.manager'),
            'description': type.StringType(),
            'display_name': type.StringType(),
            'vendor': type.StringType(),
        },
        HardwareSupportManagerInfo,
        False,
        None))



    def list(self):
        """
        Returns the list of registered Hardware Support Managers (HSMs) in the
        system.


        :rtype: :class:`list` of :class:`Managers.HardwareSupportManagerInfo`
        :return: List of currently registered Hardware Support Manager (HSMs)
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.lifecycleSettings.Read``.
        """
        return self._invoke('list', None)
class _ManagersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/esx/settings/hardware-support/managers',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Managers.HardwareSupportManagerInfo')),
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
            self, iface_name='com.vmware.esx.settings.hardware_support.managers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Managers': Managers,
        'managers': 'com.vmware.esx.settings.hardware_support.managers_client.StubFactory',
    }

