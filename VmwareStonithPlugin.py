#!/usr/bin/python
# vim: set filetype=python

import sys
import os
import time
import subprocess
import requests
import json


class VmwareStonithPlugin:
    def __init__(self, *args, **kargs):
        self._confignames = ['ip', 'port', 'server_id', 'authorization', 'verify']
        with open('/etc/vmware-restapi.json') as f:
            self.config = json.load(f)
        self.config['server_id'] = os.environ.get('server-id')
        self.config['nodename'] = 'app1 app2'
        self.verify = self.config.get('verify') or False
        self.api = 'https://{0}:{1}/api/vms/{2}/power'.format(
            self.config.get('ip'), self.config.get('port'),
            self.config.get('server_id'))
        self.headers = {'Accept': 'application/vnd.vmware.vmw.rest-v1+json',
                        'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json',
                        'Authorization': 'Basic '+self.config.get('authorization')}
        self.operations =  ['on', 'off', 'shutdown', 'suspend', 'pause', 'unpause']
    
    def status(self):
        res = requests.get(self.api, headers=self.headers, verify=self.verify)
        if res.status_code == 200:
            self.echo(res.json())
            return(0)
        return(res.status_code)

    def on(self):
        res = requests.put(self.api, data='on', verify=self.verify)
        if res.status_code == 200:
            return(0)
        return(res.status_code)

    def off(self):
        res = requests.put(self.api, data='off', verify=self.verify)
        if res.status_code == 200:
            return(0)
        return(res.status_code)

    def reset(self):
        res = []
        res.append(self.off())
        res.append(self.on())
        if res == [0,0]:
            return(0)
        return(sum(res))

    def gethosts(self):
        self.echo(self.config.get('nodename'))
        return(0)

    def getconfignames(self):
        self.echo('server_id')
        return(0)
    
    def getinfo_devid(self):
        self.echo("External Stonith Plugin for Vmware Workstation pro 15 and above")
        return(0)

    def getinfo_devname(self):
        self.echo("External Stonith Plugin for Vmware Workstation pro 15 and above")
        return(0)

    def getinfo_devdescr(self):
        self.echo("External Stonith Plugin for Vmware Workstation pro 15 and above")
        return(0)

    def getinfo_devurl(self):
        self.echo("https://vmware.com")
        return(0)

    def getinfo_xml(self):
        info = """<parameters>
            <parameter name="server_id" unique="1" required="1">
                <content type="string" />
                <shortdesc lang="en">vm server id</shortdesc>
                <longdesc lang="en">
                    Vmware vm server id.
                </longdesc>
            </parameter>
        </parameters>
        """
        self.echo(info)
        return(0)
    
    def echo_log(self, level, *args):
        subprocess.call(('ha_log.sh', level) +  args)

    def _echo_debug(self, *args):
        self.echo_log('debug', *args)

    def echo(self, *args):
        what = ''.join([str(x) for x in args])
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()
        self._echo_debug("STDOUT:", what)

    def process(self, argv):
        cmd = argv[0]
        try:
            cmd = cmd.lower().replace('-', '_')
            func = getattr(self, cmd, None)
            rc = func()
            return(rc)
        except Exception as e:
            self.echo(e)
            return(1)


if __name__ == '__main__':
    stonith = VmwareStonithPlugin()
    rc = stonith.process(sys.argv[1:])
    sys.exit(rc)
