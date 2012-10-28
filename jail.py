import uuid
import pbs
from string import Template
import os
import shutil


lxc = pbs.lxc
lxc_create = pbs.Command("/usr/bin/lxc-create")

cfg_template =   """
lxc.utsname = ${name}
lxc.network.type = empty

lxc.cgroup.cpuset.cpus = 0,1
lxc.cgroup.cpu.shares = 1234
lxc.cgroup.devices.deny = a
lxc.cgroup.devices.allow = c 1:3 rw
lxc.cgroup.devices.allow = b 8:0 rw

lxc.pts = 1024

lxc.rootfs = ${root}

lxc.mount.entry = none ${root}/usr aufs br:${root}:/usr=ro 0 0
lxc.mount.entry = none ${root}/var aufs br:${root}:/var=ro 0 0
lxc.mount.entry = none ${root}/bin aufs br:${root}:/bin=ro 0 0
lxc.mount.entry = none ${root}/lib aufs br:${root}:/lib=ro 0 0
lxc.mount.entry = none ${root}/lib64 aufs br:${root}:/lib64=ro 0 0
lxc.mount.entry = none ${root}/dev/pts devpts defaults 0 0
lxc.mount.entry = none ${root}/dev/shm tmpfs defaults 0 0
"""


class Jail:

    def __init__(self, conf = {}):
        self.name = conf.get("name", uuid.uuid4())
        self.root = "/home/yves/projects/coding-challange/containers/roots/" + self.name
        self.config_file = "./containers/" + self.name + ".cfg"


    def __enter__(self):

        # create config file
        with open(self.config_file,"w") as f:
            f.write(Template(cfg_template).substitute({ "name" : self.name, "root" : self.root  }))

        # create root file systems
        required_paths = [
                "/", "/usr", "/var", "/lib", "/lib64", "/bin",
                "/dev", "/dev/pts", "/proc", "/opt", "/dev/shm"
        ]

        for path in required_paths:
            os.mkdir(self.root + path)

        # create lxc container
        lxc_create(n=self.name, f=self.config_file)
        return self


    def copy_in(self, source, jail_target):
        shutil.copy(source, self.root + "/" + jail_target)


    def copy_out(self, jail_source, target):
        shutil.copy(self.root + "/" + jail_source, target)


    def execute(self, command):
        ret = lxc("execute", self.name,"-o ./log","-l DEBUG", "--", command)
        # workaround for funny behaviour
        os.remove(self.root + "/dev/ptmx")
        return ret


    def __exit__(self, type, value, traceback):

        lxc("destroy", self.name)
        shutil.rmtree(self.root)
        #os.remove(self.config_file)

