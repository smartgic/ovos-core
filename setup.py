# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import os.path

from setuptools import setup, find_packages

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """ Find the version of ovos-core"""
    version = None
    version_file = os.path.join(BASEDIR, 'mycroft', 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'OVOS_VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'OVOS_VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'OVOS_VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'OVOS_VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if int(alpha):
        version += f"a{alpha}"
    return version


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name='ovos-core',
    version=get_version(),
    license='Apache-2.0',
    url='https://github.com/OpenVoiceOS/ovos-core',
    description='mycroft-core packaged as a library',
    install_requires=required('requirements/minimal.txt'),
    extras_require={
        'audio': required('requirements/extra-audiobackend.txt'),
        'mark1': required('requirements/extra-mark1.txt'),
        'PHAL': required('requirements/extra-PHAL.txt'),
        'stt': required('requirements/extra-stt.txt'),
        'tts': required('requirements/extra-tts.txt'),
        "skills_lgpl": required('requirements/extra-skills-lgpl.txt'),
        'skills': required('requirements/extra-skills.txt'),
        'gui': required('requirements/extra-gui.txt'),
        'bus': required('requirements/extra-bus.txt'),
        'deprecated': required('requirements/extra-deprecated.txt'),
        'all': required('requirements/requirements.txt')
    },
    packages=find_packages(include=['mycroft*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mycroft-speech-client=mycroft.listener.__main__:main',
            'mycroft-messagebus=mycroft.messagebus.service.__main__:main',
            'mycroft-skills=mycroft.skills.__main__:main',
            'mycroft-audio=mycroft.audio.__main__:main',
            'mycroft-echo-observer=mycroft.messagebus.client.ws:echo',
            'mycroft-audio-test=mycroft.util.audio_test:main',
            'mycroft-enclosure-client=ovos_PHAL.__main__:main',
            'mycroft-cli-client=mycroft.client.text.__main__:main',
            'mycroft-gui-service=mycroft.gui.__main__:main'
        ]
    }
)
