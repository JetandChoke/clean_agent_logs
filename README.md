# clean_agent_logs
Cleanup  /var/log/agent/example-agent-PID in case some agents tend to crash and logrotate doesn't make any difference

In case an agent is crashing and producing a lot of output into its log file:
/var/log/agent/example-agent-PID the systems memory can feel up with a big
number of bulky agnet log files and cause OOM event.
To address this problen this script is checking if the file names in
/var/log/agents are matching currently active PIDs. If a process has restarted
multiple times - only the last five files per agent will be kept, if there is
an archive of the logs of a long running agent, then these files are counted as
well. This will let you preserve some level of historical visibility.

Script is triggered on-logging when an agent restart is determined as per the
event-handler config below.

event-handler sk1
action bash sudo python /mnt/flash/clean.py
delay 0
!
trigger on-logging
regex initialized

This is going without the explanation:

event handler config should be copied to startup config
scipt has to be maintained in flash or drive to preser it over a reboot
