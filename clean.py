#!/usr/bin/python

import os
import re
from collections import namedtuple

LOG_ROTATE_FILES_LIMIT = 5
LOGS_PATH = "/var/log/agents/"
LOGS_RE = re.compile("^(.*)-(\d*)(\.log)*((\.\d+)?\.gz)*$")
LogFile = namedtuple("LogFile", ["file_path", "file_ctime", "agent_pid"])

def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def get_filenames():
    """ Return list of filenames of agents logs """
    (_, _, filenames) = os.walk(LOGS_PATH).next()
    return filenames

def get_agents(filenames):
    """ Return dictionary <agent_name>:LogFile """
    agents = dict()
    for file_name in filenames:
        file_path = os.path.join(LOGS_PATH, file_name)
        file_ctime = os.path.getctime(file_path)
        match = LOGS_RE.match(file_name)
        if match is None:
            print("Cannot parse filename {}".format(file_name))
            continue
        agent_name, agent_pid, _, _, _ = match.groups()
        if not agent_name or not agent_pid:
            print("Cannot parse filename {}: agent_name '{}', agent_pid '{}'".format(file_name, agent_name, agent_pid))
            continue
        log_file = LogFile(file_path, file_ctime, int(agent_pid))
        if agent_name in agents:
            agents[agent_name].append(log_file)
        else:
            agents[agent_name] = [log_file]
    return agents

def get_files_paths_to_remove(agents):
    """ Return all but youngest LOG_ROTATE_FILES_LIMIT log files paths for every agent """
    files_paths_to_remove = []
    for agent_name, log_files in agents.iteritems():
        log_files.sort(key=lambda x: x.file_ctime)
        old_log_files = log_files[:-LOG_ROTATE_FILES_LIMIT]
        files_paths_to_remove += [f.file_path for f in old_log_files]
    return files_paths_to_remove

def remove_files(files_paths):
    for file_path in files_paths:
        os.remove(file_path)
        print("{} removed".format(file_path))

assert os.path.isdir(LOGS_PATH), "'{}' is not a dir".format(LOGS_PATH)
filenames = get_filenames()
agents = get_agents(filenames)
files_paths_to_remove = get_files_paths_to_remove(agents)
remove_files(files_paths_to_remove)
