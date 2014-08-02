import subprocess

from django.conf import settings
from django.core.files.temp import NamedTemporaryFile


class PenthouseCommand(object):
    command = '{phantomjs} {penthouse} {htmlurl} {csspath}'
    encoding = 'utf8'

    def __init__(self, phantomjs=None, penthouse=None):
        self.phantomjs = phantomjs or settings.CRITICAL_PHANTOMJS_PATH
        self.penthouse = penthouse or settings.CRITICAL_PENTHOUSE_PATH

    def run(self, html, css):
        with NamedTemporaryFile(mode='wb', suffix='.html') as htmlfile,\
                NamedTemporaryFile(mode='wb', suffix='.css') as cssfile:
            htmlfile.write(html.encode(self.encoding))
            htmlfile.flush()
            cssfile.write(css)
            cssfile.flush()

            command = self.command.format(
                phantomjs=self.phantomjs,
                penthouse=self.penthouse,
                htmlurl='file:{}'.format(htmlfile.name),
                csspath=cssfile.name)

            proc = subprocess.Popen(command, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            proc.wait()
            if proc.returncode:
                raise Exception(
                    'Penthouse command failed ({code}): {message}'.format(
                        code=proc.returncode,
                        message=stderr,
                    ))
            return stdout


def get_critical_css(html, css):
    return PenthouseCommand().run(html, css)
