#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hspf helper module with common helper functions.

This module contains the common helper functions for hspf.

Attributes:
    HSPF_KEY_PREFIX (str): Hspf allows importing OS environment variables into
        the 'settings' object. Such OS environment variables must be prepended
        with HSPF_KEY_PREFIX.
    MSG_FORMATTER (str): Formatter string for log messages.
    DATE_FORMATTER (str): Date string for log messages.

"""
import os
import re
import datetime as dt
import logging
import subprocess
import copy
import socket
import uuid
import pwd
import grp
import random
import inspect
import string
import time
import toml
import datetime
import shutil
import filecmp

# for mailing
import smtplib
import email.utils
from email.mime.text import MIMEText

__version__ = '2.2.1'

HSPF_KEY_PREFIX = '__HSPF__'
MSG_FORMATTER = ('%(asctime)s.%(msecs)-3d %(levelname)-8s ' +
                 '[%(filename)s:%(lineno)d] %(message)s')
DATE_FORMATTER = '%Y.%m.%d %H:%M:%S'

# Utility objects:


class ObjDict(dict):
    """Dict-based class, which provides 'class-<dot>-attribute' access.

    Users cannot accidentally get, set or delete non-existing attributes.
    Nested ObjDicts are supported.

    Args:
        entries (dict): A dictionary to be transformed into an ObjDict.

    Returns:
        An ObjDict object

    Raises:
        AttributeError: If the user attempts to set a non-existing attribute.

    Examples:
        >>> test_dict = {'airflow': {'dry_run': True}}
        >>> test_obj_dict = ObjDict(test_dict)
        >>> test_obj_dict
        ObjDict({'airflow': ObjDict({'dry_run': True})})
        >>> test_obj_dict.dryrun = False
        Traceback (most recent call last):
            ...
        AttributeError: dryrun

    """

    def __init__(self, entries):
        super().__init__()
        for key, value in entries.items():
            try:
                self.__dict__[key] = ObjDict(value)
            except AttributeError:
                self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, name):
        if name in self.__dict__.keys():
            return self.name
        raise AttributeError(name)

    def __setattr__(self, name, value):
        # prevent adding a non-existing attribute unintentionally:
        if name in self.__dict__.keys():
            self.__dict__[name] = value
        else:
            raise AttributeError(name)

    def __str__(self):
        return 'ObjDict({})'.format(self.__dict__)

    def __repr__(self):
        return 'ObjDict({})'.format(self.__dict__)


# Utility functions:


def objdict_to_dict(objdict):
    """Turn an ObjDict into an ordinary dict.

    Args:
        objdict (ObjDict): A ObjDict object to be transformed into an dict.

    Returns:
        An dict object

    Example:
        >>> test_dict = {'airflow': {'dry_run': True}}
        >>> objdict_to_dict(ObjDict(test_dict))
        {'airflow': {'dry_run': True}}

    """
    _dict = copy.deepcopy(objdict)
    for key, value in vars(_dict).items():
        if isinstance(value, ObjDict):
            _dict[key] = objdict_to_dict(value)
        else:
            _dict[key] = value
    return vars(_dict)


def random_ascii_str(number_of_chars):
    """Generate a random string of 'number_of_chars' acii characters.

    Args:
        number_of_chars (int): The length of the random ascii string to be
        generated.

    Returns:
        A random string of 'number_of_chars' acii characters

    Example:
        >>> import random
        >>> random.seed(1)
        >>> random_ascii_str(10)
        'iKZWeqhFWC'

    """
    random_char_list = [random.choice(string.ascii_letters) for
                        _ in range(number_of_chars)]
    return ''.join(random_char_list)


def toml_strip_comments(config_txt):
    """Strip all comments from the text of a toml file.

    We do so by first reading it into a configuration dictionary and
    subsequently saving it to a new string object.

    Args:
        config_txt (str): String representation of the contents of a toml file.

    Returns:
        Equivalent contents without comments

    Example:
        >>> toml_contents = '[airflow]\\ndry_run = true\\n#No comments please!'
        >>> toml_strip_comments(toml_contents)
        '[airflow]\\ndry_run = true\\n'

    """
    config_dict = toml.loads(config_txt)
    config_txt = toml.dumps(config_dict)
    return config_txt


def toml_interpolate(config_txt, start_marker=r'${', end_marker=r'}', escape=r'$'):
    """Perform string interpolation on config_txt.

    The default value of start_marker of the strings to be interpolated is
    '${'. The default value of end_marker is '}'. If '$' is needed in the
    resulting .toml string it must be espaced by using '\$' in the toml file.

    For example: After an assignment such as 'variable = "value", a string
    like '"${variable}_other_value"' will be replaced by
    '"value_other_value"', whereas a string like '"\${variable}_other_value"'
    will become '"${variable}_other_value"'.
    """
    #the markers should not be interpreted by regex
    esc_start_marker = re.escape(start_marker)
    esc_end_marker   = re.escape(  end_marker)
    esc_escape       = re.escape(      escape)
    #find words starting with start marker, then match everything except ([^...]) end marker
    # once or more times (+) and ending with the end marker
    varRegEx    = esc_start_marker + '[^' + esc_end_marker + ']+' + esc_end_marker
    varPattr    = re.compile(varRegEx)
    #find unique set(!) of variable names
    variableSet = set(re.findall(varPattr, config_txt))
    for var in variableSet:
        #key is variable name without markers
        key     = var.lstrip(start_marker)
        key     = key.rstrip(  end_marker)
        esc_var = re.escape(var)
        #if there's a value, take the first hit & remove quotes
        value = re.findall(' *' + key + ' *= *(.*)',config_txt)
        if value:
            value = value[0].rstrip('"').lstrip('"')
            #replace entries, except ([^...]) those starting with the escape character
            # match (()) and return (\g<1>) previous character if it's not the escape char
            #note: \g<1> is an unambiguous backreference, not affected by trailing numeric values
            config_txt = re.sub('([^' + esc_escape+'])'+ esc_var,   \
                                '\g<1>' + value,                    \
                                config_txt                          )
    #replace escaped vars
    config_txt = re.sub(esc_escape + '(' + varRegEx + ')',  \
                        '\\1',                              \
                        config_txt                          )
    return config_txt


def get_name_config_toml_file():
    """Get the name of the main config toml file.

    Args:
        None.

    Returns:
        The toml file name reprsented by the os environment variable
        HSPF_KEY_PREFIX + 'FILE_CONFIG_TOML'.

    Example:
        >>> path_to_toml_file = '/path/to/toml/toml_file'                        # doctest: +SKIP
        >>> HSPF_CONFIG_TOML = (HSPF_KEY_PREFIX + 'FILE_CONFIG_TOML')            # doctest: +SKIP
        >>> os.environ[HSPF_CONFIG_TOML] = path_to_toml_file                     # doctest: +SKIP
        >>> toml_fn = get_name_config_toml_file()                                # doctest: +SKIP

    """
    HSPF_CONFIG_TOML = (HSPF_KEY_PREFIX +  # pylint:disable=invalid-name
                        'FILE_CONFIG_TOML')
    if HSPF_CONFIG_TOML in os.environ.keys():
        file_config_toml = os.environ[HSPF_CONFIG_TOML]
        if not os.path.exists(os.path.realpath(file_config_toml)):
            raise ConfTomlFileDoesNotExistError(
                os.path.realpath(file_config_toml))
    else:
        raise ConfTomlFileEnvVarNotExistError(str(os.environ.items()))
    return file_config_toml


# TODO: update test scripts & remove this function
def get_name_config_poml_file():
    """Get the name of the main config poml file.

    Args:
        None.

    Returns:
        The poml file name reprsented by the os environment variable
        HSPF_KEY_PREFIX + 'FILE_CONFIG_POML'.

    Example:
        >>> path_to_poml_file = '/path/to/toml/poml_file'                        # doctest: +SKIP
        >>> HSPF_CONFIG_POML = (HSPF_KEY_PREFIX + 'FILE_CONFIG_POML')            # doctest: +SKIP
        >>> os.environ[HSPF_CONFIG_POML] = path_to_poml_file                     # doctest: +SKIP
        >>> poml_fn = get_name_config_poml_file()                                # doctest: +SKIP

    """
    HSPF_CONFIG_POML = (HSPF_KEY_PREFIX +  # pylint:disable=invalid-name
                        'FILE_CONFIG_POML')
    if HSPF_CONFIG_POML in os.environ.keys():
        file_config_poml = os.environ[HSPF_CONFIG_POML]
        if not os.path.exists(os.path.realpath(file_config_poml)):
            raise ConfPomlFileDoesNotExistError(
                os.path.realpath(file_config_poml))
    else:
        raise ConfPomlFileEnvVarNotExistError(str(os.environ.items()))
    return file_config_poml


def get_settings_from_file(toml_file=None):
    """Get the settings from the main config toml formatted file. This can
       also be a parsed toml (poml) file.

    Args:
        toml_file (str): Name of the toml or poml file to be read.

    Returns:
        ObjDict representing the configuration.

    Example:
        >>> path_to_toml_file = '/path/to/toml/toml_file'                        # doctest: +SKIP
        >>> settings = get_settings_from_file(path_to_toml_file)                 # doctest: +SKIP

    """
    # If not provided yet, get the name of the config poml file.
    if not toml_file:
        toml_file = get_name_config_toml_file()
    #convert to poml from here
    if os.path.splitext(toml_file)[1] == '.poml':
        poml_file = toml_file
    else:
        poml_file = toml2poml(toml_file)
    # Read it:
    with open(poml_file) as fhandle:
        poml_txt = fhandle.read()
    # Parse poml_txt:
    settings = toml.loads(poml_txt)
    return settings


def toml2poml(toml_file_path):
    """
    Read an HSPF '.toml' file, remove any comments, and interpolate its
    contents. Write to the resulting '.poml' file in the same dir.

    Args:
        poml_file (str):  A '.toml' file potentially containing comments and strings to be interpolated.

    Returns:
        poml_file_path (str):  A '.poml' file

    Example:
        >>> poml_file_path = toml2poml(toml_file_path)                           # doctest: +SKIP

    """
    poml_file_path = os.path.splitext(toml_file_path)[0] + '.poml'
    #does the poml file exist?
    toml_file_timestamp = os.path.getctime(toml_file_path)
    poml_file_timestamp = 0
    if os.path.exists(poml_file_path):
        poml_file_timestamp = os.path.getctime(poml_file_path)
    #overwrite when toml is newer
    if toml_file_timestamp > poml_file_timestamp:
        with open(toml_file_path,'r') as fhandle:
            toml_contents = fhandle.read()
        toml_stripped = toml_strip_comments(toml_contents)
        toml_interpolated = toml_interpolate(toml_stripped)
        with open(poml_file_path,'w') as fhandle:
            fhandle.write(toml_interpolated)
    return poml_file_path


def save_uid_gid(settings):
    """Save the current values of uid and gid in the settings object.

    Args:
        settings (ObjDict): configuration object.

    Returns:
        None.

    Examples:
        >>> from hspf import driver_helpers                                      # doctest: +SKIP
        >>> settings = get_settings_from_file(path_to_poml_file)                 # doctest: +SKIP
        >>> settings = ObjDict(settings)                                         # doctest: +SKIP
        >>> settings = add_attributes(settings, driver_helpers.DYNAMIC_SETTINGS) # doctest: +SKIP
        >>> save_uid_gid(settings)                                               # doctest: +SKIP

    """
    user_name = pwd.getpwuid(os.getuid()).pw_name
    settings.system.uid = pwd.getpwnam(user_name).pw_uid
    try:
        settings.system.gid = grp.getgrnam(settings.system.group_name).gr_gid
    except KeyError:
        raise HspfGroupError


def current_user_in_group(group_name):
    """Check if the current user is a member of group_name.

    Args:
        group_name (str): name of group in which the current user should be.

    Returns:
        Boolean, true if the current user is a member of group_name.

    Examples:
        >>> current_user_in_group('hspf_dev')                                    # doctest: +SKIP
        True

    """
    user_name = pwd.getpwuid(os.getuid()).pw_name
    groups = subprocess.check_output(['id', '-Gn', user_name]).split()
    groups = [x.decode("utf-8") for x in groups]
    if group_name not in groups:
        return False
    return True


def check_group_membership_current_user(settings):  # pylint:disable=invalid-name
    """Test if the current user has the right group membership.

    Args:
        settings (ObjDict): configuration object.

    Returns:
        None

    Raises:
        HspfGroupError (Exception): Abort the program when the current user
            does not have the right group membership.

    Examples:
        >>> check_group_membership_current_user(settings)                        # doctest: +SKIP

    """
    if settings.system.check_user:
        # Check if we belong to 'settings.system.group_name':
        if current_user_in_group(settings.system.group_name):
            # Abort if not:
            current_user = pwd.getpwuid(os.getuid()).pw_name
            msg = (current_user + ' is not a member of ' +
                   settings.system.group_name)
            raise HspfGroupError(msg)


def makedirs(full_path_new_folder, settings, chown=True, chmod=True):
    """Create 'full_path_new_folder', taking care of its ownership.

    If 'full_path_new_folder' does not exist yet, each sub_folder relative to
    'settings.paths.folder_base' will be created step by step.

    If 'full_path_new_folder' exists already nothing will happen.

    If chown is True, then the newly created parts of path will be owned by
    'settings.system.uid:settings.system.gid'.
    If chmod == True, then the newly created parts of path will be chmodded to
    'settings.system.folder_permission_bits'.

    Note that 'settings.paths.folder_base' must be a part of
    'full_path_new_folder'.

    Args:
        full_path_new_folder (str): path to be created.
        settings (ObjDict): configuration object.
        chown (bool): newly created parts of 'full_path_new_folder' must be
            chowned to 'settings.system.uid:settings.system.gid'.
        chmod (bool): newly created parts of 'full_path_new_folder' must be
            chmodded to 'settings.system.folder_permission_bits'.

    Returns:
        None

    Raises:
        MakeDirsError (Exception): 'settings.paths.folder_base' is not a part
            of 'full_path_new_folder'.

    Examples:
        >>> makedirs('/full/path/to/new_folder', settings)                       # doctest: +SKIP

    """
    folder_base            = settings.paths.folder_base
    folder_permission_bits = settings.system.folder_permission_bits
    user_id                = settings.system.uid
    group_id               = settings.system.gid
    # obtain the the relative path to be created (wrt folder_base):
    split_full_path = full_path_new_folder.split(folder_base)
    # split_full_path[0] should be an empty string, thus false:
    if split_full_path[0]:
        print('-E- ' + folder_base + ' is not a part of ' + full_path_new_folder)
        raise MakeDirsError
    # If there is no directory to be created:
    if len(split_full_path) == 1:
        return
    rel_path_to_be_created = split_full_path[1]
    # remove potential leading forward slashes from rel_path_to_be_created:
    if rel_path_to_be_created[0] == os.sep:
        rel_path_to_be_created = rel_path_to_be_created[1:]
    # get a lis of all sub_folders to be made:
    sub_folders_to_be_made = rel_path_to_be_created.split(os.sep)
    # test if absoolute path to sub_folder exists:
    for sub_folder in sub_folders_to_be_made:
        full_path_sub_folder = os.path.join(folder_base,sub_folder)
        # update for next iteration in for loop:
        folder_base = full_path_sub_folder
        if not os.path.isdir(full_path_sub_folder):
            try:
                os.makedirs(full_path_sub_folder)
            except Exception as e:
                # a parallel process might just have created this directory
                time.sleep(0.1)
                if not os.path.isdir(full_path_sub_folder):
                    print('common_helpers.makedirs encountered a problem:')
                    print(type(e), e)
            if chmod:
                try:
                    os.chmod(full_path_sub_folder,folder_permission_bits)
                except PermissionError:
                    print('-W- Couldn\'t set permission ' + folder_permission_bits + \
                          ' of: ' + full_path_sub_folder)
            if chown:
                try:
                    os.chown(full_path_sub_folder,user_id,group_id)
                except PermissionError:
                    print('-W- Couldn\'t change owner of: ' + full_path_sub_folder)


def ms_since_epoch(dt_object=dt.datetime.utcnow()):
    """Convert a 'datetime object' to number of milliseconds since dt_object.

    Args:
        dt_object (dt.datetime): datetime object.

    Returns:
        integer indicating the number of milliseconds that have passed since
        dt_object.

    Examples:
            >>> ms_since_epoch()                                                 # doctest: +SKIP
        1534723200000 # run on dt.datetime(2018, 8, 20)
        >>> ms_since_epoch(dt.datetime(2018, 1, 1))
        1514764800000

    """
    return int((dt_object - dt.datetime(1970, 1, 1)).total_seconds() * 1000)


def files_available(folder, mask):
    """Return list of tiles available in dir."""
    potential_files = os.listdir(folder)
    files = [x for x in potential_files if x.endswith(mask)]
    return files


def get_time_uuid(extension=''):
    """Return a string consisting of 'ms_since_epoch()' and 'uuid4().hex.' and
    extension"""
    timestamp     = datetime.datetime.now()
    time_uuid_str = timestamp.strftime(timestamp.strftime('%Y%m%d-%Hh%Mm%Ss%sms'))
    uuid_str      = uuid.uuid4().hex
    if extension:  # If extension unqual to empty string we prepend a dot
        extension = '.' + extension
    time_uuid_str = time_uuid_str + '_' + uuid_str + extension
    return time_uuid_str


# Derived from https://serverfault.com/questions/690391/finding-local-ip-
# addresses-using-pythons-stdlib-under-debian-jessie:
def get_ip_address():
    """Get a host's ip address."""
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_socket.connect(('192.0.0.8', 1027))
    res = local_socket.getsockname()[0]
    local_socket.close()
    return res


def add_attributes(settings, attributes):
    """Add the elements of list 'attributes' as attributes to the namespace
    settings. Each attribute should have the form:
    'main_attribute.sub_attribute'."""
    for attribute in attributes:
        try:
            main_attribute, sub_attribute = attribute.split('.')
        except ValueError:
            raise IncorrectAttributeError(
                'Dynamic attributes must have exactly two levels, and thus ' +
                'one dot')
        try:
            # Test if the main_attribute exists already:
            settings[main_attribute] = settings[main_attribute]
        except KeyError:  # attribute/key does not exist yet
            # create the attribute/key
            settings[main_attribute] = {}
        if sub_attribute:
            settings[main_attribute][sub_attribute] = ''
            # initialize as '' instead of None. Otherwise toml will at a later
            # stage not save 'sub_attribute' to the executor's poml file.
    return settings


def write_index_file(folder):
    """Create a .txt file listing the contents of directory 'folder'."""
    index_txt = ''
    files = os.listdir(folder)
    files = [f for f in files if f != 'index.txt']
    for fname in files:
        full_fname = folder + os.sep + fname
        index_txt = index_txt + full_fname
        index_txt = (index_txt + '\t' +
                     str(os.stat(full_fname).st_mtime) + '\n')
    # Other processes may poll for the index files. We write to
    # 'index.txt.tmp', first and rename the file afterwards.
    # This will hopefully reduce the chance of race conditions.
    with open(folder + os.sep + 'index.txt.tmp', 'w') as file_handle:
        file_handle.write(index_txt[:-1])  # -1: remove last newline
    os.rename(folder + os.sep + 'index.txt.tmp',
              folder + os.sep + 'index.txt')
    return folder + os.sep + 'index.txt'


def create_index_file(settings):  # pylint: disable=redefined-outer-name, inconsistent-return-statements
    """Create an index file if necessary"""
    folder = None
    index_file = None
    if settings.cmdline_args.task == 'configure':
        folder = (settings.paths.folder_configure + os.sep +
                  settings.cmdline_args.execution_date)
    elif settings.cmdline_args.task == 'process':
        folder = (settings.paths.folder_process + os.sep +
                  settings.cmdline_args.execution_date)
    if folder:
        if os.path.exists(folder + os.sep + 'index.txt'):
            if settings.system.overwrite_existing_files:
                index_file = write_index_file(folder)
        else:
            index_file = write_index_file(folder)
    if index_file:
        return index_file  # No return value means no index file was created
    #                      # Otherwise we return the name of the index file.


def get_sub_folder(folder_name, settings):
    """Return the name of the subfolder 'foldername' for a specific 'task',
    depending on the ObjDict 'paths'.
    Valid names for folder name are 'logs', 'poml' and 'bash'."""
    sub_folder = (settings.paths.folder_idata + os.sep +
                  settings.workflow.workflow_step + os.sep +
                  settings.cmdline_args.task + os.sep +
                  settings.cmdline_args.execution_date + os.sep + folder_name)
    return sub_folder


def safeMove(source,destination):
    shutil.copy(source,destination)
    #[GIOG-183] don't trust the copy;large rename actions
    #           resulted in disappearing logfiles
    if os.path.exists(destination) and \
        filecmp.cmp(source,destination):
        os.remove(source)
    else:
        print('-E- ' + 'logfile rename '    + \
              source + ' to ' + destination + \
              ' failed.'                      )
        raise SafeFileMoveError


def _create_log_file_handler(settings):
    """Create and return the file_handler for our log file. This will create a
    new log filehandler, if there was no log filehandler yet. Otherwise the
    existing log filehandler will be resumed"""
    log_folder = get_sub_folder('logs', settings)
    # Create log_folder if necessary:
    makedirs(log_folder, settings, chown=True, chmod=True)
    if settings.paths.current_log_filename:
        if 'application_id' in settings.spark.__dict__:
            appid_ext = settings.spark.application_id + '.log'
            if settings.paths.current_log_filename.endswith(appid_ext):
                #logfile has application id
                log_fname = settings.paths.current_log_filename
            else:
                #[GIOG-93] logfile needs to get application id
                log_fname_root = os.path.splitext(settings.paths.current_log_filename)[0]
                log_fname      = log_fname_root + '_' + appid_ext
                safeMove(settings.paths.current_log_filename,log_fname)
                settings.paths.current_log_filename = log_fname
    else:
        program_name = settings.system.current_program_name
        log_name     = program_name + '_' + get_time_uuid('log')
        log_fname    = os.path.join(log_folder,log_name)
        settings.paths.current_log_filename = log_fname
    file_formatter = logging.Formatter(MSG_FORMATTER, DATE_FORMATTER)
    file_handler   = logging.FileHandler(log_fname)
    file_handler.setLevel(settings.system.log_level)
    file_handler.setFormatter(file_formatter)
    return file_handler


def get_logger(settings):
    """Obtain a logger"""
    logger = logging.getLogger(settings.system.current_program_name)
    logger.setLevel(settings.system.log_level)
    file_handler = _create_log_file_handler(settings)
    console_handler = logging.StreamHandler()
    # Avoid adding handlers twice:
    if not logger.handlers:
        logger.addHandler(file_handler)
        try:
            os.chown(settings.paths.current_log_filename, settings.system.uid,
                     settings.system.gid)
        except PermissionError:
            ip_address = get_ip_address()
            msg = ('problem on node: ' + ip_address + '. user ' +
                   str(os.getuid()) + ' cannot change ownership to: ' +
                   settings.paths.current_log_filename + ' to: (' +
                   str(settings.system.uid) + ',' +
                   str(settings.system.gid) + ')')
            raise PermissionError(msg)
        logger.addHandler(console_handler)
    return logger



def read_environment(settings):  # pylint: disable=unused-argument
    """Read the values of existing environment variables into the
    corresponding keys of the settings object"""
    logger = get_logger(settings)
    for env_var in list(os.environ.keys()):
        split_keys = env_var.split('__')
        try:
            hspf_key = split_keys[1]
        except IndexError:
            hspf_key = None
        if hspf_key == HSPF_KEY_PREFIX.replace('__', ''):
            nested_key = split_keys[2:]
            env_val = os.environ[env_var]
            try:
                test_val = settings[nested_key[0]][nested_key[1]]
                # If this succeeded, we know that the nested key exists!
                if isinstance(test_val, int):  # cast env_value
                    env_val = int(env_val)
                elif isinstance(test_val, float):
                    env_val = float(env_val)
                settings[nested_key[0]][nested_key[1]] = env_val
                msg = ("function read_environment() changed 'settings." +
                       nested_key[0] + '.' + nested_key[1] + "' into '" +
                       env_val + "'")
                logger.warning(msg)
            except KeyError:
                pass


def calling_function(level=1):
    """'calling_function' yields the name of the function, in which it is being
    called"""
    to_be_returned = inspect.stack()[level][3]
    if '<module>' in to_be_returned:
        to_be_returned = '__main__()'
    return to_be_returned


def get_kafka_addresses(pid_config_path):
    """'get_kafka_addresses' yields the addesses of the kafka brokers
    specified in a 'pid client path'."""
    with open(pid_config_path) as fhandle:
        pid_config_txt = fhandle.read()
    to_be_returned = pid_config_txt.replace(' ', '')
    to_be_returned = to_be_returned.split('brokers=')[1]
    to_be_returned = to_be_returned.split('\n')[0]
    return to_be_returned.split(',')


def accepts_connection(address, timeout=1):
    """'accepts_connection' tests if an addess of the form 'ipv4:tcp_port'
    accepts incoming connections. This function may be used to check if a kafka
    broker is listening on a specific tcp port"""
    ip_adress, tcp_port = address.split(':')
    try:
        socket.create_connection((ip_adress, int(tcp_port)), timeout=timeout)
        connected = True
    except Exception as e:
        #e is special, don't use it in string formatting
        print('Couldn\'t connect to "' + address + '":\n' + str(e))
        connected = False
    return connected


def accepts_connection_list(address_list, timeout=1):
    """'accepts_connection_list' is a convenience function that applies the
    function 'accepts_connection' to a list of addresses. It returns true if
    at least one of the addresses tested accepts a tcp connection"""
    connected = False
    for address in address_list:
        current_test = accepts_connection(address, timeout=timeout)
        if current_test:
            connected = current_test
    return connected


def replaceChevronsInDict(cfgDict,replaceStrDict):
    """Replace variables in chevrons (< & >) from a configuration
    dict using a replacements dict.


    Parameters
    ----------
    cfgDict : dict
        Configuration dictionary.
    replaceStrDict: dict
        The replacement values dictionary with keys in chevrons.


    Returns
    -------
    dict
        The resolved configuration dictionary.
    """
    #if a objDict is passed, convert to dict (a copy is made automatically)
    if isinstance(cfgDict,ObjDict):
        copiedDict = objdict_to_dict(cfgDict)
    elif isinstance(cfgDict, dict):
        copiedDict = copy.deepcopy(cfgDict)
    else:
        raise TypeError('Expected ObjDict or dict, but got {}'.format(type(cfgDict)))
    
    for key, value in copiedDict.items():
        if isinstance(value,str):
            copiedDict[key] = replaceChevronVars(value,replaceStrDict)
        elif isinstance(value,list):
            copiedDict[key] = replaceChevronsInList(value,replaceStrDict)
        elif isinstance(value,dict):
            copiedDict[key] = replaceChevronsInDict(value,replaceStrDict)
    
    if isinstance(cfgDict,ObjDict):
        copiedDict = ObjDict(copiedDict)
    return copiedDict

def replaceChevronsInSettings(settings,replaceStrDict):
    """Replace variables in chevrons (< & >) from a configuration
    dict using a replacements dict.


    Parameters
    ----------
    settings : Dynaconf settings
        Configuration dictionary.
    replaceStrDict: dict
        The replacement values dictionary with keys in chevrons.


    """
    #
    
    for key, value in settings.items():
        if isinstance(value,str):
            settings[key] = replaceChevronVars(value,replaceStrDict)
        elif isinstance(value,list):
            settings[key] = replaceChevronsInList(value,replaceStrDict)
        elif isinstance(value,dict):
            settings[key] = replaceChevronsInDict(value,replaceStrDict)
    

def replaceChevronsInList(inputList, replaceStrDict):
    """Iterate over each element of a list and call the correct function to handle the replacements
    
    Parameters
    ----------
    inputList: list
        The list to process
    replaceStrDict: dict
        The replacement values dictionary with keys in chevrons.
    Returns
    -------
    list
        The processed list
    """
    copiedList = []
    for element in inputList:
        if isinstance(element,str):
            copiedList.append(replaceChevronVars(element,replaceStrDict))
        elif isinstance(element,list):
            copiedList.append(replaceChevronsInList(element,replaceStrDict))
        elif isinstance(element,dict):
            copiedList.append(replaceChevronsInDict(element,replaceStrDict))
        else:
            copiedList.append(element)
    return copiedList

def replaceChevronVars(inputString,replaceStrDict):
    """Replace variables in chevrons (< & >) in a string
    using a replacements dict.


    Parameters
    ----------
    inputString : str
        Configuration value string.
    replaceStrDict: dict
        The replacement values dictionary with keys in chevrons.


    Returns
    -------
    dict
        The resolved configuration value string.
    """

    #replace <variables> with one(!) bracket
    # catch words with one or more brackets
    substRegEx = r'[<]+\w+[>]+'
    # only resolve the ones in the dictionary (w. one bracket)
    substFunc  = lambda m: replaceStrDict.get(m.group())        \
                           if m.group() in replaceStrDict.keys()\
                           else m.group()
    resolvedString = re.sub(substRegEx,substFunc,inputString )
    #replace <<value>> with <value> for later resolution
    resolvedString = re.sub('<(<[^>]+>)>',r'\1', resolvedString)
    return resolvedString


def sendEmail(receiptLst, sender, subject, msg_text = ''):
    """Send an email to specified receipts
    
    Parameters
    ----------
    receiptLst: list of tuples of str
        Each tuple in the list consists of a name and email address.
        E.g. [(name, email address)]
    sender: tuple of str
        A (name, email address tuple) of str to indicate the sender 
    subject: str
        Subject of the mail
    msg: str
        The email body.
    """
    try:
        server = smtplib.SMTP('mail.vgt.vito.be')
        server.set_debuglevel(False) # show communication with the server
        
        for receipt in receiptLst:
            # Create the messages
            msg = MIMEText(msg_text)
            msg['To'] = email.utils.formataddr(receipt)
            msg['From'] = email.utils.formataddr(sender)
            msg['Subject'] = subject
            # Send it
            server.sendmail(sender[1], [receipt[1]], msg.as_string())
    finally:
        server.quit()


# Exception classes:


class InputError(Exception):
    """Class to report incorrect input"""
    pass


class IllegalDateError(Exception):
    """Basic exception to report Illegal date."""
    pass


class NoFilesAvailableError(Exception):
    """Basic exception to report No file available."""
    pass


class PidNotAvailableError(Exception):
    """Basic exception to report Pid not available."""
    pass


class FileRequiresWritePathError(Exception):
    """Basic exception to report that the argument 'file' requires the
    argument 'write_path' to be specified as well."""
    pass


class InvalidLogLevelError(Exception):
    """Basic exception to report that log_level is invalid."""
    pass


class BinaryDoesNotExistError(Exception):
    """Basic exception to report that the binary does not exist."""
    pass


class NotAStringError(Exception):
    """Basic exception to report a string was expected but not received."""
    pass


class NonZeroResultError(Exception):
    """Basic exception to report that there was a non-zero result."""
    pass


class IllegalProcessTypeError(Exception):
    """Basic exception to report that the process type chosen was neither
    driver nor executor."""
    pass


class IllegalPythonModeError(Exception):
    """Basic exception to report that the python_mode chosen was neither
    pyspark nor python."""
    pass


class PosttestError(Exception):
    """Basic exception to report that the posttest failed."""
    pass


class DockerError(Exception):
    """Basic exception to report that the call to docker failed."""
    pass


class UndefinedLogLevelError(Exception):
    """Basic exception to report that an undefined log level was detected."""
    pass


class ConfTomlFileDoesNotExistError(Exception):
    """Basic exception to report that the config.toml file specified by the
    environment variable 'file_config_toml' does not exist."""
    pass


class ConfPomlFileDoesNotExistError(Exception):
    """Basic exception to report that the config.poml file specified by the
    environment variable 'file_config_poml' does not exist."""
    pass


class ConfTomlFileEnvVarNotExistError(Exception):
    """Basic exception to report that the environment variable
    'file_config_toml' does not exist."""


class ConfPomlFileEnvVarNotExistError(Exception):
    """Basic exception to report that the environment variable
    'file_config_poml' does not exist."""


class EmptyDataFrameError(Exception):
    """Class to report a unexpected empty dataframe."""
    pass


class CannotCreateFolderError(Exception):
    """Class to report a inability to create a folder."""
    pass


class HspfGroupError(Exception):
    """Class to report that the current user is not a member of
    'settings.group_name'."""
    pass


class MakeDirsError(Exception):
    """Class to report an error while calling the function makedirs."""
    pass


class IncorrectAttributeError(Exception):
    """Class to report an incorrectly formatted dynamic attribute."""
    pass


class NoPIDRecordsFoundError(Exception):
    """Class to report that no PID records were found."""
    pass


class ConfigureAndProcessDoNotMatchError(Exception):
    """Class to report that the PID contains a non-matching number of
    configure and process records."""
    pass


class SafeFileMoveError(Exception):
    """Class to report an exception during a safe file move."""
    pass

class HspfWarning(Warning):
    """'Base warning for hspf."""
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
