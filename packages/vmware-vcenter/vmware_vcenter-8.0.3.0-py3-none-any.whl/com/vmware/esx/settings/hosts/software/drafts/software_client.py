# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.hosts.software.drafts.software.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.hosts.software.drafts.software_client`` module
provides classes to manage specifications in a software draft for an ESX host.

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


class AddOn(VapiInterface):
    """
    The ``AddOn`` class provides methods to manage the OEM add-on specification
    in a software draft. This class was added in vSphere API 8.0.0.1.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.add_on"
    """
    Resource type for add-on resource. This class attribute was added in vSphere
    API 8.0.0.1.

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hosts.software.drafts.software.add_on'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AddOnStub)
        self._VAPI_OPERATION_IDS = {}


    def get(self,
            host,
            draft,
            ):
        """
        Returns the OEM add-on specification in a software draft. This method
        was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:`com.vmware.esx.settings_client.AddOnInfo`
        :return: OEM add-on specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system or no add-on specification is set.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'host': host,
                            'draft': draft,
                            })

    def set(self,
            host,
            draft,
            spec,
            ):
        """
        Sets a new desired OEM add-on specification in the software draft. It
        will overwrite the existing desired OEM add-on specification if one
        already exists. This method was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  spec: :class:`com.vmware.esx.settings_client.AddOnSpec`
        :param spec: AddOn specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('set',
                            {
                            'host': host,
                            'draft': draft,
                            'spec': spec,
                            })

    def delete(self,
               host,
               draft,
               ):
        """
        Deletes the desired OEM add-on specification in the software draft.
        This method was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('delete',
                            {
                            'host': host,
                            'draft': draft,
                            })
class BaseImage(VapiInterface):
    """
    The ``BaseImage`` class provides methods to manage the base-image
    specification in a software draft. This class was added in vSphere API
    8.0.0.1.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.base_image"
    """
    Resource type for base-image resource. This class attribute was added in
    vSphere API 8.0.0.1.

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hosts.software.drafts.software.base_image'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _BaseImageStub)
        self._VAPI_OPERATION_IDS = {}


    def get(self,
            host,
            draft,
            ):
        """
        Returns the base-image specification in a software draft. This method
        was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:`com.vmware.esx.settings_client.BaseImageInfo`
        :return: Base-image specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'host': host,
                            'draft': draft,
                            })

    def set(self,
            host,
            draft,
            spec,
            ):
        """
        Sets a new desired base-image specification in the software draft. It
        will overwrite the existing desired base-image specification if one
        already exists. This method was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  spec: :class:`com.vmware.esx.settings_client.BaseImageSpec`
        :param spec: Base-image specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('set',
                            {
                            'host': host,
                            'draft': draft,
                            'spec': spec,
                            })
class Components(VapiInterface):
    """
    The ``Components`` class provides methods to manage component specification
    in a software draft. This class was added in vSphere API 8.0.0.1.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.component"
    """
    Resource type for component resource. This class attribute was added in vSphere
    API 8.0.0.1.

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hosts.software.drafts.software.components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ComponentsStub)
        self._VAPI_OPERATION_IDS = {}

    class UpdateSpec(VapiStruct):
        """
        The ``Components.UpdateSpec`` class contains attributes that are specified
        to update list of components in the draft. This class was added in vSphere
        API 8.0.0.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     components_to_set=None,
                     components_to_delete=None,
                    ):
            """
            :type  components_to_set: (:class:`dict` of :class:`str` and (:class:`str` or ``None``)) or ``None``
            :param components_to_set: List of components to be updated. If the component already exists
                in the draft, the version is updated, else it is added. If a
                component is provided without version, then its version will be
                chosen based on constraints in the system. This attribute was added
                in vSphere API 8.0.0.1.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.component``. When methods return a
                value of this class as a return value, the key in the attribute
                :class:`dict` will be an identifier for the resource type:
                ``com.vmware.esx.settings.component``.
                If None, no components will be added or updated.
            :type  components_to_delete: :class:`set` of :class:`str` or ``None``
            :param components_to_delete: List of components to be removed. This attribute was added in
                vSphere API 8.0.0.1.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.settings.component``. When methods return a value
                of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.esx.settings.component``.
                If None, no components will be removed.
            """
            self.components_to_set = components_to_set
            self.components_to_delete = components_to_delete
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hosts.software.drafts.software.components.update_spec', {
            'components_to_set': type.OptionalType(type.MapType(type.IdType(), type.OptionalType(type.StringType()))),
            'components_to_delete': type.OptionalType(type.SetType(type.IdType())),
        },
        UpdateSpec,
        False,
        None))



    def get(self,
            host,
            draft,
            component,
            ):
        """
        Returns the component version for the given component in the software
        draft. This method was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  component: :class:`str`
        :param component: Identifier of the component.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.component``.
        :rtype: :class:`com.vmware.esx.settings_client.ComponentInfo` or ``None``
        :return: Information about component version.
            If None then version will be chosen based on the constraints in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` or no component associated with ``component`` in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'host': host,
                            'draft': draft,
                            'component': component,
                            })

    def set(self,
            host,
            draft,
            component,
            version=None,
            ):
        """
        Set the component version for a given component in the software draft.
        This will overwrite any existing version for the given component. This
        method was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  component: :class:`str`
        :param component: Identifier of the component.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.component``.
        :type  version: :class:`str` or ``None``
        :param version: Component version.
            This attribute is currently required. In the future,if this
            attribute is None then version is chosen based on the constraints
            in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('set',
                            {
                            'host': host,
                            'draft': draft,
                            'component': component,
                            'version': version,
                            })

    def delete(self,
               host,
               draft,
               component,
               ):
        """
        Deletes the given component from the software draft. This method was
        added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  component: :class:`str`
        :param component: Identifier of the component.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.component``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` or no component associated with ``component`` in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('delete',
                            {
                            'host': host,
                            'draft': draft,
                            'component': component,
                            })

    def update(self,
               host,
               draft,
               spec,
               ):
        """
        Updates the list of components in a given draft. This allows set and/or
        delete of multiple components in a batch operation. This method was
        added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  spec: :class:`Components.UpdateSpec`
        :param spec: Update specification containing list of components to add and/or
            delete.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('update',
                            {
                            'host': host,
                            'draft': draft,
                            'spec': spec,
                            })

    def list(self,
             host,
             draft,
             ):
        """
        Returns the components that comprise the software draft. This method
        was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:`dict` of :class:`str` and :class:`com.vmware.esx.settings_client.ComponentInfo`
        :return: Map of component version information keyed by the component
            identifier.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``com.vmware.esx.settings.component``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('list',
                            {
                            'host': host,
                            'draft': draft,
                            })
class EffectiveComponents(VapiInterface):
    """
    The ``EffectiveComponents`` class provides methods to manage effective list
    of components. This class was added in vSphere API 8.0.0.1.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hosts.software.drafts.software.effective_components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EffectiveComponentsStub)
        self._VAPI_OPERATION_IDS = {}


    def list(self,
             host,
             draft,
             ):
        """
        Returns the components that comprise the desired software state of the
        host. This method was added in vSphere API 8.0.0.1.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:`dict` of :class:`str` and :class:`com.vmware.esx.settings_client.EffectiveComponentInfo`
        :return: Map of effective components keyed by their identifier.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``com.vmware.esx.settings.component``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('list',
                            {
                            'host': host,
                            'draft': draft,
                            })

    def list_with_removed_components(self,
                                     host,
                                     draft,
                                     ):
        """
        Returns the list of all the effective components. Pass the param
        "with-removed-components" to get even the removed components. This
        method was added in vSphere API 8.0.3.0.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the draft.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:`dict` of :class:`str` and :class:`com.vmware.esx.settings_client.EffectiveComponentInfo`
        :return: Map of effective components keyed by their identifier.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``com.vmware.esx.settings.component``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standlone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('list_with_removed_components',
                            {
                            'host': host,
                            'draft': draft,
                            })
class RemovedComponents(VapiInterface):
    """
    The ``RemovedComponents`` class provides methods to manage removal of
    components in a software draft. This class was added in vSphere API
    8.0.3.0.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.component"
    """
    Resource type for component resource. This class attribute was added in vSphere
    API 8.0.3.0.

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hosts.software.drafts.software.removed_components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _RemovedComponentsStub)
        self._VAPI_OPERATION_IDS = {}


    def get(self,
            host,
            draft,
            component,
            ):
        """
        Returns the component information for the given removed component in
        the software draft. This method was added in vSphere API 8.0.3.0.

        :type  host: :class:`str`
        :param host: Identifier of the standalone host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  component: :class:`str`
        :param component: Identifier of the component.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.component``.
        :rtype: :class:`com.vmware.esx.settings_client.ComponentInfo`
        :return: Information about component version.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no such host ``host`` or no draft associated with
            ``draft`` or no component associated with ``component`` in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'host': host,
                            'draft': draft,
                            'component': component,
                            })

    def set(self,
            host,
            draft,
            component,
            ):
        """
        Set the component to be removed in the software draft. This method was
        added in vSphere API 8.0.3.0.

        :type  host: :class:`str`
        :param host: Identifier of the standalone host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  component: :class:`str`
        :param component: Identifier of the component.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.component``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host ``host`` or no draft associated with ``draft``
            in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('set',
                            {
                            'host': host,
                            'draft': draft,
                            'component': component,
                            })

    def delete(self,
               host,
               draft,
               component,
               ):
        """
        Deletes the given component from the removed component section of the
        software draft. This method was added in vSphere API 8.0.3.0.

        :type  host: :class:`str`
        :param host: Identifier of the standalone host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  component: :class:`str`
        :param component: Identifier of the component.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.component``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('delete',
                            {
                            'host': host,
                            'draft': draft,
                            'component': component,
                            })

    def list(self,
             host,
             draft,
             ):
        """
        Returns the map of removed components that comprise the software draft.
        This method was added in vSphere API 8.0.3.0.

        :type  host: :class:`str`
        :param host: Identifier of the standalone host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:`dict` of :class:`str` and :class:`com.vmware.esx.settings_client.ComponentInfo`
        :return: Map of component information keyed by the component identifier.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``com.vmware.esx.settings.component``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host ``host`` or no draft associated with ``draft``
            in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('list',
                            {
                            'host': host,
                            'draft': draft,
                            })
class _AddOnStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/add-on',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'spec': type.ReferenceType('com.vmware.esx.settings_client', 'AddOnSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/add-on',
            request_body_parameter='spec',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/add-on',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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
                'output_type': type.ReferenceType('com.vmware.esx.settings_client', 'AddOnInfo'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
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
            'get': get_rest_metadata,
            'set': set_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.hosts.software.drafts.software.add_on',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _BaseImageStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/base-image',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'spec': type.ReferenceType('com.vmware.esx.settings_client', 'BaseImageSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/base-image',
            request_body_parameter='spec',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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
                'output_type': type.ReferenceType('com.vmware.esx.settings_client', 'BaseImageInfo'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'set': set_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.hosts.software.drafts.software.base_image',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'component': type.IdType(resource_types='com.vmware.esx.settings.component'),
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/components/{component}',
            path_variables={
                'host': 'host',
                'draft': 'draft',
                'component': 'component',
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

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'component': type.IdType(resource_types='com.vmware.esx.settings.component'),
            'version': type.OptionalType(type.StringType()),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/components/{component}',
            request_body_parameter='version',
            path_variables={
                'host': 'host',
                'draft': 'draft',
                'component': 'component',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'component': type.IdType(resource_types='com.vmware.esx.settings.component'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/components/{component}',
            path_variables={
                'host': 'host',
                'draft': 'draft',
                'component': 'component',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'spec': type.ReferenceType(__name__, 'Components.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/components',
            request_body_parameter='spec',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            http_method='GET',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/components',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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
                'output_type': type.OptionalType(type.ReferenceType('com.vmware.esx.settings_client', 'ComponentInfo')),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
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
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType('com.vmware.esx.settings_client', 'ComponentInfo')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'set': set_rest_metadata,
            'delete': delete_rest_metadata,
            'update': update_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.hosts.software.drafts.software.components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _EffectiveComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            http_method='GET',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/effective-components',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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

        # properties for list_with_removed_components operation
        list_with_removed_components_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
        })
        list_with_removed_components_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        list_with_removed_components_input_value_validator_list = [
        ]
        list_with_removed_components_output_validator_list = [
        ]
        list_with_removed_components_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/effective-components',
            path_variables={
                'host': 'host',
                'draft': 'draft',
            },
            query_parameters={
            },
            dispatch_parameters={
                'with-removed-components': 'null',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType('com.vmware.esx.settings_client', 'EffectiveComponentInfo')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list_with_removed_components': {
                'input_type': list_with_removed_components_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType('com.vmware.esx.settings_client', 'EffectiveComponentInfo')),
                'errors': list_with_removed_components_error_dict,
                'input_value_validator_list': list_with_removed_components_input_value_validator_list,
                'output_validator_list': list_with_removed_components_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'list_with_removed_components': list_with_removed_components_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.hosts.software.drafts.software.effective_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _RemovedComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'component': type.IdType(resource_types='com.vmware.esx.settings.component'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/removed-components/{component}',
            path_variables={
                'host': 'host',
                'draft': 'draft',
                'component': 'component',
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

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'component': type.IdType(resource_types='com.vmware.esx.settings.component'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/removed-components/{component}',
            path_variables={
                'host': 'host',
                'draft': 'draft',
                'component': 'component',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'component': type.IdType(resource_types='com.vmware.esx.settings.component'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/removed-components/{component}',
            path_variables={
                'host': 'host',
                'draft': 'draft',
                'component': 'component',
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

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/software/removed-components',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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
                'output_type': type.ReferenceType('com.vmware.esx.settings_client', 'ComponentInfo'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType('com.vmware.esx.settings_client', 'ComponentInfo')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'set': set_rest_metadata,
            'delete': delete_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.hosts.software.drafts.software.removed_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'AddOn': AddOn,
        'BaseImage': BaseImage,
        'Components': Components,
        'EffectiveComponents': EffectiveComponents,
        'RemovedComponents': RemovedComponents,
    }

