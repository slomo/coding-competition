#! /usr/bin/python2
import jail

with jail.Jail({"name" : "test"}) as j:

    print(j.execute("mount"))

    print(j.execute("hostname"))


