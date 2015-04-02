__author__ = 'DMunro'

import StringIO

def createTestCase(className, method, permission):
    """
    Will return a string object with data similar to..

    where in this case;
    className : WifiManager
    method : saveConfiguration()
    permission : CHANGE_WIFI_STATE

    /**
     * Verify that WifiManager#saveConfiguration() requires permissions.
     * <p>Requires Permission:
     *   {@link android.Manifest.permission#CHANGE_WIFI_STATE}.
     */
    public void testSaveConfiguration() {
        try {
            mWifiManager.saveConfiguration();
            fail("WifiManager.saveConfiguration didn't throw SecurityException as expected");
        } catch (SecurityException e) {
            // expected
        }
    }
    """
    sb = StringIO.StringIO()
    # Make Method's first letter uppercase
    ucMethodName = str(method)[0].upper() + str(method)[1:]
    # Now get Method name without parameters and uppercase
    methodName = ucMethodName.split('(')[0]

    # Create valid method + param string
    validMethodParamString = createMethodParamString(method)

    # Function javadoc comment
    sb.write('\t/**\n')
    sb.write('\t * Verify that calling {@link %s#%s}\n' % (className, ucMethodName))
    sb.write('\t * requires permissions.\n')
    sb.write('\t * <p>Tests Permission:\n')
    sb.write('\t *   {@link android.Manifest.permission#%s}.\n' % permission)
    sb.write('\t */\n')
    sb.write('\t@SmallTest\n')

    # Function
    sb.write('\tpublic void test%s() {\n' % methodName)
    sb.write('\t\ttry {\n')
    sb.write('\t\t\t{0}.{1};\n'.format(getManagerInstanceName(className), validMethodParamString))
    sb.write('\n')
    sb.write('\t\t\tfail("Was able to call %s");\n' % method)
    sb.write('\t\t} catch (SecurityException e) {\n')
    sb.write('\t\t\t// expected\n')
    sb.write('\t\t} catch (Exception e) {\n')
    sb.write('\t\t\tLog.e("%sPermissionTest", "exception", e);\n' % (className))
    sb.write('\t\t}\n')
    sb.write('\t}\n')
    sb.write('\n')

    return sb.getvalue()

def trimMethod(method):
    """
    Returns method name with parameters
    e.g. method public boolean className(arg1, arg2) -> className(arg1, arg2)
    """
    match = re.search(r'\w+\((.+)\)|\w+\(()\)', method)

    if match:
        return match.group()

def getTestCases(className, classesMethodsPermissionsMap):
    """
    Returns a dictionary where the key is a class name and the value
    is a string of

    Returns a dictionary where the key is a class name and the value
    is a list of dictionaries. The key of these dictionaries is the method name
    """
    sb = StringIO.StringIO()
    for method in classesMethodsPermissionsMap[className]:
        # Method name / permission pair
        for method, permission in method.iteritems():
            # Create test cases
            cMethod =  trimMethod(method)
            testCase = createTestCase(className, cMethod, permission)

            # Append to our test
            sb.write(testCase)

    return sb.getvalue()

def getSetupMethod(className, ctor):
    sb = StringIO.StringIO()
    managerInstance = getManagerInstanceName(className)
    sb.write('\t@Override\n')
    sb.write('\tprotected void setUp() throws Exception {\n')
    sb.write('\t\tsuper.setUp();\n')
    sb.write('\t\t{0} = {1};\n'.format(managerInstance, ctor))
    sb.write('\n')
    sb.write('\t\tassertNotNull({0});\n'.format(managerInstance))
    sb.write('\t}')
    sb.write('\n')

    return sb.getvalue()

def getInitInfo(className):
    sb = StringIO.StringIO()
    # write package name
    sb.write('package harman.gm.test.permission;\n\n')

    # write in utils
    sb.write('import android.content.Context;\n')
    sb.write('import android.test.AndroidTestCase;\n')
    sb.write('import android.test.suitebuilder.annotation.SmallTest;\n')

    # write class header comment
    sb.write('\n/**\n')
    sb.write('* Test that protected %s APIs cannot be called without permissions\n' % className)
    sb.write('*/\n')

    # write class header
    sb.write('public class %sPermissionTest extends AndroidTestCase {\n' % className)

    # write instantiation declaration of class as a global
    sb.write('\n\tprivate %s %s = null;\n' % (className, getManagerInstanceName(className)))

    return sb.getvalue()

def getManagerInstanceName(className):
    """
    Returns a formatted class name e.g. m'className'Manager

    className is the name of a class
    """
    return 'm{0}Manager'.format(className)

def createMethodParamString(method):
    #TODO: NEED TO BUILD THIS FUNCTION
    return 'foo'