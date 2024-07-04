# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.compute.policies.capabilities.cluster_scale_in_ignore_vm_capabilities.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.compute.policies.capabilities.cluster_scale_in_ignore_vm_capabilities_client``
module provides classes for the Scale-In Ignore Virtual Machine Capabilities
capability offered by vCenter in VMware Cloud on AWS. Usage beyond VMware Cloud
on AWS is not supported.

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


class CreateSpec(VapiStruct):
    """
    The ``CreateSpec`` class contains information used to create a new policy
    to ignore virtual machine capabilities when scaling-in a cluster, see
    :func:`com.vmware.vcenter.compute_client.Policies.create`. When considering
    scaling-in a cluster, policies that have been created with one of the
    listed :attr:`CreateSpec.vm_capabilities` are ignored for virtual machines
    that have the tag indicated by :attr:`CreateSpec.vm_tag` in VMware Cloud on
    AWS. Usage beyond VMware Cloud on AWS is not supported. **Warning:** This
    class is available as Technology Preview. These are early access APIs
    provided to test, automate and provide feedback on the feature. Since this
    can change based on feedback, VMware does not guarantee backwards
    compatibility and recommends against using them in production environments.
    Some Technology Preview APIs might only be applicable to specific
    environments.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_tag=None,
                 vm_capabilities=None,
                 capability='com.vmware.vcenter.compute.policies.capabilities.cluster_scale_in_ignore_vm_capabilities',
                 name=None,
                 description=None,
                ):
        """
        :type  vm_tag: :class:`str`
        :param vm_tag: When considering scaling-in a cluster, policies that have been
            created with one of the listed :attr:`CreateSpec.vm_capabilities`
            are ignored for virtual machines that have this tag. **Warning:**
            This attribute is available as Technology Preview. These are early
            access APIs provided to test, automate and provide feedback on the
            feature. Since this can change based on feedback, VMware does not
            guarantee backwards compatibility and recommends against using them
            in production environments. Some Technology Preview APIs might only
            be applicable to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``. When methods return
            a value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``.
        :type  vm_capabilities: :class:`set` of :class:`str`
        :param vm_capabilities: When considering scaling-in a cluster, policies that have been
            created with one of these capabilities are ignored for virtual
            machines that have the tag indicated by :attr:`CreateSpec.vm_tag`.
            This :class:`set` must contain at least one item. Currently, the
            only allowed capability identifier is
            ``com.vmware.vcenter.compute.policies.capabilities.disable_drs_vmotion_client``.
            In the future, other capabilities may be specified. **Warning:**
            This attribute is available as Technology Preview. These are early
            access APIs provided to test, automate and provide feedback on the
            feature. Since this can change based on feedback, VMware does not
            guarantee backwards compatibility and recommends against using them
            in production environments. Some Technology Preview APIs might only
            be applicable to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability:VirtualMachine``.
            When methods return a value of this class as a return value, the
            attribute will contain identifiers for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability:VirtualMachine``.
        :type  capability: :class:`str`
        :param capability: Identifier of the capability this policy is based on.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability``. When methods
            return a value of this class as a return value, the attribute will
            be an identifier for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability``.
        :type  name: :class:`str`
        :param name: Name of the policy. The name needs to be unique within this vCenter
            server.
        :type  description: :class:`str`
        :param description: Description of the policy.
        """
        self.vm_tag = vm_tag
        self.vm_capabilities = vm_capabilities
        self._capability = capability
        self.name = name
        self.description = description
        VapiStruct.__init__(self)

    @property
    def capability(self):
        """
        Return the discriminator value
        """
        return self._capability

CreateSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.compute.policies.capabilities.cluster_scale_in_ignore_vm_capabilities.create_spec', {
        'vm_tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag:VirtualMachine'),
        'vm_capabilities': type.SetType(type.IdType()),
        'capability': type.IdType(resource_types='com.vmware.vcenter.compute.policies.Capability'),
        'name': type.StringType(),
        'description': type.StringType(),
    },
    CreateSpec,
    False,
    None))



class Info(VapiStruct):
    """
    The ``Info`` class contains information about a policy to ignore virtual
    machine capabilities when scaling-in a cluster, see
    :func:`com.vmware.vcenter.compute_client.Policies.get`. When considering
    scaling-in a cluster, policies that have been created with one of the
    listed :attr:`Info.vm_capabilities` are ignored for virtual machines that
    have the tag indicated by :attr:`Info.vm_tag` in VMware Cloud on AWS. Usage
    beyond VMware Cloud on AWS is not supported. **Warning:** This class is
    available as Technology Preview. These are early access APIs provided to
    test, automate and provide feedback on the feature. Since this can change
    based on feedback, VMware does not guarantee backwards compatibility and
    recommends against using them in production environments. Some Technology
    Preview APIs might only be applicable to specific environments.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_tag=None,
                 vm_capabilities=None,
                 name=None,
                 description=None,
                 capability='com.vmware.vcenter.compute.policies.capabilities.cluster_scale_in_ignore_vm_capabilities',
                ):
        """
        :type  vm_tag: :class:`str`
        :param vm_tag: When considering scaling-in a cluster, policies that have been
            created with one of the listed :attr:`Info.vm_capabilities` are
            ignored for virtual machines that have this tag. **Warning:** This
            attribute is available as Technology Preview. These are early
            access APIs provided to test, automate and provide feedback on the
            feature. Since this can change based on feedback, VMware does not
            guarantee backwards compatibility and recommends against using them
            in production environments. Some Technology Preview APIs might only
            be applicable to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``. When methods return
            a value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``.
        :type  vm_capabilities: :class:`set` of :class:`str`
        :param vm_capabilities: When considering scaling-in a cluster, policies that have been
            created with one of these capabilities are ignored for virtual
            machines that have the tag indicated by :attr:`Info.vm_tag`.
            **Warning:** This attribute is available as Technology Preview.
            These are early access APIs provided to test, automate and provide
            feedback on the feature. Since this can change based on feedback,
            VMware does not guarantee backwards compatibility and recommends
            against using them in production environments. Some Technology
            Preview APIs might only be applicable to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability:VirtualMachine``.
            When methods return a value of this class as a return value, the
            attribute will contain identifiers for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability:VirtualMachine``.
        :type  name: :class:`str`
        :param name: Name of the policy.
        :type  description: :class:`str`
        :param description: Description of the policy.
        :type  capability: :class:`str`
        :param capability: Identifier of the capability this policy is based on.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability``. When methods
            return a value of this class as a return value, the attribute will
            be an identifier for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability``.
        """
        self.vm_tag = vm_tag
        self.vm_capabilities = vm_capabilities
        self.name = name
        self.description = description
        self._capability = capability
        VapiStruct.__init__(self)

    @property
    def capability(self):
        """
        Return the discriminator value
        """
        return self._capability

Info._set_binding_type(type.StructType(
    'com.vmware.vcenter.compute.policies.capabilities.cluster_scale_in_ignore_vm_capabilities.info', {
        'vm_tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag:VirtualMachine'),
        'vm_capabilities': type.SetType(type.IdType()),
        'name': type.StringType(),
        'description': type.StringType(),
        'capability': type.IdType(resource_types='com.vmware.vcenter.compute.policies.Capability'),
    },
    Info,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

