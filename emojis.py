# !/usr/bin/env python
# Copyright (c) 2013 Alexandre Gauthier
#
# Some rights reserved.
#
# Redistribution and use in source and binary forms of the software as well
# as documentation, with or without modification, are permitted provided
# that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided
#   with the distribution.
#
# THIS SOFTWARE AND DOCUMENTATION IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE AND DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

import os
import re
import sys

# I'm sorry.
try:
    import weechat
except ImportError:
    print "This is a WeeChat Script - http://www.weechat.org"
    print "It makes no sense to run it on its own."
    sys.exit(1)


# Global / Static script values
SCRIPT_NAME = "emojis"
SCRIPT_AUTHOR = "Alexandre Gauthier <alex@underwares.org>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "BSD"
SCRIPT_DESCRIPTION = "Allows you to spam emojis based on :triggers:"

SCRIPT_SETTINGS = {
    'dbfile': "emojis-db.dat",
}

EMOJIS = {}

def load_emojis(dbfile):
    """ Load emojis from file """

    global EMOJIS

    with open(dbfile) as f:
        for line in f:
            if line.startswith(':'):
                EMOJIS[line.rstrip()] = f.next().rstrip()
            else:
                weechat.prnt("", "%sMalformed line in %s: %s" \
                        % (weechat.prefix("error"), f.name, line))


    weechat.prnt("", "%s[%s] Loaded %d knifaisms." \
            % (weechat.prefix("action"), SCRIPT_NAME, len(EMOJIS))
    )

def reload_emojis():
    global EMOJIS

    weechat.prnt("", "%s[%s] Reloading emojis from %s" \
            % (weechat.prefix("action"), SCRIPT_NAME,
                SCRIPT_SETTINGS["dbfile"]))

    EMOJIS = {}

    load_emojis(SCRIPT_SETTINGS["dbfile"])


def transform_cb(data, bufferptr, command):
    """ Apply transformation to input line in specified buffer """

    if command == "/input return":
        # Get input buffer. This is where we'll apply the
        # transformation right when the user hits enter. To be brutally
        # honest, I had no idea how else to make it happen.
        line = weechat.buffer_get_string(bufferptr, 'input')

        # Ignore commands
        if line.startswith('/'):
            return weechat.WEECHAT_RC_OK

        # Apply transform.
        # FIXME: I am fairly certain this is not optimal.
        for key, value in EMOJIS.iteritems():
            if key in line:
                line = line.replace(key, value)

        # Poot transform line back into buffer's input line.
        weechat.buffer_set(bufferptr, 'input', line)

    return weechat.WEECHAT_RC_OK

def configuration_cb(data, option, value):
    """ Configuration change callback """

    global SCRIPT_SETTINGS

    pos = option.rfind('.')

    if pos > 0:
        key = option[pos+1:]
        if key in SCRIPT_SETTINGS:
            SCRIPT_SETTINGS[key] = value

    return weechat.WEECHAT_RC_OK


def completion():
    pass

def main():
    """ Entry point, initializes everything  """

    weechat.register(
        SCRIPT_NAME,
        SCRIPT_AUTHOR,
        SCRIPT_VERSION,
        SCRIPT_LICENSE,
        SCRIPT_DESCRIPTION,
        "", # Shutdown callback function
        "", # Charset (blank for utf-8)
    )

    # Apply default configuration values if anything is unset
    for option, default in SCRIPT_SETTINGS.items():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, default)

    # Hook callbacks
    weechat.hook_config("plugins.var.python." + SCRIPT_NAME + ".*",
        "configuration_cb", "")
    weechat.hook_command_run("/input return", "transform_cb", "")

    weechat.prnt("", "%s[%s] Loading emojis from %s" \
            % (weechat.prefix("action"), SCRIPT_NAME,
                SCRIPT_SETTINGS["dbfile"]))

    # FIXME: throws IOError, it would be nice to handle this more
    # gracefully.
    dbpath = os.path.join(weechat.info_get("weechat_dir", ""),
        SCRIPT_SETTINGS["dbfile"])

    load_emojis(dbpath)

    weechat.prnt("", "%s[%s] Emojis initialized, version" + SCRIPT_VERSION)

if __name__ == '__main__':
    main()

