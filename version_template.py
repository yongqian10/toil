# Copyright (C) 2015-2016 Regents of the University of California
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is a template for src/toil/version.py. Running it without arguments echoes all
globals, i.e. module attributes. Constant assignments will be echoed verbatim while callables
will be invoked and their result echoed as an assignment using the function name as the left-hand
side and the return value of the function as right-hand side. To prevent a module attribute from
being echoed, start or end the attribute name with an underscore. To print the value of a single
symbol, pass the name of that attribute to the script as a command line argument. You can also
import the expand_ function and invoke it directly with either no or exactly one argument."""

# Note to maintainers:
#
#  - don't import at module level unless you intend for the import to be included in the output
#  - only import from the Python standard run-time library

baseVersion = '3.5.0a1'

cgcloudVersion = '1.6.0a1.dev378'


def version():
    """
    A version identifier that includes the commit and whether the working copy is dirty.
    """
    return distVersion() + '-' + currentCommit() + ('-dirty' if dirty() else '')


def distVersion():
    """
    The distribution version identifying a published release on PyPI.
    """
    from pkg_resources import parse_version
    build_number = buildNumber()
    if build_number is not None and parse_version(baseVersion).is_prerelease:
        return baseVersion + '.dev' + build_number
    else:
        return baseVersion


def dockerTag():
    """
    The version that is used to tag the Docker image for the appliance.
    """
    return version()

dockerRegistry = 'quay.io/ucsc_cgl'

dockerName = 'toil'

def buildNumber():
    """
    The Jenkins build number, if defined, else None.
    """
    import os
    return os.getenv('BUILD_NUMBER')


def currentCommit():
    from subprocess import check_output
    return check_output('git log --pretty=oneline -n 1 -- $(pwd)', shell=True).split()[0]


def dirty():
    from subprocess import call
    return 0 != call('(git diff --exit-code '
                     '&& git diff --cached --exit-code) > /dev/null', shell=True)


def expand_(name=None):
    variables = {k: v for k, v in globals().iteritems()
                 if not k.startswith('_') and not k.endswith('_')}

    def resolve(k):
        v = variables[k]
        if callable(v):
            v = v()
        return v

    if name is None:
        return ''.join("%s = %s\n" % (k, repr(resolve(k))) for k, v in variables.iteritems())
    else:
        return resolve(name)


def _main():
    import sys
    sys.stdout.write(expand_(*sys.argv[1:]))


if __name__ == '__main__':
    _main()