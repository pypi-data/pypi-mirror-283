#!/bin/bash

# Create export script
cat <<EOF > /export-certs.sh
#!/bin/sh
CURRENT_DATE=\$(date '+%Y-%m-%d %T%Z')
export-certs $STORAGE_FILE $OUTPUT_PATH
echo "${CURRENT_DATE}: Certs exported to ${OUTPUT_PATH}"
EOF
chmod +x /export-certs.sh

# Setup cron job
(crontab -l 2>/dev/null; echo "${CRON_SCHEDULE} export-certs /export-certs.sh >> /var/log/cron.log 2>&1") | crontab -

echo "Docker container started. Cron job set to: ${CRON_SCHEDULE}"

if [ "$ON_START" == 1 ]; then
    export-certs $STORAGE_FILE $OUTPUT_PATH && echo "Certs exported to: ${OUTPUT_PATH}"
fi

cron -f
