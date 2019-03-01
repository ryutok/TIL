# Export git repository

## Export files only under git (w/o .git directory)

```shell
git archive (HEAD,tag) --output=hoge.zip
```


## Export as git repository

```shell
cd SavedDir
git clone --bare ProjectDir ProjectName.git
```


## Clone from exported repository

```shell
cd WorkingDir
git clone SavedDir/ProjectName.git
```
