# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.vm.guest.filesystem.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.vm.guest.filesystem_client`` module provides classes
for dealing with the filesystem of the guest operating system.

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

class ErrorReason(Enum):
    """
    The ``ErrorReason`` class defines the reasons a file or directory operation
    failed. This enumeration was added in vSphere API 7.0.2.0.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    NOT_A_FILE = None
    """
    An argument is not a file. This class attribute was added in vSphere API
    7.0.2.0.

    """
    NOT_A_DIRECTORY = None
    """
    The argument is not a directory. This class attribute was added in vSphere
    API 7.0.2.0.

    """
    PATH_TOO_LONG = None
    """
    The file path is too long. This class attribute was added in vSphere API
    7.0.2.0.

    """
    FILE_NOT_FOUND = None
    """
    The file is not found. This class attribute was added in vSphere API
    7.0.2.0.

    """
    FILE_TOO_LARGE = None
    """
    The file is too large. This class attribute was added in vSphere API
    7.0.2.0.

    """
    NO_DISK_SPACE = None
    """
    There is insufficent disk space. This class attribute was added in vSphere
    API 7.0.2.0.

    """
    DIRECTORY_NOT_EMPTY = None
    """
    Directory not empty. This class attribute was added in vSphere API 7.0.2.0.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`ErrorReason` instance.
        """
        Enum.__init__(string)

ErrorReason._set_values({
    'NOT_A_FILE': ErrorReason('NOT_A_FILE'),
    'NOT_A_DIRECTORY': ErrorReason('NOT_A_DIRECTORY'),
    'PATH_TOO_LONG': ErrorReason('PATH_TOO_LONG'),
    'FILE_NOT_FOUND': ErrorReason('FILE_NOT_FOUND'),
    'FILE_TOO_LARGE': ErrorReason('FILE_TOO_LARGE'),
    'NO_DISK_SPACE': ErrorReason('NO_DISK_SPACE'),
    'DIRECTORY_NOT_EMPTY': ErrorReason('DIRECTORY_NOT_EMPTY'),
})
ErrorReason._set_binding_type(type.EnumType(
    'com.vmware.vcenter.vm.guest.filesystem.error_reason',
    ErrorReason))




class FileErrorDetails(VapiStruct):
    """
    The ``FileErrorDetails`` class describes additional error information for
    file and directory operations. This class was added in vSphere API 7.0.2.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 reason=None,
                 file_path=None,
                ):
        """
        :type  reason: :class:`ErrorReason`
        :param reason: The reason for the error. This attribute was added in vSphere API
            7.0.2.0.
        :type  file_path: :class:`str`
        :param file_path: The file path associated with the error. This attribute was added
            in vSphere API 7.0.2.0.
        """
        self.reason = reason
        self.file_path = file_path
        VapiStruct.__init__(self)


FileErrorDetails._set_binding_type(type.StructType(
    'com.vmware.vcenter.vm.guest.filesystem.file_error_details', {
        'reason': type.ReferenceType(__name__, 'ErrorReason'),
        'file_path': type.StringType(),
    },
    FileErrorDetails,
    False,
    None))



class Directories(VapiInterface):
    """
    The ``Directories`` class provides methods to manage directories in the
    guest filesystem. This class was added in vSphere API 7.0.2.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.filesystem.directories'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DirectoriesStub)
        self._VAPI_OPERATION_IDS = {}


    def create(self,
               vm,
               credentials,
               path,
               create_parents=None,
               ):
        """
        Creates a directory in the guest operating system. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  path: :class:`str`
        :param path: The complete path to the directory to be created.
        :type  create_parents: :class:`bool` or ``None``
        :param create_parents: Whether any parent directories should be created. If any failure
            occurs, some parent directories could be left behind.
            If None parent directories are not created.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if ``path`` already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``path`` does not exist and ``create_parents`` is not set. The
            value of :attr:`com.vmware.vapi.std.errors_client.Error.data` will
            contain all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be created because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('create',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'path': path,
                            'create_parents': create_parents,
                            })

    def delete(self,
               vm,
               credentials,
               path,
               recursive=None,
               ):
        """
        Deletes a directory in the guest operating system. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  path: :class:`str`
        :param path: The complete path to the directory to be deleted.
        :type  recursive: :class:`bool` or ``None``
        :param recursive: If true, all files and subdirectories are also deleted. If false,
            the directory must be empty for the operation to succeed.
            If None, any directory content is not deleted.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is not a directory. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``path`` is not found. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInUse` 
            if ``path`` has content and ``recursive`` is None.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be deleted because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('delete',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'path': path,
                            'recursive': recursive,
                            })

    def move(self,
             vm,
             credentials,
             path,
             new_path,
             ):
        """
        Renames a directory in the guest. 
        
        Renames the directory, or copies and deletes the old contents as
        required by the underlying filsystem. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  path: :class:`str`
        :param path: The complete path to the directory to be moved.
        :type  new_path: :class:`str`
        :param new_path: The complete path to where the directory is moved or its new name.
            It cannot be a path to an existing directory or an existing file.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if ``new_path`` already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is not a directory. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``new_path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``path`` is not found. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the parent directory of ``new_path`` does not exist. The value
            of :attr:`com.vmware.vapi.std.errors_client.Error.data` will
            contain all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if a path cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if a path cannot be renamed or moved because the guest
            authentication will not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('move',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'path': path,
                            'new_path': new_path,
                            })

    def create_temporary(self,
                         vm,
                         credentials,
                         prefix,
                         suffix,
                         parent_path=None,
                         ):
        """
        Creates a temporary directory. 
        
        Creates a new unique temporary directory for the user to use as needed.
        The guest operating system may clean up the directory after a guest
        specific amount of time if ``parent_path`` is not set, or the user can
        remove the directory when no longer needed. 
        
        The new directory name will be created in a guest-specific format using
        ``prefix``, a guest generated string and ``suffix`` in ``parent_path``.
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  prefix: :class:`str`
        :param prefix: The prefix to be given to the new temporary directory.
        :type  suffix: :class:`str`
        :param suffix: The suffix to be given to the new temporary directory.
        :type  parent_path: :class:`str` or ``None``
        :param parent_path: The complete path to the directory in which to create the new
            directory.
            Directory If None a guest-specific default will be used.
        :rtype: :class:`str`
        :return: The absolute path of the temporary directory that is created.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``parent_path`` is not a directory. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``parent_path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``parent_path`` is :class:`set` and does not exist. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``parent_path`` cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if a file cannot be created because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('create_temporary',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'prefix': prefix,
                            'suffix': suffix,
                            'parent_path': parent_path,
                            })
class Files(VapiInterface):
    """
    The ``Files`` class provides methods to manage the files in the guest
    filesystem. This class was added in vSphere API 7.0.2.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.filesystem.files'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _FilesStub)
        self._VAPI_OPERATION_IDS = {}

    class FilesystemFamily(Enum):
        """
        The ``Files.FilesystemFamily`` class defines the types of guest operating
        fllesystem. This enumeration was added in vSphere API 7.0.2.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        WINDOWS = None
        """
        The guest OS is a Windows variant. This class attribute was added in
        vSphere API 7.0.2.0.

        """
        POSIX = None
        """
        Linux, Solaris, etc. This class attribute was added in vSphere API 7.0.2.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`FilesystemFamily` instance.
            """
            Enum.__init__(string)

    FilesystemFamily._set_values({
        'WINDOWS': FilesystemFamily('WINDOWS'),
        'POSIX': FilesystemFamily('POSIX'),
    })
    FilesystemFamily._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vm.guest.filesystem.files.filesystem_family',
        FilesystemFamily))


    class Type(Enum):
        """
        The ``Files.Type`` class defines the valid types of files. This enumeration
        was added in vSphere API 7.0.2.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        FILE = None
        """
        normal file. This class attribute was added in vSphere API 7.0.2.0.

        """
        DIRECTORY = None
        """
        directory. This class attribute was added in vSphere API 7.0.2.0.

        """
        SYMLINK = None
        """
        symbolic link. This class attribute was added in vSphere API 7.0.2.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'FILE': Type('FILE'),
        'DIRECTORY': Type('DIRECTORY'),
        'SYMLINK': Type('SYMLINK'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vm.guest.filesystem.files.type',
        Type))


    class LastIterationStatus(Enum):
        """
        The last status for the iterator. A field of this type is returned as part
        of the result and indicates to the caller of the API whether it can
        continue to make requests for more data. The last status only reports on
        the state of the iteration at the time data was last returned. As a result,
        it not does guarantee if the next call will succeed in getting more data or
        not. Failures to retrieve results will be returned as Error responses.
        These last statuses are only returned when the iterator is operating as
        expected. This enumeration was added in vSphere API 7.0.2.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        READY = None
        """
        Iterator has more data pending and is ready to provide it. The caller can
        request the next page of data at any time. The number of results returned
        may be less than the requested size. In other words, the iterator may not
        fill the page. The iterator has returned at least 1 result. This class
        attribute was added in vSphere API 7.0.2.0.

        """
        END_OF_DATA = None
        """
        Iterator has finished iterating through its inventory. There are currently
        no more entities to return and the caller can terminate iteration. If the
        iterator returned some data, the marker may be set to allow the iterator to
        continue from where it left off when additional data does become available.
        This value is used to indicate that all available data has been returned by
        the iterator. This class attribute was added in vSphere API 7.0.2.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`LastIterationStatus` instance.
            """
            Enum.__init__(string)

    LastIterationStatus._set_values({
        'READY': LastIterationStatus('READY'),
        'END_OF_DATA': LastIterationStatus('END_OF_DATA'),
    })
    LastIterationStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vm.guest.filesystem.files.last_iteration_status',
        LastIterationStatus))


    class WindowsFileAttributesInfo(VapiStruct):
        """
        The {\\\\@name WindowsFileAttributesInfo) {\\\\@term structure} describes
        file attributes specific to Windows Guest operating systems. This class was
        added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hidden=None,
                     read_only=None,
                     created=None,
                    ):
            """
            :type  hidden: :class:`bool`
            :param hidden: The file is hidden. This attribute was added in vSphere API
                7.0.2.0.
            :type  read_only: :class:`bool`
            :param read_only: The file is read-only. This attribute was added in vSphere API
                7.0.2.0.
            :type  created: :class:`datetime.datetime`
            :param created: The date and time the file was created. This attribute was added in
                vSphere API 7.0.2.0.
            """
            self.hidden = hidden
            self.read_only = read_only
            self.created = created
            VapiStruct.__init__(self)


    WindowsFileAttributesInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.windows_file_attributes_info', {
            'hidden': type.BooleanType(),
            'read_only': type.BooleanType(),
            'created': type.DateTimeType(),
        },
        WindowsFileAttributesInfo,
        False,
        None))


    class PosixFileAttributesInfo(VapiStruct):
        """
        The ``Files.PosixFileAttributesInfo`` class describes information about
        file attributes specific to Posix Guest operating systems. This class was
        added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     owner=None,
                     group=None,
                     permissions=None,
                    ):
            """
            :type  owner: :class:`long`
            :param owner: The owner ID. This attribute was added in vSphere API 7.0.2.0.
            :type  group: :class:`long`
            :param group: The group ID. This attribute was added in vSphere API 7.0.2.0.
            :type  permissions: :class:`str`
            :param permissions: The file permissions in chmod(2) format. This attribute is
                presented as octal. This attribute was added in vSphere API
                7.0.2.0.
            """
            self.owner = owner
            self.group = group
            self.permissions = permissions
            VapiStruct.__init__(self)


    PosixFileAttributesInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.posix_file_attributes_info', {
            'owner': type.IntegerType(),
            'group': type.IntegerType(),
            'permissions': type.StringType(),
        },
        PosixFileAttributesInfo,
        False,
        None))


    class FileAttributesInfo(VapiStruct):
        """
        The ``Files.FileAttributesInfo`` class describes the attributes of a file
        in a guest operating system. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'filesystem_family',
                {
                    'WINDOWS' : [('win_attributes', True)],
                    'POSIX' : [('posix_attributes', True)],
                }
            ),
        ]



        def __init__(self,
                     last_modified=None,
                     last_accessed=None,
                     symlink_target=None,
                     filesystem_family=None,
                     win_attributes=None,
                     posix_attributes=None,
                    ):
            """
            :type  last_modified: :class:`datetime.datetime`
            :param last_modified: The date and time the file was last modified. This attribute was
                added in vSphere API 7.0.2.0.
            :type  last_accessed: :class:`datetime.datetime`
            :param last_accessed: The date and time the file was last accessed. This attribute was
                added in vSphere API 7.0.2.0.
            :type  symlink_target: :class:`str` or ``None``
            :param symlink_target: The target for the file if it's a symbolic link. This is currently
                only set for Posix guest operating systems, but may be supported in
                the future on Windows guest operating systems that support symbolic
                links. This attribute was added in vSphere API 7.0.2.0.
                Set if the file is a symbolic link.
            :type  filesystem_family: :class:`Files.FilesystemFamily`
            :param filesystem_family: The type of guest filesystem. This attribute was added in vSphere
                API 7.0.2.0.
            :type  win_attributes: :class:`Files.WindowsFileAttributesInfo`
            :param win_attributes: Windows-specific file information. This attribute was added in
                vSphere API 7.0.2.0.
                This attribute is optional and it is only relevant when the value
                of ``filesystemFamily`` is :attr:`Files.FilesystemFamily.WINDOWS`.
            :type  posix_attributes: :class:`Files.PosixFileAttributesInfo`
            :param posix_attributes: Posix-specific file information. This attribute was added in
                vSphere API 7.0.2.0.
                This attribute is optional and it is only relevant when the value
                of ``filesystemFamily`` is :attr:`Files.FilesystemFamily.POSIX`.
            """
            self.last_modified = last_modified
            self.last_accessed = last_accessed
            self.symlink_target = symlink_target
            self.filesystem_family = filesystem_family
            self.win_attributes = win_attributes
            self.posix_attributes = posix_attributes
            VapiStruct.__init__(self)


    FileAttributesInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.file_attributes_info', {
            'last_modified': type.DateTimeType(),
            'last_accessed': type.DateTimeType(),
            'symlink_target': type.OptionalType(type.StringType()),
            'filesystem_family': type.ReferenceType(__name__, 'Files.FilesystemFamily'),
            'win_attributes': type.OptionalType(type.ReferenceType(__name__, 'Files.WindowsFileAttributesInfo')),
            'posix_attributes': type.OptionalType(type.ReferenceType(__name__, 'Files.PosixFileAttributesInfo')),
        },
        FileAttributesInfo,
        False,
        None))


    class WindowsFileAttributesUpdateSpec(VapiStruct):
        """
        The ``Files.WindowsFileAttributesUpdateSpec`` class describes attributes
        that can be changed for a Windows file. This class was added in vSphere API
        7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hidden=None,
                     read_only=None,
                    ):
            """
            :type  hidden: :class:`bool` or ``None``
            :param hidden: The file is hidden. This attribute was added in vSphere API
                7.0.2.0.
                If {term unset} the value will not be changed.
            :type  read_only: :class:`bool` or ``None``
            :param read_only: The file is read-only. This attribute was added in vSphere API
                7.0.2.0.
                If {term unset} the value will not be changed.
            """
            self.hidden = hidden
            self.read_only = read_only
            VapiStruct.__init__(self)


    WindowsFileAttributesUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.windows_file_attributes_update_spec', {
            'hidden': type.OptionalType(type.BooleanType()),
            'read_only': type.OptionalType(type.BooleanType()),
        },
        WindowsFileAttributesUpdateSpec,
        False,
        None))


    class PosixFileAttributesUpdateSpec(VapiStruct):
        """
        The ``Files.PosixFileAttributesUpdateSpec`` class describes attributes that
        can be changed for a Posix file. This class was added in vSphere API
        7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     owner_id=None,
                     group_id=None,
                     permissions=None,
                    ):
            """
            :type  owner_id: :class:`long` or ``None``
            :param owner_id: The owner ID. This attribute was added in vSphere API 7.0.2.0.
                If None the value will not be changed.
            :type  group_id: :class:`long` or ``None``
            :param group_id: The group ID. This attribute was added in vSphere API 7.0.2.0.
                If None the value will not be changed.
            :type  permissions: :class:`str` or ``None``
            :param permissions: The file permissions in chmod(2) format. This attribute is
                interpreted as octal. This attribute was added in vSphere API
                7.0.2.0.
                If None the value will not be changed.
            """
            self.owner_id = owner_id
            self.group_id = group_id
            self.permissions = permissions
            VapiStruct.__init__(self)


    PosixFileAttributesUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.posix_file_attributes_update_spec', {
            'owner_id': type.OptionalType(type.IntegerType()),
            'group_id': type.OptionalType(type.IntegerType()),
            'permissions': type.OptionalType(type.StringType()),
        },
        PosixFileAttributesUpdateSpec,
        False,
        None))


    class FileAttributesUpdateSpec(VapiStruct):
        """
        File attributes used for updating an existing file with
        :func:`Files.update`. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     last_modified=None,
                     last_accessed=None,
                     windows=None,
                     posix=None,
                    ):
            """
            :type  last_modified: :class:`datetime.datetime` or ``None``
            :param last_modified: The date and time the file was last modified. This attribute was
                added in vSphere API 7.0.2.0.
                If None the value will not be changed.
            :type  last_accessed: :class:`datetime.datetime` or ``None``
            :param last_accessed: The date and time the file was last accessed. This attribute was
                added in vSphere API 7.0.2.0.
                If None the value will not be changed.
            :type  windows: :class:`Files.WindowsFileAttributesUpdateSpec` or ``None``
            :param windows: Windows-specific file update information. This attribute was added
                in vSphere API 7.0.2.0.
                Set if the guest operating system is Windows.
            :type  posix: :class:`Files.PosixFileAttributesUpdateSpec` or ``None``
            :param posix: Posix-specific file update information. This attribute was added in
                vSphere API 7.0.2.0.
                Set if the guest operating system is Posix.
            """
            self.last_modified = last_modified
            self.last_accessed = last_accessed
            self.windows = windows
            self.posix = posix
            VapiStruct.__init__(self)


    FileAttributesUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.file_attributes_update_spec', {
            'last_modified': type.OptionalType(type.DateTimeType()),
            'last_accessed': type.OptionalType(type.DateTimeType()),
            'windows': type.OptionalType(type.ReferenceType(__name__, 'Files.WindowsFileAttributesUpdateSpec')),
            'posix': type.OptionalType(type.ReferenceType(__name__, 'Files.PosixFileAttributesUpdateSpec')),
        },
        FileAttributesUpdateSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Files.Info`` class describes a file or directory in the guest
        operating system. Returned by :func:`Files.get`. This class was added in
        vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                     size=None,
                     attributes=None,
                    ):
            """
            :type  type: :class:`Files.Type`
            :param type: The type of file. This attribute was added in vSphere API 7.0.2.0.
            :type  size: :class:`long`
            :param size: The file size in bytes. This attribute was added in vSphere API
                7.0.2.0.
            :type  attributes: :class:`Files.FileAttributesInfo`
            :param attributes: Attributes of a file. This attribute was added in vSphere API
                7.0.2.0.
            """
            self.type = type
            self.size = size
            self.attributes = attributes
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.info', {
            'type': type.ReferenceType(__name__, 'Files.Type'),
            'size': type.IntegerType(),
            'attributes': type.ReferenceType(__name__, 'Files.FileAttributesInfo'),
        },
        Info,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Files.Summary`` class describes a file or directory in the guest
        operating system returned by a :func:`Files.list` method. This class was
        added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     filename=None,
                     type=None,
                     size=None,
                    ):
            """
            :type  filename: :class:`str`
            :param filename: The name of the file or directory with any leading directories
                removed. This attribute was added in vSphere API 7.0.2.0.
            :type  type: :class:`Files.Type`
            :param type: The type of file. This attribute was added in vSphere API 7.0.2.0.
            :type  size: :class:`long`
            :param size: The file size in bytes. This attribute was added in vSphere API
                7.0.2.0.
            """
            self.filename = filename
            self.type = type
            self.size = size
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.summary', {
            'filename': type.StringType(),
            'type': type.ReferenceType(__name__, 'Files.Type'),
            'size': type.IntegerType(),
        },
        Summary,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Files.IterationSpec`` class contains attributes used to break results
        into pages when listing files. See :func:`Files.list`). This class was
        added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     size=None,
                     index=None,
                    ):
            """
            :type  size: :class:`long` or ``None``
            :param size: Specifies the maximum number of results to return. This attribute
                was added in vSphere API 7.0.2.0.
                If None information about at most 50 files will be returned.
            :type  index: :class:`long` or ``None``
            :param index: Which result to start the list with. If this value exceeds the
                number of results, an empty list will be returned. This attribute
                was added in vSphere API 7.0.2.0.
                If None, the start of the list of files will be returned.
            """
            self.size = size
            self.index = index
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.iteration_spec', {
            'size': type.OptionalType(type.IntegerType()),
            'index': type.OptionalType(type.IntegerType()),
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Files.FilterSpec`` class contains information used to filter the
        results when listing files (see :func:`Files.list`). This class was added
        in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     match_pattern=None,
                    ):
            """
            :type  match_pattern: :class:`str` or ``None``
            :param match_pattern: The perl-compatible regular expression used to filter the returned
                files. This attribute was added in vSphere API 7.0.2.0.
                If None the pattern **'.\*'** (match everything) is used.
            """
            self.match_pattern = match_pattern
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.filter_spec', {
            'match_pattern': type.OptionalType(type.StringType()),
        },
        FilterSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Files.ListResult`` class describes the results of a
        :func:`Files.list` method. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     files=None,
                     total=None,
                     start_index=None,
                     end_index=None,
                     status=None,
                    ):
            """
            :type  files: :class:`list` of :class:`Files.Summary`
            :param files: A list of :class:`Files.Summary` classes containing information for
                all the matching files. This attribute was added in vSphere API
                7.0.2.0.
            :type  total: :class:`long`
            :param total: The total number of results from the :func:`Files.list`. This is a
                hint to the user of the iterator regarding how many items are
                available to be retrieved. The total could change if the inventory
                of items are being changed. This attribute was added in vSphere API
                7.0.2.0.
            :type  start_index: :class:`long` or ``None``
            :param start_index: Positional index into the logical item list of the first item
                returned in the list of results. The first item in the logical item
                list has an index of 0. This is a hint to the user of the iterator
                regarding the logical position in the iteration. For example, this
                can be used to display to the user which page of the iteration is
                being shown. The total could change if the inventory of items are
                being changed. This attribute was added in vSphere API 7.0.2.0.
                If None no items were returned.
            :type  end_index: :class:`long` or ``None``
            :param end_index: Positional index into the logical item list of the last item
                returned in the list of results. The first item in the logical item
                list has an index of 0. This is a hint to the user of the iterator
                regarding the logical position in the iteration. For example, this
                can be used to display to the user which page of the iteration is
                being shown. The total could change if the inventory of items are
                being changed. This attribute was added in vSphere API 7.0.2.0.
                If None no items were returned.
            :type  status: :class:`Files.LastIterationStatus`
            :param status: The last status for the iterator that indicates whether any more
                results can be expected if the caller continues to make requests
                for more data using the iterator. This attribute was added in
                vSphere API 7.0.2.0.
            """
            self.files = files
            self.total = total
            self.start_index = start_index
            self.end_index = end_index
            self.status = status
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.files.list_result', {
            'files': type.ListType(type.ReferenceType(__name__, 'Files.Summary')),
            'total': type.IntegerType(),
            'start_index': type.OptionalType(type.IntegerType()),
            'end_index': type.OptionalType(type.IntegerType()),
            'status': type.ReferenceType(__name__, 'Files.LastIterationStatus'),
        },
        ListResult,
        False,
        None))



    def move(self,
             vm,
             credentials,
             path,
             new_path,
             overwrite=None,
             ):
        """
        Renames a file in the guest. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  path: :class:`str`
        :param path: The complete path to the original file or symbolic link to be
            moved.
        :type  new_path: :class:`str`
        :param new_path: The complete path to the new file. It cannot be a path to an
            existing directory.
        :type  overwrite: :class:`bool` or ``None``
        :param overwrite: If true, the destination file is overwritten.
            If None, the destination file is not overwritten.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if the ``new_path`` already exists and ``overwrite`` is false.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is not a file. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``new_path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``path`` does not exist. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the parent directory of ``new_path`` does not exist. The value
            of :attr:`com.vmware.vapi.std.errors_client.Error.data` will
            contain all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if a path cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if a path cannot be renamed because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('move',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'path': path,
                            'new_path': new_path,
                            'overwrite': overwrite,
                            })

    def update(self,
               vm,
               credentials,
               path,
               file_attributes,
               ):
        """
        Changes the file attributes of a specified file or directory inside the
        guest. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  path: :class:`str`
        :param path: The complete path to the file or directory to be changed in the
            guest. If the file points to an symbolic link, then the attributes
            of the target file are changed.
        :type  file_attributes: :class:`Files.FileAttributesUpdateSpec`
        :param file_attributes: Specifies the different file attributes of the guest file to be
            changed. See :class:`Files.FileAttributesUpdateSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``file_attributes`` does not apply to the guest operating
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is not a file. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``path`` is not found. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be updated because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('update',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'path': path,
                            'file_attributes': file_attributes,
                            })

    def delete(self,
               vm,
               credentials,
               path,
               ):
        """
        Deletes a file in the guest operating system 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  path: :class:`str`
        :param path: The complete path to the file or symbolic link to be deleted.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is not a file. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``path`` is not found. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be deleted because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('delete',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'path': path,
                            })

    def get(self,
            vm,
            credentials,
            path,
            ):
        """
        Returns information about a file or directory in the guest. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  path: :class:`str`
        :param path: The complete path to the file.
        :rtype: :class:`Files.Info`
        :return: :class:`Files.Info` object containing information for the file.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``path`` is not found. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be listed because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Query``.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'path': path,
                            })

    def create_temporary(self,
                         vm,
                         credentials,
                         prefix,
                         suffix,
                         parent_path=None,
                         ):
        """
        Creates a temporary file. 
        
        Creates a new unique temporary file for the user to use as needed. The
        user is responsible for removing it when it is no longer needed. 
        
        The new file name will be created in a guest-specific format using
        ``prefix``, a guest generated string and ``suffix`` in ``parent_path``.
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  prefix: :class:`str`
        :param prefix: The prefix to be given to the new temporary file.
        :type  suffix: :class:`str`
        :param suffix: The suffix to be given to the new temporary file.
        :type  parent_path: :class:`str` or ``None``
        :param parent_path: The complete path to the directory in which to create the file.
            Directory to use if specified, otherwise a guest-specific default
            will be used.
        :rtype: :class:`str`
        :return: The absolute path of the temporary file that is created.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``parent_path`` is :class:`set` and is not a directory. The
            value of :attr:`com.vmware.vapi.std.errors_client.Error.data` will
            contain all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``parent_path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``parent_path`` is :class:`set` and does not exist. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``parent_path`` cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if a file cannot be created because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('create_temporary',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'prefix': prefix,
                            'suffix': suffix,
                            'parent_path': parent_path,
                            })

    def list(self,
             vm,
             credentials,
             path,
             iteration=None,
             filter=None,
             ):
        """
        Returns information about files and directories in the guest. 
        
        Files are returned in operating system-specific (inode) order. If the
        directory is modified between queries, missing or duplicate results can
        occur. 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication data.
        :type  path: :class:`str`
        :param path: The complete path to the directory or file to query.
        :type  iteration: :class:`Files.IterationSpec` or ``None``
        :param iteration: The specification of a page of results to be retrieved.
            If None, the first page will be retrieved.
        :type  filter: :class:`Files.FilterSpec` or ``None``
        :param filter: Specification to match files for which information should be
            returned.
            If None, the behavior is the equivalent to a
            :class:`Files.FilterSpec` with all attributes None which means all
            filenames match the filter.
        :rtype: :class:`Files.ListResult`
        :return: A :class:`Files.ListResult` object containing information for all
            the matching files in ``filter`` and the total number of files that
            can be returned.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``path`` is too long. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``path`` is not found. The value of
            :attr:`com.vmware.vapi.std.errors_client.Error.data` will contain
            all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if ``path`` cannot be listed because the guest authentication will
            not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest
            operating system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Query``.
        """
        return self._invoke('list',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'path': path,
                            'iteration': iteration,
                            'filter': filter,
                            })
class Transfers(VapiInterface):
    """
    The ``Transfers`` class provides methods to copy files into and out of the
    guest file system. This class was added in vSphere API 7.0.2.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vm.guest.filesystem.transfers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TransfersStub)
        self._VAPI_OPERATION_IDS = {}

    class WindowsFileAttributesCreateSpec(VapiStruct):
        """
        The ``Transfers.WindowsFileAttributesCreateSpec`` class describes creation
        information about file attributes specific to Windows guest operating
        systems. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hidden=None,
                     read_only=None,
                    ):
            """
            :type  hidden: :class:`bool` or ``None``
            :param hidden: The file is hidden. This attribute was added in vSphere API
                7.0.2.0.
                If None the file will not be hidden.
            :type  read_only: :class:`bool` or ``None``
            :param read_only: The file is read-only. This attribute was added in vSphere API
                7.0.2.0.
                If None the file will be writeable.
            """
            self.hidden = hidden
            self.read_only = read_only
            VapiStruct.__init__(self)


    WindowsFileAttributesCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.transfers.windows_file_attributes_create_spec', {
            'hidden': type.OptionalType(type.BooleanType()),
            'read_only': type.OptionalType(type.BooleanType()),
        },
        WindowsFileAttributesCreateSpec,
        False,
        None))


    class PosixFileAttributesCreateSpec(VapiStruct):
        """
        The ``Transfers.PosixFileAttributesCreateSpec`` class describes creation
        information about file attributes specific to Posix guest operating
        systems. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     owner_id=None,
                     group_id=None,
                     permissions=None,
                    ):
            """
            :type  owner_id: :class:`long` or ``None``
            :param owner_id: The owner ID. If this property is not specified when passing a
                :class:`Transfers.PosixFileAttributesCreateSpec` object to
                :func:`Transfers.create`, the default value will be the owner Id of
                the user who invoked the file transfer operation. This attribute
                was added in vSphere API 7.0.2.0.
                Defaults to uid of user invoking the operation.
            :type  group_id: :class:`long` or ``None``
            :param group_id: The group ID. If this property is not specified when passing a
                :class:`Transfers.PosixFileAttributesCreateSpec` object to
                :func:`Transfers.create`, the default value will be the group Id of
                the user who invoked the file transfer operation. This attribute
                was added in vSphere API 7.0.2.0.
                Defaults to gid of user invoking the operation.
            :type  permissions: :class:`str` or ``None``
            :param permissions: The file permissions in chmod(2) format. If this property is not
                specified when passing a
                :class:`Transfers.PosixFileAttributesCreateSpec` object to
                :func:`Transfers.create`, the file will be created with 0644
                permissions. This attribute is interpreted as octal. This attribute
                was added in vSphere API 7.0.2.0.
                Defaults to 0644.
            """
            self.owner_id = owner_id
            self.group_id = group_id
            self.permissions = permissions
            VapiStruct.__init__(self)


    PosixFileAttributesCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.transfers.posix_file_attributes_create_spec', {
            'owner_id': type.OptionalType(type.IntegerType()),
            'group_id': type.OptionalType(type.IntegerType()),
            'permissions': type.OptionalType(type.StringType()),
        },
        PosixFileAttributesCreateSpec,
        False,
        None))


    class FileCreationAttributes(VapiStruct):
        """
        The ``Transfers.FileCreationAttributes`` class describes file attributes
        used when transferring a file into the guest. This class was added in
        vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     size=None,
                     overwrite=None,
                     last_modified=None,
                     last_accessed=None,
                     windows=None,
                     posix=None,
                    ):
            """
            :type  size: :class:`long`
            :param size: The size in bytes of the file to be transferred into the guest.
                This attribute was added in vSphere API 7.0.2.0.
            :type  overwrite: :class:`bool` or ``None``
            :param overwrite: Whether an existing file should be overwritten. This attribute was
                added in vSphere API 7.0.2.0.
                If None any existing file will not be overwritten.
            :type  last_modified: :class:`datetime.datetime` or ``None``
            :param last_modified: The date and time the file was last modified. This attribute was
                added in vSphere API 7.0.2.0.
                If None the value will be the time when the file is transferred
                into the guest.
            :type  last_accessed: :class:`datetime.datetime` or ``None``
            :param last_accessed: The date and time the file was last accessed. This attribute was
                added in vSphere API 7.0.2.0.
                If None the value will be the time when the file is transferred
                into the guest.
            :type  windows: :class:`Transfers.WindowsFileAttributesCreateSpec` or ``None``
            :param windows: Windows-specific file creation information. This attribute was
                added in vSphere API 7.0.2.0.
                If None, the behavior is equivalent to a
                :class:`Transfers.WindowsFileAttributesCreateSpec` with all
                attributes None which means the defaults are used. May only be
                :class:`set` if the guest operating system is Windows.
            :type  posix: :class:`Transfers.PosixFileAttributesCreateSpec` or ``None``
            :param posix: Posix-specific file creation information. This attribute was added
                in vSphere API 7.0.2.0.
                If None, the behavior is equivalent to a
                :class:`Transfers.PosixFileAttributesCreateSpec` with all
                attributes None which means the defaults are used. May only be
                :class:`set` if the guest operating system is Posix.
            """
            self.size = size
            self.overwrite = overwrite
            self.last_modified = last_modified
            self.last_accessed = last_accessed
            self.windows = windows
            self.posix = posix
            VapiStruct.__init__(self)


    FileCreationAttributes._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.transfers.file_creation_attributes', {
            'size': type.IntegerType(),
            'overwrite': type.OptionalType(type.BooleanType()),
            'last_modified': type.OptionalType(type.DateTimeType()),
            'last_accessed': type.OptionalType(type.DateTimeType()),
            'windows': type.OptionalType(type.ReferenceType(__name__, 'Transfers.WindowsFileAttributesCreateSpec')),
            'posix': type.OptionalType(type.ReferenceType(__name__, 'Transfers.PosixFileAttributesCreateSpec')),
        },
        FileCreationAttributes,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Transfers.CreateSpec`` class describes the details of a file transfer
        operation. This class was added in vSphere API 7.0.2.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     path=None,
                     attributes=None,
                    ):
            """
            :type  path: :class:`str`
            :param path: The complete destination path in the guest to transfer the file to
                or from the client. It cannot be a path to a directory or a
                symbolic link. This attribute was added in vSphere API 7.0.2.0.
            :type  attributes: :class:`Transfers.FileCreationAttributes` or ``None``
            :param attributes: Details about the file to be transferred into the guest. This
                attribute was added in vSphere API 7.0.2.0.
                Must be :class:`set` if the file is being transferred to the guest.
                Must not be :class:`set` if the file is being transferred from the
                guest.
            """
            self.path = path
            self.attributes = attributes
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vm.guest.filesystem.transfers.create_spec', {
            'path': type.StringType(),
            'attributes': type.OptionalType(type.ReferenceType(__name__, 'Transfers.FileCreationAttributes')),
        },
        CreateSpec,
        False,
        None))



    def create(self,
               vm,
               credentials,
               spec,
               ):
        """
        Initiates an operation to transfer a file to or from the guest. 
        
        If the power state of the Virtual Machine is changed when the file
        transfer is in progress, or the Virtual Machine is migrated, then the
        transfer operation is aborted. 
        
        When transferring a file into the guest and overwriting an existing
        file, the old file attributes are not preserved. 
        
        In order to ensure a secure connection to the host when transferring a
        file using HTTPS, the X.509 certificate for the host must be used to
        authenticate the remote end of the connection. The certificate of the
        host that the virtual machine is running on can be retrieved using the
        following fields: XXX insert link to certificate in Host config XXX 
        
        . This method was added in vSphere API 7.0.2.0.

        :type  vm: :class:`str`
        :param vm: Virtual Machine to perform the operation on.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  credentials: :class:`com.vmware.vcenter.vm.guest_client.Credentials`
        :param credentials: The guest authentication credentials.
        :type  spec: :class:`Transfers.CreateSpec`
        :param spec: A specification of the type of file transfer and any applicable
            attibutes.
        :rtype: :class:`str`
        :return: The URL to which the user has to send an HTTP request. The URL will
            become invalid once a successful request is sent. If the file is
            being transferred from the guest, an HTTP GET should be used. If
            the file is being transferred to the guest, HTTP PUT should be
            used. 
            The URL is valid only for 10 minutes from the time it is generated.
            The URL becomes invalid whenever the virtual machine is powered
            off, suspended, unregistered or migrated to a new host. The host
            part of the URL is returned as **\*** if the hostname to be used is
            the name of the server to which the call was made. For example, if
            the call is made to **esx-svr-1.domain1.com**, and the file is
            available for download from
            https://esx-svr-1.domain1.com/guestFile?id=1&token=1234, the URL
            returned may be https://&#42;/guestFile?id=1&token=1234. The client
            replaces the asterisk with the server name on which it invoked the
            call. 
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if :attr:`Transfers.CreateSpec.path` in ``spec`` exists and
            :attr:`Transfers.FileCreationAttributes.overwrite` is false when
            transferring a file to the guest.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if :attr:`Transfers.CreateSpec.path` in ``spec`` is not a file. The
            value of :attr:`com.vmware.vapi.std.errors_client.Error.data` will
            contain all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if :attr:`Transfers.CreateSpec.path` in ``spec`` is too long. The
            value of :attr:`com.vmware.vapi.std.errors_client.Error.data` will
            contain all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if :attr:`Transfers.CreateSpec.path` in ``spec`` is not found. The
            value of :attr:`com.vmware.vapi.std.errors_client.Error.data` will
            contain all the attributes defined in the :class:`FileErrorDetails`
            providing additional information about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the VMware Tools is not running.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if is insuffcient space for the new file when transferring a file
            to the guest.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the ``credentials`` object was not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if :attr:`Transfers.CreateSpec.path` in ``spec`` cannot be
            accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if :attr:`Transfers.CreateSpec.path` in ``spec`` cannot be copied
            because the guest authentication will not allow the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is not supported by the VMware Tools in the guest
            OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the operation is disabled by the VMware Tools in the guest OS.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.GuestOperations.Modify``.
        """
        return self._invoke('create',
                            {
                            'vm': vm,
                            'credentials': credentials,
                            'spec': spec,
                            })
class _DirectoriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'path': type.StringType(),
            'create_parents': type.OptionalType(type.BooleanType()),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/directories',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'create',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'path': type.StringType(),
            'recursive': type.OptionalType(type.BooleanType()),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.resource_in_use':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/directories',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'delete',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for move operation
        move_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'path': type.StringType(),
            'new_path': type.StringType(),
        })
        move_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        move_input_value_validator_list = [
        ]
        move_output_validator_list = [
        ]
        move_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/directories',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'move',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for create_temporary operation
        create_temporary_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'prefix': type.StringType(),
            'suffix': type.StringType(),
            'parent_path': type.OptionalType(type.StringType()),
        })
        create_temporary_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        create_temporary_input_value_validator_list = [
        ]
        create_temporary_output_validator_list = [
        ]
        create_temporary_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/directories',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'createTemporary',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'create': {
                'input_type': create_input_type,
                'output_type': type.VoidType(),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
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
            'move': {
                'input_type': move_input_type,
                'output_type': type.VoidType(),
                'errors': move_error_dict,
                'input_value_validator_list': move_input_value_validator_list,
                'output_validator_list': move_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_temporary': {
                'input_type': create_temporary_input_type,
                'output_type': type.StringType(),
                'errors': create_temporary_error_dict,
                'input_value_validator_list': create_temporary_input_value_validator_list,
                'output_validator_list': create_temporary_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'move': move_rest_metadata,
            'create_temporary': create_temporary_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.guest.filesystem.directories',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _FilesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for move operation
        move_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'path': type.StringType(),
            'new_path': type.StringType(),
            'overwrite': type.OptionalType(type.BooleanType()),
        })
        move_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        move_input_value_validator_list = [
        ]
        move_output_validator_list = [
        ]
        move_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/files',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'move',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'path': type.StringType(),
            'file_attributes': type.ReferenceType(__name__, 'Files.FileAttributesUpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/files',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'update',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'path': type.StringType(),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/files/{path}',
            path_variables={
                'vm': 'vm',
                'path': 'path',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'delete',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'path': type.StringType(),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/files/{path}',
            path_variables={
                'vm': 'vm',
                'path': 'path',
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

        # properties for create_temporary operation
        create_temporary_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'prefix': type.StringType(),
            'suffix': type.StringType(),
            'parent_path': type.OptionalType(type.StringType()),
        })
        create_temporary_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        create_temporary_input_value_validator_list = [
        ]
        create_temporary_output_validator_list = [
        ]
        create_temporary_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/files',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'createTemporary',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'path': type.StringType(),
            'iteration': type.OptionalType(type.ReferenceType(__name__, 'Files.IterationSpec')),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Files.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
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
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem/files',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'list',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'move': {
                'input_type': move_input_type,
                'output_type': type.VoidType(),
                'errors': move_error_dict,
                'input_value_validator_list': move_input_value_validator_list,
                'output_validator_list': move_output_validator_list,
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
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Files.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_temporary': {
                'input_type': create_temporary_input_type,
                'output_type': type.StringType(),
                'errors': create_temporary_error_dict,
                'input_value_validator_list': create_temporary_input_value_validator_list,
                'output_validator_list': create_temporary_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Files.ListResult'),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'move': move_rest_metadata,
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
            'create_temporary': create_temporary_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.guest.filesystem.files',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _TransfersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'credentials': type.ReferenceType('com.vmware.vcenter.vm.guest_client', 'Credentials'),
            'spec': type.ReferenceType(__name__, 'Transfers.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}/guest/filesystem',
            path_variables={
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'create',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'create': {
                'input_type': create_input_type,
                'output_type': type.URIType(),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vm.guest.filesystem.transfers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Directories': Directories,
        'Files': Files,
        'Transfers': Transfers,
    }

