---
title:
linkTitle: Green Documentation
layout: green-home
toc: false
---

## Pauli administration cheat-sheet

{{< tabs items="Slurm, Nodes administartion" >}}

{{< tab >}}

### Job-related commands
 - Changing job timelimit
```
scontrol update jobid <id of the job> timelimit=<hh:mm:ss>
```
 - Change timelimit for all jobs of specific user
```
for i in $(squeue -u <username> -h -t PD -o %i) ; do scontrol update jobid $i qos=special timelimit=<hh:mm:ss>; done
```

Other job properties can also be changed same way. Ususally it is useful to change the following properties:
 - `qos` - if the default qos is not sufficient
 - `partition` - if the job has been submitted to a wrong partition (this could be useful if other partition became available)
 - `timelimit` - if the initial time was not enough (useful for already running jobs, if job is pending, highly likely it will never start if the new timelimit exceeds the qos timelimit)


### Node-related commands
 - Restart node using slurm (Slurm will wait for jobs that are currently running on selected node to be finished)
```
scontrol reboot ASAP <node name>
```
 - If, after some hanging job, the node's state is `down`, new jobs will not use it, to return it back to normal state use
```
scontrol update nodename=<nodename> state=resume
```


{{< /tab >}}
{{< tab >}}
### Work with nodes

 - Print current nodes configuration
```
wwsh provision print
```
 - Add new node (note that we have explicit suffix `-ctl` for the name of the node)
```
wwsh node new <nodename>-ctl -n <nodename>-ctl --netdev=<name of the control network interface, usually some eth#> \
     --hwaddr=<MAC address of the network interface> --netmask=255.255.255.0 --gateway=192.168.2.100 \
     --ipaddr=<IP address of the control network interface> --mtu=1500
```
 - Configure the image and extra files that node should use
```
wwsh provision set <nodename>-ctl --bootstrap=<kernel image> --vnfs=<OS image> --files=admin,authorized_keys,dynamic_hosts,group,lmod.sh,munge.key,passwd,shadow,slurm.conf,slurm.epilog.clean,ifcfg-eth2,ifcfg-eth3
done
```
we have default kernel image to be `5.4.257-1.el8.elrepo.x86_64`. For CPU nodes the OS image should be `centos8.6`, and for GPU nodes `centos8.6_GPU`. Since we have heterogenous cluster,
configuration for different node contain different set of files (especially network-related), please see the nodes configuration.

 - For most nodes we have two additional networks. One for IO (192.168.4.0/24) and one for MPI communication (192.168.5.0/24). In case it is needed, to add new network interface use
```
wwsh node set <nodename>-ctl --netdev=<interface name> --ipaddr=<IP address> --hwaddr=<MAC address of the network device> \
                --mtu=9000 --netmask=255.255.255.0 --gateway=<gateway address either 192.168.4.100 or 192.168.5.100>
```

### Work with custom files

 - List all custom files stored in Warewulf database
```
wwsh file list
```
 - Print the content of the file
```
wwsh file show <filename>
```
 - Print properties of the file
```
wwsh file print <filename>
```
 - Update file content from the original file
```
wwsh file resync <filename>
```

### Software management

In most cases, all the software that is used on nodes is installed in `/opt/ohpc/pub` on master node and is mounted during the boot.
However, in some cases some system software needs to be installed (for example to do I/O profiling). To do that, follow this multi-step
instruction

 - Install package into the OS-image copy
```
dnf --nogpgcheck --installroot /opt/ohpc/admin/images/<image name> install <package name>
```
We have to common OS image names `centos8.6` for CPU nodes, and  `centos8.6_GPU` for GPU nodes.

 - Update warewulf image
```
wwvnfs --chroot=/opt/ohpc/admin/images/<image name>
```

 - Reboot node either using slurm, or by login on node and call reboot, or with IPMI
```
ipmitool -I lanplus -H <node IPMI IP-address> -U <IPMI Admin name> power reset
```

{{< /tab >}}

{{< /tabs >}}