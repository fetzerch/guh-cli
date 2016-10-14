# -*- coding: UTF-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                         #
#  Copyright (C) 2016 Simon Stuerz <simon.stuerz@guh.guru>                #
#                                                                         #
#  This file is part of guh-cli.                                          #
#                                                                         #
#  guh-cli is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, version 2 of the License.                #
#                                                                         #
#  guh-cli is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with guh. If not, see <http://www.gnu.org/licenses/>.            #
#                                                                         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  

import guh
import selector

        
def list_configurations():
    params = {}
    response = guh.send_command("Configuration.GetConfigurations", params)
    guh.print_json_format(response['params'])
        
        
def list_timezones():
    params = {}
    response = guh.send_command("Configuration.GetTimeZones", params)
    guh.print_json_format(response['params'])


def set_timezone():
    params = {}
    timeZones = []
    timeZones = get_timezones()
    selection = guh.get_selection("Please select one of following allowed values:", timeZones)
    if selection == None:
        return None
         
    params['timeZone'] = timeZones[selection]
    response = guh.send_command("Configuration.SetTimeZone", params)
    guh.print_json_format(response['params'])


def set_language():
    params = {}
    languages = get_languages()
    selection = guh.get_selection("Please select one of following allowed values:", languages)
    if selection == None:
        return None

    params['language'] = languages[selection]
    response = guh.send_command("Configuration.SetLanguage", params)
    guh.print_json_format(response['params'])


def set_serverName():
    params = {}         
    params['serverName'] = raw_input("Please enter the server name:")
    response = guh.send_command("Configuration.SetServerName", params)
    guh.print_json_format(response['params'])


def get_languages():
    params = {}
    response = guh.send_command("Configuration.GetAvailableLanguages", params)
    return response['params']['languages']


def get_timezones():
    params = {}
    response = guh.send_command("Configuration.GetTimeZones", params)
    return response['params']['timeZones']


def show_tcpServer_configuration():
    response = guh.send_command("Configuration.GetConfigurations")
    print "TCP server configuration\n"
    guh.print_json_format(response['params']['tcpServerConfiguration'])


def configure_tcpServer():
    configuration = guh.send_command("Configuration.GetConfigurations")
    params = {}
    params['host'] = raw_input("\nEnter the \"host\" of the TCP server (current \"%s\"): " % (configuration['params']['tcpServerConfiguration']['host'])) 
    params['port'] = raw_input("\nEnter the \"port\" of the TCP server (current %s): "% (configuration['params']['tcpServerConfiguration']['port']))
    response = guh.send_command("Configuration.SetTcpServerConfiguration", params)
    guh.print_json_format(response['params'])


def configure_webServer():
    configuration = guh.send_command("Configuration.GetConfigurations")
    params = {}
    params['host'] = raw_input("\nEnter the \"host\" of the web server (current \"%s\"): " % (configuration['params']['webServerConfiguration']['host'])) 
    params['port'] = raw_input("\nEnter the \"port\" of the web server (current %s): "% (configuration['params']['webServerConfiguration']['port']))
    response = guh.send_command("Configuration.SetWebServerConfiguration", params)
    guh.print_json_format(response['params'])


def show_webServer_configuration():
    response = guh.send_command("Configuration.GetConfigurations")
    print "Web server configuration\n"
    guh.print_json_format(response['params']['webServerConfiguration'])
    

def configure_webSocketServer():
    params = {}
    params['host'] = raw_input("\nEnter the \"host\" of the web socket server (current \"%s\"): " % (configuration['params']['webSocketServerConfiguration']['host'])) 
    params['port'] = raw_input("\nEnter the \"port\" of the web socket server (current %s): "% (configuration['params']['webSocketServerConfiguration']['port']))
    response = guh.send_command("Configuration.SetWebSocketServerConfiguration", params)
    guh.print_json_format(response['params'])


def show_webSocketServer_configuration():
    response = guh.send_command("Configuration.GetConfigurations")
    print "Web socket server configuration\n"
    guh.print_json_format(response['params']['webSocketServerConfiguration'])


def cloud_authenticate():
    params = {}
    params['username'] = raw_input("\nEnter the \"username\" of your cloud account: ")
    params['password'] = raw_input("\nEnter the \"password\" of your cloud account: ")
    response = guh.send_command("Cloud.Authenticate", params)
    guh.print_cloud_error_code(response['params']['cloudError'])
    
    
def print_cloud_status():
    params = {}
    response = guh.send_command("Cloud.GetConnectionStatus", params)
    guh.print_json_format(response['params'])

    
def enable_cloud_connection():
    params = {}
    options = ["enable", "disable"]
    selection = guh.get_selection("Do you want to do with the cloud connection: ", options)     
    if selection == 0:
        params['enable'] = True
    else:
        params['enable'] = False
    
    response = guh.send_command("Cloud.Enable", params)
    guh.print_json_format(response['params'])


def show_network_status():
    params = {}
    response = guh.send_command("NetworkManager.GetNetworkStatus", params)
    if 'status' in response['params']:
        guh.print_json_format(response['params']['status'])
    else:
        guh.print_networkmanager_error_code(response['params']['networkManagerError'])

      
def enable_networking():
    params = {}
    options = ["enable", "disable"]
    selection = guh.get_selection("Do you want to do with the networking: ", options)     
    if selection == 0:
        params['enable'] = True
    else:
        params['enable'] = False

    response = guh.send_command("NetworkManager.EnableNetworking", params)
    guh.print_networkmanager_error_code(response['params']['networkManagerError'])


def enable_wirelessnetworking():
    params = {}
    options = ["enable", "disable"]
    selection = guh.get_selection("Do you want to do with the wirless networking: ", options)     
    if selection == 0:
        params['enable'] = True
    else:
        params['enable'] = False

    response = guh.send_command("NetworkManager.EnableWirelessNetworking", params)
    guh.print_networkmanager_error_code(response['params']['networkManagerError'])
    

def selectWirelessInterface():
    params = {}    
    response = guh.send_command("NetworkManager.GetNetworkDevices", params)
    if response['params']['networkManagerError'] != 'NetworkManagerErrorNoError':
        print ("There is no wireless interface available")
        guh.print_networkmanager_error_code(response['params']['networkManagerError'])
        return None
    
    if len(response['params']['wirelessNetworkDevices']) is 1:
        return response['params']['wirelessNetworkDevices'][0]['interface']
    else:
        interfaces = []
        for wirelessNetworkDevice in response['params']['wirelessNetworkDevices']:
            interfaces.append(wirelessNetworkDevice['interface'])
        
        selection = guh.get_selection("Please select a wifi interface:", interfaces)     
        return interfaces[selection]
    
    
def list_wirelessaccesspoints():
    interface = selectWirelessInterface()
    if interface is None:
        return
        
    params = {}
    params['interface'] = interface 
    response = guh.send_command("NetworkManager.GetWirelessAccessPoints", params)
    if response['params']['networkManagerError'] != 'NetworkManagerErrorNoError':
        guh.print_networkmanager_error_code(response['params']['networkManagerError'])
    else:
        print ("Wireless accesspoints for interface %s" % interface)
        print ("---------------------------------------------------------------------")
        for accessPoint in response['params']['wirelessAccessPoints']:
            print("%20s | %5s%s | %6s %6s | %s" % (accessPoint['ssid'], accessPoint['signalStrength'], '%', accessPoint['frequency'], '[GHz]', accessPoint['macAddress']))
    

def scan_wirelessaccesspoints():
    interface = selectWirelessInterface()
    if interface is None:
        print "There is no wireless interface available"
        return
        
    params = {}
    params['interface'] = interface 
    response = guh.send_command("NetworkManager.ScanWifiNetworks", params)
    guh.print_networkmanager_error_code(response['params']['networkManagerError'])        
        
        
def list_network_devices():
    params = {}
    response = guh.send_command("NetworkManager.GetNetworkDevices", params)
    guh.print_json_format(response['params'])
    

def connect_wifi():
    interface = selectWirelessInterface()
    if interface is None:
        print "There is no wireless interface available"
        return
        
    params = {}
    params['interface'] = interface 
    wifiNetworks = []
    wifiNetworkStrings = []
    response = guh.send_command("NetworkManager.GetWirelessAccessPoints", params)
    wifiNetworks = response['params']['wirelessAccessPoints']
    for accessPoint in wifiNetworks:
        wifiNetworkStrings.append(("%10s | %s%s | %s %s | %s" % (accessPoint['ssid'], accessPoint['signalStrength'], '%', accessPoint['frequency'], '[GHz]', accessPoint['macAddress'])))
    
    selection = selector.get_selection("Wifi access points", wifiNetworkStrings)
    if not selection:
        return None
    
    params['ssid'] = wifiNetworks[selection]['ssid']
    params['password'] = raw_input("Please enter the password for wifi network %s: " % (params['ssid']))
    response = guh.send_command("NetworkManager.ConnectWifiNetwork", params)
    guh.print_networkmanager_error_code(response['params']['networkManagerError'])


def disconnect_networkdevice():
    interface = selectWirelessInterface()
    if interface is None:
        print "There is no wireless interface available"
        return
        
    params = {}
    params['interface'] = interface
    response = guh.send_command("NetworkManager.DisconnectInterface", params)
    guh.print_networkmanager_error_code(response['params']['networkManagerError'])


