__author__ = 'DMunro'
import logging
import time

import CtsCodeGeneration

# Get the logger for this module
logging.basicConfig(level=logging.NOTSET, format='%(asctime)s [%(name)s] [%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Add Console / File Loggers
    console_handler = logging.StreamHandler()
    #file_handler = logging.FileHandler('{0}/{1}_{2}.log'.format('C:\Users\dmunro\Desktop', 'PermissionTestLog', (time.time())))

    #logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    start_time = time.time()

    # Methods/Permissions class map
    cmp_entries = CtsCodeGeneration.csv_to_listoflists('permissions9.2.csv')
    class_mp_map = CtsCodeGeneration.class_to_method_permission_map(cmp_entries)
    #for k, v in class_mp_map.iteritems():
        #print'{0} {1}'.format(k, v)

    # Constructor class map
    folderPath = 'C:\\Users\\dmunro\\git\\frameworks-base2\\frameworks-base'
    class_ctor_map = CtsCodeGeneration.constructor_for_class(folderPath)
    #for k, v in class_ctor_map.iteritems():
        #print'{0} {1}'.format(k, v)





    #className = 'BluetoothMapClient'
    #ctor = 'FooManager()'

    #print getInitInfo(className)
    #print getSetupMethod(className, ctor)
    #print getTestCases(className, classesMethodsPermissionsMap)

    # Write all data blocks to test file
    """
    for className in classList:
        # CREATE TEST FILE
        PermissionTestFile = 'PermissionTests/' + className + '.java'

        classFile = open(PermissionTestFile, 'a')

        # Write static info block
        classFile.write(getInitInfo(className))

        # Write setup block
        ctor = getClassCtor(className)
        classFile.write(getSetupMethod(className, ctor))

        # Write tests block
        classFile.write(getTestCases(className, classesMethodsPermissionsMap))

        # Write closing block
        classFile.write('}')

        classFile.close()

        # CREATE ANDROID MANIFEST

    print testCases
    """

    #logger.info('Summary:')
    #logger.info('Files under path: {0}'.format(folderPath))
    #logger.info('Files found: {0}'.format(len(files)))
    #logger.info('Java classes found (.java postfix): {0}'.format(len(classes)))
    #logger.info('Java classes found with Constructor: {0}'.format(len(classCtors)))

    logger.info('--- Processing time: {0} seconds ---'.format((time.time() - start_time)))

    # Remove the logger
    logger.info('Removing logging handler to file (since it is saved)')
    logger.removeHandler(file_handler)
    logger.removeHandler(console_handler)

if __name__ == "__main__":
    main()