class CheckerLog(object):
    LEVEL_DBG = 3
    LEVEL_INFO = 2
    LEVEL_WARN = 1
    LEVEL_ERR = 0
    cur_level = 0
    def __init__(self, fil):
        self._fil = fil
    def _log(self, level, content):
        if level <= CheckerLog.cur_level:
            self._fil.write(content + '\n')
    def dbg(self, c):
        self._log(CheckerLog.LEVEL_DBG, '[DBG]'+c)
    def info(self, c):
        self._log(CheckerLog.LEVEL_INFO, '[INFO]'+c)
    def warn(self, c):
        self._log(CheckerLog.LEVEL_WARN, '[WARN]'+c)
    def err(self, c):
        self._log(CheckerLog.LEVEL_ERR, '[ERR]'+c)        
