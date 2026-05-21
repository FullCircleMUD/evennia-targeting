# SPDX-License-Identifier: BSD-3-Clause
"""Django AppConfig for evennia-targeting.

Currently a no-op — the library has no admin commands or models to
install. Present so consumers can add ``evennia_targeting`` to
``INSTALLED_APPS`` without Django complaining about the missing app
config.

If the library later grows a surface that needs the ``evennia._init``
wrap pattern (auto-installed admin commands, etc.), this is where it
lands — same shape as evennia-mob-spawner / evennia-world-builder /
evennia-shards.
"""
from django.apps import AppConfig


class EvenniaTargetingConfig(AppConfig):
    name = "evennia_targeting"
    default_auto_field = "django.db.models.BigAutoField"
