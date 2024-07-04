#!/usr/bin/env python

import os
import sys

from supervisor import childutils


class Timeout:
    def __init__(self):
        self.args = sys.argv[1:]
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.rpc = None

    def run(self):
        while 1:
            headers, payload = childutils.listener.wait(self.stdin, self.stdout)

            if not headers['eventname'].startswith('TICK'):
                # do nothing with non-TICK events
                childutils.listener.ok(self.stdout)
                continue

            process_infos = self.rpc.supervisor.getAllProcessInfo()

            for process_info in process_infos:
                pid = process_info['pid']
                name = process_info['name']
                group = process_info['group']
                uptime = process_info['now'] - process_info['start']
                self.stderr.write('PID: %s, name: %s, group %s, uptime %s' % (pid, name, group, uptime))

            self.stderr.flush()

            childutils.listener.ok(self.stdout)


def main():
    timeout = Timeout()
    timeout.rpc = childutils.getRPCInterface(os.environ)
    timeout.run()


if __name__ == '__main__':
    main()
