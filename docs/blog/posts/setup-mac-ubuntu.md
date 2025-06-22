---
title: Old Macbook Pro + Pop!_OS
date: 
  created: 2025-06-21
  updated: 2025-06-21
authors: 
  - grobauskas
categories:
  - Linux
---
# Old Macbook Pro + Pop!_OS
This weekend I took my old Macbook Pro from 2013 and installed Pop!_OS. It was easy, and so far I've been pleased.

This guide will walk you through setting up Pop!_OS on a Mac 11,1, including configuring Wi-Fi. There are also some notes on installing essential tools.

<!-- more -->

# Setting Up Pop!_OS on a Mac 11,1
I started my research with the following blog post by Alexander Swensen: [Installing Pop!_OS (Linux) on a Late 2011 MacBook Pro](https://alexswensen.io/blog/2020-12-09_popos-on-2011-macbook-pro). 

TLDR; The installation involves [downloading](https://system76.com/pop/) Pop!_OS and flashing it onto a USB drive using [balenaEtcher](https://etcher.balena.io). Then you power on holding the option key so you can boot from the USB drive.

It will take a while to boot depending on the speed of your USB drive and Mac; so you can go get coffee. Everything after that is a straightforward install except one thing: your _Wi-Fi driver_. 

Luckily, I had an adaptor for USB to RJ45 to let me get a wired connection. 

## Enable vi Command Line Editing for Bash
Of course, the first thing to do is to open a shell, and update your command line editor to be vi. I guess this is optional, but I get confused if I don't have my normal command line editor set up.

Open your `.bashrc` file:

```sh
vi ~/.bashrc
```

Add the following at the end of the file:

```sh
# Enable vi command line editing
set -o vi
```

> **Note:** Terminal cut-and-paste uses `Ctrl+Shift+C` and `Ctrl+Shift+V`.

Then you can either `source ~/.bashrc` or just reopen your terminal.

## Macbook Pro 11,1 (Late 2013) Wi-Fi Networking

Setting up networking for a 2013 Macbook Pro is relatively straightforward. 

Use a wired adapter for the initial setup and go to **Settings > Software & Updates > Pop!_OS Software** and enable:
  
- Canonical-supported free and open-source software  
- Proprietary drivers for devices (restricted)

Then open a terminal to check your hardware:

```sh
lspci -nn -d 14e4:
```

Look for Broadcom (14e4) to confirm your network adapter type. Example output:

```
02:00.0 Multimedia controller [0480]: Broadcom Inc. and subsidiaries 720p FaceTime HD Camera [14e4:1570]
03:00.0 Network controller [0280]: Broadcom Inc. and subsidiaries BCM4360 802.11ac Dual Band Wireless Network Adapter [14e4:43a0] (rev 03)
```

If you see Broadcom, great!

### Get Current
These steps might not be required, but starting from a known, up-to-date state is simpler to debug.

- Update your package list:

```sh
sudo apt update
```

- Update your PCI IDs list:

```sh
sudo update-pciids
```

### Broadcom Driver
- Install the Broadcom drivers:

```sh
sudo apt install --reinstall broadcom-sta-dkms
```

# Suggestions for Basic Setup
These are purely optional, and they are just suggestions. My current M3 Macbook Pro is my daily driver, and this older laptop will just be a laptop that is in our kitchen to be used mostly for web browsing.

Still, I like to have a few things on all computers. I already switch between Windows and Mac (and now Linux) for desktops.  So consistency is important.

I prefer to keep my chosen shell, editor, and email consistent across machines. I always set up git too, even on systems not used for development.

## Install zsh

- Install zsh:

```sh
sudo apt install zsh
```

- Install Oh My Zsh:

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

> When prompted, select zsh as your default shell.

## Add Visual Studio Code

- While the app store can be used to install the Flatpak for VS Code, it's recommended to install it directly from Microsoft for easier updates: [visualstudio.com](https://code.visualstudio.com/).
- Download the `.deb` package.
- Open a terminal and run the following (replace `<package-name>` with the actual file name):

```sh
cd ~/Downloads
sudo apt install ./<package-name>.deb
```

### Add Shell Information in VS Code

- Open VS Code settings:

  - Press `Ctrl+Shift+P` and search for `Preferences: Open Settings (JSON)`.

- Add the following to your settings:

```json
{
  "terminal.integrated.defaultProfile.linux": "zsh",
  "terminal.integrated.profiles.linux": {
    "zsh": {
      "path": "/usr/bin/zsh"
    },
    "bash": {
      "path": "/usr/bin/bash"
    }
  }
}
```

## Set VS Code as the Default Editor

- In the terminal, run:

```sh
sudo update-alternatives --set editor /usr/bin/code
```

## Add Prettier Extension to VS Code

- Install the Prettier extension and add the following to your user settings:

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## Check for Software Updates

- Open **Pop!_Shop**.
- Press `Ctrl+I` to view and apply updates.

## Outlook.com

I use Outlook.com and like to have email available wherever I’m logged in. While you can add your Microsoft account and use Geary (the default app) for email, I have found the Outlook as a PWA (Progressive Web App) to have a better UI.

To install Edge, download the `.deb` package from the [Microsoft Edge website](https://www.microsoft.com/edge) and install it with:

```sh
sudo apt install ./<package-name>.deb
```

After logging in to Outlook.com in Edge, you can choose to install it as a PWA for a more app-like experience.

## LastPass

My preferred password manager is LastPass. There are LastPass extensions for all major browsers, including Edge and Firefox.

You should have no trouble installing and enabling the extension in your browser of choice to log in to an existing account. 

If setting up new, make sure to use a strong master password and enable multifactor authentication for added security.

## GitHub CLI

You can install the GitHub CLI following [GitHub’s official documentation](https://github.com/cli/cli/blob/trunk/docs/install_linux.md). This tool makes it easy to log in, manage repositories, and automate adding an SSH key to your new Linux install.

After installing, don’t forget to set your Git username and email:

```sh
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Final Thoughts

I was pleasantly surprised by the ease of installation and the level of support for my old MacBook Pro. Installing the Wi-Fi driver was the only step that required customization beyond a standard installation.

As an early adopter of Linux in the '90s, I had a love/hate relationship with desktop Linux over the years. When I bought my first MacBook in 2013, I stopped using Linux outside of server environments.

Pop!_OS has been excellent so far. It’s based on Ubuntu, so you should find it familiar and easy to use. The hardware support, especially for older Macs, is impressive. If you’re looking to breathe new life into an old MacBook, I highly recommend giving Pop!_OS a try.

---

If you have any questions or run into issues, the Pop!_OS and Ubuntu communities are active and helpful. Happy computing!