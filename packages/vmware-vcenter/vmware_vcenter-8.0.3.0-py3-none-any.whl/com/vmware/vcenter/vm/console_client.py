# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.vm.console.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.vm.console_client`` module provides classes for
managing Virtual Machine Consoles.

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


class Tickets(VapiInterface):
    """
    The ``Tickets`` class provides methods for managing the virtual machine
    console tickets. This class was added in vSphere API 7.0.0.2.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.console.tickets'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TicketsStub)
        self._VAPI_OPERATION_IDS = {}

    class Type(Enum):
        """
        The ``Tickets.Type`` class defines the types of console tickets. This
        enumeration was added in vSphere API 7.0.0.2.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        VMRC = None
        """
        Virtual machine remote console ticket. This class attribute was added in
        vSphere API 7.0.0.2.

        """
        WEBMKS = None
        """
        Web socket console ticket. This class attribute was added in vSphere API
        7.0.0.2.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'VMRC': Type('VMRC'),
        'WEBMKS': Type('WEBMKS'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vm.console.tickets.type',
        Type))


    class CreateSpec(VapiStruct):
        """
        The ``Tickets.CreateSpec`` class defines the information used to create the
        virtual machine console ticket. This class was added in vSphere API
        7.0.0.2.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                    ):
            """
            :type  type: :class:`Tickets.Type`
            :param type: The type of virtual machine console ticket. This attribute was
                added in vSphere API 7.0.0.2.
            """
            self.type = type
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.console.tickets.create_spec', {
            'type': type.ReferenceType(__name__, 'Tickets.Type'),
        },
        CreateSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Tickets.Summary`` class contains commonly used information about the
        virtual machine console ticket. This class was added in vSphere API
        7.0.0.2.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ticket=None,
                    ):
            """
            :type  ticket: :class:`str`
            :param ticket: Console ticket URI. This attribute was added in vSphere API
                7.0.0.2.
            """
            self.ticket = ticket
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.console.tickets.summary', {
            'ticket': type.URIType(),
        },
        Summary,
        False,
        None))



    def create(self,
               vm,
               spec,
               ):
        """
        Creates a virtual machine console ticket of a given ticket type. The
        created ticket is a one time use URI. The validity of the ticket is 30
        minutes, if not used with in the time frame the ticket expires. 
        
        The :attr:`Tickets.Type.VMRC` ticket contains the IP address or the DNS
        resolvable name of the vCenter server. This ticket requires
        installation of VMware Workstation, VMware Fusion or VMRC to be
        installed on the machine where the ticket has to be opened. This ticket
        can be acquired even when the VM is turned off. 
        
        The :attr:`Tickets.Type.WEBMKS` ticket contains the IP address of the
        DNS resolvable name of the ESX server. This ticket requires user to
        embed this ticket in a HTML page using VMware HTML Console SDK -
        https://www.vmware.com/support/developer/html-console This ticket can
        be acquired only when the VM is turned on.. This method was added in
        vSphere API 7.0.0.2.

        :type  vm: :class:`str`
        :param vm: Virtual machine identifier.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  spec: :class:`Tickets.CreateSpec`
        :param spec: Specification for the console ticket to be created.
        :rtype: :class:`Tickets.Summary`
        :return: Commonly used information about the virtual machine console ticket.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the {\\\\@link CreateSpec#type) {\\\\@term field} contains a
            value that is not supported by the server.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is powered off and requested ticket type is
            :attr:`Tickets.Type.WEBMKS`
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the virtual machine's configuration or execution state cannot be
            accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('create',
                            {
                            'vm': vm,
                            'spec': spec,
                            })
class _TicketsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'spec': type.ReferenceType(__name__, 'Tickets.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/console/tickets',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        operations = {
            'create': {
                'input_type': create_input_type,
                'output_type': type.ReferenceType(__name__, 'Tickets.Summary'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.console.tickets',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Tickets': Tickets,
    }

