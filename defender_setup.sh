#!/usr/bin/env bash

echo '192.168.60.60 target.com target' | sudo tee -a /etc/hosts > /dev/null

cat <<'EOF' | sudo tee /usr/local/bin/startmon.sh
#!/usr/bin/env bash

f_date="$(date +%y%m%d%H%M%S)"
filename="${f_date}_capture.pcap"
# capture ipv4 packets without resolving hostname & ports; in addition capture all traffic including files
sudo tcpdump -i eth1 'ip and not host 127.0.0.1' -nn -s0 -U -w - | \
tee "/vagrant/$filename" | \
tcpdump -r -
EOF

sudo chmod +x /usr/local/bin/startmon.sh
