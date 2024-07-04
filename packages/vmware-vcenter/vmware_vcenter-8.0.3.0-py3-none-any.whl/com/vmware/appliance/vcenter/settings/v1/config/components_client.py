# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.vcenter.settings.v1.config.components_client``
module provides classes to manage the ConfigManagement.

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



class StubFactory(StubFactoryBase):
    _attrs = {
        'applmgmt': 'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt_client.StubFactory',
        'authcommon': 'com.vmware.appliance.vcenter.settings.v1.config.components.authcommon_client.StubFactory',
        'authmanagement': 'com.vmware.appliance.vcenter.settings.v1.config.components.authmanagement_client.StubFactory',
        'inventory': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory_client.StubFactory',
        'inventoryauthorization': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventoryauthorization_client.StubFactory',
        'managementcluster': 'com.vmware.appliance.vcenter.settings.v1.config.components.managementcluster_client.StubFactory',
        'vsphereuiconfiguration': 'com.vmware.appliance.vcenter.settings.v1.config.components.vsphereuiconfiguration_client.StubFactory',
    }

