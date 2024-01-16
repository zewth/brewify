# Brewify
This Python script simplifies the management of Homebrew packages on macOS. It provides an easy-to-use interface to install, uninstall, and create bundles of Homebrew formulas and casks. Whether you're a developer or a power user, this tool can streamline the process of managing your software packages.

**Note: This script is designed for macOS users who use Homebrew, a package manager specific to macOS. If you're using other package managers or operating systems, the functionality may differ.**

## Usage

Before using the script, make sure you have the following prerequisites:
- ``python3``` (3.6 and so):
- ```pyfzf``` & ```requests``` - These Python packages are required for the script to work. You can install them with `pip3` if needed.
- ```fzf```

Here's how to use the script:

- Run the script in your terminal to initiate the Homebrew package manager.
- Choose from the following options:
  - **Install**: Install individual formulas, casks, or bundles.
  - **Uninstall**: Remove installed packages.
  - **Bundle**: Create a bundle of packages to install as a group.

The script uses Fzf for a user-friendly interface, making package management more efficient and straightforward. You can select packages from a list and follow the prompts to complete the installation or uninstallation process.

Feel free to explore the script's capabilities and simplify your Homebrew package management on macOS.

## Installation

1. Clone this repository to your local machine.
2. Make sure you have the prerequisites mentioned above installed.
3. Run the script in your terminal by executing `python brewify.py`.

Enjoy hassle-free Homebrew package management with this script!

## Demo
![][brewify_demo.gif]

## Author
- Antoine Carreño

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
