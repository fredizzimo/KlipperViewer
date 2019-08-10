# Viewer for Klipper toolpaths
# Copyright (C) 2019  Fred Sundvik
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import absolute_import
from .msgproto import MessageParser

class SerialParser(object):
    def __init__(self, serial, dictionary, logger):
        self.serial = serial
        self.dictionary = dictionary
        self.logger = logger
    
    def parse(self):
        with open(self.dictionary, "rb") as f:
            dictionary = f.read()

        mp = MessageParser()
        mp.process_identify(dictionary, decompress=False)
        self.messages = []

        with open(self.serial, "rb") as f:
            data = ""
            while True:
                newdata = f.read(4096)
                if len(newdata) == 0:
                    break
                data += newdata
                while True:
                    l = mp.check_packet(data)
                    if l == 0:
                        break
                    if l < 0:
                        self.logger.error("Invalid data")
                        data = data[-l:]
                        continue
                    self.messages += mp.dump(bytearray(data[:l]))
                    data = data[l:]
        for m in self.messages[:50]:
            self.logger.info(m)