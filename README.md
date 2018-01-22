# Ansible ZNC [![Build Status](https://travis-ci.org/triplepoint/ansible-znc.svg?branch=master)](https://travis-ci.org/triplepoint/ansible-znc)
Install and configure the ZNC IRC bouncer.

Includes the [ClientBuffer module](http://wiki.znc.in/Clientbuffer) to support multiple separate client buffers per account.

Because this role depends on a Docker container, it's not as straightforward how to call the `znc` binary for utility functions, like `--makepass`.  For reference, here's how to run the password command from a machine which has Docker set up:
```
docker run -it --rm triplepoint/docker-znc:latest znc --makepass
```

## Requirements
No hard dependency roles, but some sort of docker environment needs to be running on the host for this role to deploy.  The `geerlingguy.docker` role satisfies this requirement.

## Role Variables
For more details on ZNC's configuration, see the [ZNC configuration documentation](http://wiki.znc.in/Configuration).

For more information on ZNC's global, user, and network modules, see the [ZNC module documentation](http://wiki.znc.in/Modules).

### ZNC Install
```
znc_exec_user: znc-admin    # The user to create under which znc will run
znc_exec_user_and_group_id: 1066  # The uid and gid of the exec user
znc_docker_image_version: 0.1.6   # The tagged version of the `triplepoint/docker-znc` docker image
znc_install_version: 1.6.5  # The version of znc installed with the docker image.  Should be kept in sync.
znc_config_root: /etc/znc   # The root location of znc's configuration file structure
```

### ZNC Global Configuration
```
znc_max_buffer_size: 100000    # The max size of any user buffer.  This is used as the default if no user-specific value is given.
znc_host: 0.0.0.0              # What host address to use?
znc_port: 6666                 # What port will znc listen on?
znc_ipv4: true                 # Should ZNC listen for ipv4 connections?
znc_ipv6: false                # ipv6?
znc_ssl: true                  # Should ZNC expect connections over ssl?
znc_ssl_certfile: "{{ znc_config_root }}/znc.pem"   # If ssl is enabled, where is the PEM file? This is generated by the Ansible build.
znc_global_modules:                                 # Which global modules should be installed for use across all users and networks?  Note that these are separate from user and network modules defined below.
  - webadmin
```

### ZNC User Definition Configuration
```
znc_users:                                # It's advisable to have a separate admin user with no networks, for administering the ZNC server directly.  Here we just have the one user, for brevity.
  - name: admin
    password:                             # These can be generated with `znc --makepass`.  This one is for password "admin".
      method: "sha256"
      hash: "481fe84cc70161b20eb0c487d212e8b94cabb45cb9f08b6c51cc2c0131c1b42e"
      salt: "J*;s-Z!gjJ:oJ.kThRZv"
    nick: adminuser
    realname: Admin ZNC User
    admin: true                           # There should be at least one admin user, but your typical user probably shouldn't be an admin.
    allow: "*"                            # Optional
    altnick: adminuser_                   # Optional
    autoclearchanbuffer: true             # Optional, should be false if clientbuffer is being used
    autoclearquerybuffer: true            # Optional, should be false if clientbuffer is being used
    buffer: 100000                        # Optional
    chanmodes: "+stn"                     # Optional
    ident: adminuser_                     # Optional
    multiclients: false                   # Optional
    networks:                             # Optional, though without any networks the user won't connect to any external IRC servers.
      freenode:
        server: chat.freenode.net
        port: 6697
        ssl: true
        password: ""                      # Optional, this is the password with which the user will log into the remote chat server.
        channels:                         # Optional list, the user will connect to each of these channels on the remote chat server.
          - "#freenode"                   # These need to be commented for YAML, if there's a hash in the channel name.
        modules:                          # Optional list, thes are the network-specific modules.
          - route_replies
          - keepnick
          - clientbuffer                  # Be sure to disable `autoclearchanbuffer` and `autoclearquerybuffer` if this is enabled for this user.
    modules:                              # These are the user-specific modules.
      - chansaver
      - controlpanel
      - webadmin
```

## Dependencies
None.

## Example Playbook
    - hosts: whatever
      roles:
        - triplepoint.znc

## Role Testing
This role is tested with `molecule`, using `pipenv` to handle dependencies and the Python testing environment.

### Setting Up Your Execution Environment
``` sh
pip install pipenv
```
Note, `pip-tools` doesn't appear to play nice with `pipenv`.  You should not have `pip-tools` installed for this to work correctly.

Once you have `pipenv` installed, you can build the execution virtualenv with:
``` sh
pipenv install --ignore-pipfile
```
This will create a virtual environment with all the Python dependency packages installed.

### Running Tests
Once you have your environment configured, you can execute `molecule` with:
``` sh
pipenv run molecule test
```

### Regenerating the Lock File
You shouldn't have to do this very often, but if you change the Python package requirements using `pipenv install {some_package}` commands or by editing the `Pipfile` directly, or if you find the build dependencies have fallen out of date, you might need to regenerate the `Pipfile.lock`.
``` sh
pipenv lock
```
Be sure and check in the regenerated `Pipfile.lock` when this process is complete.

## License
MIT
