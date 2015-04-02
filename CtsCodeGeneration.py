__author__ = 'DMunro'
from os.path import basename
import utils
import logging
import textwrap
import csv
import os
import re

# Get the logger for this module
logger = logging.getLogger(__name__)


def print_class_constructors(class_name, class_list):
    params = []

    for index, param in enumerate(class_list):
        params.append('{param} arg{index}'.format(param=param, index=index))

    return textwrap.dedent('''
        ClassName :: {class_name}
        Constructor List:
        public {class_name}(
            {params}
        )
    '''.format(
        class_name=class_name,
        params=', '.join(params)
    ))


def csv_to_listoflists(permission_file):
    cmp_entries = []
    infile = open(permission_file, 'rt')
    reader = csv.reader(infile)
    for line in reader:
        class_name = line[2]
        method_name = line[3]
        permission = line[5]

        if permission and permission != 'n/a':
            entry = []
            entry.append(class_name)
            entry.append(method_name)
            entry.append(permission)

            cmp_entries.append(entry)

    infile.close()

    return cmp_entries


def class_to_method_permission_map(cmp_entries):
    """
    Returns a dictionary where the key is a class name and the value
    is a list of dictionaries. The key of these dictionaries is the method name
    and the value being the permission required to use the method.

    {class_name : [{method_name1 : permission}, {method_name2 : permission} ..]}

    cmp_entries is a list of class, method and permissions where each entry
    has a permission and the permission is not 'n/a'.
    """
    class_method_permission_map = {}
    param_string = ''
    for entry in cmp_entries:
        class_name = entry[0]
        permission = entry[2]

        # build valid parameters and reconstruct the method if parameters exist
        trimmed_method_name = utils.trim_method(entry[1])
        if trimmed_method_name:
            # Get method parameters
            params = utils.parameter_string(trimmed_method_name)
            if params:
                params_no_paren = params[1:-1]
                clean_params = params_no_paren.split(',')

                parameters = map(str.strip, clean_params)

            # Rebuild method with valid parameters
            #return '{params}'.format(params=', '.join(parameters))
            param_string = str(parameters)

            method_name_no_params = trimmed_method_name.split('(')[0]
            method_name = method_name_no_params + '(' + param_string + ')'

            # check if class_name already an entry in class_method_permission_map
            if class_method_permission_map.has_key(class_name):
                # check if method already exist in list
                if method_name not in class_method_permission_map[class_name]:
                    class_method_permission_map[class_name].append({method_name: permission})
                else:
                    logger.debug('{0} method already exist in dictionary'.format(method_name))

            # class_name doesn't exist, lets create a new entry and init the values
            else:
                class_method_permission_map[class_name] = [{method_name: permission}]

    return class_method_permission_map


def constructor_for_class(frameworkbase_path):
    # Class name / Path dict, so we can access the files later to get the constructors
    class_path_map = {}

    for subdir, dirs, files in os.walk(frameworkbase_path):
        for file in files:
            if file.endswith('.java'):
                class_name = os.path.splitext(basename(file))[0]
                file_path = os.path.join(subdir, file)

                class_path_map[class_name] = file_path

    # Lets search all the class files for their constructors
    class_ctor_map = {}
    for className, filePath in class_path_map.iteritems():
        ctors = []
        pattern = r'(public|private)[ \t]*' + re.escape(className) + '\(([^)]+)\)'

        infile = open(filePath, 'r')

        for line in infile:
            match = re.search(pattern, line)
            if match:
                ctors.append(match.group())

        infile.close()

        valid_ctors = []
        if ctors:
            for ctor in ctors:
                # Get constructor parameters
                ctor_params = []
                params = utils.parameter_string(ctor)
                if params:
                    # regex search for each object/word in params
                    words = re.findall(r'[a-zA-Z0-9_]+', params)
                    # data types are even index's
                    for index in range(len(words)):
                        if index % 2 == 0:
                            ctor_params.append(words[index])

                # Reconstruct constructor with valid parameters
                #TODO
                #return '{params}'.format(params=', '.join(parameters))
                valid_param_string = str(ctor_params)

                valid_ctor = className + '(' + valid_param_string + ')'
                valid_ctors.append(valid_ctor)

            class_ctor_map[className] = valid_ctors

    return class_ctor_map