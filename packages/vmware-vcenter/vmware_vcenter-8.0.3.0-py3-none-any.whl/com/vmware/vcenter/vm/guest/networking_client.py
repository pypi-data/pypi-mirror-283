# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.vm.guest.networking.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.vm.guest.networking_client`` module provides classes
for dealing with the guest operating system networking.

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


class Interfaces(VapiInterface):
    """
    The ``Interfaces`` class provides methods for retrieving guest operating
    system network interface information. This class was added in vSphere API
    7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.networking.interfaces'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _InterfacesStub)
        self._VAPI_OPERATION_IDS = {}

    class IpAddressOrigin(Enum):
        """
        The ``Interfaces.IpAddressOrigin`` class specifies how an IP address was
        obtained for an interface. See RFC 4293 IpAddressOriginTC. This enumeration
        was added in vSphere API 7.0.0.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        OTHER = None
        """
        Any other type of address configuration other than the below mentioned ones
        will fall under this category. For e.g., automatic address configuration
        for the link local address falls under this type. This class attribute was
        added in vSphere API 7.0.0.0.

        """
        MANUAL = None
        """
        The address is configured manually. This class attribute was added in
        vSphere API 7.0.0.0.

        """
        DHCP = None
        """
        The address is configured through dhcp. This class attribute was added in
        vSphere API 7.0.0.0.

        """
        LINKLAYER = None
        """
        The address is obtained through stateless autoconfiguration (autoconf). See
        RFC 4862, IPv6 Stateless Address Autoconfiguration. This class attribute
        was added in vSphere API 7.0.0.0.

        """
        RANDOM = None
        """
        The address is chosen by the system at random e.g., an IPv4 address within
        169.254/16, or an RFC 3041 privacy address. This class attribute was added
        in vSphere API 7.0.0.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`IpAddressOrigin` instance.
            """
            Enum.__init__(string)

    IpAddressOrigin._set_values({
        'OTHER': IpAddressOrigin('OTHER'),
        'MANUAL': IpAddressOrigin('MANUAL'),
        'DHCP': IpAddressOrigin('DHCP'),
        'LINKLAYER': IpAddressOrigin('LINKLAYER'),
        'RANDOM': IpAddressOrigin('RANDOM'),
    })
    IpAddressOrigin._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vm.guest.networking.interfaces.ip_address_origin',
        IpAddressOrigin))


    class IpAddressStatus(Enum):
        """
        The ``Interfaces.IpAddressStatus`` class defines the present status of an
        address on an interface. See RFC 4293 IpAddressStatusTC. This enumeration
        was added in vSphere API 7.0.0.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        PREFERRED = None
        """
        Indicates that this is a valid address. This class attribute was added in
        vSphere API 7.0.0.0.

        """
        DEPRECATED = None
        """
        Indicates that this is a valid but deprecated address that should no longer
        be used as a source address. This class attribute was added in vSphere API
        7.0.0.0.

        """
        INVALID = None
        """
        Indicates that this isn't a valid address. This class attribute was added
        in vSphere API 7.0.0.0.

        """
        INACCESSIBLE = None
        """
        Indicates that the address is not accessible because interface is not
        operational. This class attribute was added in vSphere API 7.0.0.0.

        """
        UNKNOWN = None
        """
        Indicates that the status cannot be determined. This class attribute was
        added in vSphere API 7.0.0.0.

        """
        TENTATIVE = None
        """
        Indicates that the uniqueness of the address on the link is presently being
        verified. This class attribute was added in vSphere API 7.0.0.0.

        """
        DUPLICATE = None
        """
        Indicates the address has been determined to be non-unique on the link,
        this address will not be reachable. This class attribute was added in
        vSphere API 7.0.0.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`IpAddressStatus` instance.
            """
            Enum.__init__(string)

    IpAddressStatus._set_values({
        'PREFERRED': IpAddressStatus('PREFERRED'),
        'DEPRECATED': IpAddressStatus('DEPRECATED'),
        'INVALID': IpAddressStatus('INVALID'),
        'INACCESSIBLE': IpAddressStatus('INACCESSIBLE'),
        'UNKNOWN': IpAddressStatus('UNKNOWN'),
        'TENTATIVE': IpAddressStatus('TENTATIVE'),
        'DUPLICATE': IpAddressStatus('DUPLICATE'),
    })
    IpAddressStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vm.guest.networking.interfaces.ip_address_status',
        IpAddressStatus))


    class IpAddressInfo(VapiStruct):
        """
        The ``Interfaces.IpAddressInfo`` class describes a specific IP Address.
        This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ip_address=None,
                     prefix_length=None,
                     origin=None,
                     state=None,
                    ):
            """
            :type  ip_address: :class:`str`
            :param ip_address: IPv4 address is specified using dotted decimal notation. For
                example, "192.0.2.1". IPv6 addresses are 128-bit addresses
                specified using eight fields of up to four hexadecimal digits. A
                colon separates each field (:). For example,
                2001:DB8:101::230:6eff:fe04:d9ff. The address can also consist of
                the symbol '::' to represent multiple 16-bit groups of contiguous
                0's only once in an address as described in RFC 2373. This
                attribute was added in vSphere API 7.0.0.0.
            :type  prefix_length: :class:`long`
            :param prefix_length: Denotes the length of a generic Internet network address prefix.
                Prefix length: the valid range of values is 0-32 for IPv4, and
                0-128 for IPv6. A value of n corresponds to an IP address mask that
                has n contiguous 1-bits from the most significant bit (MSB), with
                all other bits set to 0. A value of zero is valid only if the
                calling context defines it. This attribute was added in vSphere API
                7.0.0.0.
            :type  origin: :class:`Interfaces.IpAddressOrigin` or ``None``
            :param origin: How this address was configured. This attribute was added in
                vSphere API 7.0.0.0.
                If None the data was not available.
            :type  state: :class:`Interfaces.IpAddressStatus`
            :param state: The state of this ipAddress. This attribute was added in vSphere
                API 7.0.0.0.
            """
            self.ip_address = ip_address
            self.prefix_length = prefix_length
            self.origin = origin
            self.state = state
            VapiStruct.__init__(self)


    IpAddressInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.networking.interfaces.ip_address_info', {
            'ip_address': type.StringType(),
            'prefix_length': type.IntegerType(),
            'origin': type.OptionalType(type.ReferenceType(__name__, 'Interfaces.IpAddressOrigin')),
            'state': type.ReferenceType(__name__, 'Interfaces.IpAddressStatus'),
        },
        IpAddressInfo,
        False,
        None))


    class IpConfigInfo(VapiStruct):
        """
        The ``Interfaces.IpConfigInfo`` class describes the protocol version
        independent address reporting data object for network interfaces. This
        class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ip_addresses=None,
                     dhcp=None,
                    ):
            """
            :type  ip_addresses: :class:`list` of :class:`Interfaces.IpAddressInfo`
            :param ip_addresses: IP addresses configured on the interface. This attribute was added
                in vSphere API 7.0.0.0.
            :type  dhcp: :class:`com.vmware.vcenter.vm.guest_client.DhcpConfigInfo` or ``None``
            :param dhcp: Client side DHCP for an interface. This attribute was added in
                vSphere API 7.0.0.0.
                If None the IP was not configured by DHCP.
            """
            self.ip_addresses = ip_addresses
            self.dhcp = dhcp
            VapiStruct.__init__(self)


    IpConfigInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.networking.interfaces.ip_config_info', {
            'ip_addresses': type.ListType(type.ReferenceType(__name__, 'Interfaces.IpAddressInfo')),
            'dhcp': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'DhcpConfigInfo')),
        },
        IpConfigInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Interfaces.Info`` class describes a virtual network adapter
        configured in the guest operating system. This class was added in vSphere
        API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     dns_values=None,
                     mac_address=None,
                     dns=None,
                     ip=None,
                     wins_servers=None,
                     nic=None,
                    ):
            """
            :type  dns_values: :class:`com.vmware.vcenter.vm.guest_client.DnsAssignedValues` or ``None``
            :param dns_values: Client DNS values. Data assigned by DNS. This attribute was added
                in vSphere API 7.0.0.0.
                If None no DNS assigned value exists.
            :type  mac_address: :class:`str` or ``None``
            :param mac_address: MAC address of the adapter. This attribute was added in vSphere API
                7.0.0.0.
                If None then not supported by the Guest OS.
            :type  dns: :class:`com.vmware.vcenter.vm.guest_client.DnsConfigInfo` or ``None``
            :param dns: DNS configuration of the adapter. See
                :attr:`com.vmware.vcenter.vm.guest_client.Networking.Info.dns` for
                system wide settings. This attribute was added in vSphere API
                7.0.0.0.
                If None then not assigned by the Guest OS.
            :type  ip: :class:`Interfaces.IpConfigInfo` or ``None``
            :param ip: IP configuration settings of the adapter. This attribute was added
                in vSphere API 7.0.0.0.
                If None then not supported by the Guest OS.
            :type  wins_servers: :class:`list` of :class:`str` or ``None``
            :param wins_servers: The IP addresses of any WINS name servers for the adapter. This
                attribute was added in vSphere API 7.0.0.0.
                If None then not supported by the Guest OS.
            :type  nic: :class:`str` or ``None``
            :param nic: Link to the corresponding virtual device. This attribute was added
                in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.vm.hardware.Ethernet``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.vm.hardware.Ethernet``.
                If None then the interface is not backed by a virtual device.
            """
            self.dns_values = dns_values
            self.mac_address = mac_address
            self.dns = dns
            self.ip = ip
            self.wins_servers = wins_servers
            self.nic = nic
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.networking.interfaces.info', {
            'dns_values': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'DnsAssignedValues')),
            'mac_address': type.OptionalType(type.StringType()),
            'dns': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'DnsConfigInfo')),
            'ip': type.OptionalType(type.ReferenceType(__name__, 'Interfaces.IpConfigInfo')),
            'wins_servers': type.OptionalType(type.ListType(type.StringType())),
            'nic': type.OptionalType(type.IdType()),
        },
        Info,
        False,
        None))



    def list(self,
             vm,
             ):
        """
        Returns information about the networking interfaces in the guest
        operating system. This method was added in vSphere API 7.0.0.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine ID
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`list` of :class:`Interfaces.Info`
        :return: Information about the interfaces configured in the guest operating
            system. Interfaces are ordered in a guest operating system specific
            determined order.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools is not running.
        """
        return self._invoke('list',
                            {
                            'vm': vm,
                            })
class Routes(VapiInterface):
    """
    The ``Routes`` class provides methods for retrieving guest operating system
    network routing information. This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.networking.routes'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _RoutesStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Routes.Info`` class describes an individual host, network or default
        destination network reachable through a gateway. This class was added in
        vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     network=None,
                     prefix_length=None,
                     gateway_address=None,
                     interface_index=None,
                    ):
            """
            :type  network: :class:`str`
            :param network: IP Address of the destination IP network. IPv4 address is specified
                using dotted decimal notation. For example, "192.0.2.1". IPv6
                addresses are 128-bit specified using as eight fields of up to four
                hexadecimal digits. A colon separates each field (:). For example,
                2001:DB8:101::230:6eff:fe04:d9ff. The address can also consist of
                symbol '::' to represent multiple 16-bit groups of contiguous 0's
                only once in an address as described in RFC 2373. This attribute
                was added in vSphere API 7.0.0.0.
            :type  prefix_length: :class:`long`
            :param prefix_length: The prefix length. For IPv4 the value range is 0-32. For IPv6
                prefixLength is a decimal value range 0-128. The property
                represents the number of contiguous, higher-order bits of the
                address that make up the network portion of the IP address. This
                attribute was added in vSphere API 7.0.0.0.
            :type  gateway_address: :class:`str` or ``None``
            :param gateway_address: Where to send the packets for this route. Unicast IP Address of the
                next hop router. IPv4 address is specified using dotted decimal
                notation. For example, "192.0.2.1". IPv6 addresses are 128-bit
                specified using as eight fields of up to four hexadecimal digits. A
                colon separates each field (:). For example,
                2001:DB8:101::230:6eff:fe04:d9ff. The address can also consist of
                symbol '::' to represent multiple 16-bit groups of contiguous 0's
                only once in an address as described in RFC 2373. This attribute
                was added in vSphere API 7.0.0.0.
                If None no gateway is set for the route.
            :type  interface_index: :class:`long` or ``None``
            :param interface_index: The network interface associated with this route. This is an index
                into the result of :func:`Interfaces.list` The index refers to the
                relative position of an element in a :class:`list`. For example, an
                index of 0 refers to the first element in the :class:`list` while
                an index of 1 refers to the second element. This attribute was
                added in vSphere API 7.0.0.0.
                If None the route is not associated with a network interface.
            """
            self.network = network
            self.prefix_length = prefix_length
            self.gateway_address = gateway_address
            self.interface_index = interface_index
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.networking.routes.info', {
            'network': type.StringType(),
            'prefix_length': type.IntegerType(),
            'gateway_address': type.OptionalType(type.StringType()),
            'interface_index': type.OptionalType(type.IntegerType()),
        },
        Info,
        False,
        None))



    def list(self,
             vm,
             ):
        """
        Returns information about network routing in the guest operating
        system. This method was added in vSphere API 7.0.0.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine ID
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`list` of :class:`Routes.Info`
        :return: Information about the network routes configured in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools is not running.
        """
        return self._invoke('list',
                            {
                            'vm': vm,
                            })
class _InterfacesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/vm/{vm}/guest/networking/interfaces',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Interfaces.Info')),
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
            self, iface_name='com.vmware.vcenter.vm.guest.networking.interfaces',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _RoutesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/vm/{vm}/guest/networking/routes',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Routes.Info')),
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
            self, iface_name='com.vmware.vcenter.vm.guest.networking.routes',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Interfaces': Interfaces,
        'Routes': Routes,
    }

