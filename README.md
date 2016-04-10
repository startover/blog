# My Pelican Blog


## Usage


```
$ git clone git@github.com:startover/blog.git
$ cd blog
$ pip install pelican markdown fabric  # install dependency
$ fab build  # generate the .md files to output folder
$ fab serve  # start server bind to localhost:8001
```

## Publish

```
$ pip install ghp-import
$ make github
```

