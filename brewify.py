# Author: Antoine Carreño
# Last Updated: October 27, 2023

import subprocess
import requests
from pyfzf import FzfPrompt

global install_command

# Check and install necessary Python packages
def check_and_install_packages():
    try:
        import pyfzf
    except ImportError:
        print("The 'pyfzf' package is not installed. Installing...")
        subprocess.check_call(['pip3', 'install', 'pyfzf', '--quiet'])

    try:
        import requests
    except ImportError:
        print("The 'requests' package is not installed. Installing...")
        subprocess.check_call(['pip3', 'install', 'requests', '--quiet'])

    if not subprocess.call(['command', '-v', 'fzf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
        print("'fzf' is not installed. Installing...")
        subprocess.check_call(['brew', 'install', 'fzf'])

# Check if Xcode is installed, and if not, initiate the installation
def check_xcode():
    check_path = "xcode-select -p"

    try:
        subprocess.check_output(check_path, shell=True)
        print("Xcode is already installed on your system.")
    except subprocess.CalledProcessError:
        print("Xcode is not installed. Initiating installation...")

        install_xcode = "xcode-select --install"

        try:
            subprocess.check_call(install_xcode, shell=True)
            print("Xcode has been successfully installed.")
        except subprocess.CalledProcessError as e:
            print("Xcode installation failed. Error:", e)

# Check if Homebrew is installed, and if not, initiate the installation
def check_homebrew():
    check_path = 'brew --version'

    try:
        subprocess.check_output(check_path, shell=True)
        print("Homebrew is already installed on your system.")
    except subprocess.CalledProcessError:
        print("Homebrew is not installed. Checking Xcode...")

        check_xcode()

        print("Initiating Homebrew installation...")

        install_brew = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'

        try:
            subprocess.check_call(install_brew, shell=True)
            print("Homebrew has been successfully installed.")
        except subprocess.CalledProcessError as e:
            print("Homebrew installation failed. Error:", e)

# Fetch and return a list of available formulas from Homebrew
def search_formulas():
    response = requests.get("https://formulae.brew.sh/api/formula.json")
    if response.status_code == 200:
        data = response.json()
        formula_names = [app["name"] for app in data]
        return formula_names
    else:
        print("Error fetching formula data:", response.status_code)
    return []

# Fetch and return a list of available casks from Homebrew
def search_casks():
    response = requests.get("https://formulae.brew.sh/api/cask.json")
    if response.status_code == 200:
        data = response.json()
        cask_names = [app["token"] for app in data]
        return cask_names
    else:
        print("Error fetching cask data:", response.status_code)
    return []

# Use FzfPrompt to search and select an item from a given list
def search_and_select_item(items):
    fzf = FzfPrompt()
    selected_items = fzf.prompt([f"Search and select an item:"] + items)
    return selected_items[0] if selected_items else None

# Install a Homebrew formula based on user selection
def install_application():
    form_name = search_and_select_item(search_formulas())
    if form_name:
        install_command = f'brew install {form_name}'
        subprocess.check_call(install_command, shell=True)
        print(f"{form_name} has been successfully installed.")

# Install a Homebrew cask based on user selection
def install_cask():
    cask_name = search_and_select_item(search_casks())
    if cask_name:
        install_command = f'brew install --cask {cask_name}'
        subprocess.check_call(install_command, shell=True)
        print(f"{cask_name} has been successfully installed.")

# Uninstall a Homebrew package based on user selection
def uninstall_package():
    installed_packages = subprocess.check_output(["brew", "list"]).decode("utf-8").splitlines()
    if not installed_packages:
        print("No Homebrew packages are installed on the system.")
        return

    package_to_uninstall = search_and_select_item(installed_packages)
    if package_to_uninstall:
        uninstall_command = f'brew uninstall --zap {package_to_uninstall}'
        subprocess.check_call(uninstall_command, shell=True)
        print(f"{package_to_uninstall} has been successfully uninstalled.")

# Install a bundle of Homebrew packages
def install_bundle():
    package_list = []
    package_type = None 

    while True:
        package_type = input("Do you want to add a (F)ormula or a (C)ask to the bundle (A)bort: ").lower()
        if package_type == "f":
            available_packages = search_formulas()
        elif package_type == "c":
            available_packages = search_casks()
        elif package_type == "a":
            break
        else:
            print("Invalid operation. Try again.")
            continue

        package = search_and_select_item(available_packages)
        if package:
            package_list.append(package)
            print(f"{package} has been added to the bundle.")

        continue_adding = input("Do you want to add more packages to the bundle? (Y)es (N)o: ").lower()
        if continue_adding != "y":
            break

    if package_list:
        print("Installing bundle packages...")
        installed_packages = subprocess.check_output(["brew", "list"]).decode("utf-8").splitlines()


        for package in package_list:
            if package in installed_packages:
                print(f"{package} is already installed, skipping.")
                continue
            elif package_type == "f":
                install_command = f'brew install --formula {package}' 
            elif package_type == "c":
                install_command = f'brew install --cask {package}'
            else:
                print("Skipping installation.")
                continue
            subprocess.check_call(install_command, shell=True)
            print(f"{package} has been successfully installed.")

# Main program logic
def main():
    while True:
        operation = input("What operation do you want to perform? (I)nstall (U)ninstall (E)xit: ").lower()
        if operation == "e":
            break
        if operation not in ["i", "u"]:
            print("Invalid operation. Try again.")
            continue
        
        if operation == "i":
            operation_type = input("Do you want to install a (F)ormula (C)ask (B)undle (A)bort: ").lower()
            if operation_type == "f":
                install_application()
            elif operation_type == "c":
                install_cask()
            elif operation_type == "b":
                install_bundle()
            elif operation_type == "a":
                break
            else:
                print("Invalid operation. Try again.")
        elif operation == "u":
            uninstall_package()

# Check and install Python packages
check_and_install_packages()

# Check and install Xcode and Homebrew if needed
check_xcode()
check_homebrew()

# Run the main program
main()
