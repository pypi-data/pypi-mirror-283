# `timestep`

Awesome Portal Gun

**Usage**:

```console
$ timestep [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `load`: Load the portal gun
* `shoot`: Shoot the portal gun
* `test`
* `unload`: Unload the portal gun

## `timestep load`

Load the portal gun

**Usage**:

```console
$ timestep load [OPTIONS]
```

**Options**:

* `--llamafile-path TEXT`: [default: /home/mjschock/Projects/timestep/models/TinyLlama-1.1B-Chat-v1.0.F16.llamafile]
* `--help`: Show this message and exit.

## `timestep shoot`

Shoot the portal gun

**Usage**:

```console
$ timestep shoot [OPTIONS]
```

**Options**:

* `--message TEXT`: [default: Count to 10, with a comma between each number and no newlines. E.g., 1, 2, 3, ...]
* `--help`: Show this message and exit.

## `timestep test`

**Usage**:

```console
$ timestep test [OPTIONS]
```

**Options**:

* `--gpu-layers INTEGER`: [default: 0]
* `--help`: Show this message and exit.

## `timestep unload`

Unload the portal gun

**Usage**:

```console
$ timestep unload [OPTIONS] PID
```

**Arguments**:

* `PID`: [required]

**Options**:

* `--help`: Show this message and exit.
