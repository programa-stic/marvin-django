#!/bin/bash

nohup python marvin_download_agent.py tummy > download.log &
nohup python marvin_androlyze_agent.py rummy > androlyze.log &
nohup python marvin_vuln_agent.py chummy > vuln.log &

