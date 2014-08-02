from appconf import AppConf


class CriticalConf(AppConf):
    PHANTOMJS_PATH = 'phantomjs'
    PENTHOUSE_PATH = 'penthouse.js'

    class Meta:
        prefix = 'critical'
