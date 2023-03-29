# EOL (End-of-life)

***

> #### Language
> English [한국어](README.KR.md)

# vlive-backup-bot

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/box-archived/vlive-backup)](https://github.com/box-archived/vlive-backup/releases)
[![Discord](https://img.shields.io/discord/824605893885820939)](https://discord.gg/84sVr2mQKX)

Auto backup bot for vlive

This is the program for bulk downloading vlive posts

## Installation

3.7 or later version of python is required You can download python on [python.org](https://www.python.org/downloads/).

You MUST check __Add Python 3.x to PATH__ during installation, if you install python on window.

![Untitled-2](https://user-images.githubusercontent.com/76082716/112562713-4488a880-8e1b-11eb-9a8b-fce406cd4957.jpg)

### Windows 7, 8, 10

Execute __run-windows.bat__ file from unzipped release file.

If the SmartScreen alert has shown, Click <u>More Info</u> text. Then, you can see **Run Anyway** button. Click the
button to run!

Or, you can execute the program with Command Prompt. Open the Command Prompt, drap-and-drop __run-windows.bat__ to it and press
enter!

```console
C:\> path\to\vlive-backup-bot\run-windows.bat
```

### Other OS

On Linux, macOS, etc., you can execute the program with Shell script. Drag-and-drop __run-others.sh__ to terminal and press
enter!

```console
$ sh path/to/vlive-backup-bot/run-others.sh
```

## How To Use

You can control the program with keyboard and mouse.

Use `arrow-key` to move between items, `Tab` key to move between buttons. Mouse scroll is not supported. Please
use `PageUp`, `PageDown` key to scroll.

Downloaded items will be saved in the folder named "downloaded/*ChannelCode*_*BoardCode*".

### Email Account

The program uses email account (Social-login is not supported). Social-login account user must register email account
on [Profile page](https://www.vlive.tv/my/profile) (PC ONLY).

User account is saved to user's PC as `cache/vlive-backup-bot.session` for preserve login state. Account information is
NEVER used/saved for any other purpose.

If you don't use the login information anymore, please delete the session file for your account security.

### Failed History

Failed history can be found on __failed.txt__ file.

### Downloaded History

Download history file named `ChannelCode_BoardCode.txt` is stored in __cache__ folder to prevent duplicate download

Modify or delete the file to re-download the posts.

### Migrate Settings

Copy `cache` folder to unzipped release file, If you want to migrate settings(account, history) to new software or PC.

## Download Mode

### Simple

- Download All posts from the board.
- Membership setting is the only option to configure.

### Advanced

Download posts with more options. Option description is below.

- Official Video Post Download: Download official videos like vlive replay(VOD) and video
- Post Download: Download other posts like photo or notice.
- Load Amount: Amount of items to load from the board. `0` to load all items, other numbers to load specific amount of
  item from the latest item
- Select posts: You can select items to download. Press `<Select All>` button to download all items
