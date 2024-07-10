## Install

1. Edit `iotheartclient.service` and fix the path in the `ExecStart` property.
2. Edit `iotheart_client.py` and ensure the `target_ip` property matches the server IP.
2. Copy the files into the correct folders:

```commandline
sudo cp ./iotheart_client.py ~/
sudo cp ./iotheartclient.service /etc/systemd/system/iotheartclient.service
```

### Enable
```commandline
sudo systemctl enable iotheartclient.service
```

## Start
```commandline
sudo systemctl start iotheartclient.service
```

## Stop
```commandline
sudo systemctl stop iotheartclient.service
```

## Disable
```commandline
sudo systemctl disable iotheartclient.service
```