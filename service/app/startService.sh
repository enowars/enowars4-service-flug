#!/bin/bash
bash clean.sh &
socat TCP-LISTEN:7478,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"
