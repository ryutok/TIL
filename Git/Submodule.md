# Git submodule

## Add submodule

```sh
git submodule add remoteserver:child-repository.git local_subdir
```


## Clone remote repository which has submodule

```sh
git clone remoteserver:parent-repository.git localdir
cd localdir
git submodule init
git submodule update
```

or

```sh
git clone --recursive remoteserver:parent-repository.git localdir
```

When you want to edit the submodule, you have to checkout some repository like

```sh
cd local_subdir
git checkout master
```

because initially the submodule is *detached HEAD* state.
