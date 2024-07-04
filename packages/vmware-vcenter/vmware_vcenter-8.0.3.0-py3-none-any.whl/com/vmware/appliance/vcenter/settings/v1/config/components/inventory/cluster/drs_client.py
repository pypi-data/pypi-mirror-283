# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.
#---------------------------------------------------------------------------

"""
The
``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client``
module provides classes to manage the vCenter Server Inventory Cluster DRS
settings.

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

class ScaleSharesBehavior(Enum):
    """
    

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    DISABLED = None
    """
    Do not scale shares

    """
    SCALE_CPU_AND_MEMORY_SHARES = None
    """
    Scale both CPU and memory shares

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`ScaleSharesBehavior` instance.
        """
        Enum.__init__(string)

ScaleSharesBehavior._set_values({
    'DISABLED': ScaleSharesBehavior('DISABLED'),
    'SCALE_CPU_AND_MEMORY_SHARES': ScaleSharesBehavior('SCALE_CPU_AND_MEMORY_SHARES'),
})
ScaleSharesBehavior._set_binding_type(type.EnumType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.scale_shares_behavior',
    ScaleSharesBehavior))



class DrsBehaviorInfo(Enum):
    """
    The ``DrsBehaviorInfo`` class defines the automation levels that can be set
    on a DRS cluster.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    MANUAL = None
    """
    Specifies that VirtualCenter should generate recommendations for virtual
    machine migration and for placement with a host, but should not implement
    the recommendations automatically.

    """
    PARTIALLY_AUTOMATED = None
    """
    Specifies that VirtualCenter should generate recommendations for virtual
    machine migration and for placement with a host, but should automatically
    implement only the placement at power on.

    """
    FULLY_AUTOMATED = None
    """
    Specifies that VirtualCenter should automate both the migration of virtual
    machines and their placement with a host at power on.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`DrsBehaviorInfo` instance.
        """
        Enum.__init__(string)

DrsBehaviorInfo._set_values({
    'MANUAL': DrsBehaviorInfo('MANUAL'),
    'PARTIALLY_AUTOMATED': DrsBehaviorInfo('PARTIALLY_AUTOMATED'),
    'FULLY_AUTOMATED': DrsBehaviorInfo('FULLY_AUTOMATED'),
})
DrsBehaviorInfo._set_binding_type(type.EnumType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.drs_behavior_info',
    DrsBehaviorInfo))



class DpmBehaviorInfo(Enum):
    """
    The ``DpmBehaviorInfo`` class defines the automation level for DPM service
    on a cluster.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    MANUAL = None
    """
    Specifies that VirtualCenter should generate recommendations for host power
    operations, but should not execute the recommendations automatically.

    """
    AUTOMATED = None
    """
    Specifies that VirtualCenter should generate recommendations for host power
    operations, and should execute the recommendations automatically.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`DpmBehaviorInfo` instance.
        """
        Enum.__init__(string)

DpmBehaviorInfo._set_values({
    'MANUAL': DpmBehaviorInfo('MANUAL'),
    'AUTOMATED': DpmBehaviorInfo('AUTOMATED'),
})
DpmBehaviorInfo._set_binding_type(type.EnumType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.dpm_behavior_info',
    DpmBehaviorInfo))



class Status(Enum):
    """
    The Status enumeration defines a general "health" value for a managed
    entity.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    GRAY = None
    """
    The status is unknown.

    """
    GREEN = None
    """
    The entity is OK.

    """
    YELLOW = None
    """
    The entity might have a problem.

    """
    RED = None
    """
    The entity definitely has a problem.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`Status` instance.
        """
        Enum.__init__(string)

Status._set_values({
    'GRAY': Status('GRAY'),
    'GREEN': Status('GREEN'),
    'YELLOW': Status('YELLOW'),
    'RED': Status('RED'),
})
Status._set_binding_type(type.EnumType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.status',
    Status))




class AdditionalOptions(VapiStruct):
    """
    The ``AdditionalOptions`` class contains attributes describing the HA
    specific configurations of a cluster. It contains cluster-wide
    configurations for vSphereHA.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 advanced_options=None,
                 scalable_shares=None,
                ):
        """
        :type  advanced_options: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.OptionValue` or ``None``
        :param advanced_options: Drs configuration additional options
        :type  scalable_shares: :class:`ScaleSharesBehavior` or ``None``
        :param scalable_shares: Enable scalable shares for the resource pools on this cluster.
        """
        self.advanced_options = advanced_options
        self.scalable_shares = scalable_shares
        VapiStruct.__init__(self)


AdditionalOptions._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.additional_options', {
        'advanced_options': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'OptionValue'))),
        'scalable_shares': type.OptionalType(type.ReferenceType(__name__, 'ScaleSharesBehavior')),
    },
    AdditionalOptions,
    False,
    None))



class Automation(VapiStruct):
    """
    The ``Automation`` class contains attributes describing the HA specific
    configurations of a cluster. It contains cluster-wide configurations for
    vSphereHA.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 automation_level=None,
                 migration_threshold=None,
                 proactive_drs_enabled=None,
                 virtual_machine_automation=None,
                ):
        """
        :type  automation_level: :class:`DrsBehaviorInfo` or ``None``
        :param automation_level: Specifies the cluster-wide default DRS behavior for virtual
            machines. You can override the default behavior for a virtual
            machine.
            If None or empty, the value is skipped.
        :type  migration_threshold: :class:`long` or ``None``
        :param migration_threshold: Threshold for generated recommendations. DRS generates only those
            recommendations that are above the specified vmotionRate. Ratings
            vary from 1 to 5.
            If None or empty, the value is skipped.
        :type  proactive_drs_enabled: :class:`bool` or ``None``
        :param proactive_drs_enabled: Flag indicating whether or not the ProactiveDRS is enabled.
            If None or empty, the value is skipped.
        :type  virtual_machine_automation: :class:`bool` or ``None``
        :param virtual_machine_automation: Flag that dictates whether DRS Behavior overrides for individual
            VMs.
        """
        self.automation_level = automation_level
        self.migration_threshold = migration_threshold
        self.proactive_drs_enabled = proactive_drs_enabled
        self.virtual_machine_automation = virtual_machine_automation
        VapiStruct.__init__(self)


Automation._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.automation', {
        'automation_level': type.OptionalType(type.ReferenceType(__name__, 'DrsBehaviorInfo')),
        'migration_threshold': type.OptionalType(type.IntegerType()),
        'proactive_drs_enabled': type.OptionalType(type.BooleanType()),
        'virtual_machine_automation': type.OptionalType(type.BooleanType()),
    },
    Automation,
    False,
    None))



class DrsConfig(VapiStruct):
    """
    The ``DrsConfig`` class contains attributes describing the HA specific
    configurations of a cluster. It contains cluster-wide configurations for
    DAS.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                 automation=None,
                 additional_options=None,
                 power_management=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Flag indicating whether or not DRS service is enabled.
            If None or empty, the value is skipped.
        :type  automation: :class:`Automation` or ``None``
        :param automation: vSphere HA configuration for Automation Level, Migration Threshold
            Predictive DRS and VM Automation.
        :type  additional_options: :class:`AdditionalOptions` or ``None``
        :param additional_options: vSphere HA configuration for VM Distribution, CPU Over commit
            Scalable Shares.
        :type  power_management: :class:`PowerManagement` or ``None``
        :param power_management: vSphere HA configuration for DPM, AutomationLevel, DPM Threshold.
        """
        self.enabled = enabled
        self.automation = automation
        self.additional_options = additional_options
        self.power_management = power_management
        VapiStruct.__init__(self)


DrsConfig._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.drs_config', {
        'enabled': type.OptionalType(type.BooleanType()),
        'automation': type.OptionalType(type.ReferenceType(__name__, 'Automation')),
        'additional_options': type.OptionalType(type.ReferenceType(__name__, 'AdditionalOptions')),
        'power_management': type.OptionalType(type.ReferenceType(__name__, 'PowerManagement')),
    },
    DrsConfig,
    False,
    None))



class DrsVmOverrides(VapiStruct):
    """
    The ``DrsVmOverrides`` class contains the fields describing DRS behavior
    override for individual virtual machines in the cluster.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 behavior=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Reference to the virtual machine.
        :type  behavior: :class:`DrsBehaviorInfo` or ``None``
        :param behavior: Specifies the particular DRS behavior for this virtual machine.
            If None or empty, the value is skipped.
        """
        self.name = name
        self.behavior = behavior
        VapiStruct.__init__(self)


DrsVmOverrides._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.drs_vm_overrides', {
        'name': type.OptionalType(type.StringType()),
        'behavior': type.OptionalType(type.ReferenceType(__name__, 'DrsBehaviorInfo')),
    },
    DrsVmOverrides,
    False,
    None))



class GroupDetails(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 entities=None,
                 user_created=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Unique name of the group.
        :type  entities: :class:`list` of :class:`str` or ``None``
        :param entities: List of VMs or Hosts belonging to the group.
            If None or empty, the value is skipped.
        :type  user_created: :class:`bool` or ``None``
        :param user_created: Flag to indicate whether the group is created by the user or the
            system.
            If None or empty, the value is skipped.
        """
        self.name = name
        self.entities = entities
        self.user_created = user_created
        VapiStruct.__init__(self)


GroupDetails._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.group_details', {
        'name': type.OptionalType(type.StringType()),
        'entities': type.OptionalType(type.ListType(type.StringType())),
        'user_created': type.OptionalType(type.BooleanType()),
    },
    GroupDetails,
    False,
    None))



class Group(VapiStruct):
    """
    The ``Group`` class describes the properties of virtual machine and host
    groups.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_groups=None,
                 host_groups=None,
                ):
        """
        :type  vm_groups: :class:`list` of :class:`GroupDetails` or ``None``
        :param vm_groups: List of VM Group details.
            If None or empty, the value is skipped.
        :type  host_groups: :class:`list` of :class:`GroupDetails` or ``None``
        :param host_groups: List of HOST Group details.
            If None or empty, the value is skipped.
        """
        self.vm_groups = vm_groups
        self.host_groups = host_groups
        VapiStruct.__init__(self)


Group._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.group', {
        'vm_groups': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'GroupDetails'))),
        'host_groups': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'GroupDetails'))),
    },
    Group,
    False,
    None))



class PowerManagement(VapiStruct):
    """
    The ``PowerManagement`` class contains the fields describing DPM specific
    configurations of a cluster.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 dpm_enabled=None,
                 automation_level=None,
                 dpm_threshold=None,
                ):
        """
        :type  dpm_enabled: :class:`bool` or ``None``
        :param dpm_enabled: Flag indicating whether or not the service is enabled. This service
            can not be enabled, unless DRS is enabled as well.
            If None or empty, the value is skipped.
        :type  automation_level: :class:`DpmBehaviorInfo` or ``None``
        :param automation_level: Specifies the default VMware DPM behavior for hosts. This default
            behavior can be overridden on a per host.
            If None or empty, the value is skipped.
        :type  dpm_threshold: :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.OptionValue` or ``None``
        :param dpm_threshold: DPM Advanced options.
            If None or empty, the value is skipped.
        """
        self.dpm_enabled = dpm_enabled
        self.automation_level = automation_level
        self.dpm_threshold = dpm_threshold
        VapiStruct.__init__(self)


PowerManagement._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.power_management', {
        'dpm_enabled': type.OptionalType(type.BooleanType()),
        'automation_level': type.OptionalType(type.ReferenceType(__name__, 'DpmBehaviorInfo')),
        'dpm_threshold': type.OptionalType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'OptionValue')),
    },
    PowerManagement,
    False,
    None))



class ProactiveHAConfig(VapiStruct):
    """
    The ``ProactiveHAConfig`` class defines the Configuration of the vSphere
    InfraUpdateHA service on a cluster.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                 automation_level=None,
                 remediation=None,
                 providers=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Flag indicating whether or not the service is enabled.
            InfraUpdateHA will not be active, unless DRS is enabled as well.
            If None or empty, the value is skipped.
        :type  automation_level: :class:`ProactiveHAConfig.BehaviorType` or ``None``
        :param automation_level: Configured behavior. Values are of type
            InfraUpdateHaConfig.BehaviorType.
            If None or empty, the value is skipped.
        :type  remediation: :class:`ProactiveHAConfig.RemediationType` or ``None``
        :param remediation: Configured remediation for moderately degraded hosts. Values are of
            type InfraUpdateHaConfig.RemediationType.
            If None or empty, the value is skipped.
        :type  providers: :class:`list` of :class:`str` or ``None``
        :param providers: The list of health update providers configured for this cluster.
            Providers are identified by their id. If the provider list is
            empty, InfraUpdateHA will not be active.
            If None or empty, the value is skipped.
        """
        self.enabled = enabled
        self.automation_level = automation_level
        self.remediation = remediation
        self.providers = providers
        VapiStruct.__init__(self)


    class BehaviorType(Enum):
        """
        The ``ProactiveHAConfig.BehaviorType`` class defines the behavior for
        executing the proposed DRS recommendations.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        MANUAL = None
        """
        With this behavior configured, the proposed DRS recommendations require
        manual approval before they are executed.

        """
        AUTOMATED = None
        """
        With this behavior configured, the proposed DRS recommendations are
        executed immediately.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`BehaviorType` instance.
            """
            Enum.__init__(string)

    BehaviorType._set_values({
        'MANUAL': BehaviorType('MANUAL'),
        'AUTOMATED': BehaviorType('AUTOMATED'),
    })
    BehaviorType._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.proactive_HA_config.behavior_type',
        BehaviorType))

    class RemediationType(Enum):
        """
        The ``ProactiveHAConfig.RemediationType`` class defines the types of
        remediation behaviours that can be configured.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        QUARANTINE_MODE = None
        """
        With this behavior configured, a degraded host will be recommended to be
        placed in Quarantine Mode.

        """
        MAINTENANCE_MODE = None
        """
        With this behavior configured, a degraded host will be recommended to be
        placed in Maintenance Mode.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`RemediationType` instance.
            """
            Enum.__init__(string)

    RemediationType._set_values({
        'QUARANTINE_MODE': RemediationType('QUARANTINE_MODE'),
        'MAINTENANCE_MODE': RemediationType('MAINTENANCE_MODE'),
    })
    RemediationType._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.proactive_HA_config.remediation_type',
        RemediationType))

ProactiveHAConfig._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.proactive_HA_config', {
        'enabled': type.OptionalType(type.BooleanType()),
        'automation_level': type.OptionalType(type.ReferenceType(__name__, 'ProactiveHAConfig.BehaviorType')),
        'remediation': type.OptionalType(type.ReferenceType(__name__, 'ProactiveHAConfig.RemediationType')),
        'providers': type.OptionalType(type.ListType(type.StringType())),
    },
    ProactiveHAConfig,
    False,
    None))



class AffinityRule(VapiStruct):
    """
    The ``AffinityRule`` class defines a set of virtual machines that DRS will
    attempt to run on the same host.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 status=None,
                 enabled=None,
                 in_compliance=None,
                 name=None,
                 mandatory=None,
                 user_created=None,
                 vms=None,
                ):
        """
        :type  status: :class:`Status` or ``None``
        :param status: Flag to indicate whether or not the rule is currently satisfied.
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Flag to indicate whether or not the rule is enabled. Set this
            property when user configures the rule. The default value is false
            (disabled). If there is a rule conflict, the Server can override
            the setting to disable a rule.
            If None or empty, the value is skipped.
        :type  in_compliance: :class:`bool` or ``None``
        :param in_compliance: Flag to indicate if the rule is in compliance.
            If None or empty, the value is skipped.
        :type  name: :class:`str` or ``None``
        :param name: Name of the rule.
        :type  mandatory: :class:`bool` or ``None``
        :param mandatory: Flag to indicate whether compliance with this rule is mandatory or
            optional. The default value is false (optional).
            If None or empty, the value is skipped.
        :type  user_created: :class:`bool` or ``None``
        :param user_created: Flag to indicate whether the rule is created by the user or the
            system.
            If None or empty, the value is skipped.
        :type  vms: :class:`list` of :class:`str` or ``None``
        :param vms: List of virtual machines.
        """
        self.status = status
        self.enabled = enabled
        self.in_compliance = in_compliance
        self.name = name
        self.mandatory = mandatory
        self.user_created = user_created
        self.vms = vms
        VapiStruct.__init__(self)


AffinityRule._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.affinity_rule', {
        'status': type.OptionalType(type.ReferenceType(__name__, 'Status')),
        'enabled': type.OptionalType(type.BooleanType()),
        'in_compliance': type.OptionalType(type.BooleanType()),
        'name': type.OptionalType(type.StringType()),
        'mandatory': type.OptionalType(type.BooleanType()),
        'user_created': type.OptionalType(type.BooleanType()),
        'vms': type.OptionalType(type.ListType(type.StringType())),
    },
    AffinityRule,
    False,
    None))



class DependencyRule(VapiStruct):
    """
    The ``DependencyRule`` class defines VM-to-VM dependencies. 
    
    A VM-VM Dependency rule identifies the following groups. 
    
    * A virtual machine group - :attr:`DependencyRule.vm_group`
    * A "depends on" virtual machine group -
      :attr:`DependencyRule.depends_on_vm_group`.
    
    
    
    The VMs in :attr:`DependencyRule.vm_group` depends on the list of VMs
    specified in :attr:`DependencyRule.depends_on_vm_group`.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 status=None,
                 enabled=None,
                 in_compliance=None,
                 name=None,
                 mandatory=None,
                 user_created=None,
                 vm_group=None,
                 depends_on_vm_group=None,
                ):
        """
        :type  status: :class:`Status` or ``None``
        :param status: Flag to indicate whether or not the rule is currently satisfied.
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Flag to indicate whether or not the rule is enabled. Set this
            property when user configures the rule. The default value is false
            (disabled). If there is a rule conflict, the Server can override
            the setting to disable a rule.
            If None or empty, the value is skipped.
        :type  in_compliance: :class:`bool` or ``None``
        :param in_compliance: Flag to indicate if the rule is in compliance.
            If None or empty, the value is skipped.
        :type  name: :class:`str` or ``None``
        :param name: Name of the rule.
        :type  mandatory: :class:`bool` or ``None``
        :param mandatory: Flag to indicate whether compliance with this rule is mandatory or
            optional. The default value is false (optional).
            If None or empty, the value is skipped.
        :type  user_created: :class:`bool` or ``None``
        :param user_created: Flag to indicate whether the rule is created by the user or the
            system.
            If None or empty, the value is skipped.
        :type  vm_group: :class:`str` or ``None``
        :param vm_group: Virtual group name. The virtual group may contain one or more
            virtual machines.
        :type  depends_on_vm_group: :class:`str` or ``None``
        :param depends_on_vm_group: Depdendency virtual group name. The virtual group may contain one
            or more virtual machines.
        """
        self.status = status
        self.enabled = enabled
        self.in_compliance = in_compliance
        self.name = name
        self.mandatory = mandatory
        self.user_created = user_created
        self.vm_group = vm_group
        self.depends_on_vm_group = depends_on_vm_group
        VapiStruct.__init__(self)


DependencyRule._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.dependency_rule', {
        'status': type.OptionalType(type.ReferenceType(__name__, 'Status')),
        'enabled': type.OptionalType(type.BooleanType()),
        'in_compliance': type.OptionalType(type.BooleanType()),
        'name': type.OptionalType(type.StringType()),
        'mandatory': type.OptionalType(type.BooleanType()),
        'user_created': type.OptionalType(type.BooleanType()),
        'vm_group': type.OptionalType(type.StringType()),
        'depends_on_vm_group': type.OptionalType(type.StringType()),
    },
    DependencyRule,
    False,
    None))



class VmHostRule(VapiStruct):
    """
    The ``VmHostRule`` class defines virtual machines and host groups that
    determine virtual machine placement. The virtual machines and hosts
    referenced by a VM-Host rule must be in the same cluster. 
    
    A VM-Host rule identifies the following groups. 
    
    * A virtual machine group (vim.cluster.VmGroup).
    * Two host groups - an affine host group and an anti-affine host group
      (vim.cluster.HostGroup). At least one of the groups must contain one or
      more hosts.
    
    

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 status=None,
                 enabled=None,
                 in_compliance=None,
                 name=None,
                 mandatory=None,
                 user_created=None,
                 vm_group_name=None,
                 affine_host_group_name=None,
                 anti_affine_host_group_name=None,
                ):
        """
        :type  status: :class:`Status` or ``None``
        :param status: Flag to indicate whether or not the rule is currently satisfied.
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Flag to indicate whether or not the rule is enabled. Set this
            property when user configures the rule. The default value is false
            (disabled). If there is a rule conflict, the Server can override
            the setting to disable a rule.
            If None or empty, the value is skipped.
        :type  in_compliance: :class:`bool` or ``None``
        :param in_compliance: Flag to indicate if the rule is in compliance.
            If None or empty, the value is skipped.
        :type  name: :class:`str` or ``None``
        :param name: Name of the rule.
        :type  mandatory: :class:`bool` or ``None``
        :param mandatory: Flag to indicate whether compliance with this rule is mandatory or
            optional. The default value is false (optional).
            If None or empty, the value is skipped.
        :type  user_created: :class:`bool` or ``None``
        :param user_created: Flag to indicate whether the rule is created by the user or the
            system.
            If None or empty, the value is skipped.
        :type  vm_group_name: :class:`str` or ``None``
        :param vm_group_name: Virtual group name.
            If None or empty, the value is skipped.
        :type  affine_host_group_name: :class:`str` or ``None``
        :param affine_host_group_name: Name of the affine host group. The affine host group identifies
            hosts on which VmHotRule#vmGroupName virtual machines can be
            powered-on.
            If None or empty, the value is skipped.
        :type  anti_affine_host_group_name: :class:`str` or ``None``
        :param anti_affine_host_group_name: Name of the anti-affine host group. The anti-affine host group
            identifies hosts on which VmHotRule#vmGroupName virtual machines
            should not be powered-on.
            If None or empty, the value is skipped.
        """
        self.status = status
        self.enabled = enabled
        self.in_compliance = in_compliance
        self.name = name
        self.mandatory = mandatory
        self.user_created = user_created
        self.vm_group_name = vm_group_name
        self.affine_host_group_name = affine_host_group_name
        self.anti_affine_host_group_name = anti_affine_host_group_name
        VapiStruct.__init__(self)


VmHostRule._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.vm_host_rule', {
        'status': type.OptionalType(type.ReferenceType(__name__, 'Status')),
        'enabled': type.OptionalType(type.BooleanType()),
        'in_compliance': type.OptionalType(type.BooleanType()),
        'name': type.OptionalType(type.StringType()),
        'mandatory': type.OptionalType(type.BooleanType()),
        'user_created': type.OptionalType(type.BooleanType()),
        'vm_group_name': type.OptionalType(type.StringType()),
        'affine_host_group_name': type.OptionalType(type.StringType()),
        'anti_affine_host_group_name': type.OptionalType(type.StringType()),
    },
    VmHostRule,
    False,
    None))



class Rule(VapiStruct):
    """
    The ``Rule`` class describes affinity and anti-affinity DRS rules that
    affect the placement of virtual machines in a cluster.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_affinity_rules=None,
                 vm_anti_affinity_rules=None,
                 dependency_rule=None,
                 vm_host_rule=None,
                ):
        """
        :type  vm_affinity_rules: :class:`list` of :class:`AffinityRule` or ``None``
        :param vm_affinity_rules: Cluster-wide VM affinity rules.If this is set then
            AntiAffinityRule, :class:`DependencyRule`, :class:`VmHostRule` can
            not be set.
            If None or empty, the value is skipped.
        :type  vm_anti_affinity_rules: :class:`list` of :class:`AffinityRule` or ``None``
        :param vm_anti_affinity_rules: Cluster-wide VM anti affinity rules.If this is set then
            AntiAffinityRule, :class:`DependencyRule`, :class:`VmHostRule` can
            not be set.
            If None or empty, the value is skipped.
        :type  dependency_rule: :class:`list` of :class:`DependencyRule` or ``None``
        :param dependency_rule: Cluster-wide VM-to-VM dependency rules.If this is set then
            :class:`AffinityRule`, AntiAffinityRule, :class:`VmHostRule` can
            not be set.
            If None or empty, the value is skipped.
        :type  vm_host_rule: :class:`list` of :class:`VmHostRule` or ``None``
        :param vm_host_rule: Cluster-wide VM-to-Host affinity rules.If this is set then
            :class:`AffinityRule`, AntiAffinityRule, :class:`DependencyRule`
            can not be set.
            If None or empty, the value is skipped.
        """
        self.vm_affinity_rules = vm_affinity_rules
        self.vm_anti_affinity_rules = vm_anti_affinity_rules
        self.dependency_rule = dependency_rule
        self.vm_host_rule = vm_host_rule
        VapiStruct.__init__(self)


Rule._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs.rule', {
        'vm_affinity_rules': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'AffinityRule'))),
        'vm_anti_affinity_rules': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'AffinityRule'))),
        'dependency_rule': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'DependencyRule'))),
        'vm_host_rule': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VmHostRule'))),
    },
    Rule,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

