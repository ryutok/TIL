# Backup data from WS to HDD

```shell
rsync -au --progress --append-verify hostname:backup_dir/ stored_dir/
```

## rsync
A fast, versatile, remote (and local) file-copying tool

### Options

|      |                 |                                           |
|:-----|:----------------|:------------------------------------------|
| `-a` | `--archive`       | archive mode; equals `-rlptgoD`           |
| `-r` | `--recursive`     | recurse into directories                  |
| `-l` | `--links`         | copy symlinks as symlinks                 |
| `-p` | `--perms`         | preserve permissions                      |
| `-t` | `--times`         | preserve modification times               |
| `-g` | `--group`         | preserve group                            |
| `-o` | `--owner`         | preserve owner (super-user only)          |
| `-D` |                   | same as `--devices --specials`            |
|      | `--devices`       | preserve device files (super-user only)   |
|      | `--specials`      | preserve special files                    |
| `-u` | `--update`        | skip files that are newer on the receiver |
|      | `--progress`      | show progress during transfer             |
|      | `--append-verify` | `--append` with old data in file checksum |
|      | `--append`        | append data onto shorter files            |
