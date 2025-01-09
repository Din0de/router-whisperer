# router-whisperer

This script includes:

A RouterConfigurator class that handles all router operations
SSH connectivity using paramiko
Functions for each configuration option
Error handling and graceful disconnection
A main menu system with all requested options
Secure password input using getpass

---------------------------------------------------------

Install the required package(s) on Ubuntu:

Update the package list:
sudo apt update

Install pip (if it's not already installed):
sudo apt install python3-pip

Install Paramiko using pip:
pip3 install paramiko

---------------------------------------------------------

Make sure you have network connectivity to the router
Have valid credentials for the router

---------------------------------------------------------

Best tested with:

Best tested using Ubuntu virtual machines imported into GNS3. 
You can set up Linux-based VMs in GNS3 and connect them to 
Cisco routers to fully simulate and test the configuration process.

---------------------------------------------------------

The script provides:

Secure SSH connections
Error handling for connection issues
A clean interface for router configuration
Proper command timing using sleep
Clean disconnection when finished

---------------------------------------------------------

When running the script, it will:

Prompt for router connection details
Connect to the router
Present the main menu
Execute the selected configuration
Ask for next steps
Properly disconnect when finished
The script handles all the required functionality while maintaining a clean and user-friendly interface. It also includes error handling to prevent crashes and ensure proper resource cleanup.
