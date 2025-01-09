import paramiko
import time
import sys
from getpass import getpass

class RouterConfigurator:
    def __init__(self):
        self.ssh = None
        self.channel = None

    def connect_to_router(self, ip, username, password, enable_password):
        try:
            # Initialize SSH client
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect to the router
            self.ssh.connect(ip, username=username, password=password, look_for_keys=False)
            
            # Invoke shell
            self.channel = self.ssh.invoke_shell()
            time.sleep(1)
            
            # Enter enable mode
            self.channel.send('enable\n')
            time.sleep(1)
            self.channel.send(f'{enable_password}\n')
            time.sleep(1)
            
            # Enter config mode
            self.channel.send('configure terminal\n')
            time.sleep(1)
            
            return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    def send_command(self, command):
        self.channel.send(f'{command}\n')
        time.sleep(1)
        output = self.channel.recv(65535).decode('utf-8')
        return output

    def configure_ip_address(self):
        interface = input("Enter interface name (e.g., GigabitEthernet0/0): ")
        ip_address = input("Enter IP address: ")
        subnet_mask = input("Enter subnet mask: ")

        commands = [
            f'interface {interface}',
            'no shutdown',
            f'ip address {ip_address} {subnet_mask}',
            'exit'
        ]

        for cmd in commands:
            self.send_command(cmd)
        print(f"IP address configured on {interface}")

    def configure_vlan(self):
        vlan_id = input("Enter VLAN ID: ")
        vlan_name = input("Enter VLAN name: ")

        commands = [
            f'vlan {vlan_id}',
            f'name {vlan_name}',
            'exit'
        ]

        for cmd in commands:
            self.send_command(cmd)
        print(f"VLAN {vlan_id} configured")

    def configure_ospf(self):
        process_id = input("Enter OSPF process ID: ")
        network = input("Enter network address (e.g., 10.1.0.0): ")
        wildcard = input("Enter wildcard mask (e.g., 0.0.0.255): ")
        area = input("Enter area number: ")

        commands = [
            f'router ospf {process_id}',
            f'network {network} {wildcard} area {area}',
            'exit'
        ]

        for cmd in commands:
            self.send_command(cmd)
        print("OSPF configured")

    def reset_ospf_interface(self):
        interface = input("Enter interface name to reset OSPF: ")
        
        commands = [
            f'interface {interface}',
            'no ip ospf',
            'exit'
        ]

        for cmd in commands:
            self.send_command(cmd)
        print(f"OSPF reset on {interface}")

    def disconnect(self):
        if self.ssh:
            self.ssh.close()

def main_menu():
    print("\nWhat would you like to configure?")
    print("1. Configure an IP address")
    print("2. Configure a VLAN")
    print("3. Configure OSPF")
    print("4. Reset OSPF configuration on an interface")
    print("5. Exit")
    return input("Enter your choice (1-5): ")

def main():
    router = RouterConfigurator()
    
    # Initial connection
    print("Router Connection Setup")
    ip = input("Enter router IP address: ")
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    enable_password = getpass("Enter enable password: ")

    if not router.connect_to_router(ip, username, password, enable_password):
        print("Failed to connect to router")
        sys.exit(1)

    while True:
        choice = main_menu()
        
        if choice == '1':
            router.configure_ip_address()
        elif choice == '2':
            router.configure_vlan()
        elif choice == '3':
            router.configure_ospf()
        elif choice == '4':
            router.reset_ospf_interface()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

        next_step = input("\nWhat would you like to do next?\n"
                         "1. Configure something else\n"
                         "2. Return to main menu\n"
                         "3. Exit\n"
                         "Enter your choice (1-3): ")
        
        if next_step == '3':
            break
        elif next_step not in ['1', '2']:
            print("Invalid choice. Returning to main menu.")

    router.disconnect()
    print("Disconnected from router")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript terminated by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")