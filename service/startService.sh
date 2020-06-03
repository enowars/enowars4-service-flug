#!/bin/bash
gcc flug2.c
socat TCP-LISTEN:1337,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"
