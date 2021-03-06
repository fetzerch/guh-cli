# -*- coding: UTF-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                         #
#  Copyright (C) 2015 Simon Stuerz <simon.stuerz@guh.guru>                #
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
import devices

def get_stateType(stateTypeId):
    params = {}
    params['stateTypeId'] = stateTypeId
    response = guh.send_command("States.GetStateType", params);
    if "stateType" in response['params']:
        return response['params']['stateType']
    return None
    

def get_stateTypes(deviceClassId):
    params = {}
    params['deviceClassId'] = deviceClassId
    response = guh.send_command("Devices.GetStateTypes", params);
    if "stateTypes" in response['params']:
        return response['params']['stateTypes']
    else:
        return None


def select_stateType(deviceClassId):
    stateTypes = get_stateTypes(deviceClassId)
    if not stateTypes:
        print "\n    This device has no states.\n"
        print "\n========================================================"
        raw_input("-> Press \"enter\" to select an other device!  ")
        return None
    stateTypeList = []
    for i in range(len(stateTypes)):
        stateTypeList.append(stateTypes[i]['name'])
    selection = guh.get_selection("Please select a state type:", stateTypeList)
    if selection != None:
        return stateTypes[selection]
    return None

def create_stateDescriptor():
    print "-> Creating a new stateDescriptor:\n"
    deviceId = devices.select_configured_device()
    device = devices.get_device(deviceId)
    if device == None:
        return None
    stateType = select_stateType(device['deviceClassId']);
    if stateType == None:
        return None
    valueOperator = guh.select_valueOperator(stateType['name'])

    stateDescriptor = {}

    print "\nThe StateType looks like this:\n", guh.print_json_format(stateType)
    print "Please enter the value for state \"%s\" (type: %s): " % (stateType['name'], stateType['type'])
    # make bool selectable to make shore they are "true" or "false"
    if any("possibleValues" in item for item in stateType):
        # has to be a string (for sorting list)
        possibleValues = []
        for value in stateType['possibleValues']:
            possibleValues.append(str(value))
        selection = guh.get_selection("Please select one of following possible values:", possibleValues)
        if selection == None:
            return None
        stateValue = stateType['possibleValues'][selection]
    else:
        # make bool selectable to make shore they are "true" or "false"
        if stateType['type'] == "Bool":
            boolTypes = ["true","false"]
            selectionString = "Please enter the value for state \"%s\" (type: %s): " % (stateType['name'], stateType['type'])
            selection = guh.get_selection(selectionString, boolTypes)
            if selection == None:
                return None
            stateValue = boolTypes[selection] 
        elif stateType['type'] == "Int": 
            stateValue = int(raw_input("%s %s " % (stateType['name'], guh.get_valueOperator_string(valueOperator))))
        elif stateType['type'] == "Double": 
            stateValue = float(raw_input("%s %s " % (stateType['name'], guh.get_valueOperator_string(valueOperator))))
        elif stateType['type'] == "Uint": 
            stateValue = int(raw_input("%s %s " % (stateType['name'], guh.get_valueOperator_string(valueOperator))))
        else:
            stateValue = raw_input("%s %s " % (stateType['name'], guh.get_valueOperator_string(valueOperator))) 

    stateDescriptor['deviceId'] = deviceId
    stateDescriptor['stateTypeId'] = stateType['id']
    stateDescriptor['value'] = stateValue
    stateDescriptor['operator'] = valueOperator
    print guh.print_json_format(stateDescriptor)
    return stateDescriptor


def create_stateDescriptors():
    enough = False
    stateDescriptors = []
    while not enough:
        stateDescriptor = create_stateDescriptor()
        if stateDescriptor != None:
            stateDescriptors.append(stateDescriptor)
            input = raw_input("Do you want to add another stateDescriptor? (y/N): ")
            if not input == "y":
                enough = True
    return stateDescriptors


def create_stateEvaluator(stateDescriptors = None):
    # check if we already have created a stateDescriptor
    if stateDescriptors == None:
        stateDescriptors = create_stateDescriptors()
        # if we have more than one stateDescriptor created...
        if len(stateDescriptors) > 1:
            # create child operators
            childEvaluators = []
            for i in range(len(stateDescriptors)):
                # recursive call... create a stateEvaluator for each stateDescriptor
                stateDescriptor = []                            # has to be a list to enable recursive calls
                stateDescriptor.append(stateDescriptors[i])                # append the single stateDescriptor to list (count =1)
                childEvaluators.append(create_stateEvaluator(stateDescriptor))        # append the new childEvaluator to the real child... recursive call
            stateEvaluator = {}
            stateEvaluator['childEvaluators'] = childEvaluators
            stateEvaluator['operator'] = guh.select_stateOperator()
            return stateEvaluator
        else:
            # add single stateDescriptor to the stateEvaluator
            stateEvaluator = {}
            stateEvaluator['stateDescriptor'] = stateDescriptors[0]
            return stateEvaluator
    else:
        # we got already a stateDescriptors list
        if len(stateDescriptors) > 1:
            # create child operators
            childEvaluators = []
            for i in range(len(stateDescriptors)):
                # recursive call... create a stateEvaluator for each stateDescriptor
                stateDescriptor = []                            # has to be a list to enable recursive calls
                stateDescriptor.append(stateDescriptors[i])                # append the single stateDescriptor to list (count =1)
                childEvaluators.append(create_stateEvaluator(stateDescriptor))        # append the new childEvaluator to the real child... recursive call
            stateEvaluator = {}
            stateEvaluator['childEvaluators'] = childEvaluators
            stateEvaluator['operator'] = guh.select_stateOperator()
            return stateEvaluator
        else:
            # add single stateDescriptor to the stateEvaluator
            stateEvaluator = {}
            stateEvaluator['stateDescriptor'] = stateDescriptors[0]
            return stateEvaluator


def print_stateEvaluator(stateEvaluator):
    if not stateEvaluator:
        return None
    if 'stateDescriptor' in stateEvaluator:
        stateType = get_stateType(stateEvaluator['stateDescriptor']['stateTypeId'])
        deviceName = devices.get_full_device_name(stateEvaluator['stateDescriptor']['deviceId'])
        print "%5s. -> %40s -> state: \"%s\"" %(0, deviceName, stateType['name'])
        print "%50s %s %s" %(stateType['name'], guh.get_valueOperator_string(stateEvaluator['stateDescriptor']['operator']), stateEvaluator['stateDescriptor']['value'])
    else:
        if not 'childEvaluators' in stateEvaluator:
            return None
        for i in range(len(stateEvaluator['childEvaluators'])):
            device = devices.get_device(stateEvaluator['childEvaluators'][i]['stateDescriptor']['deviceId'])
            stateType = get_stateType(stateEvaluator['childEvaluators'][i]['stateDescriptor']['stateTypeId'])
            print "(%s:%s" % (device['name'], stateType['name']),
            print guh.get_valueOperator_string(stateEvaluator['childEvaluators'][i]['stateDescriptor']['operator']),
            print stateEvaluator['childEvaluators'][i]['stateDescriptor']['value'], ")", 
            if i != (len(stateEvaluator['childEvaluators']) - 1):
                print "%s%s" % (guh.get_stateEvaluator_string(stateEvaluator['operator']), guh.get_stateEvaluator_string(stateEvaluator['operator'])),
        print "\n"


def print_stateType():
    deviceId = devices.select_configured_device()
    device = devices.get_device(deviceId)
    if device == None:
        return None
    stateType = select_stateType(device['deviceClassId']);
    if stateType == None:
        return None
    guh.print_json_format(stateType)




