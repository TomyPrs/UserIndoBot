# UserindoBot
# Copyright (C) 2020  UserindoBot Team, <https://github.com/MoveAngel/UserIndoBot.git>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from enum import IntEnum, unique

from telegram import Message

from ubotindo.modules.helper_funcs.string_handling import button_markdown_parser


@unique
class Types(IntEnum):
    TEXT = 0
    BUTTON_TEXT = 1
    STICKER = 2
    DOCUMENT = 3
    PHOTO = 4
    AUDIO = 5
    VOICE = 6
    VIDEO = 7


def get_note_type(msg: Message):
    data_type = None
    content = None
    text = ""
    raw_text = msg.text or msg.caption
    # use python's maxsplit to separate cmd and args
    args = raw_text.split(None, 2)
    note_name = args[1]

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if len(args) >= 3:
        offset = len(args[2]) - len(
            raw_text
        )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            args[2],
            entities=msg.parse_entities() or msg.parse_caption_entities(),
            offset=offset,
        )
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    elif msg.reply_to_message:
        entities = msg.reply_to_message.parse_entities()
        msgtext = msg.reply_to_message.text or msg.reply_to_message.caption
        if len(args) >= 2 and msg.reply_to_message.text:  # not caption, text
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            if buttons:
                data_type = Types.BUTTON_TEXT
            else:
                data_type = Types.TEXT

        elif msg.reply_to_message.sticker:
            content = msg.reply_to_message.sticker.file_id
            data_type = Types.STICKER

        elif msg.reply_to_message.document:
            content = msg.reply_to_message.document.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.DOCUMENT

        elif msg.reply_to_message.photo:
            # last elem = best quality
            content = msg.reply_to_message.photo[-1].file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.PHOTO

        elif msg.reply_to_message.audio:
            content = msg.reply_to_message.audio.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.AUDIO

        elif msg.reply_to_message.voice:
            content = msg.reply_to_message.voice.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VOICE

        elif msg.reply_to_message.video:
            content = msg.reply_to_message.video.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VIDEO

    return note_name, text, data_type, content, buttons


# note: add own args?
def get_welcome_type(msg: Message):
    data_type = None
    content = None
    text = ""
    raw_text = msg.text or msg.caption
    args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if len(args) >= 2:
        offset = len(args[1]) - len(raw_text)  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(args[1], entities=msg.parse_entities() or msg.parse_caption_entities(),
                                               offset=offset)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    elif msg.reply_to_message:
        entities = msg.reply_to_message.parse_entities()
        msgtext = msg.reply_to_message.text or msg.reply_to_message.caption
        if len(args) >= 1 and msg.reply_to_message.text:  # not caption, text
            text, buttons = button_markdown_parser(msgtext,
                                                   entities=entities)
            if buttons:
                data_type = Types.BUTTON_TEXT
            else:
                data_type = Types.TEXT

        elif msg.reply_to_message.sticker:
            content = msg.reply_to_message.sticker.file_id
            data_type = Types.STICKER

        elif msg.reply_to_message.document:
            content = msg.reply_to_message.document.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.DOCUMENT

        elif msg.reply_to_message.photo:
            content = msg.reply_to_message.photo[-1].file_id  # last elem = best quality
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.PHOTO

        elif msg.reply_to_message.audio:
            content = msg.reply_to_message.audio.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.AUDIO

        elif msg.reply_to_message.voice:
            content = msg.reply_to_message.voice.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VOICE

        elif msg.reply_to_message.video:
            content = msg.reply_to_message.video.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VIDEO

        elif msg.reply_to_message.video_note:
            content = msg.reply_to_message.video_note.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VIDEO_NOTE

    return text, data_type, content, buttons


def get_filter_type(msg: Message):

    if not msg.reply_to_message and msg.text and len(msg.text.split()) >= 3:
        content = None
        text = msg.text.split(None, 2)[2]
        data_type = Types.TEXT

    elif (
        msg.reply_to_message
        and msg.reply_to_message.text
        and len(msg.text.split()) >= 2
    ):
        content = None
        text = msg.reply_to_message.text
        data_type = Types.TEXT

    elif msg.reply_to_message and msg.reply_to_message.sticker:
        content = msg.reply_to_message.sticker.file_id
        text = None
        data_type = Types.STICKER

    elif msg.reply_to_message and msg.reply_to_message.document:
        content = msg.reply_to_message.document.file_id
        text = msg.reply_to_message.caption
        data_type = Types.DOCUMENT

    elif msg.reply_to_message and msg.reply_to_message.photo:
        # last elem = best quality
        content = msg.reply_to_message.photo[-1].file_id
        text = msg.reply_to_message.caption
        data_type = Types.PHOTO

    elif msg.reply_to_message and msg.reply_to_message.audio:
        content = msg.reply_to_message.audio.file_id
        text = msg.reply_to_message.caption
        data_type = Types.AUDIO

    elif msg.reply_to_message and msg.reply_to_message.voice:
        content = msg.reply_to_message.voice.file_id
        text = msg.reply_to_message.caption
        data_type = Types.VOICE

    elif msg.reply_to_message and msg.reply_to_message.video:
        content = msg.reply_to_message.video.file_id
        text = msg.reply_to_message.caption
        data_type = Types.VIDEO

    elif msg.reply_to_message and msg.reply_to_message.video_note:
        content = msg.reply_to_message.video_note.file_id
        text = None
        data_type = Types.VIDEO_NOTE

    else:
        text = None
        data_type = None
        content = None

    return text, data_type, content
