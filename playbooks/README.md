Ansible Playbooks and Playbook Bash script
==========================================

### Most of these should be a guide and should be configured to your setup. ###

##### Read Ansible documentation or quick start guides first! #####

  * ansible.cfg:
      * Local ansible configs for the playbooks. Ansible searches from local directory upwards until it finds an ansible.cfg or it uses the default. It's best to keep one in the same folder as the playbooks it is meant for.
      * No major changes aside from ssh. These are made for the system we have because of the interference.
          * `-c arcfour256` sets encryption to be the least secure, but fastest when using ssh. rPI must be setup to accept it.
              * To allow the rPIs to accept arcfour256 you'd have to append these lines to the end of the `/etc/ssh/sshd_config` file:  
                      `#Adding ciphers back in`  
                      `ciphers arcfour256,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com,chacha20-poly1305@openssh.com`
          * `-o ControlMaster=auto` ssh option decide if it should use ControlMaster
          * `-o ControlPersist=5m` ssh option to keep connection open for 5 minutes even if there is no activity.
          * `-o ServerAliveCountMax=10` ssh option to kill connection if the server hasn't responded after 10 pings.
          * `-o ServerAliveInterval=2` ssh option for interval in seconds to ping server when connected.
          * `pipelining = True` most new ssh versions should support this.

  * copy-pictures.yml:
      * The main workhorse of the ansible playbooks. Gathering facts is disabled due to the nature of the wireless interference in our current setup.
      * Make sure to change the ansible variables to your location for the images taken by the bramble.
          * `img_dir` and `local_dir`
          * Use absolute full paths
          * Change the delegate_to host to your localhost as defined by your hosts file.
      * Assumes all images on the rPI are in a flat directory structure and are in their own solo folder. They can be any file type. In our case, they are bundled in `.tar` files.
      * Make any changes necessary to work with your configuration.
      
  * sudo-plays.yml:
      * Ansible playbook containing changes made to rPIs:
          * Change timezone
          * Disable utmp
          * Disable reverse DNS lookup
          * Add/remove cron jobs both locally and on the bramble.
          
  * take-pictures.yml:
      * Take pictures on all the rPIs manually..
      
  * wireless-power.yml:
      * Permanently set wireless transmit power on rPI by transferring pi_config file.
      * Change the src to the interfaces file.
