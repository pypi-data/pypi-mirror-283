# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datacenter.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory
.datacenter`` module provides classes to manage the datacenter config.

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


class Datacenter(VapiStruct):
    """
    The ``Datacenter`` class contains spec to define datacenter in vCenter
    Server.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 parent_path=None,
                 permissions=None,
                 standalone_hosts=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Name of the datacenter.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datacenter``.
            When methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datacenter``.
        :type  parent_path: :class:`str` or ``None``
        :param parent_path: Absolute path of the inventory object's parent.
            If None, then inventory object placed in root folder.
        :type  permissions: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.Permission` or ``None``
        :param permissions: Permissions defined on the datacenter.
            If None, then no permissions defined on this inventory object.
        :type  standalone_hosts: :class:`list` of :class:`str` or ``None``
        :param standalone_hosts: Host configuration on the datacenter.
            If None, then no hosts present in the datacenter.
        """
        self.name = name
        self.parent_path = parent_path
        self.permissions = permissions
        self.standalone_hosts = standalone_hosts
        VapiStruct.__init__(self)


Datacenter._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datacenter.datacenter', {
        'name': type.IdType(resource_types='com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datacenter'),
        'parent_path': type.OptionalType(type.StringType()),
        'permissions': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'Permission'))),
        'standalone_hosts': type.OptionalType(type.ListType(type.StringType())),
    },
    Datacenter,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

