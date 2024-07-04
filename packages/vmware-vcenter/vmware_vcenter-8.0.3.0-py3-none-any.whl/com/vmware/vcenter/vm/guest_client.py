# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.vm.guest.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.vm.guest_client`` module provides classes for dealing
with the guest operating system. This includes information about the state of
local file systems and network interfaces and methods to manipulate the guest
file system and processes.

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


class Credentials(VapiStruct):
    """
    The ``Credentials`` class defines the guest credentials used for guest
    operation authentication. This class was added in vSphere API 7.0.2.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'type',
            {
                'USERNAME_PASSWORD' : [('user_name', False), ('password', True)],
                'SAML_BEARER_TOKEN' : [('user_name', False), ('saml_token', True)],
            }
        ),
    ]



    def __init__(self,
                 interactive_session=None,
                 type=None,
                 user_name=None,
                 password=None,
                 saml_token=None,
                ):
        """
        :type  interactive_session: :class:`bool`
        :param interactive_session: If :class:`set`, the method will interact with the logged-in
            desktop session in the guest. This requires that the logged-on user
            matches the user specified by the :class:`Credentials`. This is
            currently only supported for
            :attr:`Credentials.Type.USERNAME_PASSWORD`. This attribute was
            added in vSphere API 7.0.2.0.
        :type  type: :class:`Credentials.Type`
        :param type: The guest credentials type. This attribute was added in vSphere API
            7.0.2.0.
        :type  user_name: :class:`str` or ``None``
        :param user_name: For :attr:`Credentials.Type.SAML_BEARER_TOKEN`, this is the guest
            user to be associated with the credentials. For
            :attr:`Credentials.Type.USERNAME_PASSWORD` this is the guest
            username. This attribute was added in vSphere API 7.0.2.0.
            If no user is specified for
            :attr:`Credentials.Type.SAML_BEARER_TOKEN`, a guest dependent
            mapping will decide what guest user account is applied.
        :type  password: :class:`str`
        :param password: password. This attribute was added in vSphere API 7.0.2.0.
            This attribute is optional and it is only relevant when the value
            of ``type`` is :attr:`Credentials.Type.USERNAME_PASSWORD`.
        :type  saml_token: :class:`str`
        :param saml_token: SAML Bearer Token. This attribute was added in vSphere API 7.0.2.0.
            This attribute is optional and it is only relevant when the value
            of ``type`` is :attr:`Credentials.Type.SAML_BEARER_TOKEN`.
        """
        self.interactive_session = interactive_session
        self.type = type
        self.user_name = user_name
        self.password = password
        self.saml_token = saml_token
        VapiStruct.__init__(self)


    class Type(Enum):
        """
        Types of guest credentials. This enumeration was added in vSphere API
        7.0.2.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        USERNAME_PASSWORD = None
        """
        USERNAME_PASSWORD credentials contains the information necessary to
        authenticate within a guest using a username and password. This method of
        authentication is stateless. 
        
        To use USERNAME_PASSWORD, populate userName and password with the
        appropriate login information. 
        
        Once populated, you can use USERNAME_PASSWORD in any guest operations
        method.. This class attribute was added in vSphere API 7.0.2.0.

        """
        SAML_BEARER_TOKEN = None
        """
        SAML_BEARER_TOKEN contains the information necessary to authenticate within
        a guest using a SAML token. SAML Bearer token credentials relies on a guest
        alias that associates a guest account with the subject and certificate
        encoded in a SAML Bearer token obtained from the VMware SSO Server. This
        class attribute was added in vSphere API 7.0.2.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'USERNAME_PASSWORD': Type('USERNAME_PASSWORD'),
        'SAML_BEARER_TOKEN': Type('SAML_BEARER_TOKEN'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vm.guest.credentials.type',
        Type))

Credentials._set_binding_type(type.StructType(
    'com.vmware.vcenter.vm.guest.credentials', {
        'interactive_session': type.BooleanType(),
        'type': type.ReferenceType(__name__, 'Credentials.Type'),
        'user_name': type.OptionalType(type.StringType()),
        'password': type.OptionalType(type.SecretType()),
        'saml_token': type.OptionalType(type.SecretType()),
    },
    Credentials,
    False,
    None))



class DnsAssignedValues(VapiStruct):
    """
    The {\\\\@name DnsAssignedValues) {\\\\@term structure} describes values
    assigned by a Domain Name Server (DNS). This class was added in vSphere API
    7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 host_name=None,
                 domain_name=None,
                ):
        """
        :type  host_name: :class:`str`
        :param host_name: The host name portion of DNS name. For example, "esx01" part of
            esx01.example.com. This attribute was added in vSphere API 7.0.0.0.
        :type  domain_name: :class:`str`
        :param domain_name: The domain name portion of the DNS name. "example.com" part of
            esx01.example.com. This attribute was added in vSphere API 7.0.0.0.
        """
        self.host_name = host_name
        self.domain_name = domain_name
        VapiStruct.__init__(self)


DnsAssignedValues._set_binding_type(type.StructType(
    'com.vmware.vcenter.vm.guest.dns_assigned_values', {
        'host_name': type.StringType(),
        'domain_name': type.StringType(),
    },
    DnsAssignedValues,
    False,
    None))



class DnsConfigInfo(VapiStruct):
    """
    The ``DnsConfigInfo`` class describes the configuration of RFC 1034 DNS
    settings. This class was added in vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 ip_addresses=None,
                 search_domains=None,
                ):
        """
        :type  ip_addresses: :class:`list` of :class:`str`
        :param ip_addresses: The IP addresses of the DNS servers in order of use. IPv4 addresses
            are specified using dotted decimal notation. For example,
            "192.0.2.1". IPv6 addresses are 128-bit addresses represented as
            eight fields of up to four hexadecimal digits. A colon separates
            each field (:). For example, 2001:DB8:101::230:6eff:fe04:d9ff. The
            address can also consist of the symbol '::' to represent multiple
            16-bit groups of contiguous 0's only once in an address as
            described in RFC 2373. This attribute was added in vSphere API
            7.0.0.0.
        :type  search_domains: :class:`list` of :class:`str`
        :param search_domains: The domain in which to search for hosts, placed in order of
            preference. These are the domain name portion of the DNS names.
            This attribute was added in vSphere API 7.0.0.0.
        """
        self.ip_addresses = ip_addresses
        self.search_domains = search_domains
        VapiStruct.__init__(self)


DnsConfigInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.vm.guest.dns_config_info', {
        'ip_addresses': type.ListType(type.StringType()),
        'search_domains': type.ListType(type.StringType()),
    },
    DnsConfigInfo,
    False,
    None))



class DhcpConfigInfo(VapiStruct):
    """
    The ``DhcpConfigInfo`` class specifies when Dynamic Host Configuration
    Protocol is enabled. This class was added in vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 ipv4_enabled=None,
                 ipv6_enabled=None,
                ):
        """
        :type  ipv4_enabled: :class:`bool`
        :param ipv4_enabled: True if IPv4 DHCP is enabled, false otherwise. This attribute was
            added in vSphere API 7.0.0.0.
        :type  ipv6_enabled: :class:`bool`
        :param ipv6_enabled: True if IPv6 DHCP is enabled, false otherwise. This attribute was
            added in vSphere API 7.0.0.0.
        """
        self.ipv4_enabled = ipv4_enabled
        self.ipv6_enabled = ipv6_enabled
        VapiStruct.__init__(self)


DhcpConfigInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.vm.guest.dhcp_config_info', {
        'ipv4_enabled': type.BooleanType(),
        'ipv6_enabled': type.BooleanType(),
    },
    DhcpConfigInfo,
    False,
    None))



class Customization(VapiInterface):
    """
    The ``Customization`` class provides methods to apply a customization
    specification to a virtual machine in powered-off status. This class was
    added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.customization'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CustomizationStub)
        self._VAPI_OPERATION_IDS = {}

    class SetSpec(VapiStruct):
        """
        The ``Customization.SetSpec`` class contains specification information that
        has to be applied to a virtual machine. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     spec=None,
                    ):
            """
            :type  name: :class:`str` or ``None``
            :param name: The name of the customization specification that has be retrieved
                from the virtual center inventory and applied for the virtual
                machine. Either one of ``name`` or ``spec`` or none of them should
                be specified. This attribute was added in vSphere API 7.0.0.0.
                If None and ``spec`` is also None when executing
                :func:`Customization.set` method, then any pending customization
                for the virtual machine will be cleared.
            :type  spec: :class:`com.vmware.vcenter.guest_client.CustomizationSpec` or ``None``
            :param spec: The customization specification that has to be applied for the
                virtual machine. Either one of ``name`` or ``spec`` or none of them
                should be specified. This attribute was added in vSphere API
                7.0.0.0.
                If None and ``name`` is also None when executing
                :func:`Customization.set` method, then any pending customization
                for the virtual machine will be cleared.
            """
            self.name = name
            self.spec = spec
            VapiStruct.__init__(self)


    SetSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.customization.set_spec', {
            'name': type.OptionalType(type.StringType()),
            'spec': type.OptionalType(type.ReferenceType('com.vmware.vcenter.guest_client', 'CustomizationSpec')),
        },
        SetSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Customization.Info`` class contains the status of a customization
        operation applied to a virtual machine. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'FAILED' : [('error', False), ('start_time', False), ('end_time', False)],
                    'RUNNING' : [('start_time', False)],
                    'SUCCEEDED' : [('start_time', False), ('end_time', False)],
                    'IDLE' : [],
                    'PENDING' : [],
                }
            ),
        ]



        def __init__(self,
                     status=None,
                     error=None,
                     start_time=None,
                     end_time=None,
                    ):
            """
            :type  status: :class:`Customization.Info.Status`
            :param status: The status of the customization operation. This attribute was added
                in vSphere API 7.0.0.0.
            :type  error: :class:`str` or ``None``
            :param error: Description of the error if the :attr:`Customization.Info.status`
                of customization operation is
                :attr:`Customization.Info.Status.FAILED`. This attribute was added
                in vSphere API 7.0.0.0.
                This attribute will be None if the status is not FAILED or there is
                no information available for the error.
            :type  start_time: :class:`datetime.datetime` or ``None``
            :param start_time: Time when the customization process has started inside the guest
                operating system. This attribute was added in vSphere API 7.0.0.0.
                This attribute will be None if the status is PENDING.
            :type  end_time: :class:`datetime.datetime` or ``None``
            :param end_time: Time when the customization process has completed inside the guest
                operating system. This attribute was added in vSphere API 7.0.0.0.
                This attribute will be None if the status is not SUCCEEDED or
                FAILED.
            """
            self.status = status
            self.error = error
            self.start_time = start_time
            self.end_time = end_time
            VapiStruct.__init__(self)


        class Status(Enum):
            """
            The ``Customization.Info.Status`` class defines the status values that can
            be reported for the customization operation. This enumeration was added in
            vSphere API 7.0.0.0.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            IDLE = None
            """
            No customization spec is applied to the guest operating system. This class
            attribute was added in vSphere API 7.0.3.0.

            """
            PENDING = None
            """
            The customization process has not yet started inside the guest operating
            system. This class attribute was added in vSphere API 7.0.0.0.

            """
            RUNNING = None
            """
            The customization process is currently running inside the guest operating
            system. This class attribute was added in vSphere API 7.0.0.0.

            """
            SUCCEEDED = None
            """
            The customization process has completed successfully inside the guest
            operating system. This class attribute was added in vSphere API 7.0.0.0.

            """
            FAILED = None
            """
            The customizatio process has failed inside the guest operating system. This
            class attribute was added in vSphere API 7.0.0.0.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Status` instance.
                """
                Enum.__init__(string)

        Status._set_values({
            'IDLE': Status('IDLE'),
            'PENDING': Status('PENDING'),
            'RUNNING': Status('RUNNING'),
            'SUCCEEDED': Status('SUCCEEDED'),
            'FAILED': Status('FAILED'),
        })
        Status._set_binding_type(type.EnumType(
            'com.vmware.vcenter.vm.guest.customization.info.status',
            Status))

    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.customization.info', {
            'status': type.ReferenceType(__name__, 'Customization.Info.Status'),
            'error': type.OptionalType(type.StringType()),
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
        },
        Info,
        False,
        None))



    def set(self,
            vm,
            spec,
            ):
        """
        Applies a customization specification in ``spec`` on the virtual
        machine in ``vm``. This method only sets the specification settings for
        the virtual machine. The actual customization happens inside the guest
        when the virtual machine is powered on. If ``spec`` has None values,
        then any pending customization settings for the virtual machine are
        cleared. If there is a pending customization for the virtual machine
        and ``spec`` has valid content, then the existing customization setting
        will be overwritten with the new settings. This method was added in
        vSphere API 7.0.0.0.

        :type  vm: :class:`str`
        :param vm: The unique identifier of the virtual machine that needs to be
            customized.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  spec: :class:`Customization.SetSpec`
        :param spec: The customization settings to be applied to the guest operating
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the customization settings in ``spec`` are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine ``vm`` is not in a powered off state.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if a customization specification is not found with the unique name
            in ``spec``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the virtual machine ``vm`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.Provisioning.Customize``.
        """
        return self._invoke('set',
                            {
                            'vm': vm,
                            'spec': spec,
                            })

    def get(self,
            vm,
            ):
        """
        Returns the status of the customization operation that has been applied
        for the virtual machine in ``vm``. This method was added in vSphere API
        7.0.3.0.

        :type  vm: :class:`str`
        :param vm: The unique identifier of the virtual machine that needs to be
            queried.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`Customization.Info`
        :return: The status of the customization operation applied for the virtual
            machine.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the virtual machine ``vm`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``System.View``.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            })
class Environment(VapiInterface):
    """
    The ``Environment`` class provides methods to manage environment variables
    in the guest operating system. This class was added in vSphere API 7.0.2.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.environment'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EnvironmentStub)
        self._VAPI_OPERATION_IDS = {}


    def get(self,
            vm,
            credentials,
            name,
            ):
        """
        Reads a single environment variable from the guest operating system. 
        
        If the authentication uses :attr:`Credentials.interactive_session`,
        then the environment being read will be that of the user logged into
        the desktop. Otherwise it's the environment of the system user. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`Credentials`
        :param credentials: The guest authentication data. See :class:`Credentials`.
        :type  name: :class:`str`
        :param name: The name of the environment variable to be read.
        :rtype: :class:`str`
        :return: The value of the ``name`` environment variable.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine ``vm`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the environment variable ``name`` is not not set in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware tools in the guest
            OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware tools in the guest OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine ``vm`` is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware tools are not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Query``.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'name': name,
                            })

    def list(self,
             vm,
             credentials,
             names,
             ):
        """
        Reads a list of environment variables from the guest operating system. 
        
        If the authentication uses :attr:`Credentials.interactive_session`,
        then the environment being read will be that of the user logged into
        the desktop. Otherwise it's the environment of the system user. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`Credentials`
        :param credentials: The guest authentication data. See :class:`Credentials`.
        :type  names: :class:`set` of :class:`str`
        :param names: The names of the variables to be read. If the :class:`set` is
            empty, then all the environment variables are returned.
        :rtype: :class:`dict` of :class:`str` and :class:`str`
        :return: Mapping from environment variable names to environment variable
            values, or all environment variables if nothing is specified. If
            any specified environment variable contained in ``names`` is not
            set, then nothing is returned for that variable.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine ``vm`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware tools in the guest
            OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware tools in the guest OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine ``vm`` is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware tools are not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Query``.
        """
        return self._invoke('list',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'names': names,
                            })
class Identity(VapiInterface):
    """
    The ``Identity`` class provides methods for retrieving guest operating
    system identification information. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.identity'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _IdentityStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Identity.Info`` class contains information describing the guest
        operating system identification. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     family=None,
                     full_name=None,
                     host_name=None,
                     ip_address=None,
                    ):
            """
            :type  name: :class:`com.vmware.vcenter.vm_client.GuestOS`
            :param name: Guest operating system identifier (short name). This attribute was
                added in vSphere API 6.7.
            :type  family: :class:`com.vmware.vcenter.vm_client.GuestOSFamily`
            :param family: Guest operating system family. This attribute was added in vSphere
                API 6.7.
            :type  full_name: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param full_name: Guest operating system full name. This attribute was added in
                vSphere API 6.7.
            :type  host_name: :class:`str`
            :param host_name: Hostname of the guest operating system. This attribute was added in
                vSphere API 6.7.
            :type  ip_address: :class:`str` or ``None``
            :param ip_address: IP address assigned by the guest operating system. This attribute
                was added in vSphere API 6.7.
                If None the guest does not have an IP address.
            """
            self.name = name
            self.family = family
            self.full_name = full_name
            self.host_name = host_name
            self.ip_address = ip_address
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.identity.info', {
            'name': type.ReferenceType('com.vmware.vcenter.vm_client', 'GuestOS'),
            'family': type.ReferenceType('com.vmware.vcenter.vm_client', 'GuestOSFamily'),
            'full_name': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
            'host_name': type.StringType(),
            'ip_address': type.OptionalType(type.StringType()),
        },
        Info,
        False,
        None))



    def get(self,
            vm,
            ):
        """
        Return information about the guest. This method was added in vSphere
        API 6.7.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`Identity.Info`
        :return: guest identification information.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools has not provided any data.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            })
class LocalFilesystem(VapiInterface):
    """
    The ``LocalFilesystem`` class provides methods for retrieving information
    about the guest operating system local file systems. This class was added
    in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.local_filesystem'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LocalFilesystemStub)
        self._VAPI_OPERATION_IDS = {}

    class VirtualDiskMapping(VapiStruct):
        """
        Describes the virtual disk backing a local guest disk. This class was added
        in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     disk=None,
                    ):
            """
            :type  disk: :class:`str`
            :param disk: The virtual disk. This attribute was added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.vm.hardware.Disk``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.vm.hardware.Disk``.
            """
            self.disk = disk
            VapiStruct.__init__(self)


    VirtualDiskMapping._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.local_filesystem.virtual_disk_mapping', {
            'disk': type.IdType(resource_types='com.vmware.vcenter.vm.hardware.Disk'),
        },
        VirtualDiskMapping,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``LocalFilesystem.Info`` class contains information about a local file
        system configured in the guest operating system. This class was added in
        vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     capacity=None,
                     free_space=None,
                     filesystem=None,
                     mappings=None,
                    ):
            """
            :type  capacity: :class:`long`
            :param capacity: Total capacity of the file system, in bytes. This attribute was
                added in vSphere API 6.7.
            :type  free_space: :class:`long`
            :param free_space: Free space on the file system, in bytes. This attribute was added
                in vSphere API 6.7.
            :type  filesystem: :class:`str` or ``None``
            :param filesystem: Filesystem type, if known. For example, ext3 or NTFS. This
                attribute was added in vSphere API 7.0.0.0.
                :class:`set` if VMware Tools reports a value.
            :type  mappings: :class:`list` of :class:`LocalFilesystem.VirtualDiskMapping`
            :param mappings: VirtualDisks backing the guest partition, if known. This attribute
                was added in vSphere API 7.0.0.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.capacity = capacity
            self.free_space = free_space
            self.filesystem = filesystem
            self.mappings = mappings
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.local_filesystem.info', {
            'capacity': type.IntegerType(),
            'free_space': type.IntegerType(),
            'filesystem': type.OptionalType(type.StringType()),
            'mappings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'LocalFilesystem.VirtualDiskMapping'))),
        },
        Info,
        False,
        None))



    def get(self,
            vm,
            ):
        """
        Returns details of the local file systems in the guest operating
        system. This method was added in vSphere API 6.7.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`dict` of :class:`str` and :class:`LocalFilesystem.Info`
        :return: Information about the local file systems configured in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools has not provided any data.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            })
class Networking(VapiInterface):
    """
    The ``Networking`` class provides methods for retrieving guest operating
    system network information. This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.networking'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NetworkingStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Networking.Info`` class contains information about networking as
        configured in the guest operating system. This class was added in vSphere
        API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     dns_values=None,
                     dns=None,
                    ):
            """
            :type  dns_values: :class:`DnsAssignedValues` or ``None``
            :param dns_values: Client DNS values. Data assigned by DNS. This attribute was added
                in vSphere API 7.0.0.0.
                If None no DNS assigned value exists.
            :type  dns: :class:`DnsConfigInfo` or ``None``
            :param dns: Client DNS configuration. How DNS queries are resolved. This
                attribute was added in vSphere API 7.0.0.0.
                If None no DNS assigned value exists.
            """
            self.dns_values = dns_values
            self.dns = dns
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.networking.info', {
            'dns_values': type.OptionalType(type.ReferenceType(__name__, 'DnsAssignedValues')),
            'dns': type.OptionalType(type.ReferenceType(__name__, 'DnsConfigInfo')),
        },
        Info,
        False,
        None))



    def get(self,
            vm,
            ):
        """
        Returns information about the network configuration in the guest
        operating system. This method was added in vSphere API 7.0.0.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine ID
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`Networking.Info`
        :return: Information about the networking configuration in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            })
class Operations(VapiInterface):
    """
    Status of operations in the guest OS. This class was added in vSphere API
    7.0.2.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.operations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _OperationsStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        Guest operating system operation status information. This class was added
        in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     guest_operations_ready=None,
                     interactive_guest_operations_ready=None,
                    ):
            """
            :type  guest_operations_ready: :class:`bool`
            :param guest_operations_ready: Guest operations availability. Whether or not the virtual machine
                is ready to process guest operations. This attribute was added in
                vSphere API 7.0.2.0.
            :type  interactive_guest_operations_ready: :class:`bool`
            :param interactive_guest_operations_ready: Interactive guest operations availability. Whether or not the
                virtual machine is ready to process interactive guest operations.
                This attribute was added in vSphere API 7.0.2.0.
            """
            self.guest_operations_ready = guest_operations_ready
            self.interactive_guest_operations_ready = interactive_guest_operations_ready
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.operations.info', {
            'guest_operations_ready': type.BooleanType(),
            'interactive_guest_operations_ready': type.BooleanType(),
        },
        Info,
        False,
        None))



    def get(self,
            vm,
            ):
        """
        Get information about the guest operation status. This method was added
        in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`Operations.Info`
        :return: guest operations readiness.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the state of VMware Tools is unknown.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            })
class Power(VapiInterface):
    """
    The ``Power`` class provides methods for managing the guest operating
    system power state of a virtual machine. This class was added in vSphere
    API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.power'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PowerStub)
        self._VAPI_OPERATION_IDS = {}

    class State(Enum):
        """
        Possible guest power states. This enumeration was added in vSphere API 6.7.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        RUNNING = None
        """
        The guest OS is running. This class attribute was added in vSphere API 6.7.

        """
        SHUTTING_DOWN = None
        """
        The guest OS is shutting down. This class attribute was added in vSphere
        API 6.7.

        """
        RESETTING = None
        """
        The guest OS is resetting. This class attribute was added in vSphere API
        6.7.

        """
        STANDBY = None
        """
        The guest OS is in standby. This class attribute was added in vSphere API
        6.7.

        """
        NOT_RUNNING = None
        """
        The guest OS is not running. This class attribute was added in vSphere API
        6.7.

        """
        UNAVAILABLE = None
        """
        The guest OS power state is unknown. This class attribute was added in
        vSphere API 6.7.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`State` instance.
            """
            Enum.__init__(string)

    State._set_values({
        'RUNNING': State('RUNNING'),
        'SHUTTING_DOWN': State('SHUTTING_DOWN'),
        'RESETTING': State('RESETTING'),
        'STANDBY': State('STANDBY'),
        'NOT_RUNNING': State('NOT_RUNNING'),
        'UNAVAILABLE': State('UNAVAILABLE'),
    })
    State._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vm.guest.power.state',
        State))


    class Info(VapiStruct):
        """
        Information about the guest operating system power state. This class was
        added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     state=None,
                     operations_ready=None,
                    ):
            """
            :type  state: :class:`Power.State`
            :param state: The power state of the guest operating system. This attribute was
                added in vSphere API 6.7.
            :type  operations_ready: :class:`bool`
            :param operations_ready: Flag indicating if the virtual machine is ready to process soft
                power operations. This attribute was added in vSphere API 6.7.
            """
            self.state = state
            self.operations_ready = operations_ready
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.power.info', {
            'state': type.ReferenceType(__name__, 'Power.State'),
            'operations_ready': type.BooleanType(),
        },
        Info,
        False,
        None))



    def get(self,
            vm,
            ):
        """
        Returns information about the guest operating system power state. This
        method was added in vSphere API 6.7.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`Power.Info`
        :return: Guest OS powerstate information.
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

    def shutdown(self,
                 vm,
                 ):
        """
        Issues a request to the guest operating system asking it to perform a
        clean shutdown of all services. This request returns immediately and
        does not wait for the guest operating system to complete the operation.
        This method was added in vSphere API 6.7.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if the virtual machine is not powered on.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is suspended.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is performing another operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the virtual machine does not support being powered on (e.g.
            marked as a template, serving as a fault-tolerance secondary
            virtual machine).
        """
        return self._invoke('shutdown',
                            {
                            'vm': vm,
                            })

    def reboot(self,
               vm,
               ):
        """
        Issues a request to the guest operating system asking it to perform a
        reboot. This request returns immediately and does not wait for the
        guest operating system to complete the operation. This method was added
        in vSphere API 6.7.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not powered on.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is performing another operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the virtual machine does not support being powered on (e.g.
            marked as a template, serving as a fault-tolerance secondary
            virtual machine).
        """
        return self._invoke('reboot',
                            {
                            'vm': vm,
                            })

    def standby(self,
                vm,
                ):
        """
        Issues a request to the guest operating system asking it to perform a
        suspend operation. This method was added in vSphere API 6.7.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if the virtual machine is suspended.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not powered on.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is performing another operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the virtual machine does not support being powered on (e.g.
            marked as a template, serving as a fault-tolerance secondary
            virtual machine).
        """
        return self._invoke('standby',
                            {
                            'vm': vm,
                            })
class Processes(VapiInterface):
    """
    The ``Processes`` class provides methods to manage processes in the guest
    operating system. This class was added in vSphere API 7.0.2.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.processes'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProcessesStub)
        self._VAPI_OPERATION_IDS = {}

    class ProcessErrorDetails(VapiStruct):
        """
        The ``Processes.ProcessErrorDetails`` class describes additional error
        information for process operations. This class was added in vSphere API
        7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     pid=None,
                    ):
            """
            :type  pid: :class:`long`
            :param pid: The process associated with the error. This attribute was added in
                vSphere API 7.0.2.0.
            """
            self.pid = pid
            VapiStruct.__init__(self)


    ProcessErrorDetails._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.processes.process_error_details', {
            'pid': type.IntegerType(),
        },
        ProcessErrorDetails,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Processes.CreateSpec`` class describes the arguments to
        :func:`Processes.create`. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     path=None,
                     arguments=None,
                     working_directory=None,
                     environment_variables=None,
                     start_minimized=None,
                    ):
            """
            :type  path: :class:`str`
            :param path: The absolute path to the program to start. 
                
                For Linux guest operating systems, /bin/bash is used to start the
                program. 
                
                For Solaris guest operating systems, if /bin/bash exists, its used
                to start the program, otherwise /bin/sh is used. If /bin/sh is
                used, then the process ID returned by :func:`Processes.create` will
                be that of the shell used to start the program, rather than the
                program itself, due to the differences in how /bin/sh and /bin/bash
                work. This PID will still be usable for watching the process with
                :func:`Processes.list` to find its exit code and elapsed time. 
                
                For Windows, no shell is used. Using a simple batch file instead by
                prepending ``c:\windows\system32\cmd.exe /c`` will allow stdio
                redirection to work if passed in the ``arguments`` parameter.. This
                attribute was added in vSphere API 7.0.2.0.
            :type  arguments: :class:`str` or ``None``
            :param arguments: The arguments to the program. 
                
                Characters which must be escaped to the shell should also be
                escaped in ``arguments``. 
                
                In Linux and Solaris guest operating systems, stdio redirection
                arguments may be used. 
                
                For Windows, stdio redirection can be added to the argments if
                ``path`` is prefixed with ``c:\windows\system32\cmd.exe /c``.. This
                attribute was added in vSphere API 7.0.2.0.
                If None no arguments are passed to the program.
            :type  working_directory: :class:`str` or ``None``
            :param working_directory: The absolute path of the working directory for the program to be
                run. VMware recommends explicitly setting the working directory for
                the program to be run. This attribute was added in vSphere API
                7.0.2.0.
                If None or is an empty string, the behavior depends on the guest
                operating system. For Linux guest operating systems, if None or is
                an empty string, the working directory will be the home directory
                of the user associated with the guest authentication. For other
                guest operating systems, if None, the behavior is unspecified.
            :type  environment_variables: (:class:`dict` of :class:`str` and :class:`str`) or ``None``
            :param environment_variables: A map of environment variables, specified using the guest OS rules
                (for example ``PATH, c:\bin;c:\windows\system32`` or
                ``LD_LIBRARY_PATH,/usr/lib:/lib``), to be set for the program being
                run. Note that these are not additions to the default environment
                variables; they define the complete set available to the program.
                This attribute was added in vSphere API 7.0.2.0.
                If None, the environment variables used are guest dependent
                defaults.
            :type  start_minimized: :class:`bool` or ``None``
            :param start_minimized: Makes any program window start minimized in Windows operating
                systems. Returns an error if :class:`set` for non-Windows guests.
                This attribute was added in vSphere API 7.0.2.0.
                Defaults to false.
            """
            self.path = path
            self.arguments = arguments
            self.working_directory = working_directory
            self.environment_variables = environment_variables
            self.start_minimized = start_minimized
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.processes.create_spec', {
            'path': type.StringType(),
            'arguments': type.OptionalType(type.StringType()),
            'working_directory': type.OptionalType(type.StringType()),
            'environment_variables': type.OptionalType(type.MapType(type.StringType(), type.StringType())),
            'start_minimized': type.OptionalType(type.BooleanType()),
        },
        CreateSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Processes.Info`` class describes the state of a guest process. This
        class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     owner=None,
                     command=None,
                     started=None,
                     finished=None,
                     exit_code=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The process name. This attribute was added in vSphere API 7.0.2.0.
            :type  owner: :class:`str`
            :param owner: The process owner. This attribute was added in vSphere API 7.0.2.0.
            :type  command: :class:`str`
            :param command: The full command line of the process. This attribute was added in
                vSphere API 7.0.2.0.
            :type  started: :class:`datetime.datetime`
            :param started: The start time of the process. This attribute was added in vSphere
                API 7.0.2.0.
            :type  finished: :class:`datetime.datetime` or ``None``
            :param finished: If the process was started using :func:`Processes.create` then the
                process completion time will be available if queried within 5
                minutes after it completes. This attribute was added in vSphere API
                7.0.2.0.
                Set if the process was started with :func:`Processes.create` and
                has recently exited.
            :type  exit_code: :class:`long` or ``None``
            :param exit_code: If the process was started using :func:`Processes.create` then the
                process exit code will be available if queried within 5 minutes
                after it completes. This attribute was added in vSphere API
                7.0.2.0.
                Set if the process was started with :func:`Processes.create` and
                has recently exited.
            """
            self.name = name
            self.owner = owner
            self.command = command
            self.started = started
            self.finished = finished
            self.exit_code = exit_code
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.processes.info', {
            'name': type.StringType(),
            'owner': type.StringType(),
            'command': type.StringType(),
            'started': type.DateTimeType(),
            'finished': type.OptionalType(type.DateTimeType()),
            'exit_code': type.OptionalType(type.IntegerType()),
        },
        Info,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Processes.Summary`` class describes the state of a guest process.
        This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     pid=None,
                     owner=None,
                     command=None,
                     started=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The process name. This attribute was added in vSphere API 7.0.2.0.
            :type  pid: :class:`long`
            :param pid: The process ID. This attribute was added in vSphere API 7.0.2.0.
            :type  owner: :class:`str`
            :param owner: The process owner. This attribute was added in vSphere API 7.0.2.0.
            :type  command: :class:`str`
            :param command: The full command line of the process. This attribute was added in
                vSphere API 7.0.2.0.
            :type  started: :class:`datetime.datetime`
            :param started: The start time of the process. This attribute was added in vSphere
                API 7.0.2.0.
            """
            self.name = name
            self.pid = pid
            self.owner = owner
            self.command = command
            self.started = started
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.processes.summary', {
            'name': type.StringType(),
            'pid': type.IntegerType(),
            'owner': type.StringType(),
            'command': type.StringType(),
            'started': type.DateTimeType(),
        },
        Summary,
        False,
        None))



    def create(self,
               vm,
               credentials,
               spec,
               ):
        """
        Starts a program in the guest operating system. 
        
        A process started this way can have its status queried with
        :func:`Processes.list` or :func:`Processes.get`. When the process
        completes, its exit code and end time will be available for 5 minutes
        after completion. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`Credentials`
        :param credentials: The guest authentication data. See :class:`Credentials`. The
            program will be run as the user associated with this data.
        :type  spec: :class:`Processes.CreateSpec`
        :param spec: The arguments describing the program to be started.
        :rtype: :class:`long`
        :return: The process id of the program started.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the :attr:`Processes.CreateSpec.start_minimized` attribute is
            set and the guest is not a Windows operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the program path is not a valid path. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the
            :class:`com.vmware.vcenter.vm.guest.filesystem_client.FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the working directory is not a valid directory. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the
            :class:`com.vmware.vcenter.vm.guest.filesystem_client.FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine ``vm`` is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine ``vm`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the program path does not exist. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the
            :class:`com.vmware.vcenter.vm.guest.filesystem_client.FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware tools are not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if the program fails to start.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the ``path`` attribute of ``spec`` cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the ``path`` attribute of ``spec`` cannot be run because
            ``credentials`` will not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware tools in the guest
            OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware tools in the guest OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Execute``.
        """
        return self._invoke('create',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'spec': spec,
                            })

    def get(self,
            vm,
            credentials,
            pid,
            ):
        """
        Returns the status of a process running in the guest operating system,
        including those started by :func:`Processes.create` that may have
        recently completed. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`Credentials`
        :param credentials: The guest authentication data. See :class:`Credentials`.
        :type  pid: :class:`long`
        :param pid: Specifies the process to query.
        :rtype: :class:`Processes.Info`
        :return: The  for the process with id ``pid``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine ``vm`` is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine ``vm`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the process ``pid`` is not found. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the
            :class:`Processes.ProcessErrorDetails` providing additional
            information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware tools are not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` is not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware tools in the guest
            OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware tools in the guest OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Query``.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'pid': pid,
                            })

    def list(self,
             vm,
             credentials,
             ):
        """
        List the processes running in the guest operating system, plus those
        started by :func:`Processes.create` that have recently completed. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`Credentials`
        :param credentials: The guest authentication data. See :class:`Credentials`.
        :rtype: :class:`list` of :class:`Processes.Summary`
        :return: The list of running processes is returned in an array of  classes.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine ``vm`` is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine ``vm`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware tools are not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` is not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware tools in the guest
            OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware tools in the guest OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Query``.
        """
        return self._invoke('list',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            })

    def delete(self,
               vm,
               credentials,
               pid,
               ):
        """
        Terminates a process in the guest OS. 
        
        On Posix guests, the process is sent a SIGTERM signal. If that doesn't
        terminate the process, a SIGKILL signal is sent. A process may still be
        running if it's stuck. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`Credentials`
        :param credentials: The guest authentication data. See :class:`Credentials`.
        :type  pid: :class:`long`
        :param pid: Process ID of the process to be terminated
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine ``vm`` is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine ``vm`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the ``pid`` is not found. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the
            :class:`Processes.ProcessErrorDetails` providing additional
            information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware tools are not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if ``credentials`` is not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``credentials`` does not have permission to terminate the
            process.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware tools in the guest
            OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware tools in the guest OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Execute``.
        """
        return self._invoke('delete',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'pid': pid,
                            })
class _CustomizationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'spec': type.ReferenceType(__name__, 'Customization.SetSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/vcenter/vm/{vm}/guest/customization',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        get_error_dict = {
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
            url_template='/vcenter/vm/{vm}/guest/customization',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Customization.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'set': set_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.guest.customization',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _EnvironmentStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType(__name__, 'Credentials'),
            'name': type.StringType(),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/environment/{name}',
            path_variables={
                'vm': 'vm',
                'name': 'name',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'get',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType(__name__, 'Credentials'),
            'names': type.SetType(type.StringType()),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
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
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/environment',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'list',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.StringType(),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.MapType(type.StringType(), type.StringType()),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.guest.environment',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _IdentityStub(ApiInterfaceStub):
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
            url_template='/vcenter/vm/{vm}/guest/identity',
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
                'output_type': type.ReferenceType(__name__, 'Identity.Info'),
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
            self, iface_name='com.vmware.vcenter.vm.guest.identity',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _LocalFilesystemStub(ApiInterfaceStub):
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
            url_template='/vcenter/vm/{vm}/guest/local-filesystem',
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
                'output_type': type.MapType(type.StringType(), type.ReferenceType(__name__, 'LocalFilesystem.Info')),
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
            self, iface_name='com.vmware.vcenter.vm.guest.local_filesystem',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _NetworkingStub(ApiInterfaceStub):
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
            url_template='/vcenter/vm/{vm}/guest/networking',
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
                'output_type': type.ReferenceType(__name__, 'Networking.Info'),
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
            self, iface_name='com.vmware.vcenter.vm.guest.networking',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _OperationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/vm/{vm}/guest/operations',
            path_variables={
                'vm': 'vm',
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
                'output_type': type.ReferenceType(__name__, 'Operations.Info'),
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
            self, iface_name='com.vmware.vcenter.vm.guest.operations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _PowerStub(ApiInterfaceStub):
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
            url_template='/vcenter/vm/{vm}/guest/power',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for shutdown operation
        shutdown_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        shutdown_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        shutdown_input_value_validator_list = [
        ]
        shutdown_output_validator_list = [
        ]
        shutdown_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/power',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for reboot operation
        reboot_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        reboot_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        reboot_input_value_validator_list = [
        ]
        reboot_output_validator_list = [
        ]
        reboot_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/power',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for standby operation
        standby_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        standby_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        standby_input_value_validator_list = [
        ]
        standby_output_validator_list = [
        ]
        standby_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/power',
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
                'output_type': type.ReferenceType(__name__, 'Power.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'shutdown': {
                'input_type': shutdown_input_type,
                'output_type': type.VoidType(),
                'errors': shutdown_error_dict,
                'input_value_validator_list': shutdown_input_value_validator_list,
                'output_validator_list': shutdown_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'reboot': {
                'input_type': reboot_input_type,
                'output_type': type.VoidType(),
                'errors': reboot_error_dict,
                'input_value_validator_list': reboot_input_value_validator_list,
                'output_validator_list': reboot_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'standby': {
                'input_type': standby_input_type,
                'output_type': type.VoidType(),
                'errors': standby_error_dict,
                'input_value_validator_list': standby_input_value_validator_list,
                'output_validator_list': standby_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'shutdown': shutdown_rest_metadata,
            'reboot': reboot_rest_metadata,
            'standby': standby_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.guest.power',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ProcessesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType(__name__, 'Credentials'),
            'spec': type.ReferenceType(__name__, 'Processes.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/processes',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'create',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType(__name__, 'Credentials'),
            'pid': type.IntegerType(),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/processes/{pid}',
            path_variables={
                'vm': 'vm',
                'pid': 'pid',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'get',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType(__name__, 'Credentials'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/processes',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'list',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType(__name__, 'Credentials'),
            'pid': type.IntegerType(),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/processes/{pid}',
            path_variables={
                'vm': 'vm',
                'pid': 'pid',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'delete',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'create': {
                'input_type': create_input_type,
                'output_type': type.IntegerType(),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Processes.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Processes.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.guest.processes',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Customization': Customization,
        'Environment': Environment,
        'Identity': Identity,
        'LocalFilesystem': LocalFilesystem,
        'Networking': Networking,
        'Operations': Operations,
        'Power': Power,
        'Processes': Processes,
        'filesystem': 'com.vmware.vcenter.vm.guest.filesystem_client.StubFactory',
        'networking': 'com.vmware.vcenter.vm.guest.networking_client.StubFactory',
    }

