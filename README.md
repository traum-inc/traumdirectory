# Traum Directory

A simple tool for creating templated directory structures.

![Screenshot](https://raw.githubusercontent.com/traum-inc/traumdirectory/master/screenshot.png)

## Installation

First, download a binary for your platform from the [release page](https://github.com/traum-inc/traumdirectory/releases/tag/v0.1-alpha). On Windows, unzip and run the .exe executable within the folder. On macOS, extract the app from the disk image and double-click to run.

## Instructions

This is a simple application to create a directory structure based on text templates. Select a template from the drop-down on the right of the window, fill in the template variables, then click the `Generate` button and select a destination folder.

## Templates

Example templates are in the `templates` folder. The hierarchy is denoted by tab indentation, and template variables are enclosed in curly brackets. For instance:

```
{ProjectName}
    Assets
        3D
        Textures
        Audio
    Client
        Brief
        {ClientName}
    Reference
        Images
        Videos
        Sounds
```

It's important that the indents are tab characters, not spaces, or the template will fail to load.

You can edit or replace the template files within the templates folder (on macOS, you'll need to right click on the app to 'Show Package Contents').


## Building

First make sure you have a Python 3.7.3 environment at least. Create a new virtualenv and install the requirements:

```
$ git clone https://github.com/traum-inc/traumdirectory.git
$ cd traumdirectory
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

At this point you should be able to run the application from the terminal:

```
$ python traumdir
```

If that works, you can build a self-contained executable or app by installing PyInstaller, and then running the build script:

```
$ pip install PyInstaller
$ ./scripts/build.sh
```

This will either build a tarball or a disk image in the `dist/` folder.

### Windows

On Windows it's a similar process, but use the PowerShell build script:

```
PS> git clone https://github.com/traum-inc/traumdirectory.git
PS> cd traumdirectory
PS> virtualenv venv
PS> venv/Scripts/activate
PS> pip install -r requirements.txt
```

You'll need to install the development version of PyInstaller to run the build script.

```
PS> pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
PS> scripts/build.ps1
```

This will create a zip file in the `dist/` folder.
