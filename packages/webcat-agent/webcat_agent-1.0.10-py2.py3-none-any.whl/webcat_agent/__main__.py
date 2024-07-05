#!/usr/bin/env python3
# WebCat Agent (c) Clouden Oy 2024
from configparser import ConfigParser
from pathlib import Path
import urllib.request
import os
import sys
import json
import uuid
import argparse
import subprocess
import getpass

AGENT_VERSION = '1.0.10'
APP_NAME = 'webcat-agent'
OS_RELEASE_MAPPING = {
    'PRETTY_NAME': 'osPrettyName',
    'NAME': 'osName',
    'VERSION_ID': 'osVersionId',
    'VERSION': 'osVersion',
    'VERSION_CODENAME': 'osVersionCodename',
    'ID': 'osId',
    'ID_LIKE': 'osIdLike',
    'SUPPORT_END': 'osSupportEnd',
}

def get_config_dir():
    if 'APPDATA' in os.environ:
        return os.path.join(os.environ['APPDATA'], APP_NAME)
    elif 'XDG_CONFIG_HOME' in os.environ:
        return os.path.join(os.environ['XDG_CONFIG_HOME'], APP_NAME)
    else:
        return os.path.expanduser('~/.config/' + APP_NAME)

def read_config():
    config_dir = get_config_dir()
    config = ConfigParser()
    config.read(os.path.join(config_dir, 'webcat-agent.ini'))
    return config

def write_config(config):
    config_dir = get_config_dir()
    Path(config_dir).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(config_dir, 'webcat-agent.ini'), 'w') as configfile:
        config.write(configfile)

def create_cronjob():
    if os.geteuid() == 0:
        # Root cronjob
        if os.path.exists('/etc/cron.d'):
            if not os.path.exists('/etc/cron.d/webcat-agent'):
                with open('/etc/cron.d/webcat-agent', 'w') as f:
                    f.write('0 * * * * root ' + sys.executable + ' -m webcat_agent run\n')
        else:
            print('Cronjob directory /etc/cron.d not found')
    else:
        # User cronjob
        subprocess.run(['crontab -l|(grep -v webcat_agent;echo "0 * * * * ' + sys.executable +' -m webcat_agent run")|crontab -'], shell=True)

def send_system_info(config, system_info):
    url = config.get('webcat-agent', 'api_url', fallback='https://apiv2.webcat.fi/servers-api/update-system')
    system_id = config.get('webcat-agent', 'system_id')
    url += '/' + system_id
    data = json.dumps(system_info).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config.get('webcat-agent', 'api_key'),
    }
    req = urllib.request.Request(url, headers=headers, data=data, method='PUT')
    with urllib.request.urlopen(req) as res:
        response_data = res.read().decode('utf-8')
        if res.status != 200:
            print('Error sending system info:', response_data)

def collect_kernel_info(config, system_info):
    uname = os.uname()
    system_info['name'] = uname.nodename
    system_info['hostname'] = uname.nodename
    system_info['kernelName'] = uname.sysname
    system_info['kernelRelease'] = uname.release
    system_info['kernelVersion'] = uname.version
    system_info['machine'] = uname.machine
    try:
        system_info['memory'] = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    except:
        pass

def collect_os_release_info(config, system_info):
    os_release_file = '/etc/os-release'
    if os.path.exists(os_release_file):
        with open(os_release_file, 'r') as f:
            for line in f:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    key = parts[0]
                    value = parts[1].strip('"')
                    if key in OS_RELEASE_MAPPING:
                        system_info[OS_RELEASE_MAPPING[key]] = value

def collect_os_misc_info(config, system_info):
    reboot_required = os.path.exists('/var/run/reboot-required')
    system_info['osRebootRequired'] = reboot_required
    system_info['osPackageUpdates'] = None
    system_info['osSecurityUpdates'] = None
    if os.path.exists('/usr/lib/update-notifier/apt-check'):
        apt_check = subprocess.run(['/usr/lib/update-notifier/apt-check'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_buf = apt_check.stdout.decode('utf-8').strip()
        stderr_buf = apt_check.stderr.decode('utf-8').strip()
        apt_check_output = (stdout_buf + stderr_buf).split(';')
        if len(apt_check_output) == 2:
            system_info['osPackageUpdates'] = int(apt_check_output[0])
            system_info['osSecurityUpdates'] = int(apt_check_output[1])

def main():
    parser = argparse.ArgumentParser(
                    prog='webcat-agent',
                    description='WebCat Agent collects system information and sends it to WebCat API',
                    epilog='Copyright (C) Clouden Oy 2024')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s %(AGENT_VERSION)s') # Update in pyproject.toml
    parser.add_argument('--api-key', '-k', help='API key for WebCat API')
    parser.add_argument('--api-url', '-u', help='API URL for WebCat API')
    parser.add_argument('--system-id', '-i', help='System ID for WebCat API')
    parser.add_argument('--yes', '-y', action='store_true', help='Answer yes to all questions')
    parser.add_argument('command', choices=['install', 'run', 'config'], help='Command to run')
    args = parser.parse_args()

    if 'version' in args and args.version:
        print(args.version)
        return

    api_key = args.api_key
    api_url = args.api_url
    system_id = args.system_id

    if os.geteuid() == 0 and not args.yes:
        print('Running as root, continue? [y/N]', end=' ')
        if input().strip().lower() != 'y':
            print('Aborted.')
            sys.exit(1)

    config = read_config()
    if not config.has_section('webcat-agent'):
        config.add_section('webcat-agent')
        write_config(config)

    if not api_key:
        api_key = config.get('webcat-agent', 'api_key', fallback=None)

    if not system_id:
        system_id = config.get('webcat-agent', 'system_id', fallback=None)

    if args.command == 'config':
        print('config_file:', os.path.join(get_config_dir(), 'webcat-agent.ini'))
        print('api_key:', api_key)
        if api_url:
            print('api_url:', api_url)
        print('system_id:', system_id)
        return

    if args.command == 'install':
        print('Installing WebCat Agent...')
        print('Configuration file:', os.path.join(get_config_dir(), 'webcat-agent.ini'))
        if not api_key:
            print('Please enter your API key:', end=' ')
            api_key = input().strip()
            if not api_key:
                print('API key not set. Exiting.')
                sys.exit(2)
        config.set('webcat-agent', 'api_key', api_key)
        if api_url:
            config.set('webcat-agent', 'api_url', api_url)
        if system_id:
            config.set('webcat-agent', 'system_id', system_id)
        write_config(config)
        create_cronjob()
        print('WebCat Agent installed.')
        # Run once after install

    if not api_key:
        print('API key not set. Please run webcat-agent install.')
        sys.exit(2)

    if not system_id:
        system_id = str(uuid.uuid4())
        config.set('webcat-agent', 'system_id', system_id)
        write_config(config)

    agent_user = 'unknown'
    try:
        agent_user = getpass.getuser()
    except:
        pass

    system_info = {
        'agentVersion': AGENT_VERSION,
        'agentUser': agent_user,
        'systemId': system_id,
    }

    try:
        collect_kernel_info(config, system_info)
    except Exception as e:
        print('Error collecting kernel info:', e)
        pass
    try:
        collect_os_release_info(config, system_info)
    except Exception as e:
        print('Error collecting os-release info:', e)
        pass
    try:
        collect_os_misc_info(config, system_info)
    except Exception as e:
        print('Error collecting os misc info:', e)
        pass
    send_system_info(config, system_info)

if __name__ == '__main__':
    main()
