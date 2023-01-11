# Pwning-CCTV-cameras
Exploiting cameras with a very distinctive HTTP Server header of "JAWS/1.0".

The detailed description of the vulnerability is shown in the link below.  
https://www.pentestpartners.com/security-blog/pwning-cctv-cameras/

Through searching the string "JAWS/1.0" in Shodan or Zoomeye, we can get target IP list. Executing the JAWS_bot.py to get the devices which have the vulnerability.
JAWS_bot.py is based on two methods: weak password and the built-in web shell.  
  -weak password: "root":"juantech".  
  -built-in web shell: inputing url like "http://192.168.3.101/shell?/usr/sbin/telnetd -l/bin/sh -p 25" to bind the telnet service to port 25 that without password.  
