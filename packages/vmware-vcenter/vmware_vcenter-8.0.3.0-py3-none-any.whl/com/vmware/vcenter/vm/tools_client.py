# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.vm.tools.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.vm_client`` module provides classes for managing
VMware Tools.

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


class Installer(VapiInterface):
    """
    The ``Installer`` (\\\\@term service} provides methods to install VMware
    Tools in the guest operating system. This class was added in vSphere API
    7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.tools.installer'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _InstallerStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Installer.Info`` class contains information about the VMWare Tools
        installer. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     is_connected=None,
                    ):
            """
            :type  is_connected: :class:`bool`
            :param is_connected: Flag indicating whether the VMware Tools installer is mounted as a
                CD-ROM. This attribute was added in vSphere API 7.0.0.0.
            """
            self.is_connected = is_connected
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.tools.installer.info', {
            'is_connected': type.BooleanType(),
        },
        Info,
        False,
        None))



    def get(self,
            vm,
            ):
        """
        Get information about the VMware Tools installer. This method was added
        in vSphere API 7.0.0.0.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`Installer.Info`
        :return: information about the VMware Tools installer.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            })

    def connect(self,
                vm,
                ):
        """
        Connects the VMware Tools CD installer as a CD-ROM for the guest
        operating system. On Windows guest operating systems with autorun, this
        should cause the installer to initiate the Tools installation which
        will need user input to complete. On other (non-Windows) guest
        operating systems this will make the Tools installation available, and
        a a user will need to do guest-specific actions. On Linux, this
        includes opening an archive and running the installer. To monitor the
        status of the Tools install, clients should check the ``versionStatus``
        and ``runState`` from :func:`com.vmware.vcenter.vm_client.Tools.get`.
        This method was added in vSphere API 7.0.0.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine ID
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not powered on.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if the VMware Tools CD is already connected.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the Tools installation fails in the guest operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        """
        return self._invoke('connect',
                            {
                            'vm': vm,
                            })

    def disconnect(self,
                   vm,
                   ):
        """
        Disconnect the VMware Tools installer CD image. This method was added
        in vSphere API 7.0.0.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine ID
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not powered on.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        """
        return self._invoke('disconnect',
                            {
                            'vm': vm,
                            })
class _InstallerStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/vm/{vm}/tools/installer',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for connect operation
        connect_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        connect_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        connect_input_value_validator_list = [
        ]
        connect_output_validator_list = [
        ]
        connect_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/tools/installer',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for disconnect operation
        disconnect_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        disconnect_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        disconnect_input_value_validator_list = [
        ]
        disconnect_output_validator_list = [
        ]
        disconnect_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/tools/installer',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Installer.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'connect': {
                'input_type': connect_input_type,
                'output_type': type.VoidType(),
                'errors': connect_error_dict,
                'input_value_validator_list': connect_input_value_validator_list,
                'output_validator_list': connect_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'disconnect': {
                'input_type': disconnect_input_type,
                'output_type': type.VoidType(),
                'errors': disconnect_error_dict,
                'input_value_validator_list': disconnect_input_value_validator_list,
                'output_validator_list': disconnect_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'connect': connect_rest_metadata,
            'disconnect': disconnect_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.tools.installer',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Installer': Installer,
    }

