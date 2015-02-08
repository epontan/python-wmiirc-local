import sys
import traceback
from glob import glob
from os.path import dirname, basename

class AbortModuleLoadException(Exception):
    pass

if __name__ == 'local':
    _modules = [basename(f)[:-3] for f in glob(dirname(__file__) + "/*.py")]
    __all__ = _modules

    for module in _modules:
        try:
            __import__('local.%s' % module)
        except AbortModuleLoadException:
            pass
        except Exception, e:
            print >>sys.stderr, "Failed loading local adaptation module: %s" % module
            traceback.print_exc(sys.stderr)
            print >>sys.stderr, ""
