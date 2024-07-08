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
$ timestep shoot [OPTIONS] MESSAGE
```

**Arguments**:

* `MESSAGE`: [required]

**Options**:

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
