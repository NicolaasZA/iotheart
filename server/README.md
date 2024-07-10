## Install

1. Edit `iotheartserver.service` and fix the path in the `ExecStart` property.
2. Copy the files into the correct folders:

```commandline
sudo cp ./iotheart_server.py ~/
sudo cp ./iotheartserver.service /etc/systemd/system/iotheartserver.service
```

### Enable
```commandline
sudo systemctl enable iotheartserver.service
```

## Start
```commandline
sudo systemctl start iotheartserver.service
```

## Stop
```commandline
sudo systemctl stop iotheartserver.service
```

## Disable
```commandline
sudo systemctl disable iotheartserver.service
```