#! /usr/bin/python

############################################
# Program:   virt-back.py
# Author:    russell.ballestrini.net
# Date:      Fri Mar 18 15:56:59 EDT 2011
# License:   Public Domain
############################################

DESCRIPTION = """A backup utility for QEMU, KVM, XEN, and Virtualbox guests.
Virt-back is a python application that uses the libvirt api to safely 
shutdown, gzip, and restart guests.  The backup process logs to syslog
for auditing and virt-back works great with cron for scheduling outages.
Virt-back has been placed in the public domain and 
the latest version may be downloaded here:
https://git.unturf.com/python/virt-back
"""

"""The variable doms represents a list of libvirt dom objects.
Use the Domfetcher class to acquire a list of dom objects."""

import libvirt
import tarfile
import syslog
import re
from time import sleep
from datetime import date
from sys import exit
import argparse
from os import path, remove
from shutil import move, copy2
import subprocess

try:
    from operator import methodcaller
except ImportError:

    def methodcaller(name, *args, **kwargs):
        def caller(obj):
            return getattr(obj, name)(*args, **kwargs)

        return caller


class Domfetcher(object):
    """Abstract libvirt API, supply methods to return dom object lists"""

    def __init__(self, uri=None):
        """Connect to hypervisor uri with read write access"""
        # register logit as the error handler
        libvirt.registerErrorHandler(logit, "libvirt error")

        try:
            self.c = libvirt.open(uri)
        except:
            self.c = None
            logit("libvirt error", "Failed to open connection to the hypervisor")

    def get_running_doms(self):
        """Return a list of running dom objects"""
        doms = []
        for id in self.c.listDomainsID():  # loop over the running ids
            dom = self.c.lookupByID(id)  # fetch dom object by id
            if "Domain-" not in dom.name():  # prevent actions on the Xen hypervisor
                doms.append(dom)  # append dom object to doms
        return doms

    def get_shutoff_doms(self):
        """Return a list of all shutoff but defined dom objects"""
        return [self.c.lookupByName(name) for name in self.c.listDefinedDomains()]

    def get_doms_by_names(self, guest_names):
        """Accept a list of guest_names, return a list of related dom objects"""
        doms = []
        for name in guest_names:
            try:
                dom = self.c.lookupByName(name)
                doms.append(dom)
            except libvirt.libvirtError:
                pass  # logit reg'd as libvirt error handler
        return doms

    def get_all_doms(self):
        """Return a list of all dom objects"""
        return self.get_running_doms() + self.get_shutoff_doms()


def invoke(doms, method):
    """Pattern to invoke shutdown, destroy, and start on a list of doms"""
    f = methodcaller(method)
    for dom in doms:
        try:
            logit(method, "invoking %s on %s" % (method, dom.name()))
            retcode = f(dom)
            if retcode:  # log retcode
                logit(
                    method,
                    "{0} returned {1} on {2}".format(method, retcode, dom.name()),
                )
        except libvirt.libvirtError:
            pass


def backup(doms):
    """Accept a list of dom objects, run backup procedure on each"""
    for dom in doms:
        recreate = dom.isActive()

        if dom.isActive():  # if dom is active, shutdown
            shutdown([dom])

        if dom.isActive():  # if dom is active, error
            logit(
                "error",
                "unable to shutdown or destroy %s and BACKUP FAILED!" % dom.name(),
            )
            continue  # skip to the next dom

        xml = dom.XMLDesc(0)
        xmlfile = path.join(options.backpath, dom.name() + ".xml")
        with open(xmlfile, "w") as f:
            f.write(xml)

        # Updated regular expression to match file= and dev= within <disk> elements
        disklist = re.findall(
            r"<disk.*?<source (?:file|dev)='(.*?)'.*?</disk>", xml, re.DOTALL
        )

        logit("backup", "invoking backup for " + dom.name())

        for disk_source in disklist:
            if disk_source.endswith(".iso"):
                logit(
                    "backup", "skipping ISO file %s for %s" % (disk_source, dom.name())
                )
                continue

            if is_zfs_dataset(disk_source):
                # Handle ZFS dataset
                zfs_dataset = (
                    disk_source[len("/dev/zvol/") :]
                    if disk_source.startswith("/dev/zvol/")
                    else disk_source
                )
                zfs_snapshot_base = f"{zfs_dataset}@backup-{TODAY}"
                zfs_snapshot = zfs_snapshot_base
                suffix = 1

                # Increment snapshot name until an available name is found
                while (
                    subprocess.run(
                        ["zfs", "list", zfs_snapshot],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    ).returncode
                    == 0
                ):
                    zfs_snapshot = f"{zfs_snapshot_base}-{suffix}"
                    suffix += 1

                zfs_file = path.join(options.backpath, f"{dom.name()}-{TODAY}.zfs")
                if not options.nogzip:
                    zfs_file += ".gz"

                # Create ZFS snapshot
                logit(
                    "backup", f"creating ZFS snapshot {zfs_snapshot} for {dom.name()}"
                )
                try:
                    subprocess.run(["zfs", "snapshot", zfs_snapshot], check=True)
                except subprocess.CalledProcessError as e:
                    logit("error", f"Failed to create ZFS snapshot {zfs_snapshot}: {e}")
                    continue

                # Send ZFS snapshot to file with optional compression
                logit(
                    "backup",
                    f"sending ZFS snapshot {zfs_snapshot} to {zfs_file} for {dom.name()}",
                )
                try:
                    with open(zfs_file, "wb") as f:
                        if options.nogzip:
                            subprocess.run(
                                ["zfs", "send", zfs_snapshot], stdout=f, check=True
                            )
                        else:
                            send_proc = subprocess.Popen(
                                ["zfs", "send", zfs_snapshot], stdout=subprocess.PIPE
                            )
                            gzip_proc = subprocess.Popen(
                                ["gzip"], stdin=send_proc.stdout, stdout=f
                            )
                            send_proc.stdout.close()  # Allow send_proc to receive a SIGPIPE if gzip_proc exits
                            gzip_proc.communicate()
                except subprocess.CalledProcessError as e:
                    logit("error", f"Failed to send ZFS snapshot {zfs_snapshot}: {e}")
                    continue
            else:
                # Handle QCOW2 or other file-based disk
                logit("backup", f"{disk_source} is not a ZFS dataset")
                disk_file = disk_source.split("/")[-1]
                disk_dest = path.join(options.backpath, disk_file)

                logit(
                    "backup",
                    "copying %s to %s for %s" % (disk_source, disk_dest, dom.name()),
                )
                copy2(disk_source, disk_dest)

        if recreate:  # if true, start guest after backup
            create([dom])  # start dom

        ext, tarmode = ".tar.gz", "w:gz"
        if options.nogzip:
            ext, tarmode = ".tar", "w"

        tarfilename = dom.name() + ext
        if options.tardate:
            tarfilename = dom.name() + "-" + TODAY + ext

        tarpath = path.join(options.backpath, tarfilename)

        if path.isfile(tarpath):  # if file exists, run rotate
            logit("backup", "rotating backup files for " + dom.name())
            rotate(tarpath, options.retention)

        logit("backup", "archiving files for %s to %s" % (dom.name(), tarpath))
        tar = tarfile.open(tarpath, tarmode)

        logit("backup", "archiving %s for %s" % (xmlfile, dom.name()))
        tar.add(xmlfile)  # add xml to tar
        remove(xmlfile)  # cleanup tmp files

        for disk_source in disklist:
            if disk_source.endswith(".iso"):
                continue

            if is_zfs_dataset(disk_source):
                zfs_file = path.join(options.backpath, f"{dom.name()}-{TODAY}.zfs")
                if not options.nogzip:
                    zfs_file += ".gz"
                if path.isfile(zfs_file):
                    logit("backup", "archiving %s for %s" % (zfs_file, dom.name()))
                    tar.add(zfs_file)  # add zfs snapshot to tar
                    remove(zfs_file)  # cleanup tmp files
                else:
                    logit(
                        "error",
                        f"ZFS snapshot file {zfs_file} not found for {dom.name()}",
                    )
            else:
                disk_file = disk_source.split("/")[-1]
                disk_dest = path.join(options.backpath, disk_file)
                logit("backup", "archiving %s for %s" % (disk_dest, dom.name()))
                tar.add(disk_dest)  # add img to tar
                remove(disk_dest)  # cleanup tmp files

        tar.close()

        logit("backup", "finished backup for " + dom.name())


def is_zfs_dataset(disk_source):
    """Check if the disk source is a ZFS dataset"""
    logit("backup", f"checking if {disk_source} is a ZFS dataset")
    try:
        # Extract the ZFS dataset name from the device path
        if disk_source.startswith("/dev/zvol/"):
            zfs_dataset = disk_source[len("/dev/zvol/") :]
        else:
            zfs_dataset = disk_source

        result = subprocess.run(
            ["zfs", "list", zfs_dataset], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        is_zfs = result.returncode == 0
        logit("backup", f"{zfs_dataset} is {'a' if is_zfs else 'not a'} ZFS dataset")
        return is_zfs
    except Exception as e:
        logit("error", f"Error checking ZFS dataset: {e}")
        return False


def shutdown(doms, wait=180):
    """Accept a list of dom objects, attempt to shutdown the active ones"""
    # get all running guests from list and invoke shutdown
    invoke(get_all_running(doms), "shutdown")

    """loop until all guests are shut off or destroy 
       all active guests if wait timer is reached."""

    secs = 10
    wait /= secs  # divide wait by secs

    wait = int(wait)

    for i in range(0, wait + 1):

        # if all doms are shut off, leave loop
        if check_all_shutoff(doms):
            break
        else:
            logit(
                "shutdown",
                "waited "
                + str(i * secs)
                + " seconds for "
                + ", ".join(dom.name() for dom in get_all_running(doms))
                + " to shut off",
            )

        # if the wait time is reached, destroy all active doms
        if i == wait:
            invoke(get_all_running(doms), "destroy")

        sleep(secs)


def create(doms):
    """Accept a list of dom objects, attempt to start the inactive ones"""
    # get all shutoff guests from list and invoke create
    invoke(get_all_shutoff(doms), "create")


def reboot(doms):
    """Accept a list of dom objects, attempt to shutdown then start"""
    shutdown(doms)
    create(doms)


def info(doms):
    """Accept a list of dom objects, attempt to display info for all"""
    # invoke( doms, 'name' )
    # invoke( doms, 'info')
    if check_all_running(doms):
        print("NOTE: All guests are running")
    if check_all_shutoff(doms):
        print("NOTE: All guests are shut off")

    print("")
    print("running guests: " + ", ".join([dom.name() for dom in get_all_running(doms)]))
    print("shutoff guests: " + ", ".join([dom.name() for dom in get_all_shutoff(doms)]))
    print("")
    print(
        "DomName".ljust(16)
        + "Memory MB".rjust(12)
        + "vCPUs".rjust(8)
        + "CPUtime ms".rjust(18)
    )
    print("======================================================")
    for dom in doms:
        name = dom.name()
        rams = str(dom.info()[2] / 1024) + "/" + str(dom.info()[1] / 1024)
        cpus = str(dom.info()[3])
        time = str(dom.info()[4] / 1000000)
        print(name.ljust(16) + rams.rjust(12) + cpus.rjust(8) + time.rjust(18))


def check_all_running(doms):
    """Accept a list of dom objects, check if all guest dom are active"""
    if sum([dom.isActive() for dom in doms]) == len(doms):
        return True
    return False


def check_all_shutoff(doms):
    """Accept a list of dom objects, check if all guest dom are shut off"""
    if sum([dom.isActive() for dom in doms]):
        return False
    return True


def get_all_running(doms):
    """Accept a list of dom objects, return a list of running dom objects"""
    return [dom for dom in doms if dom.isActive()]


def get_all_shutoff(doms):
    """Accept a list of dom objects, return a list of shutoff dom objects"""
    return [dom for dom in doms if not dom.isActive()]


def logit(context, message, quiet=False):
    """syslog and error handler"""
    if type(message) is tuple:
        message = message[2]  # libvirt message is a tuple

    try:
        quiet = options.quiet
    except NameError:
        pass

    if quiet:
        pass
    else:
        print(context + ": " + message)

    syslog.openlog("virt-back", 0, syslog.LOG_LOCAL3)
    syslog.syslog(message)
    syslog.closelog()


def rotate(target, retention=3):
    """file rotation routine"""
    for i in range(retention - 2, 0, -1):  # count backwards
        old_name = "%s.%s" % (target, i)
        new_name = "%s.%s" % (target, i + 1)
        try:
            move(old_name, new_name)
        except IOError:
            pass
    move(target, target + ".1")


def getoptions():
    """Fetch cli args, parse and map to python, test sanity"""

    # create an argument parser object
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        default=False,
        help="prevent output to stdout",
    )

    parser.add_argument(
        "-d",
        "--date",
        dest="tardate",
        action="store_true",
        default=False,
        help="append date to tar filename [default: no date]",
    )

    parser.add_argument(
        "-g",
        "--no-gzip",
        dest="nogzip",
        action="store_true",
        default=False,
        help="do not gzip the resulting tar file",
    )

    parser.add_argument(
        "-a",
        "--retention",
        dest="retention",
        metavar="amount",
        default=3,
        type=int,
        help="backups to retain [default: 3]",
    )

    parser.add_argument(
        "-p",
        "--path",
        dest="backpath",
        metavar="'PATH'",
        default="/KVMBACK",
        help="backup path [default: '/KVMBACK']",
    )

    parser.add_argument(
        "-u", "--uri", dest="uri", metavar="'URI'", help="optional hypervisor uri"
    )

    # Actions for info testing: These options display info/ test a list of guests only.
    info_group = parser.add_argument_group(
        "Actions for info testing",
        "These options display info or test a list of guests.",
    )

    info_group.add_argument(
        "-i",
        "--info",
        dest="info",
        action="store_true",
        default=False,
        help="info/test a list of guests (space delimited dom names)",
    )

    info_group.add_argument(
        "--info-all",
        dest="infoall",
        action="store_true",
        default=False,
        help="attempt to show info on ALL guests",
    )

    # WARNING: Dangerous options below, option grouping for scary actions
    action_group = parser.add_argument_group(
        "Actions for a list of dom names",
        "WARNING:  These options WILL bring down guests!",
    )

    action_group.add_argument(
        "-b",
        "--backup",
        dest="backup",
        action="store_true",
        default=False,
        help="backup a list of guests (space delimited dom names)",
    )

    action_group.add_argument(
        "-r",
        "--reboot",
        dest="reboot",
        action="store_true",
        default=False,
        help="reboot a list of guests (space delimited dom names)",
    )

    action_group.add_argument(
        "-s",
        "--shutdown",
        dest="shutdown",
        action="store_true",
        default=False,
        help="shutdown a list of guests (space delimited dom names)",
    )

    action_group.add_argument(
        "-c",
        "--create",
        dest="create",
        action="store_true",
        default=False,
        help="start a list of guests (space delimited dom names)",
    )

    all_group = parser.add_argument_group(
        "Actions for all doms", "WARNING:  These options WILL bring down ALL guests!"
    )

    all_group.add_argument(
        "--backup-all",
        dest="backupall",
        action="store_true",
        default=False,
        help="attempt to shutdown, backup, and start ALL guests",
    )

    all_group.add_argument(
        "--reboot-all",
        dest="rebootall",
        action="store_true",
        default=False,
        help="attempt to shutdown and then start ALL guests",
    )

    all_group.add_argument(
        "--shutdown-all",
        dest="shutdownall",
        action="store_true",
        default=False,
        help="attempt to shutdown ALL guests",
    )

    all_group.add_argument(
        "--create-all",
        dest="createall",
        action="store_true",
        default=False,
        help="attempt to start ALL guests",
    )

    # parse options and args
    options, unknown_args = parser.parse_known_args()

    # the actionsum should be 1 to continue, bool math ftw
    actions = [
        options.backup,
        options.reboot,
        options.shutdown,
        options.create,
        options.info,
        options.backupall,
        options.rebootall,
        options.shutdownall,
        options.createall,
        options.infoall,
    ]
    actionsum = sum(actions)

    if actionsum == 1:
        guest_names = unknown_args
        return options, guest_names
    else:
        exit(
            "\nYou must have 1 action, no more, no less.\n\nRun 'virt-back --help' for help.\n"
        )


if __name__ == "__main__":
    TODAY = str(date.today())
    # Get the list of options and list of guest_names from cli
    options, guest_names = getoptions()
    # connect to hypervisor with Domfetcher (read-only)
    domfetcher = Domfetcher(options.uri)

    if (
        options.backup
        or options.reboot
        or options.shutdown
        or options.create
        or options.info
    ):
        doms = domfetcher.get_doms_by_names(guest_names)
    else:
        doms = domfetcher.get_all_doms()

    if options.backup or options.backupall:
        backup(doms)
    if options.reboot or options.rebootall:
        reboot(doms)
    if options.shutdown or options.shutdownall:
        shutdown(doms)
    if options.create or options.createall:
        create(doms)
    if options.info or options.infoall:
        info(doms)
