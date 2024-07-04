# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.deployment.migrate.
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


class ActiveDirectorySpec(VapiStruct):
    """
    The ``ActiveDirectorySpec`` class contains information used to join the
    migrated vCenter Server appliance to the Active Directory. This class was
    added in vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 domain=None,
                 username=None,
                 password=None,
                ):
        """
        :type  domain: :class:`str`
        :param domain: The domain name of the Active Directory server to which the
            migrated vCenter Server appliance should be joined. This attribute
            was added in vSphere API 7.0.0.0.
        :type  username: :class:`str`
        :param username: Active Directory user that has permission to join the Active
            Directory after the vCenter Server is migrated to appliance. This
            attribute was added in vSphere API 7.0.0.0.
        :type  password: :class:`str`
        :param password: Active Directory user password that has permission to join the
            Active Directory after the vCenter Server is migrated to appliance.
            This attribute was added in vSphere API 7.0.0.0.
        """
        self.domain = domain
        self.username = username
        self.password = password
        VapiStruct.__init__(self)


ActiveDirectorySpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.migrate.active_directory_spec', {
        'domain': type.StringType(),
        'username': type.StringType(),
        'password': type.StringType(),
    },
    ActiveDirectorySpec,
    False,
    None))



class ActiveDirectory(VapiInterface):
    """
    The ``ActiveDirectory`` class provides methods to check if the migrated
    vCenter Server appliance can join to the given domain using the provided
    credentials. This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.deployment.migrate.active_directory'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ActiveDirectoryStub)
        self._VAPI_OPERATION_IDS = {}

    class CheckSpec(VapiStruct):
        """
        The ``ActiveDirectory.CheckSpec`` class contains information used to join
        the migrated vCenter Server appliance to the Active Directory. This class
        was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     dns_servers=None,
                     domain=None,
                     username=None,
                     password=None,
                    ):
            """
            :type  dns_servers: :class:`list` of :class:`str`
            :param dns_servers: IP addresses of the DNS servers of the Active Directory server.
                This attribute was added in vSphere API 7.0.0.0.
            :type  domain: :class:`str`
            :param domain: The domain name of the Active Directory server to which the
                migrated vCenter Server appliance should be joined. This attribute
                was added in vSphere API 7.0.0.0.
            :type  username: :class:`str`
            :param username: Active Directory user that has permission to join the Active
                Directory after the vCenter Server is migrated to appliance. This
                attribute was added in vSphere API 7.0.0.0.
            :type  password: :class:`str`
            :param password: Active Directory user password that has permission to join the
                Active Directory after the vCenter Server is migrated to appliance.
                This attribute was added in vSphere API 7.0.0.0.
            """
            self.dns_servers = dns_servers
            self.domain = domain
            self.username = username
            self.password = password
            VapiStruct.__init__(self)


    CheckSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.migrate.active_directory.check_spec', {
            'dns_servers': type.ListType(type.StringType()),
            'domain': type.StringType(),
            'username': type.StringType(),
            'password': type.StringType(),
        },
        CheckSpec,
        False,
        None))



    def check(self,
              spec,
              ):
        """
        Checks whether the provided Active Directory user has permission to
        join the migrated vCenter Server appliance to the domain. This method
        was added in vSphere API 7.0.0.0.

        :type  spec: :class:`ActiveDirectory.CheckSpec`
        :param spec: Information to connect to Active Directory.
        :rtype: :class:`com.vmware.vcenter.deployment_client.CheckInfo`
        :return: Information about the success or failure of the checks that were
            performed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in INITIALIZED state.
        """
        return self._invoke('check',
                            {
                            'spec': spec,
                            })
class _ActiveDirectoryStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'ActiveDirectory.CheckSpec'),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/migrate/active-directory?action=check',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'check': {
                'input_type': check_input_type,
                'output_type': type.ReferenceType('com.vmware.vcenter.deployment_client', 'CheckInfo'),
                'errors': check_error_dict,
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': check_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'check': check_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.deployment.migrate.active_directory',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ActiveDirectory': ActiveDirectory,
    }

