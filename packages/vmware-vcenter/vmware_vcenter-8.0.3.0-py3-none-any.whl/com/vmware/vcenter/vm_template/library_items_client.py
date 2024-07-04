# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.vm_template.library_items.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.vm_template.library_items_client`` module provides
classes and classes for managing virtual machine template library items. This
includes methods for checking out virtual machine template library items and
querying previous versions of checked in virtual machines.

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


class CheckOuts(VapiInterface):
    """
    The ``CheckOuts`` class provides methods for managing the checkouts of a
    library item containing a virtual machine template. This class provides
    operations to check out a library item to update the virtual machine
    template, and to check in the library item when the virtual machine changes
    are complete. This class was added in vSphere API 6.9.1.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm_template.library_items.check_outs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CheckOutsStub)
        self._VAPI_OPERATION_IDS = {}

    class CheckOutSpec(VapiStruct):
        """
        The ``CheckOuts.CheckOutSpec`` class defines the information required to
        check out a library item containing a virtual machine template. This class
        was added in vSphere API 6.9.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     placement=None,
                     powered_on=None,
                    ):
            """
            :type  name: :class:`str` or ``None``
            :param name: Name of the virtual machine to check out of the library item. This
                attribute was added in vSphere API 6.9.1.
                This attribute is currently required. In the future, if this
                attribute is None, the system will choose a suitable name for the
                virtual machine.
            :type  placement: :class:`CheckOuts.PlacementSpec` or ``None``
            :param placement: Information used to place the checked out virtual machine. This
                attribute was added in vSphere API 6.9.1.
                This attribute is currently required. In the future, if this
                attribute is None, the system will place the virtual machine on a
                suitable resource. 
                
                If specified, each attribute will be used for placement. If the
                attributes result in disjoint placement, the operation will fail.
                If the attributes along with the placement values of the source
                virtual machine template result in disjoint placement, the
                operation will fail. 
            :type  powered_on: :class:`bool` or ``None``
            :param powered_on: Specifies whether the virtual machine should be powered on after
                check out. This attribute was added in vSphere API 6.9.1.
                If None, the virtual machine will not be powered on after check
                out.
            """
            self.name = name
            self.placement = placement
            self.powered_on = powered_on
            VapiStruct.__init__(self)


    CheckOutSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm_template.library_items.check_outs.check_out_spec', {
            'name': type.OptionalType(type.StringType()),
            'placement': type.OptionalType(type.ReferenceType(__name__, 'CheckOuts.PlacementSpec')),
            'powered_on': type.OptionalType(type.BooleanType()),
        },
        CheckOutSpec,
        False,
        None))


    class PlacementSpec(VapiStruct):
        """
        The ``CheckOuts.PlacementSpec`` class contains information used to place a
        checked out virtual machine onto resources within the vCenter inventory.
        The specified compute resource should have access to the storage associated
        with the checked out virtual machine. This class was added in vSphere API
        6.9.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     resource_pool=None,
                     host=None,
                     cluster=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the virtual machine should be
                placed. This attribute was added in vSphere API 6.9.1.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                If None, the virtual machine will be placed in the same folder as
                the source virtual machine template.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the virtual machine should be placed. This
                attribute was added in vSphere API 6.9.1.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                If None, the system will attempt to choose a suitable resource pool
                for the virtual machine; if a resource pool cannot be chosen, the
                operation will fail.
            :type  host: :class:`str` or ``None``
            :param host: Host onto which the virtual machine should be placed. If ``host``
                and ``resourcePool`` are both specified, ``resourcePool`` must
                belong to ``host``. If ``host`` and ``cluster`` are both specified,
                ``host`` must be a member of ``cluster``. This attribute was added
                in vSphere API 6.9.1.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                This attribute may be None if ``resourcePool`` or ``cluster`` is
                specified. If None, the system will attempt to choose a suitable
                host for the virtual machine; if a host cannot be chosen, the
                operation will fail.
            :type  cluster: :class:`str` or ``None``
            :param cluster: Cluster onto which the virtual machine should be placed. If
                ``cluster`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``cluster``. If ``cluster`` and
                ``host`` are both specified, ``host`` must be a member of
                ``cluster``. This attribute was added in vSphere API 6.9.1.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If ``resourcePool`` or ``host`` is specified, it is recommended
                that this attribute be None.
            """
            self.folder = folder
            self.resource_pool = resource_pool
            self.host = host
            self.cluster = cluster
            VapiStruct.__init__(self)


    PlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm_template.library_items.check_outs.placement_spec', {
            'folder': type.OptionalType(type.IdType()),
            'resource_pool': type.OptionalType(type.IdType()),
            'host': type.OptionalType(type.IdType()),
            'cluster': type.OptionalType(type.IdType()),
        },
        PlacementSpec,
        False,
        None))


    class CheckInSpec(VapiStruct):
        """
        The ``CheckOuts.CheckInSpec`` class defines the information required to
        check in a virtual machine into a library item. This class was added in
        vSphere API 6.9.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     message=None,
                    ):
            """
            :type  message: :class:`str`
            :param message: Message describing the changes made to the virtual machine. This
                attribute was added in vSphere API 6.9.1.
            """
            self.message = message
            VapiStruct.__init__(self)


    CheckInSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm_template.library_items.check_outs.check_in_spec', {
            'message': type.StringType(),
        },
        CheckInSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``CheckOuts.Summary`` class contains commonly used information about a
        checked out virtual machine. This class was added in vSphere API 6.9.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm=None,
                    ):
            """
            :type  vm: :class:`str`
            :param vm: Identifier of the checked out virtual machine. This attribute was
                added in vSphere API 6.9.1.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            """
            self.vm = vm
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm_template.library_items.check_outs.summary', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``CheckOuts.Info`` class contains information about a checked out
        virtual machine. This class was added in vSphere API 6.9.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     time=None,
                     user=None,
                    ):
            """
            :type  time: :class:`datetime.datetime`
            :param time: Date and time when the virtual machine was checked out. This
                attribute was added in vSphere API 6.9.1.
            :type  user: :class:`str`
            :param user: Name of the user who checked out the virtual machine. This
                attribute was added in vSphere API 6.9.1.
            """
            self.time = time
            self.user = user
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm_template.library_items.check_outs.info', {
            'time': type.DateTimeType(),
            'user': type.StringType(),
        },
        Info,
        False,
        None))



    def check_out(self,
                  template_library_item,
                  spec=None,
                  ):
        """
        Checks out a library item containing a virtual machine template. This
        method makes a copy of the source virtual machine template contained in
        the library item as a virtual machine. The virtual machine is copied
        with the same storage specification as the source virtual machine
        template. Changes to the checked out virtual machine do not affect the
        virtual machine template contained in the library item. To save these
        changes back into the library item, :func:`CheckOuts.check_in` the
        virtual machine. To discard the changes, :func:`CheckOuts.delete` the
        virtual machine. This method was added in vSphere API 6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the content library item containing the source
            virtual machine template to be checked out.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :type  spec: :class:`CheckOuts.CheckOutSpec` or ``None``
        :param spec: Specification used to check out the source virtual machine template
            as a virtual machine.
            This parameter is currently required. In the future, if this
            parameter is None, the system will apply suitable defaults.
        :rtype: :class:`str`
        :return: Identifier of the virtual machine that was checked out of the
            library item.
            The return value will be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a virtual machine with the name specified by
            :attr:`CheckOuts.CheckOutSpec.name` already exists in the folder
            specified by :attr:`CheckOuts.PlacementSpec.folder`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``spec`` contains invalid arguments.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the library item is a member of a subscribed library.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the library item specified by ``template_library_item`` cannot
            be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if there is an error accessing the files of the source virtual
            machine template contained in the library item specified by
            ``template_library_item``.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if the limit for the number of virtual machines checked out of a
            library item (currently 1) has been exceeded.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires
              ``ContentLibrary.CheckOutTemplate``.
            * The resource ``Folder`` referenced by the attribute
              :attr:`CheckOuts.PlacementSpec.folder` requires ``System.Read``.
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`CheckOuts.PlacementSpec.resource_pool` requires
              ``System.Read``.
            * The resource ``HostSystem`` referenced by the attribute
              :attr:`CheckOuts.PlacementSpec.host` requires ``System.Read``.
            * The resource ``ClusterComputeResource`` referenced by the
              attribute :attr:`CheckOuts.PlacementSpec.cluster` requires
              ``System.Read``.
        """
        return self._invoke('check_out',
                            {
                            'template_library_item': template_library_item,
                            'spec': spec,
                            })

    def check_in(self,
                 template_library_item,
                 vm,
                 spec=None,
                 ):
        """
        Checks in a virtual machine into the library item. This method updates
        the library item to contain the virtual machine being checked in as a
        template. This template becomes the latest version of the library item.
        The previous virtual machine template contained in the library item is
        available as a backup and its information can be queried using the
        ``Versions`` class. At most one previous version of a virtual machine
        template is retained in the library item. This method was added in
        vSphere API 6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the content library item in which the virtual machine
            is checked in.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine to check into the library item.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  spec: :class:`CheckOuts.CheckInSpec` or ``None``
        :param spec: Specification used to check in the virtual machine into the library
            item.
            This parameter is currently required. In the future, if this
            parameter is None, the system will apply suitable defaults.
        :rtype: :class:`str`
        :return: The new version of the library item.
            The return value will be an identifier for the resource type:
            ``com.vmware.content.library.item.Version``.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the virtual machine identified by ``vm`` was not checked out of
            the item specified by ``template_library_item``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the method cannot be performed because of the virtual machine's
            current state. For example, if the virtual machine is not powered
            off.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the item specified by ``template_library_item`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine specified by ``vm`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if there is an error accessing a file from the virtual machine.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires
              ``ContentLibrary.CheckInTemplate``.
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``System.Read``.
        """
        return self._invoke('check_in',
                            {
                            'template_library_item': template_library_item,
                            'vm': vm,
                            'spec': spec,
                            })

    def list(self,
             template_library_item,
             ):
        """
        Returns commonly used information about the virtual machines that are
        checked out of the library item. This method was added in vSphere API
        6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the VM template library item.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :rtype: :class:`list` of :class:`CheckOuts.Summary`
        :return: List of commonly used information about the check outs.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the library item is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the library item does not contain a virtual machine template.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires ``System.Read``.
        """
        return self._invoke('list',
                            {
                            'template_library_item': template_library_item,
                            })

    def get(self,
            template_library_item,
            vm,
            ):
        """
        Returns the information about a checked out virtual machine. This
        method was added in vSphere API 6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the VM template library item.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :type  vm: :class:`str`
        :param vm: Identifier of the checked out virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`CheckOuts.Info`
        :return: Information about a check out.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the library item or virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the virtual machine is not checked out of the library item.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the library item does not contain a virtual machine template.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires ``System.Read``.
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'template_library_item': template_library_item,
                            'vm': vm,
                            })

    def delete(self,
               template_library_item,
               vm,
               ):
        """
        Deletes the checked out virtual machine. This method was added in
        vSphere API 6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the VM template library item.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :type  vm: :class:`str`
        :param vm: Identifier of the checked out virtual machine to delete.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the library item or virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the virtual machine is not checked out of the library item.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is running (powered on).
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy performing another operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the virtual machine's configuration state cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.Inventory.Delete``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires ``System.Read``.
        """
        return self._invoke('delete',
                            {
                            'template_library_item': template_library_item,
                            'vm': vm,
                            })
class Versions(VapiInterface):
    """
    The ``Versions`` class provides methods for managing the live versions of
    the virtual machine templates contained in a library item. Live versions
    include the latest and previous virtual machine templates that are
    available on disk. As new versions of virtual machine templates are checked
    in, old versions of virtual machine templates are automatically purged.
    Currently, at most one previous virtual machine template version is stored.
    This class was added in vSphere API 6.9.1.
    """
    RESOURCE_TYPE = "com.vmware.content.library.item.Version"
    """
    Resource type for library item versions. This class attribute was added in
    vSphere API 6.9.1.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm_template.library_items.versions'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VersionsStub)
        self._VAPI_OPERATION_IDS = {}

    class Summary(VapiStruct):
        """
        The ``Versions.Summary`` class contains commonly used information about a
        version of a library item containing a virtual machine template. This class
        was added in vSphere API 6.9.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     version=None,
                     vm_template=None,
                    ):
            """
            :type  version: :class:`str`
            :param version: The version of the library item. This attribute was added in
                vSphere API 6.9.1.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.content.library.item.Version``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.content.library.item.Version``.
            :type  vm_template: :class:`str`
            :param vm_template: Identifier of the virtual machine template associated with the
                library item version. This attribute is the managed object
                identifier used to identify the virtual machine template in the
                vSphere Management (SOAP) API. This attribute was added in vSphere
                API 6.9.1.
            """
            self.version = version
            self.vm_template = vm_template
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm_template.library_items.versions.summary', {
            'version': type.IdType(resource_types='com.vmware.content.library.item.Version'),
            'vm_template': type.StringType(),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Versions.Info`` class contains information about a version of a
        library item containing a virtual machine template. This class was added in
        vSphere API 6.9.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm_template=None,
                    ):
            """
            :type  vm_template: :class:`str`
            :param vm_template: Identifier of the virtual machine template associated with the
                library item version. This attribute is the managed object
                identifier used to identify the virtual machine template in the
                vSphere Management (SOAP) API. This attribute was added in vSphere
                API 6.9.1.
            """
            self.vm_template = vm_template
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm_template.library_items.versions.info', {
            'vm_template': type.StringType(),
        },
        Info,
        False,
        None))


    class RollbackSpec(VapiStruct):
        """
        The ``Versions.RollbackSpec`` class defines the information required to
        rollback a virtual machine template library item to a previous version.
        This class was added in vSphere API 6.9.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     message=None,
                    ):
            """
            :type  message: :class:`str`
            :param message: Message describing the reason for the rollback. This attribute was
                added in vSphere API 6.9.1.
            """
            self.message = message
            VapiStruct.__init__(self)


    RollbackSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm_template.library_items.versions.rollback_spec', {
            'message': type.StringType(),
        },
        RollbackSpec,
        False,
        None))



    def list(self,
             template_library_item,
             ):
        """
        Returns commonly used information about the live versions of a virtual
        machine template library item. This method was added in vSphere API
        6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the VM template library item.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :rtype: :class:`list` of :class:`Versions.Summary`
        :return: List of commonly used information about the library item versions.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the library item is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the library item does not contain a virtual machine template.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires ``System.Read``.
        """
        return self._invoke('list',
                            {
                            'template_library_item': template_library_item,
                            })

    def get(self,
            template_library_item,
            version,
            ):
        """
        Returns information about the live version of a library item containing
        a virtual machine template. This method was added in vSphere API 6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the VM template library item.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :type  version: :class:`str`
        :param version: Version of the library item.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.item.Version``.
        :rtype: :class:`Versions.Info`
        :return: Information about the specified library item version.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the library item or version is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the library item does not contain a virtual machine template.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires ``System.Read``.
            * The resource ``com.vmware.content.library.item.Version``
              referenced by the parameter ``version`` requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'template_library_item': template_library_item,
                            'version': version,
                            })

    def rollback(self,
                 template_library_item,
                 version,
                 spec=None,
                 ):
        """
        Rollbacks a library item containing a virtual machine template to a
        previous version. The virtual machine template at the specified version
        becomes the latest virtual machine template with a new version
        identifier. This method was added in vSphere API 6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the VM template library item.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :type  version: :class:`str`
        :param version: Version of the library item to rollback.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.item.Version``.
        :type  spec: :class:`Versions.RollbackSpec` or ``None``
        :param spec: Specification to rollback the library item.
            This parameter is currently required. In the future, if this
            parameter is None, the system will apply suitable defaults.
        :rtype: :class:`str`
        :return: The new version of the library item.
            The return value will be an identifier for the resource type:
            ``com.vmware.content.library.item.Version``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the library item or version is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the specified version is the latest version of the library item.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the library item does not contain a virtual machine template.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if a virtual machine is checked out of the library item.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires
              ``ContentLibrary.CheckInTemplate``.
            * The resource ``com.vmware.content.library.item.Version``
              referenced by the parameter ``version`` requires ``System.Read``.
        """
        return self._invoke('rollback',
                            {
                            'template_library_item': template_library_item,
                            'version': version,
                            'spec': spec,
                            })

    def delete(self,
               template_library_item,
               version,
               ):
        """
        Deletes the virtual machine template contained in the library item at
        the specified version. This method was added in vSphere API 6.9.1.

        :type  template_library_item: :class:`str`
        :param template_library_item: Identifier of the VM template library item.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.Item``.
        :type  version: :class:`str`
        :param version: Version of the library item to delete.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.library.item.Version``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the library item or version is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the specified version is the latest version of the library item.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the library item does not contain a virtual machine template.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the virtual machine template's configuration state cannot be
            accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user that requested the method cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user that requested the method is not authorized to perform
            the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.content.library.Item`` referenced by
              the parameter ``template_library_item`` requires
              ``ContentLibrary.DeleteLibraryItem``.
            * The resource ``com.vmware.content.library.item.Version``
              referenced by the parameter ``version`` requires ``System.Read``.
        """
        return self._invoke('delete',
                            {
                            'template_library_item': template_library_item,
                            'version': version,
                            })
class _CheckOutsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for check_out operation
        check_out_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'CheckOuts.CheckOutSpec')),
        })
        check_out_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        check_out_input_value_validator_list = [
        ]
        check_out_output_validator_list = [
        ]
        check_out_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm-template/library-items/{item}/check-outs',
            path_variables={
                'template_library_item': 'item',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for check_in operation
        check_in_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
            'vm': type.IdType(resource_types='VirtualMachine'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'CheckOuts.CheckInSpec')),
        })
        check_in_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        check_in_input_value_validator_list = [
        ]
        check_in_output_validator_list = [
        ]
        check_in_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm-template/library-items/{item}/check-outs/{vm}',
            path_variables={
                'template_library_item': 'item',
                'vm': 'vm',
            },
             header_parameters={
                   },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/vm-template/library-items/{item}/check-outs',
            path_variables={
                'template_library_item': 'item',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/vm-template/library-items/{item}/check-outs/{vm}',
            path_variables={
                'template_library_item': 'item',
                'vm': 'vm',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/vm-template/library-items/{item}/check-outs/{vm}',
            path_variables={
                'template_library_item': 'item',
                'vm': 'vm',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        operations = {
            'check_out': {
                'input_type': check_out_input_type,
                'output_type': type.IdType(resource_types='VirtualMachine'),
                'errors': check_out_error_dict,
                'input_value_validator_list': check_out_input_value_validator_list,
                'output_validator_list': check_out_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check_in': {
                'input_type': check_in_input_type,
                'output_type': type.IdType(resource_types='com.vmware.content.library.item.Version'),
                'errors': check_in_error_dict,
                'input_value_validator_list': check_in_input_value_validator_list,
                'output_validator_list': check_in_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'CheckOuts.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'CheckOuts.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
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
            'check_out': check_out_rest_metadata,
            'check_in': check_in_rest_metadata,
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm_template.library_items.check_outs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _VersionsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/vm-template/library-items/{item}/versions',
            path_variables={
                'template_library_item': 'item',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
            'version': type.IdType(resource_types='com.vmware.content.library.item.Version'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/vm-template/library-items/{item}/versions/{version}',
            path_variables={
                'template_library_item': 'item',
                'version': 'version',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for rollback operation
        rollback_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
            'version': type.IdType(resource_types='com.vmware.content.library.item.Version'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'Versions.RollbackSpec')),
        })
        rollback_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        rollback_input_value_validator_list = [
        ]
        rollback_output_validator_list = [
        ]
        rollback_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm-template/library-items/{item}/versions/{version}',
            path_variables={
                'template_library_item': 'item',
                'version': 'version',
            },
             header_parameters={
                   },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'template_library_item': type.IdType(resource_types='com.vmware.content.library.Item'),
            'version': type.IdType(resource_types='com.vmware.content.library.item.Version'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/vm-template/library-items/{item}/versions/{version}',
            path_variables={
                'template_library_item': 'item',
                'version': 'version',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Versions.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Versions.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'rollback': {
                'input_type': rollback_input_type,
                'output_type': type.IdType(resource_types='com.vmware.content.library.item.Version'),
                'errors': rollback_error_dict,
                'input_value_validator_list': rollback_input_value_validator_list,
                'output_validator_list': rollback_output_validator_list,
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
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'rollback': rollback_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm_template.library_items.versions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'CheckOuts': CheckOuts,
        'Versions': Versions,
    }

