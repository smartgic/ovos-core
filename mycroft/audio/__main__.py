# Copyright 2017 Mycroft AI Inc.
#
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
from mycroft.audio.service import PlaybackService, on_ready, on_error, on_stopping
from ovos_config.locale import setup_locale
from mycroft.lock import Lock as PIDLock  # Create/Support PID locking file
from mycroft.util import reset_sigint_handler, wait_for_exit_signal, \
    check_for_signal

service = None  # Added for backwards-compat.


def main(ready_hook=on_ready, error_hook=on_error, stopping_hook=on_stopping,
         watchdog=lambda: None):
    global service
    """Start the Audio Service and connect to the Message Bus"""
    reset_sigint_handler()
    check_for_signal("isSpeaking")
    PIDLock("audio")
    setup_locale()
    service = PlaybackService(ready_hook=ready_hook, error_hook=error_hook,
                              stopping_hook=stopping_hook, watchdog=watchdog)
    service.daemon = True
    service.start()
    wait_for_exit_signal()
    service.shutdown()


if __name__ == '__main__':
    main()
