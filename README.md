# AutoTabNamer for Sublime Text 3

A Sublime Text 3 plugin that automatically renames tabs for **unsaved files** based on specific rules. This helps quickly identify unsaved buffers and allows setting a custom temporary name via a header comment.

## Features

*   Automatically renames **unsaved** tabs (files that haven't been saved yet).
*   Uses text following `## ` (note the space) on the **first found line** (within the first ~500 characters) as the tab name.
*   Defaults the tab name to `! UnSaved` if no specific header (`## `) is found near the beginning of the file.
*   Optimized: Uses debouncing on file modification to minimize performance impact while typing.
*   Lightweight and focuses solely on unsaved files.

**Important Note on Maintenance and Compatibility**

Please be aware that this plugin was created as a personal tool primarily for my own use with **Sublime Text 3**. I am not a professional developer.

Consequently, please understand that **this plugin is provided 'as-is' and I will not be providing active maintenance or support.** My focus remains on Sublime Text 3, and I do not have the time or resources to guarantee compatibility with future versions or to address issues promptly.

Should you encounter issues, particularly with versions of Sublime Text beyond ST3 or if the plugin stops working as expected, you may find it useful to **consult an AI assistant (like ChatGPT, Claude, Gemini, etc.) to help debug or adapt the Python code** for your needs.

Thank you for your understanding.

## Installation

### Manually (Git)

Using Git:

1.  Open your Sublime Text `Packages` directory. You can find it using the menu: `Preferences` -> `Browse Packages...`.
2.  Open a terminal or command prompt in this `Packages` directory.
3.  Clone the repository:
    ```bash
    git clone https://github.com/Zeurgh/AutoTabNamer.git AutoTabNamer
    ```
4.  Restart Sublime Text.

### Manually (Download ZIP)

1.  Go to the repository page: `https://github.com/Zeurgh/AutoTabNamer`
2.  Click the green "Code" button, then "Download ZIP".
3.  Extract the contents of the ZIP file.
4.  Rename the extracted folder from `AutoTabNamer-main` (or similar) to just `AutoTabNamer`.
5.  Move the `AutoTabNamer` folder into your Sublime Text `Packages` directory (`Preferences` -> `Browse Packages...`).
6.  Restart Sublime Text.

## Usage

The plugin works automatically in the background for **unsaved files only**.

*   **Header Naming:** To set a custom name for an unsaved tab, add a line starting *exactly* with `## ` (including the space) near the beginning of the file (within the first ~500 characters). The text following this prefix will be used as the tab name. Only the *first* such line encountered is used.

    *Example:*
    ```
    ## My Temporary Notes

    This is the rest of my unsaved file content...
    ```
    The tab for this unsaved file will be named `My Temporary Notes`.

*   **Default Naming:** If no line starting with `## ` is found near the beginning of the unsaved file, the tab will be named `! UnSaved`.

## Configuration

Currently, there are no configurable settings for this plugin. The behavior is determined by the constants (`HEADER_PREFIX`, `DEFAULT_UNSAVED_NAME`) within the plugin code.

## License

This project is licensed under the [Your License Name] - see the [LICENSE](LICENSE) file for details.

*(Remember to create a LICENSE file in your repository and replace `[Your License Name]` above)*
