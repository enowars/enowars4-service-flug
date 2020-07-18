
while [ 1 ]; do
        find /users -maxdepth 1 -mmin +20 -type f -delete;
        find /tickets -maxdepth 1 -mmin +20 -type f -delete;
        sleep 120;
done
