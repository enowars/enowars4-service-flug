
while [ 1 ]; do
        find /users -maxdepth 1 -mmin +30 -type f -delete;
        find /tickets -maxdepth 1 -mmin +30 -type f -delete;
        sleep 600;
done