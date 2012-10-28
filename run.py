#!/usr/bin/env python
from jail import Jail
import du

def preform_verfication(challange, challange_archive, code_archive):

    tmp_dir = "/tmp/"

    """
    deflate code
    """
    challange_dir = challange_archive + "/"
    code_dir = code_archive + "/"

    """
    if challange needs build
        * deflate challange buildscript
        * create jail
        * compile in jail
    """

    if challange["needs_build"]:

        with Jail() as build_jail:

            build_jail.copy_in(code_dir + "/src", "/opt/src")
            build_jail.copy_in(challange_dir + "/build", "/opt")

            build_jail.execute("make -C /opt")

            build_jail.copy_out("/opt/bin", tmp_dir)

    """
    perfom correctness check
        * start challange code
        * start 
    """


    """
    # perform checks (following possible):
        * binary size
        * benchmark (given by challange)
    """

    for check in challange["checks"]:

        if check == "binary_size":
            a = pbs.du("-s", tmp_dir)



if __name__ == '__main__':


