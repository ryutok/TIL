# Export git repository

## Export files only under git (w/o .git directory)

```
$ git archive (HEAD,tag) --output=hoge.zip
```


## Export as git repository

```
$ cd SavedDir
$ git clone --bare ProjectDir ProjectName.git
```


## Clone from exported repository

```
$ cd WorkingDir
$ git clone SavedDir/ProjectName.git
```
