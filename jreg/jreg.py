#!/usr/bin/env python3
#
# Copyright (c) 2017, Robert Simmons
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""This is a Python module for testing and using Java regular expressions.

The RegexChecker class is modified from:
https://checkerframework.org/tutorial/src/RegexExample.java
"""

import base64
import pathlib
import shutil
import subprocess
import tempfile

regex_checker = 'yv66vgAAADUAOAoACgAYCgAUABkKABQAGgoAFQAbCQAcAB0KABUAHgoAHwAgCgAcACEHACIHACMBAAY8aW5pdD4BAAMoKVYBAARDb2'
regex_checker += 'RlAQAPTGluZU51bWJlclRhYmxlAQAEbWFpbgEAFihbTGphdmEvbGFuZy9TdHJpbmc7KVYBAA1TdGFja01hcFRhYmxlBwAkBwAlBwA'
regex_checker += 'mBwAnAQAKU291cmNlRmlsZQEAEVJlZ2V4Q2hlY2tlci5qYXZhDAALAAwMACgAKQwAKgArDAAsAC0HAC4MAC8AMAwAMQAyBwAzDAA0'
regex_checker += 'ADUMADYANwEADFJlZ2V4Q2hlY2tlcgEAEGphdmEvbGFuZy9PYmplY3QBABNbTGphdmEvbGFuZy9TdHJpbmc7AQAQamF2YS9sYW5nL'
regex_checker += '1N0cmluZwEAF2phdmEvdXRpbC9yZWdleC9QYXR0ZXJuAQAXamF2YS91dGlsL3JlZ2V4L01hdGNoZXIBAAdjb21waWxlAQAtKExqYX'
regex_checker += 'ZhL2xhbmcvU3RyaW5nOylMamF2YS91dGlsL3JlZ2V4L1BhdHRlcm47AQAHbWF0Y2hlcgEAMyhMamF2YS9sYW5nL0NoYXJTZXF1ZW5'
regex_checker += 'jZTspTGphdmEvdXRpbC9yZWdleC9NYXRjaGVyOwEAB21hdGNoZXMBAAMoKVoBABBqYXZhL2xhbmcvU3lzdGVtAQADb3V0AQAVTGph'
regex_checker += 'dmEvaW8vUHJpbnRTdHJlYW07AQAFZ3JvdXABABUoSSlMamF2YS9sYW5nL1N0cmluZzsBABNqYXZhL2lvL1ByaW50U3RyZWFtAQAHc'
regex_checker += 'HJpbnRsbgEAFShMamF2YS9sYW5nL1N0cmluZzspVgEABGV4aXQBAAQoSSlWACEACQAKAAAAAAACAAEACwAMAAEADQAAAB0AAQABAA'
regex_checker += 'AABSq3AAGxAAAAAQAOAAAABgABAAAABwAJAA8AEAABAA0AAACDAAMABQAAADAqAzJMKgQyTSu4AAJOLSy2AAM6BBkEtgAEmQASsgA'
regex_checker += 'FGQQDtgAGtgAHpwAHBrgACLEAAAACAA4AAAAiAAgAAAAJAAQACgAIAAwADQANABQADwAcABAAKwASAC8AFAARAAAAGQAC/wArAAUH'
regex_checker += 'ABIHABMHABMHABQHABUAAAMAAQAWAAAAAgAX'


class JavaRegex:
    """Class for handling all java regex functionality."""

    def __init__(self, javapath=pathlib.Path('java'), custom_regex_checker_class_path=None, debug=False):
        """Instantiate the class."""
        self.javapath = javapath
        self.debug = debug

        self._temp_dir = tempfile.TemporaryDirectory()
        self._path = pathlib.Path(self._temp_dir.name)

        regex_checker_class = base64.b64decode(regex_checker)

        # if there is no custom regex checker class given, use the default one
        if custom_regex_checker_class_path is None:
            class_path = self._path.joinpath('RegexChecker.class')
            self.java_command = 'RegexChecker'
            with open(class_path, 'wb') as fh:
                fh.write(regex_checker_class)
        # if the path to a custom regex checker class is given, copy it into the temp. directory
        else:
            file_name = custom_regex_checker_class_path.split('/')[-1]
            self.java_command = file_name.split('.class')[0]
            class_path = self._path.joinpath(file_name)
            shutil.copyfile(custom_regex_checker_class_path, class_path)

    def match(self, regex, string):
        """Perform the regex match. Requires a raw string as regex input."""
        command = [self.javapath, self.java_command, "'{}'".format(regex), "'{}'".format(string)]

        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self._temp_dir.name)
        result = process.stdout.decode().strip().strip("'")

        if self.debug:
            print('Result: {}\nProcess: {}'.format(result, process))

        if process.returncode == 3:
            return None
        else:
            return result

    def __del__(self):
        """Cleanup the temp directory."""
        self._temp_dir.cleanup()

if __name__ == '__main__':
    jre = JavaRegex(debug=True)
    print(jre._temp_dir)
    assert jre.match(r'[01]?\d-([0123]?\d)-\d{4}+\b', '01-24-2013') == '01-24-2013'
