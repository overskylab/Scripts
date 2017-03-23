# The MIT License (MIT)
#
# Copyright (c) 2015, Red Hat, Inc. and others
# Copyright (c) 2015, Rackspace US, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ----------------------------------------------------------------------------
#
# Note that this callback plugin isn't enabled by default.  If you'd like to
# enable it, add the following line to ansible.cfg in the 'playbooks'
# directory in this repository:
#
#    callback_plugins = plugins/callbacks
#
# Add that line prior to running the playbooks and you will have detailed
# timing information for Ansible tasks right after each playbook finishes
# running.
#
# User comment
# put it to roles/plugins/callback/profile_tasks.py
# and config ansible.cfg to this roles path
#
import time


class CallbackModule(object):
    """
    A plugin for timing tasks
    """
    def __init__(self):
        self.stats = {}
        self.current = None

    def playbook_on_task_start(self, name, is_conditional):
        """
        Logs the start of each task
        """
        if self.current is not None:
            # Record the running time of the last executed task
            self.stats[self.current] = time.time() - self.stats[self.current]

        # Record the start time of the current task
        self.current = name
        self.stats[self.current] = time.time()

    def playbook_on_stats(self, stats):
        """
        Prints the timings
        """
        # Record the timing of the very last task
        if self.current is not None:
            self.stats[self.current] = time.time() - self.stats[self.current]

        # Sort the tasks by their running time
        results = sorted(self.stats.items(), key=lambda value: value[1],
                         reverse=True)

        # Just keep the top 10
        results = results[:10]
