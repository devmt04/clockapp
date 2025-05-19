#!/usr/bin/env bash

set -euo pipefail

if [ ! -z "$(pgrep --uid "$(id -u)" -f codetantra-sea)" ]; then
    echo "codetantra-sea already running"
    exit
fi

# Detect display sockets and variables
XSOCK="/tmp/.X11-unix"
WAYLAND_SOCK="/run/user/$(id -u)/wayland-0"
PULSE_SOCK="/run/user/$(id -u)/pulse/native"
PIPEWIRE_SOCK="/run/user/$(id -u)/pipewire-0"

exec bwrap \
  --ro-bind /home/mohit/Downloads/sea/opt/CodeTantraSEA /app \
  --ro-bind /usr /usr \
  --ro-bind /bin /bin \
  --ro-bind /lib /lib \
  --ro-bind /lib64 /lib64 \
  --proc /proc \
  --dev /dev \
  --tmpfs /run \
  --tmpfs /tmp \
  --ro-bind /etc/passwd /etc/passwd \
  --ro-bind /etc/group /etc/group \
  --ro-bind /etc/hostname /etc/hostname \
  --ro-bind /etc/hosts /etc/hosts \
  --ro-bind /etc/localtime /etc/localtime \
  --ro-bind-try /etc/resolv.conf /etc/resolv.conf \
  --ro-bind-try /etc/xdg /etc/xdg \
  --ro-bind-try /etc/pulse /etc/pulse \
  --ro-bind-try /etc/pipewire /etc/pipewire \
  --bind-try "$XSOCK" "$XSOCK" \
  --ro-bind-try "$WAYLAND_SOCK" "$WAYLAND_SOCK" \
  --ro-bind-try "$PULSE_SOCK" "$PULSE_SOCK" \
  --ro-bind-try "$PIPEWIRE_SOCK" "$PIPEWIRE_SOCK" \
  --setenv DISPLAY "${DISPLAY:-}" \
  --setenv WAYLAND_DISPLAY "${WAYLAND_DISPLAY:-wayland-0}" \
  --setenv PULSE_SERVER "unix:${PULSE_SOCK}" \
  --unsetenv DBUS_SESSION_BUS_ADDRESS \
  --unshare-all \
  --share-net \
  --hostname sandboxed \
  /app/codetantra-sea
