# robocopy -- rsync like command

Copies file data.

[robocopy | Microsoft Docs](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy)


## Syntax

```sh
robocopy <Source> <Destination> [<File>[ ...]] [<Options>]
```

- `<Source>` and `<Destination>` should be directories.
- Only files are copied in default.
- The files you want to copy are specified in `<File>`.
- Wildcard is available in  `<File>`.


## Options

| Option                 | Description |
|:-----------------------|:------------|
| `/s`                   | Copies subdirectories. |
| `/e`                   | Copies subdirectories even when they are empty. |
| `/xo`                  | Excludes older files. |
| `/xd <Directory>[...]` | Excludes following directories. |
| `/r:<N>`               | The number of retries on failed copies. |
| `/ndl`                 | Exclude directory names from logs. |
| `/np`                  | Don't display the progress of the copy. |

