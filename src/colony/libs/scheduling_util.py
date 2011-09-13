#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time
import threading

DEFAULT_SLEEP_STEP = 0.5
""" The default sleep step to be used in the scheduler """

class Scheduler(threading.Thread):
    """
    Class that implements a scheduler to be used
    to "call" callable objects for a provided timestamp.
    """

    sleep_step = None
    """ The amount of time to be used during a sleep iteration """

    continue_flag = True
    """ Flag controlling the execution of the scheduler """

    timestamp_queue = []
    """ Ordered list (queue) of timestamps for callables """

    timestamp_map = {}
    """ The map associating the timestamp with a list of callables """

    def __init__(self, sleep_step = DEFAULT_SLEEP_STEP):
        """
        Constructor of the class.

        @type plugin: Plugin
        @param plugin: The plugin to be used.
        @type sleep_step: float
        @param sleep_step: The amount of time to be used
        during a sleep iteration.
        """

        threading.Thread.__init__(self)

        self.sleep_step = sleep_step

        self.timestamp_queue = []
        self.timestamp_map = {}

    def run(self):
        # iterates while the continue
        # flag is set
        while self.continue_flag:
            # retrieves the current timestamp
            current_timestamp = time.time()

            # iterates over the timestamp queue
            while True:
                # in case the timestamp queue is invalid
                # (possibly empty)
                if not self.timestamp_queue:
                    # breaks the loop (no more work
                    # to be processed for now)
                    break

                # retrieves the timestamp from the
                # timestamp queue
                timestamp = self.timestamp_queue[0]

                # in case the final timestamp has been
                # reached
                if current_timestamp < timestamp:
                    # breaks the loop (no more work
                    # to be processed for now)
                    break

                # retrieves the callable (elements) list
                # for the timestamp
                callable_list = self.timestamp_map[timestamp]

                # iterates over all the callables to call
                # them
                for callable in callable_list:
                    # calls the callable (element)
                    callable()

                # removes the callable list for the timestmap
                del self.timestamp_map[timestamp]

                # pops (removes first element) the timestamp
                # from the timestamp queue
                self.timestamp_queue.pop(0)

            # ACABA AKI O LOCK

            # sleeps for the amount of time defined
            # in the sleep step
            time.sleep(self.sleep_step)

    def start_scheduler(self):
        # sets the continue flag
        self.continue_flag = True

        # starts the thread
        self.start()

    def stop_scheduler(self):
        # unsets the continue flag
        self.continue_flag = False

    def clear_scheduler(self, callable):
        self.continue_flag = True
        self.timestamp_queue = []
        self.timestamp_map = {}

    def add_callable(self, callbable, timestamp):
        callable_list = self.timestamp_map.get(timestamp, [])
        callable_list.append(callbable)
        self.timestamp_map[timestamp] = callable_list

        # starts the index value
        index = 0

        for _timestamp in self.timestamp_queue:
            if timestamp < _timestamp:
                break

            # increments the index
            index += 1

        # insets the timestamp in the timestamp queue
        # for the correct index (in order to maintain order)
        self.timestamp_queue.insert(index, timestamp)