# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vapi.metadata.cli.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vapi.metadata.cli_client`` module provides classes that expose
all the information required to display namespace or command help, execute a
command and display it's result.

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


class Command(VapiInterface):
    """
    The ``Command`` class provides methods to get information about command
    line interface (CLI) commands.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vapi.metadata.cli.command'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CommandStub)
        self._VAPI_OPERATION_IDS = {}

    class FormatterType(Enum):
        """
        The ``Command.FormatterType`` class defines supported CLI output formatter
        types. See :attr:`Command.Info.formatter`.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        SIMPLE = None
        """
        Displays command output as it is.

        """
        TABLE = None
        """
        Displays command output in table format.

        """
        JSON = None
        """
        Displays command output in JSON format.

        """
        XML = None
        """
        Displays command output in XML format.

        """
        CSV = None
        """
        Displays command output in CSV format.

        """
        HTML = None
        """
        Displays command output in HTML format.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`FormatterType` instance.
            """
            Enum.__init__(string)

    FormatterType._set_values({
        'SIMPLE': FormatterType('SIMPLE'),
        'TABLE': FormatterType('TABLE'),
        'JSON': FormatterType('JSON'),
        'XML': FormatterType('XML'),
        'CSV': FormatterType('CSV'),
        'HTML': FormatterType('HTML'),
    })
    FormatterType._set_binding_type(type.EnumType(
        'com.vmware.vapi.metadata.cli.command.formatter_type',
        FormatterType))


    class GenericType(Enum):
        """
        The ``Command.GenericType`` class defines generic types supported by
        ``Command`` class. See :attr:`Command.OptionInfo.generic`.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        NONE = None
        """
        Default case.

        """
        OPTIONAL = None
        """
        Input parameter is an optional.

        """
        LIST = None
        """
        Input parameter is a list.

        """
        OPTIONAL_LIST = None
        """
        Input parameter is an optional of type list. This class attribute was added
        in vSphere API 6.5.

        """
        LIST_OPTIONAL = None
        """
        Input parameter is a list of optionals. This class attribute was added in
        vSphere API 6.5.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`GenericType` instance.
            """
            Enum.__init__(string)

    GenericType._set_values({
        'NONE': GenericType('NONE'),
        'OPTIONAL': GenericType('OPTIONAL'),
        'LIST': GenericType('LIST'),
        'OPTIONAL_LIST': GenericType('OPTIONAL_LIST'),
        'LIST_OPTIONAL': GenericType('LIST_OPTIONAL'),
    })
    GenericType._set_binding_type(type.EnumType(
        'com.vmware.vapi.metadata.cli.command.generic_type',
        GenericType))


    class OutputFieldInfo(VapiStruct):
        """
        The ``Command.OutputFieldInfo`` class describes the name used by the CLI to
        display a single attribute of a class element in the interface definition
        language.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     field_name=None,
                     display_name=None,
                    ):
            """
            :type  field_name: :class:`str`
            :param field_name: Name of the attribute.
            :type  display_name: :class:`str`
            :param display_name: Name used by the CLI to display the attribute.
            """
            self.field_name = field_name
            self.display_name = display_name
            VapiStruct.__init__(self)


    OutputFieldInfo._set_binding_type(type.StructType(
        'com.vmware.vapi.metadata.cli.command.output_field_info', {
            'field_name': type.StringType(),
            'display_name': type.StringType(),
        },
        OutputFieldInfo,
        False,
        None))


    class OutputInfo(VapiStruct):
        """
        The ``Command.OutputInfo`` class describes the names used by the CLI to
        display the attributes of a class element in the interface definition
        language as well as the order in which the attributes will be displayed.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     structure_id=None,
                     output_fields=None,
                    ):
            """
            :type  structure_id: :class:`str`
            :param structure_id: Name of the class.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.structure``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.structure``.
            :type  output_fields: :class:`list` of :class:`Command.OutputFieldInfo`
            :param output_fields: The order in which the attributes of the class will be displayed by
                the CLI as well as the names used to display the attributes.
            """
            self.structure_id = structure_id
            self.output_fields = output_fields
            VapiStruct.__init__(self)


    OutputInfo._set_binding_type(type.StructType(
        'com.vmware.vapi.metadata.cli.command.output_info', {
            'structure_id': type.IdType(resource_types='com.vmware.vapi.structure'),
            'output_fields': type.ListType(type.ReferenceType(__name__, 'Command.OutputFieldInfo')),
        },
        OutputInfo,
        False,
        None))


    class OptionInfo(VapiStruct):
        """
        The ``Command.OptionInfo`` class describes information about a specific
        input option of a command.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     long_option=None,
                     short_option=None,
                     field_name=None,
                     description=None,
                     type=None,
                     generic=None,
                    ):
            """
            :type  long_option: :class:`str`
            :param long_option: The long option name of the parameter as used by the user.
            :type  short_option: :class:`str` or ``None``
            :param short_option: The single character value option name.
                If not present, there's no single character option for the
                parameter.
            :type  field_name: :class:`str`
            :param field_name: The fully qualified name of the option referred to by the operation
                element in :attr:`Command.Info.operation_id`.
            :type  description: :class:`str`
            :param description: The description of the option to be displayed to the user when they
                request usage information for a CLI command.
            :type  type: :class:`str`
            :param type: The type of option. This is used to display information about what
                kind of data is expected (string, number, boolean, etc.) for the
                option when they request usage information for a CLI command. For
                class this stores the fully qualified class id.
            :type  generic: :class:`Command.GenericType`
            :param generic: This is used to tell the user whether the option is required or
                optional, or whether they can specify the option multiple times.
            """
            self.long_option = long_option
            self.short_option = short_option
            self.field_name = field_name
            self.description = description
            self.type = type
            self.generic = generic
            VapiStruct.__init__(self)


    OptionInfo._set_binding_type(type.StructType(
        'com.vmware.vapi.metadata.cli.command.option_info', {
            'long_option': type.StringType(),
            'short_option': type.OptionalType(type.StringType()),
            'field_name': type.StringType(),
            'description': type.StringType(),
            'type': type.StringType(),
            'generic': type.ReferenceType(__name__, 'Command.GenericType'),
        },
        OptionInfo,
        False,
        None))


    class Identity(VapiStruct):
        """
        The ``Command.Identity`` class uniquely identifies a command in the CLI
        commands tree.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     path=None,
                     name=None,
                    ):
            """
            :type  path: :class:`str`
            :param path: The dot-separated path of the namespace containing the command in
                the CLI command tree.
            :type  name: :class:`str`
            :param name: Name of the command.
            """
            self.path = path
            self.name = name
            VapiStruct.__init__(self)


    Identity._set_binding_type(type.StructType(
        'com.vmware.vapi.metadata.cli.command.identity', {
            'path': type.StringType(),
            'name': type.StringType(),
        },
        Identity,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Command.Info`` class contains information about a command. It
        includes the identity of the command, a description, information about the
        class and method that implement the command, and CLI-specific information
        for the command.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     identity=None,
                     description=None,
                     service_id=None,
                     operation_id=None,
                     options=None,
                     formatter=None,
                     output_field_list=None,
                    ):
            """
            :type  identity: :class:`Command.Identity`
            :param identity: Basic command identity.
            :type  description: :class:`str`
            :param description: The text description displayed to the user in help output.
            :type  service_id: :class:`str`
            :param service_id: The service identifier that contains the operations for this CLI
                command.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.service``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.service``.
            :type  operation_id: :class:`str`
            :param operation_id: The operation identifier corresponding to this CLI command.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.operation``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.operation``.
            :type  options: :class:`list` of :class:`Command.OptionInfo`
            :param options: The input for this command.
            :type  formatter: :class:`Command.FormatterType` or ``None``
            :param formatter: The formatter to use when displaying the output of this command.
                If not present, client can choose a default output formatter.
            :type  output_field_list: :class:`list` of :class:`Command.OutputInfo`
            :param output_field_list: List of output structure name and output field info.
            """
            self.identity = identity
            self.description = description
            self.service_id = service_id
            self.operation_id = operation_id
            self.options = options
            self.formatter = formatter
            self.output_field_list = output_field_list
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vapi.metadata.cli.command.info', {
            'identity': type.ReferenceType(__name__, 'Command.Identity'),
            'description': type.StringType(),
            'service_id': type.IdType(resource_types='com.vmware.vapi.service'),
            'operation_id': type.IdType(resource_types='com.vmware.vapi.operation'),
            'options': type.ListType(type.ReferenceType(__name__, 'Command.OptionInfo')),
            'formatter': type.OptionalType(type.ReferenceType(__name__, 'Command.FormatterType')),
            'output_field_list': type.ListType(type.ReferenceType(__name__, 'Command.OutputInfo')),
        },
        Info,
        False,
        None))



    def list(self,
             path=None,
             ):
        """
        Returns the identifiers of all commands, or commands in a specific
        namespace.

        :type  path: :class:`str` or ``None``
        :param path: The dot-separated path of the namespace for which command
            identifiers should be returned.
            If None identifiers of all commands registered with the
            infrastructure will be returned.
        :rtype: :class:`list` of :class:`Command.Identity`
        :return: Identifiers of the requested commands.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if a namespace corresponding to ``path`` doesn't exist.
        """
        return self._invoke('list',
                            {
                            'path': path,
                            })

    def get(self,
            identity,
            ):
        """
        Retrieves information about a command including information about how
        to execute that command.

        :type  identity: :class:`Command.Identity`
        :param identity: Identifier of the command for which to retreive information.
        :rtype: :class:`Command.Info`
        :return: Information about the command including information about how to
            execute that command.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if a command corresponding to ``identity`` doesn't exist.
        """
        return self._invoke('get',
                            {
                            'identity': identity,
                            })

    def fingerprint(self):
        """
        Returns the aggregate fingerprint of all the command metadata from all
        the metadata sources. 
        
        The fingerprint provides clients an efficient way to check if the
        metadata for commands has been modified on the server.


        :rtype: :class:`str`
        :return: Fingerprint of all the command metadata present on the server.
        """
        return self._invoke('fingerprint', None)
class Namespace(VapiInterface):
    """
    The ``Namespace`` class provides methods to get information about command
    line interface (CLI) namespaces.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vapi.metadata.cli.namespace'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NamespaceStub)
        self._VAPI_OPERATION_IDS = {}

    class Identity(VapiStruct):
        """
        The ``Namespace.Identity`` class uniquely identifies a namespace in the CLI
        namespace tree.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     path=None,
                     name=None,
                    ):
            """
            :type  path: :class:`str`
            :param path: The dot-separated path of the namespace containing the namespace in
                the CLI node tree. For top-level namespace this will be empty.
            :type  name: :class:`str`
            :param name: The name displayed to the user for this namespace.
            """
            self.path = path
            self.name = name
            VapiStruct.__init__(self)


    Identity._set_binding_type(type.StructType(
        'com.vmware.vapi.metadata.cli.namespace.identity', {
            'path': type.StringType(),
            'name': type.StringType(),
        },
        Identity,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Namespace.Info`` class contains information about a namespace. It
        includes the identity of the namespace, a description, information children
        namespaces.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     identity=None,
                     description=None,
                     children=None,
                    ):
            """
            :type  identity: :class:`Namespace.Identity`
            :param identity: Basic namespace identity.
            :type  description: :class:`str`
            :param description: The text description displayed to the user in help output.
            :type  children: :class:`list` of :class:`Namespace.Identity`
            :param children: The children of this namespace in the tree of CLI namespaces.
            """
            self.identity = identity
            self.description = description
            self.children = children
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vapi.metadata.cli.namespace.info', {
            'identity': type.ReferenceType(__name__, 'Namespace.Identity'),
            'description': type.StringType(),
            'children': type.ListType(type.ReferenceType(__name__, 'Namespace.Identity')),
        },
        Info,
        False,
        None))



    def list(self):
        """
        Returns the identifiers of all namespaces registered with the
        infrastructure.


        :rtype: :class:`list` of :class:`Namespace.Identity`
        :return: Identifiers of all the namespaces.
        """
        return self._invoke('list', None)

    def get(self,
            identity,
            ):
        """
        Retreives information about a namespace including information about
        children of that namespace.

        :type  identity: :class:`Namespace.Identity`
        :param identity: Identifier of the namespace for which to retreive information.
        :rtype: :class:`Namespace.Info`
        :return: Information about the namespace including information about child
            of that namespace.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if a namespace corresponding to ``identity`` doesn't exist.
        """
        return self._invoke('get',
                            {
                            'identity': identity,
                            })

    def fingerprint(self):
        """
        Returns the aggregate fingerprint of all the namespace metadata from
        all the metadata sources. 
        
        The fingerprint provides clients an efficient way to check if the
        metadata for namespaces has been modified on the server.


        :rtype: :class:`str`
        :return: Fingerprint of all the namespace metadata present on the server.
        """
        return self._invoke('fingerprint', None)
class _CommandStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'path': type.OptionalType(type.StringType()),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vapi/metadata/cli/command',
            path_variables={
            },
            query_parameters={
                'path': 'path',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'identity': type.ReferenceType(__name__, 'Command.Identity'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vapi/metadata/cli/command',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'get',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for fingerprint operation
        fingerprint_input_type = type.StructType('operation-input', {})
        fingerprint_error_dict = {}
        fingerprint_input_value_validator_list = [
        ]
        fingerprint_output_validator_list = [
        ]
        fingerprint_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vapi/metadata/cli/command/fingerprint',
            path_variables={
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Command.Identity')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Command.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'fingerprint': {
                'input_type': fingerprint_input_type,
                'output_type': type.StringType(),
                'errors': fingerprint_error_dict,
                'input_value_validator_list': fingerprint_input_value_validator_list,
                'output_validator_list': fingerprint_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'fingerprint': fingerprint_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vapi.metadata.cli.command',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _NamespaceStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {}
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vapi/metadata/cli/namespace',
            path_variables={
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'identity': type.ReferenceType(__name__, 'Namespace.Identity'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vapi/metadata/cli/namespace',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'get',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for fingerprint operation
        fingerprint_input_type = type.StructType('operation-input', {})
        fingerprint_error_dict = {}
        fingerprint_input_value_validator_list = [
        ]
        fingerprint_output_validator_list = [
        ]
        fingerprint_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vapi/metadata/cli/namespace/fingerprint',
            path_variables={
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Namespace.Identity')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Namespace.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'fingerprint': {
                'input_type': fingerprint_input_type,
                'output_type': type.StringType(),
                'errors': fingerprint_error_dict,
                'input_value_validator_list': fingerprint_input_value_validator_list,
                'output_validator_list': fingerprint_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'fingerprint': fingerprint_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vapi.metadata.cli.namespace',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Command': Command,
        'Namespace': Namespace,
    }

