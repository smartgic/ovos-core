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
from os.path import abspath, dirname, join
from ovos_config.config import Configuration
from mycroft.api import Api
from mycroft.messagebus.message import Message

from ovos_utils.intents import AdaptIntent, IntentBuilder, Intent
from mycroft.skills.context import adds_context, removes_context
from mycroft.skills import (MycroftSkill, FallbackSkill,
                            intent_handler, intent_file_handler)
from mycroft.util.log import LOG

MYCROFT_ROOT_PATH = abspath(join(dirname(__file__), '..'))

__all__ = ['MYCROFT_ROOT_PATH',
           'Api',
           'Message']

_cfg = Configuration()
_log_level = _cfg.get("log_level", "INFO")
_logs_conf = _cfg.get("logs") or {}
_logs_conf["level"] = _log_level
LOG.init(_logs_conf)  # read log level from config
