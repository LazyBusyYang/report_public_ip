# Overview

The main function of this project is to obtain the public IP address of the current host and notify the user about IP changes via email. Some internet service providers, such as China Unicom, provide users with unstable public IP addresses that change every time the router restarts. This can affect services that are mapped from the local area network to the public network. 

# Usage

`check_public_ip.py` retrieves the current public IP address using an [https api](https://api.ipify.org/) and compares it with the string in the input file. It returns 1 when there is a change in the IP address and 0 when there is no change.

`send_email.py`  sends a local text file as the body of an email to a specified email address. The test results from sending emails using an Outlook mailbox were successful.

# Example

After `touch input_ip.txt`, setting a scheduled task(say crontab) to run the bash below, one can get email notification as long as the public IP changes.

```bash
#!/bin/bash
# note that PATH_TO_YOUR_WORK_DIR, YOUR_EMAIL_ADDR, YOUR_EMIAL_PWD, REIC_EMIAL_ADDR
# should be replaced before running
# note that smtp.office365.com:587 is only for outlook senders in Dec 2023
cd PATH_TO_YOUR_WORK_DIR/report_public_ip/

python check_public_ip.py \
    --input_path input_ip.txt \
    --output_path output_ip.txt
return_value=$?

if [ $return_value -eq 0 ]; then
    exit 0
elif [ $return_value -eq 1 ]; then
    python send_email.py \
        --smtp_host smtp.office365.com \
        --smtp_port 587 \
        --sender YOUR_EMAIL_ADDR \
        --password YOUR_EMIAL_PWD \
        --recipient REIC_EMIAL_ADDR \
        --subject "IP Update" \
        --body_path output_ip.txt &&
    mv output_ip.txt input_ip.txt
else
    echo "get_public_ip.py unexpected return code：$return_value"
    exit 1
fi
```
