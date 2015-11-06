# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import datetime

from sopel.logger import get_logger


LOGGER = get_logger(__name__)

PRIVMSG_TMPL = '{datetime} <{nick}> {message}'
ACTION_TMPL = '{datetime} * {nick} {message}'
NOTICE_TMPL = '{datetime} -{nick}- {message}'
NICK_TMPL = '{datetime} *** {nick} is now known as {sender}'
JOIN_TMPL = '{datetime} *** Joins: {nick} ({ident}@{host})'
PART_TMPL = '{datetime} *** Parts: {nick} ({ident}@{host}) ({message})'
QUIT_TMPL = '{datetime} *** Quits: {nick} ({ident}@{host}) ({message})'
KICK_TMPL = '{datetime} *** {nick} was kicked by {sender} ({message})'
MODE_TMPL = '{datetime} *** {nick} sets mode: {args_str}'


def preformat(bot, trigger, channel):
    event = {
        'channel':  channel,
        'type':     trigger.event,
        'message':  trigger.match.string,
        'nick':     trigger.nick,
        'ident':    trigger.user,
        'host':     trigger.host,
        'sender':   trigger.sender,
        'datetime': datetime.datetime.utcnow().isoformat(),
        'date':     datetime.datetime.utcnow().date().isoformat(),
        'time':     datetime.datetime.utcnow().time().isoformat(),
        'args':     trigger.args,
        'args_str': ' '.join(trigger.args[1:]),
        'tags':     trigger.tags,
        'intent':   None
    }

    if event['message'].startswith("\001ACTION ") and event['message'].endswith("\001"):
        event['type'] = 'ACTION'
        event['message'] = event['message'][8:-1]

    if 'intent' in trigger.tags:
        event['intent'] = trigger.tags['intent']
    return event


def format(bot, event):
    if 'type' not in event:
        raise ValueError('Event type was unspecified!')

    if getattr(bot.config.chanlogs2, event['type'].lower() + '_template'):
        return getattr(bot.config.chanlogs2, event['type'].lower() + '_template').format(**event)

    if event['type'].upper() + '_TMPL' not in globals():
        LOGGER.warn('No template defined for \'{type}\''.format(event['type'].upper()))

    return globals()[event['type'].upper() + '_TMPL'].format(**event)