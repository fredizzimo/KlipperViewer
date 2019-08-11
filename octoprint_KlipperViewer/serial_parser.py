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
        self.raw_messages = []

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
                    self.messages += mp.parse_packet(bytearray(data[:l]))
                    self.raw_messages += mp.dump(bytearray(data[:l]))
                    data = data[l:]
        self.generate_coordinates()

    def generate_coordinates(self):
        for m in self.messages:
            name = m["#name"]
            if name == "allocate_oids":
                num_oids = m["count"]
                current_clock = [0 for _ in range(num_oids)]
                current_step = [0 for _ in range(num_oids)]
                step_dir = [1 for _ in range(num_oids)]
                self.steps = [[] for _ in range(num_oids)]
            elif name == "reset_step_clock":
                oid = m["oid"]
                current_clock[oid] = m["clock"]
            elif name == "set_next_step_dir":
                oid = m["oid"]
                d = m["dir"]
                step_dir[oid] = 1 if d == 0 else -1 
            elif name == "queue_step":
                oid = m["oid"]
                interval = m["interval"]
                count = m["count"]
                add = m["add"]
                time = current_clock[oid]
                d = step_dir[oid]
                for _ in range(count):
                    current_step[oid] += d
                    time += interval
                    self.steps[oid].append((time, current_step[oid]))
                    interval += add
                current_clock[oid] = time