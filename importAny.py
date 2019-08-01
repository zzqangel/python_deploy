import Constant


def importAny(name):
    try:
        return __import__(name, fromlist=[''])
    except:
        try:
            i = name.rfind('.')
            mod = __import__(name[:i], fromlist=[''])
            return getattr(mod, name[i + 1:])
        except Exception as e:
            logger = Constant.logging.getLogger("importAny")
            logger.error("e: {}".format(e))
            return None
            # raise RuntimeError('No module of: {0} found'.format(name))
