# AT-switch-ssh
Allied Telesis switch ssh automation implemented by paramiko

This scipt scans all the files under one specified folder, transfers each of them to their corresponding switch using SFTP, and then execute it on the switch to adjust switch configuration, OpenFlow rules, etc.

# Attention
1. Filename needs to be exactly same as the hostname of the target switch.

2. Since filename is used to determine the target switch here, every host can only receive one file at one time.
