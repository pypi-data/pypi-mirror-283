# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.host.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.vcenter.settings.v1.config.components
inventory.host`` module provides classes to manage the ConfigManagement.

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


class HostConfig(VapiStruct):
    """
    The ``HostConfig`` class contains attributes describing the configuration
    of a Stand alone host.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 permissions=None,
                 parent_path=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Name of the host
        :type  permissions: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.Permission` or ``None``
        :param permissions: Permission on the host.
            If None, then no permissions defined on this inventory object.
        :type  parent_path: :class:`str` or ``None``
        :param parent_path: Parent of this inventory object.
            If None, then inventory object placed in root folder.
        """
        self.name = name
        self.permissions = permissions
        self.parent_path = parent_path
        VapiStruct.__init__(self)


HostConfig._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.host.host_config', {
        'name': type.StringType(),
        'permissions': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'Permission'))),
        'parent_path': type.OptionalType(type.StringType()),
    },
    HostConfig,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

