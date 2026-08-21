#!/bin/bash

case "$1" in
    start)
       echo "Starting service...."
       ;;
     stop)
          echo  "Stopping service..."
          ;;
     restart)
           echo "Restarting service..."
          ;;
     status)
          echo "Checking service status..."
          ;;
      *)
          echo "Usage: $0 {start|stop| restart|status}"
         exit 1
          ;;

esac
