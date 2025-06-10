# mtrash - CLI Trash Management System

A lightweight, safe alternative to `rm` that moves files to a trash directory instead of permanently deleting them. Includes a comprehensive trash management interface for viewing, restoring, and permanently deleting files.

## 🚀 Quick Install

Run this one-liner to install the latest version directly from GitHub:

```bash
curl -fsSL https://raw.githubusercontent.com/gdhanush27/Notes/main/Scripts/mtrash/setup-mtrash.sh | bash
```

This will:
- Download the latest versions of `mtrash` and `safe-rm`
- Prompt you to configure trash directory and size limits
- Install both scripts to `~/.local/bin`
- Set up your PATH automatically
- Create the necessary trash directory structure

## 📁 Files Description

### Core Scripts

- **`safe-rm`** - Safe replacement for the `rm` command
  - Moves files to trash instead of permanent deletion
  - Automatic trash size management with cleanup options
  - Creates timestamped backups to avoid name conflicts
  - Generates `.trashinfo` metadata files for each trashed item

- **`mtrash`** - Interactive trash management utility
  - View all trashed files in a tree format
  - Search and restore files by keyword matching
  - Permanently delete files from trash
  - Batch operations with index selection

### Setup & Installation

- **`setup-mtrash.sh`** - Automated installation script
  - Downloads latest versions from GitHub
  - Configurable trash directory and size limits
  - Automatic PATH configuration
  - Creates necessary directory structure

## 🛠️ Usage

### Safe File Removal
```bash
safe-rm file1.txt folder1/ file2.log
```

### View Trash Contents
```bash
mtrash -v
```

### Restore Files
```bash
mtrash -r keyword
```

### Permanently Delete from Trash
```bash
mtrash -d keyword
```

### Get Help
```bash
mtrash -h
```

## ⚙️ Configuration

During installation, you'll be prompted to configure:

- **Trash Directory**: Default is `~/.trash`
- **Max Size**: Default is 1024MB with automatic cleanup options

## 🗂️ Trash Structure

```
~/.trash/
├── files/          # Actual trashed files and folders
└── info/           # Metadata (.trashinfo files)
```

Each trashed item gets:
- A timestamped name to prevent conflicts
- A `.trashinfo` file containing original path and deletion date

## 🔄 Automatic Cleanup

When trash exceeds the configured size limit, `safe-rm` offers cleanup options:
1. Delete files older than 1 month
2. Delete files older than 3 months  
3. Delete files older than 6 months
4. Cancel operation

## 🛡️ Safety Features

- **No accidental permanent deletion** - Files always go to trash first
- **Conflict resolution** - Timestamped names prevent overwrites
- **Size monitoring** - Automatic alerts when trash gets too large
- **Metadata preservation** - Original paths and deletion dates stored
- **Batch operations** - Review before restore/delete with index selection

## 📋 Requirements

- Bash shell
- `curl` or `wget` for installation
- Standard Unix utilities (`mv`, `rm`, `find`, `du`)

## 🔗 Manual Installation

If you prefer manual installation:

1. Download the scripts:
```bash
curl -O https://raw.githubusercontent.com/gdhanush27/Notes/main/Scripts/mtrash/safe-rm
curl -O https://raw.githubusercontent.com/gdhanush27/Notes/main/Scripts/mtrash/mtrash
```

2. Make them executable:
```bash
chmod +x safe-rm mtrash
```

3. Move to a directory in your PATH:
```bash
mv safe-rm mtrash ~/.local/bin/
```

4. Create trash directories:
```bash
mkdir -p ~/.trash/{files,info}
```

## 🤝 Contributing

Feel free to submit issues and pull requests to improve the trash management system.

## 📄 License

This project is open source and available under standard terms.