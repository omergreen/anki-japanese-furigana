# -*- coding: utf-8 -*-

# This file is part of Japanese Furigana <https://github.com/obynio/anki-japanese-furigana>.
#
# Japanese Furigana is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Japanese Furigana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Japanese Furigana.  If not, see <http://www.gnu.org/licenses/>.

import json
import re

from aqt.qt import *

from anki.buildinfo import version

class Selection:

    js_get_html = u"""
        var selection = window.getSelection();
        var range = selection.getRangeAt(0);
        var div = document.createElement('div');
        div.appendChild(range.cloneContents());
        div.innerHTML;
    """

    def __init__(self, window, callback):
        self.window = window
        self.setHtml(None, callback)

    def isDeprecated(self):
        return int(version.replace('.', '')) < 2141

    def setHtml(self, elements, callback, allowEmpty=False):
        self.selected = elements
        if self.selected == None:
            if self.isDeprecated():
                self.window.web.eval("setFormat('selectAll');")
                self.window.web.page().runJavaScript(self.js_get_html, lambda x: self.setHtml(x, callback, True))
            else:
                self.window.web.page().runJavaScript("getCurrentField().fieldHTML", lambda x: self.setHtml(x, callback, True))
            return
        self.selected = self.convertMalformedSpaces(self.selected)
        callback(self)

    def convertMalformedSpaces(self, text):
        return re.sub(r'& ?nbsp ?;', ' ', text)

    def modify(self, html):
        html = self.convertMalformedSpaces(html)
        if self.isDeprecated():
            self.window.web.eval("setFormat('insertHTML', %s);" % json.dumps(html))
        else:
            self.window.web.page().runJavaScript("getCurrentField().fieldHTML = %s;" % json.dumps(html))
