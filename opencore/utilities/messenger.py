# Copyright (C) 2008-2009 Open Society Institute
#               Thomas Moroz: tmoroz.org
#               2010-2011 Large Blue
#               Fergus Doyle: fergus.doyle@largeblue.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License Version 2 as published
# by the Free Software Foundation.  You may not use, modify or distribute
# this program under any other version of the GNU General Public License.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from __future__ import with_statement

import os

from zope.interface import implements
from zope.component import queryUtility
from repoze.bfg.interfaces import ISettings
from repoze.bfg.settings import asbool
from opencore.utils import find_site
from opencore.utilities.interfaces import IMessenger
from opencore.utilities.mbox import Mailbox
from opencore.utilities.message import MboxMessage
import logging

log = logging.getLogger(__name__)

def messenger_factory(os=os): # accepts 'os' for unit test purposes
    """Factory method for creating an instance of IMessenger
    for use by this application.
    """
    settings = queryUtility(ISettings)

    # If settings utility not present, we are probably testing and should
    # suppress sending mail.  Can also be set explicitly in environment
    # variable
    suppress_messenger = asbool(os.environ.get('SUPPRESS_MESSENGER', ''))

    if settings is None or suppress_messenger:
        return FakeMessenger()
 
    return Messenger()


class Messenger(object):
    implements(IMessenger)

    def send(self, mfrom, profile, msg):
        root = find_site(profile)
        queue = Mailbox.open_queue(root, profile.__name__)
        if not isinstance(msg, MboxMessage):
            try:
                msg = MboxMessage(msg)
            except Exception, e:
                log.warning('Unable to convert to MboxMessage from  received '
                            'type (%s)' % msg.__class__.__name__) 
                raise e   
        msg['from'] = mfrom
        queue.add(msg)   

class FakeMessenger:
    implements(IMessenger)

    def __init__(self, quiet=True):
        self.quiet = quiet

    def send(self, mfrom, profile, msg):
        if not self.quiet:
            log.info('Sent Message=%s, From=%s, To=%s' % (msg,
              mfrom, profile.__name__))
          

