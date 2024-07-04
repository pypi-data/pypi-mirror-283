# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.compute.policies.capabilities.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.compute.policies.capabilities_client`` module provides
classes for compute policy capabilities offered by vCenter in VMware Cloud on
AWS. Usage beyond VMware Cloud on AWS is not supported.

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
        'cluster_scale_in_ignore_vm_capabilities': 'com.vmware.vcenter.compute.policies.capabilities.cluster_scale_in_ignore_vm_capabilities_client.StubFactory',
        'disable_drs_vmotion': 'com.vmware.vcenter.compute.policies.capabilities.disable_drs_vmotion_client.StubFactory',
        'vm_host_affinity': 'com.vmware.vcenter.compute.policies.capabilities.vm_host_affinity_client.StubFactory',
        'vm_host_anti_affinity': 'com.vmware.vcenter.compute.policies.capabilities.vm_host_anti_affinity_client.StubFactory',
        'vm_vm_affinity': 'com.vmware.vcenter.compute.policies.capabilities.vm_vm_affinity_client.StubFactory',
        'vm_vm_anti_affinity': 'com.vmware.vcenter.compute.policies.capabilities.vm_vm_anti_affinity_client.StubFactory',
    }

