# Bit
### Version Control System (Friendly Edition)

> [!NOTE]
> This VCS tool is in development and not recommended for larger projects.

## Indexing Items
Here's how to index files & folders using **Bit**:

### Add Items
```shell
$ bit stage index.html
```

### Remove Items
Removing specific items from index:
```shell
$ bit unstage index.html
```

Removing all indexed items:
```shell
$ bit unstage *
```

### List Indexed Items
To get a list of indexed items:

```shell
$ bit staged
```
