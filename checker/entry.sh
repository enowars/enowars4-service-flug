
env

export PWNLIB_NOTERM=true 
gunicorn -c gunicorn-conf.py checker:app