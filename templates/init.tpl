#!/bin/sh

# chkconfig: 2345 60 20
# description: {{name}}

# Source function library.
. /etc/init.d/functions


{% block variables %}
NAME={{name}}
SCRIPT="/usr/bin/${NAME}"
PIDFILE="/var/run/${NAME}.pid"
LOGFILE="/var/log/${NAME}.log"
ENVFILE="/etc/default/${NAME}"
{% endblock variables %}

start() {
{% block start %}
  if [ -f "${PIDFILE}" ] && kill -0 $(cat "${PIDFILE}") &> /dev/null; then
    echo "${NAME} already running with PID $(cat ${PIDFILE})" >&2
    return 1
  fi

  echo "Starting ${NAME}" >&2
  . "${ENVFILE}"

  if [ -z $USER ]; then
    USER=root
  fi

  daemon --user $USER --pidfile="$PIDFILE" "${SCRIPT} &"  2&> $LOGFILE

  echo `pidof $NAME` > ${PIDFILE}

  echo "${NAME} started with PID $(cat ${PIDFILE})" >&2
  sleep 1
  if [ -f "${PIDFILE}" ] && kill -0 $(cat "${PIDFILE}") &> /dev/null; then
    echo "${NAME} started successfully." >&2
  else
    echo "${NAME} was not started OK"
    return 1
  fi
{% endblock start %}
}

stop() {
{% block stop %}
  if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE") &> /dev/null; then
    echo "${NAME} not running" >&2
    return 1
  fi
  echo "Stopping ${NAME}..." >&2
  kill -15 $(cat "$PIDFILE")
  rm -f "$PIDFILE"
  echo "${NAME} stopped" >&2
{% endblock stop %}
}

status() {
{% block status %}
  if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE") &> /dev/null; then
    echo "${NAME} is not running" >&2
  else
    echo "${NAME} is running" >&2
  fi
{% endblock status %}
}

uninstall() {
{% block uninstall %}
  echo -n "Are you really sure you want to uninstall ${NAME}? That cannot be undone. [yes|No] "
  local SURE
  read SURE
  if [ "$SURE" = "yes" ]; then
    stop
    rm -f "$PIDFILE"
    echo "Notice: log file is not be removed: '$LOGFILE'" >&2
    update-rc.d -f <NAME> remove
    rm -fv "$0"
  fi
{% endblock uninstall %}
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  uninstall)
    uninstall
    ;;
  retart)
    stop
    start
    ;;
  status)
  status
  ;;
  *)
    echo "Usage: $0 {start|stop|restart|uninstall}"
esac
