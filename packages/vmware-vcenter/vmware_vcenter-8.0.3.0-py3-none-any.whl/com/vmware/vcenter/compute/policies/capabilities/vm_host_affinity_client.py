# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.compute.policies.capabilities.vm_host_affinity.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.compute.policies.capabilities.vm_host_affinity_client``
module provides classes for the VM Host affinity capability offered by vCenter
in VMware Cloud on AWS. Usage beyond VMware Cloud on AWS is not supported.

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
    The ``CreateSpec`` class contains information used to create a new virtual
    machine to host affinity policy, see
    :func:`com.vmware.vcenter.compute_client.Policies.create`. Virtual machines
    that have the tag indicated by :attr:`CreateSpec.vm_tag` will be affine to
    hosts that have the tag indicated by :attr:`CreateSpec.host_tag` in VMware
    Cloud on AWS. Usage beyond VMware Cloud on AWS is not supported.
    **Warning:** This class is available as Technology Preview. These are early
    access APIs provided to test, automate and provide feedback on the feature.
    Since this can change based on feedback, VMware does not guarantee
    backwards compatibility and recommends against using them in production
    environments. Some Technology Preview APIs might only be applicable to
    specific environments.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_tag=None,
                 host_tag=None,
                 capability='com.vmware.vcenter.compute.policies.capabilities.vm_host_affinity',
                 name=None,
                 description=None,
                ):
        """
        :type  vm_tag: :class:`str`
        :param vm_tag: Identifier of a tag that can be associated with a virtual machine.
            Virtual machines with this tag will be affine to the hosts
            indicated by :attr:`CreateSpec.host_tag`. **Warning:** This
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
        :type  host_tag: :class:`str`
        :param host_tag: Identifier of a tag that can be associated with a host. Virtual
            machines indicated by :attr:`CreateSpec.vm_tag` will be affine to
            hosts with this tag. **Warning:** This attribute is available as
            Technology Preview. These are early access APIs provided to test,
            automate and provide feedback on the feature. Since this can change
            based on feedback, VMware does not guarantee backwards
            compatibility and recommends against using them in production
            environments. Some Technology Preview APIs might only be applicable
            to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:HostSystem``. When methods return a
            value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:HostSystem``.
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
        self.host_tag = host_tag
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
    'com.vmware.vcenter.compute.policies.capabilities.vm_host_affinity.create_spec', {
        'vm_tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag:VirtualMachine'),
        'host_tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag:HostSystem'),
        'capability': type.IdType(resource_types='com.vmware.vcenter.compute.policies.Capability'),
        'name': type.StringType(),
        'description': type.StringType(),
    },
    CreateSpec,
    False,
    None))



class Info(VapiStruct):
    """
    The ``Info`` class contains information about a virtual machine to host
    affinity policy, see
    :func:`com.vmware.vcenter.compute_client.Policies.get`. Virtual machines
    that have the tag indicated by :attr:`Info.vm_tag` will be affine to hosts
    that have the tag indicated by :attr:`Info.host_tag` in VMware Cloud on
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
                 host_tag=None,
                 name=None,
                 description=None,
                 capability='com.vmware.vcenter.compute.policies.capabilities.vm_host_affinity',
                ):
        """
        :type  vm_tag: :class:`str`
        :param vm_tag: Identifier of a tag that can be associated with a virtual machine.
            Virtual machines with this tag will be affine to the hosts
            indicated by :attr:`Info.host_tag`. **Warning:** This attribute is
            available as Technology Preview. These are early access APIs
            provided to test, automate and provide feedback on the feature.
            Since this can change based on feedback, VMware does not guarantee
            backwards compatibility and recommends against using them in
            production environments. Some Technology Preview APIs might only be
            applicable to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``. When methods return
            a value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``.
        :type  host_tag: :class:`str`
        :param host_tag: Identifier of a tag that can be associated with a host. Virtual
            machines indicated by :attr:`Info.vm_tag` will be affine to hosts
            with this tag. **Warning:** This attribute is available as
            Technology Preview. These are early access APIs provided to test,
            automate and provide feedback on the feature. Since this can change
            based on feedback, VMware does not guarantee backwards
            compatibility and recommends against using them in production
            environments. Some Technology Preview APIs might only be applicable
            to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:HostSystem``. When methods return a
            value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:HostSystem``.
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
        self.host_tag = host_tag
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
    'com.vmware.vcenter.compute.policies.capabilities.vm_host_affinity.info', {
        'vm_tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag:VirtualMachine'),
        'host_tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag:HostSystem'),
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

