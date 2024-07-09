control-tmux
============

This is a wrapper around [tmux](https://github.com/tmux/tmux) that allows you to quickly
switch between sessions, save sessions while preserving bash history.

Requirements
------------

* Python 3.6 or higher with PIP. On Ubuntu, run `sudo apt install python3-pip`.
* Tmux 3.0a or higher. On Ubuntu, run `sudo apt install tmux`.
* Bash 4.0 or higher (probably works with older versions, but not tested)

Installation
------------

`control-tmux` can be installed using PIP:

```
python3 -m pip install control-tmux
```

In order to use the save and restore features, you must set it up in `.bashrc` for each
user. Simply run:

```
python3 -m controltmux --setup t
```

This will install `tmux.setup.sh` and `tmux.default.conf` in your home directory, and add
references to them to `.bashrc` and `.tmux.conf`.

You can specify one or more aliases to set up for `control-tmux`. I recommend `t` because
it is short and easy to type, but power users might already have an alias configured. I
use `scn` as an alias because this project started out many years ago as a wrapper for GNU
`screen`. Aliases will only apply to terminals opened in the future, but you can run `exec
bash` to reload your aliases in an existing terminal.

The installer will also create a default .tmux.conf if you don't have one. This
configuration is not necessary for `control-tmux` to run, but includes many bindings that
make tmux easier to use.

Simple usage
------------

These usage examples all assume you have aliased `t` to `control-tmux` during installatin

If run without arguments, `t` or `control-tmux` will list all your current sessions:

![](help-img/ctmux-list.gif)

To start or switch to a session named `blah`, just run `t blah`:

![](help-img/ctmux-switch.gif)

This works whether you are running from within tmux or outside of it. If run from outside,
this runs either `tmux attach -t blah` or `tmux new-session -s blah` (if `blah` doesn't
exist) . If run from inside tmux, then it does `tmux switch-client -t blah`, which
switches your current client to the session named `blah`.

In either case, this will detach any other terminals that are connected to `blah`, unless
you prefix the session name with `n` (e.g. `t n blah`)

![](help-img/ctmux-double-window.gif)

To save the `blah` session to `~/.tmuxsave/blah.zip`, run `t s blah`. To restore, run `t r
blah`. Restore only works when the session doesn't already exist. You can save all open
sessions by running `t s all`:

![](help-img/ctmux-save-restore.gif)

Restoring a session restores the current working directory and the command history of the
shell running within it. It does not automatically restart any commands that were running.

Recovering from a crash
-----------------------

The bash hooks in `.tmux.setup.sh` write your history to disk as soon as you launch a
command. In most cases, after a power failure or crash, the session data will be
recoverable. All you need to do is run `t s all` before running tmux.

If you forget and try to run `t <session>` before `t s all`, then it will start a new
instance of tmux and running `t s all` will save the sessions from the new index. However,
the data for the old session is still present in `~/.tmuxsave`. Run `ls -ld
~/.tmuxsave/tmux-default-*` to see all previous sessions. Each directory will have a
timestamp indicating when that particular instance of tmux was started. Once you have that
directory, just run `t -s ~/.tmuxsave/tmux-default-2018-XX-XX__XX-XX-XX s all` and it will
save the sessions from the previous instance.
