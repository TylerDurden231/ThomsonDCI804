# -*- coding: utf-8 -*-
# Test name = Software Upgrade
# Test description = Set environment, perform software upgrade and check STB state after sw upgrade

from datetime import datetime
from time import gmtime, strftime
import time
import device
import TEST_CREATION_API
import shutil
import os.path
import sys
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')

try:    
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py")) == False) or (str(os.path.getmtime('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py')) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))))):
        shutil.copy2('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py', os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))
except:
    pass

import NOS_API
    
try:
    # Get model
    model_type = NOS_API.get_model()

    # Check if folder with thresholds exists, if not create it
    if(os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds")) == False):
        os.makedirs(os.path.join(os.path.dirname(sys.executable), "Thresholds"))

    # Copy file with threshold if does not exists or if it is updated
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt")) == False) or (str(os.path.getmtime(NOS_API.THRESHOLDS_PATH + model_type + ".txt")) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))))):
        shutil.copy2(NOS_API.THRESHOLDS_PATH + model_type + ".txt", os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))
except Exception as error_message:
    pass
    
## Number of alphanumeric characters in SN
SN_LENGTH = 15 

## Number of alphanumeric characters in Cas_Id
CASID_LENGTH = 12

## Number of alphanumeric characters in MAC
MAC_LENGTH = 12

## Time in seconds which define when dialog will be closed
DIALOG_TIMEOUT = 10

## Number of alphanumeric characters in MAC
MAC_LENGTH = 12

## Constant multiplier used for conversion from seconds to milliseconds
MS_MULTIPLIER = 1000

## Max time to perform sw upgrade (in seconds)
SW_UPGRADE_TIMEOUT = 440

## Time needed to STB power on (in seconds)
WAIT_TO_POWER_STB = 20

## Time to press V+/V- simultaneous in seconds
TIMEOUT_CAUSE_SW_UPGRADE = 4

## Time to switch from HDMI to SCART in seconds
WAIT_TO_SWITCH_SCART = 6

def runTest():
    
    System_Failure = 0
    
    NOS_API.read_thresholds()
    
    NOS_API.reset_test_cases_results_info() 
   
    ## Skip this test case if some previous test failed
    if not(NOS_API.test_cases_results_info.isTestOK):
        TEST_CREATION_API.update_test_result(TEST_CREATION_API.TestCaseResult.FAIL)
        return
    
    while (System_Failure < 2):
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"
            
            error_codes = ""
            error_messages = ""
            SN_LABEL = False
            CASID_LABEL = False
            MAC_LABEL = False 
            
            Repeat_Block = 0

            Max_Num_Boots = 4

            NoBoot = 0
            
            ## Read STB Labels using barcode reader (S/N, CAS ID, MAC and SAP) and LOG it 
            try:      
                all_scanned_barcodes = NOS_API.get_all_scanned_barcodes()
                NOS_API.test_cases_results_info.s_n_using_barcode = all_scanned_barcodes[1]
                NOS_API.test_cases_results_info.cas_id_using_barcode = all_scanned_barcodes[2]
                NOS_API.test_cases_results_info.mac_using_barcode = all_scanned_barcodes[3]
                NOS_API.test_cases_results_info.nos_sap_number = all_scanned_barcodes[0]
            except Exception as error:
                TEST_CREATION_API.write_log_to_file(error)
                TEST_CREATION_API.write_log_to_file("Bad Scanning")
                test_result = "FAIL"
                #TEST_CREATION_API.update_test_result(test_result)                
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message 
                System_Failure = 2
                
            test_number = NOS_API.get_test_number(NOS_API.test_cases_results_info.s_n_using_barcode)
            device.updateUITestSlotInfo("Teste N\xb0: " + str(int(test_number)+1))
            
            if ((len(NOS_API.test_cases_results_info.s_n_using_barcode) == SN_LENGTH) and (NOS_API.test_cases_results_info.s_n_using_barcode.isalnum() or NOS_API.test_cases_results_info.s_n_using_barcode.isdigit())):
                SN_LABEL = True
            
            if ((len(NOS_API.test_cases_results_info.cas_id_using_barcode) == CASID_LENGTH) and (NOS_API.test_cases_results_info.cas_id_using_barcode.isalnum() or NOS_API.test_cases_results_info.cas_id_using_barcode.isdigit())):
                CASID_LABEL = True
                
            if ((len(NOS_API.test_cases_results_info.mac_using_barcode) == MAC_LENGTH) and (NOS_API.test_cases_results_info.mac_using_barcode.isalnum() or NOS_API.test_cases_results_info.mac_using_barcode.isdigit())):
                MAC_LABEL = True
            
            if not(SN_LABEL and CASID_LABEL and MAC_LABEL):
                TEST_CREATION_API.write_log_to_file("Bad Scanning")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message         
                test_result = "FAIL"
                
                NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                report_file = ""
                if (test_result != "PASS"):
                    report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                    NOS_API.upload_file_report(report_file)
                    NOS_API.test_cases_results_info.isTestOK = False


                ## Update test result
                TEST_CREATION_API.update_test_result(test_result)
                
                ## Return DUT to initial state and de-initialize grabber device
                NOS_API.deinitialize()
                
                NOS_API.send_report_over_mqtt_test_plan(
                    test_result,
                    end_time,
                    error_codes,
                    report_file)

                return
            
    ####################################################################################################################################################################################################################################
    ################################################################################################### Sofware Upgrade ################################################################################################################
    #################################################################################################################################################################################################################################### 
     
            ## Initialize grabber device
            NOS_API.initialize_grabber()
            
            #NOS_API.reset_dut()

            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)

            if ((len(NOS_API.test_cases_results_info.mac_using_barcode) == MAC_LENGTH) and (NOS_API.test_cases_results_info.mac_using_barcode.isalnum() or NOS_API.test_cases_results_info.mac_using_barcode.isdigit())):

                ## Power off STB with energenie
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_off()): 
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)

                        return
                    time.sleep(1)
                    ## Power on STB with energenie
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        test_result = "FAIL"
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                        
                        return
                    time.sleep(1)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    NOS_API.set_error_message("POWER SWITCH")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                    error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    NOS_API.add_test_case_result_to_file_report(
                            test_result,
                            "- - - - - - - - - - - - - - - - - - - -",
                            "- - - - - - - - - - - - - - - - - - - -",
                            error_codes,
                            error_messages)
                
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = NOS_API.create_test_case_log_file(
                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                NOS_API.test_cases_results_info.nos_sap_number,
                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                NOS_API.test_cases_results_info.mac_using_barcode,
                                end_time)
                    NOS_API.upload_file_report(report_file)
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                   
                    return 
                
                if(System_Failure == 0):
                    if not(NOS_API.display_new_dialog("Conectores?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                        TEST_CREATION_API.write_log_to_file("Conectores NOK")
                        NOS_API.set_error_message("Danos Externos")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.conector_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.conector_nok_error_message)
                        error_codes = NOS_API.test_cases_results_info.conector_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.conector_nok_error_message  
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
            
            
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        return
                    if not(NOS_API.display_new_dialog("Chassis?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                        TEST_CREATION_API.write_log_to_file("Chassis NOK")
                        NOS_API.set_error_message("Danos Externos")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.chassis_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.chassis_nok_error_message) 
                        error_codes = NOS_API.test_cases_results_info.chassis_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.chassis_nok_error_message  
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
            
            
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)

                        return
                    if not(NOS_API.display_custom_dialog("A STB est\xe1 ligada? Insira o SmartCard", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"): 
                        TEST_CREATION_API.write_log_to_file("No Power")

                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_power_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_power_error_message)
                        NOS_API.set_error_message("Não Liga")
                        error_codes = NOS_API.test_cases_results_info.no_power_error_code
                        error_messages = NOS_API.test_cases_results_info.no_power_error_message 
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
            
            
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
        
                        return
                    if not(NOS_API.display_custom_dialog("O Led REC ligou?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                        TEST_CREATION_API.write_log_to_file("Led REC NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.led_rec_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.led_rec_nok_error_message)
                        NOS_API.set_error_message("Led's")
                        error_codes = NOS_API.test_cases_results_info.led_rec_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.led_rec_nok_error_message 
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
            
            
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
        
                        return
                    if not(NOS_API.display_custom_dialog("Ventoinha?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                        TEST_CREATION_API.write_log_to_file("FAN is not running")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.fan_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.fan_error_message)
                        NOS_API.set_error_message("Ventoinha")
                        error_codes = NOS_API.test_cases_results_info.fan_error_code
                        error_messages = NOS_API.test_cases_results_info.fan_error_message
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
            
            
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
        
                        return
                    
                while(Repeat_Block < Max_Num_Boots and NoBoot < 2):
                    if (Repeat_Block != 0 or NoBoot != 0):
                        if not(NOS_API.power_off()):
                            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            NOS_API.set_error_message("POWER SWITCH")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                            error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                            error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                        
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                            NOS_API.upload_file_report(report_file)
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                            
                            return
                        time.sleep(3)
                        ## Power on STB with energenie
                        if not(NOS_API.power_on()):
                            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            NOS_API.set_error_message("POWER SWITCH")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                            error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                            error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                        
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                            NOS_API.upload_file_report(report_file)
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                            
                            return
                        time.sleep(10)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                    
                        ## Initialize grabber device
                        NOS_API.initialize_grabber()
                        
                        ## Start grabber device with video on default video source
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                        
                    ## Check is signal present on HDMI during sw upgrade
                    if (NOS_API.is_signal_present_on_video_source()):

                        ## Wait to display image after signal is present 
                        time.sleep(5)
                        TEST_CREATION_API.send_ir_rc_command("[CH+]")
                        time.sleep(2)
                        TEST_CREATION_API.send_ir_rc_command("[CH-]")
                        time.sleep(1)
                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                        time.sleep(2)
                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                        time.sleep(2)
                        TEST_CREATION_API.send_ir_rc_command("[MENU]")
                        time.sleep(2)

                        if not(NOS_API.grab_picture("menu")):
                            if (Repeat_Block == 3):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                return   
                            else:
                                TEST_CREATION_API.write_log_to_file("STB lost Signal during boot. Try Again")
                                Repeat_Block = Repeat_Block + 1
                                continue

                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "576" and video_height != "720" and video_height != "1080"):
                            time.sleep(10)
                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "576" and video_height != "720" and video_height != "1080"):
                                TEST_CREATION_API.write_log_to_file("Detected height of HDMI Signal was " + video_height + ". Expected height was 576 or 720 or 1080.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                return
                        if(video_height == "720"):
                            result = NOS_API.wait_for_multiple_pictures(
                                    ["blue_ref1", "blue_ref2", "blue_ref3", "Upgrade_Error_ref", "update_ref_NOS", "update_screen_576_ref", "update_screen_720_ref", "update_screen_1080_ref", "update_ref"],
                                    5,
                                    ["[OLD_ZON]", "[OLD_ZON]", "[OLD_ZON]", "[Upgrade_Error_new]", "[FULL_SCREEN]", "[UPDATE_SCREEN_576]", "[UPDATE_SCREEN_720]", "[UPDATE_SCREEN_1080]", "[FULL_SCREEN]"],
                                    [80, 80, 80, 80, 80, 80, 80, 80, 80])
                            if (result == -2):
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                
                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                
                                return        
                            elif (result >= 0 and result < 4):
                                NOS_API.test_cases_results_info.isTestOK = False  
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_message)
                                NOS_API.set_error_message("Não Actualiza")
                                error_codes = NOS_API.test_cases_results_info.sw_upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.sw_upgrade_nok_error_message
                                test_result = "FAIL"

                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                return
                            elif (result >= 4 and result < 8):
                                time.sleep(5)
                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                if (NOS_API.wait_for_signal_sw_upgrade_thomson(600)):
                                    time.sleep(10)
                                    if (NOS_API.wait_for_signal_sw_upgrade_thomson(600)):
                                        time.sleep(60)    
                                if not(NOS_API.is_signal_present_on_video_source()):
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(5)
                                result = NOS_API.wait_for_multiple_pictures(
                                        ["blue_ref1", "blue_ref2", "blue_ref3", "Upgrade_Error_ref", "update_ref_NOS", "update_screen_576_ref", "update_screen_720_ref", "update_screen_1080_ref", "update_ref"],
                                        5,
                                        ["[OLD_ZON]", "[OLD_ZON]", "[OLD_ZON]", "[Upgrade_Error_new]", "[FULL_SCREEN]", "[UPDATE_SCREEN_576]", "[UPDATE_SCREEN_720]", "[UPDATE_SCREEN_1080]", "[FULL_SCREEN]"],
                                        [80, 80, 80, 80, 80, 80, 80, 80, 80])
                                if (result == -2):
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                    
                                    return        
                                elif (result >= 0 and result < 8):
                                    NOS_API.test_cases_results_info.isTestOK = False  
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_message)
                                    NOS_API.set_error_message("Não Actualiza")
                                    error_codes = NOS_API.test_cases_results_info.sw_upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.sw_upgrade_nok_error_message
                                    test_result = "FAIL"

                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                    return
                                elif (result == 8):
                                    result_nagra = 0
                                    while(result_nagra == 0):
                                        time.sleep(2)
                                        result_nagra = NOS_API.wait_for_multiple_pictures(["update_ref"], 5, ["[FULL_SCREEN]"], [80])
                                        NOS_API.test_cases_results_info.DidUpgrade = 1
                                    time.sleep(1)
                                    result_error = NOS_API.wait_for_multiple_pictures(["Upgrade_Error_ref"], 5, ["[Upgrade_Error_new]"], [80])
                                    if(result_error == 0):
                                        NOS_API.test_cases_results_info.isTestOK = False  
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_message)
                                        NOS_API.set_error_message("Não Actualiza")
                                        error_codes = NOS_API.test_cases_results_info.sw_upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.sw_upgrade_nok_error_message
                                        test_result = "FAIL"

                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                        return
                                    
                            elif (result == 8):
                                result_nagra = 0
                                while(result_nagra == 0):
                                    time.sleep(2)
                                    result_nagra = NOS_API.wait_for_multiple_pictures(["update_ref"], 5, ["[FULL_SCREEN]"], [80])
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                time.sleep(1)
                                result_error = NOS_API.wait_for_multiple_pictures(["Upgrade_Error_ref"], 5, ["[Upgrade_Error_new]"], [80])
                                if(result_error == 0):
                                    NOS_API.test_cases_results_info.isTestOK = False  
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_message)
                                    NOS_API.set_error_message("Não Actualiza")
                                    error_codes = NOS_API.test_cases_results_info.sw_upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.sw_upgrade_nok_error_message
                                    test_result = "FAIL"

                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                    return
                        if(video_height == "576" or video_height == "1080"):
                            NOS_API.SET_720 = True
                        else:
                            NOS_API.SET_720 = False                                    
                            
                        if not(video_height == "576"):
                            threshold = TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD
                        else:
                            threshold = NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD

                        ## Depends on resolution set appropriate picture and macro
                        if (TEST_CREATION_API.compare_pictures("menu_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menublack_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menu_" + video_height + "_eng_ref", "menu", "[MENU_" + video_height + "]", threshold)):
                            #############################################
                            if(NOS_API.SET_720):
                                ## Set resolution to 720p and navigate to the signal level settings
                                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                time.sleep(3)
                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                if(video_height != "720"):
                                    time.sleep(1)
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                    TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                    time.sleep(3)
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                    if (video_height != "720"):
                                        NOS_API.set_error_message("Resolução")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                        error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                        error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                        test_result = "FAIL"
                                    
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                        
                                        return 

                            NOS_API.test_cases_results_info.channel_boot_up_state = True
                        else:
                            if(video_height == "720"):
                                result = NOS_API.wait_for_multiple_pictures(["installation_boot_up_ref", "installation_boot_up_ref_NOS", "installation_boot_up_eng_ref"], 8, ["[Inst_Mode]", "[Inst_Mode]", "[Inst_Mode_Eng]"], [80, 80, 80])
                                if not(result == 0 or result == 1 or result == 2):
                                    TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                    TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                    time.sleep(2)

                                    if not(NOS_API.grab_picture("menu")):
                                        if (Repeat_Block == 3):
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
        
        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                            return                                            
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal during boot. Try Again")
                                            Repeat_Block = Repeat_Block + 1
                                            continue

                                    ## Depends on resolution set appropriate picture and macro
                                    if (TEST_CREATION_API.compare_pictures("menu_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menublack_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menu_" + video_height + "_eng_ref", "menu", "[MENU_" + video_height + "]", threshold)):
                                        #############################################
                                        if(NOS_API.SET_720):
                                            ## Set resolution to 720p and navigate to the signal level settings
                                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                            TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                            time.sleep(3)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                            if(video_height != "720"):
                                                time.sleep(1)
                                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                                TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                                time.sleep(3)
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                if (video_height != "720"):
                                                    NOS_API.set_error_message("Resolução")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                                    error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                                    error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                                    test_result = "FAIL"
                                                
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                    
                                                    return 
                                        
                                        NOS_API.test_cases_results_info.channel_boot_up_state = True
                                    else:
                                        if not(NOS_API.grab_picture("menu_1")):
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
        
        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                            return
                                        
                                        if(TEST_CREATION_API.compare_pictures("menu", "menu_1")):
                                            if (Repeat_Block == 3):
                                                TEST_CREATION_API.write_log_to_file("STB Blocks")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.block_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.block_error_message)
                                                NOS_API.set_error_message("STB bloqueou")
                                                error_codes = NOS_API.test_cases_results_info.block_error_code
                                                error_messages = NOS_API.test_cases_results_info.block_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                test_result = "FAIL"
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                
                                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                            
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                return
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB Blocks. Try Again")
                                                Repeat_Block = Repeat_Block + 1
                                                continue
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
        
        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                            return                                       
                                else:
                                    NOS_API.test_cases_results_info.channel_boot_up_state = False

                            else:
                                TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                time.sleep(2)

                                if not(NOS_API.grab_picture("menu")):
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False


                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    return 

                                ## Depends on resolution set appropriate picture and macro
                                if (TEST_CREATION_API.compare_pictures("menu_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menublack_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menu_" + video_height + "_eng_ref", "menu", "[MENU_" + video_height + "]", threshold)):
                                    #############################################
                                    if(NOS_API.SET_720):
                                        ## Set resolution to 720p and navigate to the signal level settings
                                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                        TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                        time.sleep(3)
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                        if(video_height != "720"):
                                            time.sleep(1)
                                            TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                            TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                            time.sleep(3)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                            if (video_height != "720"):
                                                NOS_API.set_error_message("Resolução")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                                test_result = "FAIL"
                                            
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                
                                                return 
                                    
                                    NOS_API.test_cases_results_info.channel_boot_up_state = True

                                    if (TEST_CREATION_API.compare_pictures("menu_" + video_height + "_eng_ref", "menu", "[MENU_" + video_height + "]", threshold)):
                                        NOS_API.IN_PT = False
                                else:
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message) 
                                    NOS_API.set_error_message("IR")
                                    error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                                    test_result = "FAIL"
                        
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                
                                    return                                                          
                        test_result = "PASS"
                        Repeat_Block = 4
                    else:
                        NOS_API.grabber_stop_video_source()
                        time.sleep(0.4)
                        ## Initialize input interfaces of DUT RT-AV101 device 
                        NOS_API.reset_dut()  
                        ## Start grabber device with video on SCART video source
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                        ## Check is signal present on SCART
                        if (NOS_API.is_signal_present_on_video_source()):
                            if not(NOS_API.grab_picture("SCART")):
                                TEST_CREATION_API.write_log_to_file("Failed to get picture")                                                            
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on SCART")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                                NOS_API.set_error_message("Video SCART")
                                error_codes = NOS_API.test_cases_results_info.scart_image_absence_error_code
                                error_messages = NOS_API.test_cases_results_info.scart_image_absence_error_message
                                test_result = "FAIL"
                            
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                return        
                                            
                            NOS_API.grabber_stop_video_source()
                            
                            ## Start grabber device with video on HDMI video source
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)

                            ## Check is signal present on HDMI
                            if not(NOS_API.is_signal_present_on_video_source()): 
                            
                                NOS_API.display_dialog("Confirme o cabo HDMI e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                time.sleep(3)
                                
                                ## Check is signal present on HDMI
                                if not(NOS_API.is_signal_present_on_video_source()): 
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI (Não Retestar)")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    test_result = "FAIL"
                                
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
    
    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    
                                    return        
                        
                        else:
                            NOS_API.grabber_stop_video_source()
                            time.sleep(0.4)
                            
                            ## Start grabber device with video on HDMI video source
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)

                        ## If signal is not present on HDMI, power on STB
                        if not(NOS_API.is_signal_present_on_video_source()):
                            ## Press POWER key
                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                            if not(NOS_API.is_signal_present_on_video_source()):
                                time.sleep(5)
                                if not(NOS_API.is_signal_present_on_video_source()):
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(5)
                                    if not(NOS_API.is_signal_present_on_video_source()):
                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                        time.sleep(3)
                                    if not(NOS_API.is_signal_present_on_video_source()):
                                        NOS_API.grabber_stop_video_source()
                                        time.sleep(0.4)
                                        
                                        ## Initialize input interfaces of DUT RT-AV101 device 
                                        NOS_API.reset_dut()
                                        ## Start grabber device with video on SCART video source
                                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                                        
                                        ## Check is signal present on SCART
                                        if (NOS_API.is_signal_present_on_video_source()):
                                            if not(NOS_API.grab_picture("SCART")):
                                                TEST_CREATION_API.write_log_to_file("Failed to get picture")                                                            
                                                TEST_CREATION_API.write_log_to_file("Image is not displayed on SCART")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                                                NOS_API.set_error_message("Video SCART")
                                                error_codes = NOS_API.test_cases_results_info.scart_image_absence_error_code
                                                error_messages = NOS_API.test_cases_results_info.scart_image_absence_error_message
                                                test_result = "FAIL"
                                            
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                
                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                return        
                                            
                                            NOS_API.grabber_stop_video_source()
                                            time.sleep(0.4)
                                            
                                            ## Start grabber device with video on HDMI video source
                                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                            
                                            if not(NOS_API.is_signal_present_on_video_source()):
                                                NOS_API.display_dialog("Confirme o cabo HDMI e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                                time.sleep(3)
                                                if not(NOS_API.is_signal_present_on_video_source()):
                                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                    NOS_API.set_error_message("Video HDMI")
                                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                    test_result = "FAIL"
                                        
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                    return        
                                        else:
                                            if (NoBoot == 1):
                                                TEST_CREATION_API.write_log_to_file("No boot")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                                #NOS_API.set_error_message("N\xe3o arranca")
                                                NOS_API.set_error_message("Não arranca")
                                                error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                                error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                                test_result = "FAIL"
                                            
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                
                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                return 
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB didn't boot. Try Again")
                                                NoBoot = NoBoot + 1
                                                continue
                    
                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "576" and video_height != "720" and video_height != "1080"):
                                time.sleep(10)
                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                if (video_height != "576" and video_height != "720" and video_height != "1080"):
                                    TEST_CREATION_API.write_log_to_file("Detected height of HDMI Signal was " + video_height + ". Expected height was 576 or 720 or 1080.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False


                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    
                                    return
                            if not(NOS_API.grab_picture("menu")):                          
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                
                                return 
                            result = NOS_API.wait_for_multiple_pictures(
                                    ["blue_ref1", "blue_ref2", "blue_ref3", "Upgrade_Error_ref", "update_ref_NOS", "update_screen_576_ref", "update_screen_720_ref", "update_screen_1080_ref", "update_ref"],
                                    10,
                                    ["[OLD_ZON]", "[OLD_ZON]", "[OLD_ZON]", "[Upgrade_Error_new]", "[FULL_SCREEN]", "[UPDATE_SCREEN_576]", "[UPDATE_SCREEN_720]", "[UPDATE_SCREEN_1080]", "[FULL_SCREEN]"],
                                    [80, 80, 80, 80, 80, 80, 80, 80, 80])
                            if (result == -2):
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                
                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                
                                return        
                            elif (result >= 0 and result < 4):
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                NOS_API.set_error_message("Não Actualiza") 
                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                return  
                            elif (result >= 4 and result < 8):
                                time.sleep(5)
                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                if (NOS_API.wait_for_signal_sw_upgrade_thomson(600)):
                                    time.sleep(10)
                                    if (NOS_API.wait_for_signal_sw_upgrade_thomson(600)):
                                        time.sleep(60)   
                                if not(NOS_API.is_signal_present_on_video_source()):
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(5)        
                                result = NOS_API.wait_for_multiple_pictures(
                                        ["blue_ref1", "blue_ref2", "blue_ref3", "Upgrade_Error_ref", "update_ref_NOS", "update_screen_576_ref", "update_screen_720_ref", "update_screen_1080_ref", "update_ref"],
                                        5,
                                        ["[OLD_ZON]", "[OLD_ZON]", "[OLD_ZON]", "[Upgrade_Error_new]", "[FULL_SCREEN]", "[UPDATE_SCREEN_576]", "[UPDATE_SCREEN_720]", "[UPDATE_SCREEN_1080]", "[FULL_SCREEN]"],
                                        [80, 80, 80, 80, 80, 80, 80, 80, 80])
                                if (result == -2):
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                    
                                    return        
                                elif (result >= 0 and result < 8):
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False


                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    return  
                                elif (result == 8):
                                    result_nagra = 0
                                    while(result_nagra == 0):
                                        time.sleep(2)
                                        result_nagra = NOS_API.wait_for_multiple_pictures(["update_ref"], 5, ["[FULL_SCREEN]"], [80])
                                        NOS_API.test_cases_results_info.DidUpgrade = 1
                                    time.sleep(1)
                                    result_error = NOS_API.wait_for_multiple_pictures(["Upgrade_Error_ref"], 5, ["[Upgrade_Error_new]"], [80])
                                    if(result_error == 0):
                                        NOS_API.test_cases_results_info.isTestOK = False  
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_message)
                                        NOS_API.set_error_message("Não Actualiza")
                                        error_codes = NOS_API.test_cases_results_info.sw_upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.sw_upgrade_nok_error_message
                                        test_result = "FAIL"

                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                        return
                            elif (result == 8):
                                result_nagra = 0
                                while(result_nagra == 0):
                                    time.sleep(2)
                                    result_nagra = NOS_API.wait_for_multiple_pictures(["update_ref"], 5, ["[FULL_SCREEN]"], [80])
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                time.sleep(1)
                                result_error = NOS_API.wait_for_multiple_pictures(["Upgrade_Error_ref"], 5, ["[Upgrade_Error_new]"], [80])
                                if(result_error == 0):
                                    NOS_API.test_cases_results_info.isTestOK = False  
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_message)
                                    NOS_API.set_error_message("Não Actualiza")
                                    error_codes = NOS_API.test_cases_results_info.sw_upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.sw_upgrade_nok_error_message
                                    test_result = "FAIL"

                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                    return

                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")

                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "576" and video_height != "720" and video_height != "1080"):
                            time.sleep(10)
                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "576" and video_height != "720" and video_height != "1080"):
                                TEST_CREATION_API.write_log_to_file("Detected height of HDMI Signal was " + video_height + ". Expected height was 576 or 720 or 1080.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                
                                return
                        if(video_height == "720"):
                            if not(NOS_API.grab_picture("screen")):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                return        
                                                                                                    
                            if(TEST_CREATION_API.compare_pictures("black_screen_" + video_height + "_ref", "screen")):
                                TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                time.sleep(2)
                                TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                time.sleep(1)
                                TEST_CREATION_API.send_ir_rc_command(NOS_API.SD_CHANNEL)
                                time.sleep(1)
                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                time.sleep(1)

                                if not(NOS_API.grab_picture("screen")):
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False


                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    
                                    return 
                                        
                                if(TEST_CREATION_API.compare_pictures("black_screen_" + video_height + "_ref", "screen")):
                                    time.sleep(5)
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(10)
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(5)
                                    TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                    time.sleep(1)
                                    TEST_CREATION_API.send_ir_rc_command(NOS_API.SD_CHANNEL)
                                    time.sleep(1)
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
       
                            TEST_CREATION_API.send_ir_rc_command(NOS_API.SD_CHANNEL)
                            time.sleep(2)

                        ## check is signal present after STB is powered on
                        if (NOS_API.is_signal_present_on_video_source()): 
                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                            time.sleep(1)                           
                            TEST_CREATION_API.send_ir_rc_command("[MENU]")
                            TEST_CREATION_API.send_ir_rc_command("[MENU]")
                            time.sleep(3)

                            if not(NOS_API.grab_picture("menu")):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                return        

                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "576" and video_height != "720" and video_height != "1080"):
                                time.sleep(10)
                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                if (video_height != "576" and video_height != "720" and video_height != "1080"):
                                    TEST_CREATION_API.write_log_to_file("Detected height of HDMI Signal was " + video_height + ". Expected height was 576 or 720 or 1080.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False


                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    
                                    return
                            if(TEST_CREATION_API.compare_pictures("black_screen_" + video_height + "_ref", "menu")):
                                TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                time.sleep(2)
                                TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                time.sleep(1)
                                TEST_CREATION_API.send_ir_rc_command(NOS_API.SD_CHANNEL)
                                time.sleep(1)
                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                time.sleep(1)
                                
                                if not(NOS_API.grab_picture("menu")):
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False


                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    
                                    return 
                                    
                                if(TEST_CREATION_API.compare_pictures("black_screen_" + video_height + "_ref", "menu")):
                                    time.sleep(5)
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(10)
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(5)
                                    TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                    time.sleep(1)
                                    TEST_CREATION_API.send_ir_rc_command(NOS_API.SD_CHANNEL)
                                    time.sleep(1)
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
        
                                TEST_CREATION_API.send_ir_rc_command(NOS_API.SD_CHANNEL)
                                time.sleep(2)
                        
                                TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                if not(NOS_API.grab_picture("menu")):
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False


                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    return        

                            result = NOS_API.wait_for_multiple_pictures(
                                    ["blue_ref1", "blue_ref2", "blue_ref3", "Upgrade_Error_ref", "update_ref_NOS", "update_screen_576_ref", "update_screen_720_ref", "update_screen_1080_ref", "update_ref"],
                                    5,
                                    ["[OLD_ZON]", "[OLD_ZON]", "[OLD_ZON]", "[Upgrade_Error_new]", "[FULL_SCREEN]", "[UPDATE_SCREEN_576]", "[UPDATE_SCREEN_720]", "[UPDATE_SCREEN_1080]", "[FULL_SCREEN]"],
                                    [80, 80, 80, 80, 80, 80, 80, 80, 80])
                            if (result == -2):
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                
                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                
                                return        
                            elif (result >= 0 and result < 4):
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                NOS_API.set_error_message("Não Actualiza") 
                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False


                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                return  
                            elif (result >= 4 and result < 8):
                                time.sleep(5)
                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                if (NOS_API.wait_for_signal_sw_upgrade_thomson(600)):
                                    time.sleep(10)
                                    if (NOS_API.wait_for_signal_sw_upgrade_thomson(600)):
                                        time.sleep(60)   
                                if not(NOS_API.is_signal_present_on_video_source()):
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(5)        
                                result = NOS_API.wait_for_multiple_pictures(
                                        ["blue_ref1", "blue_ref2", "blue_ref3", "Upgrade_Error_ref", "update_ref_NOS", "update_screen_576_ref", "update_screen_720_ref", "update_screen_1080_ref", "update_ref"],
                                        5,
                                        ["[OLD_ZON]", "[OLD_ZON]", "[OLD_ZON]", "[Upgrade_Error_new]", "[FULL_SCREEN]", "[UPDATE_SCREEN_576]", "[UPDATE_SCREEN_720]", "[UPDATE_SCREEN_1080]", "[FULL_SCREEN]"],
                                        [80, 80, 80, 80, 80, 80, 80, 80, 80])
                                if (result == -2):
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                    
                                    return        
                                elif (result >= 0 and result < 8):
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False


                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    return  
                                elif (result == 8):
                                    result_nagra = 0
                                    while(result_nagra == 0):
                                        time.sleep(2)
                                        result_nagra = NOS_API.wait_for_multiple_pictures(["update_ref"], 5, ["[FULL_SCREEN]"], [80])
                                        NOS_API.test_cases_results_info.DidUpgrade = 1
                                    time.sleep(1)
                                    result_error = NOS_API.wait_for_multiple_pictures(["Upgrade_Error_ref"], 5, ["[Upgrade_Error_new]"], [80])
                                    if(result_error == 0):
                                        NOS_API.test_cases_results_info.isTestOK = False  
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_message)
                                        NOS_API.set_error_message("Não Actualiza")
                                        error_codes = NOS_API.test_cases_results_info.sw_upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.sw_upgrade_nok_error_message
                                        test_result = "FAIL"

                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                        return
                            elif (result == 8):
                                result_nagra = 0
                                while(result_nagra == 0):
                                    time.sleep(2)
                                    result_nagra = NOS_API.wait_for_multiple_pictures(["update_ref"], 5, ["[FULL_SCREEN]"], [80])
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                time.sleep(1)
                                result_error = NOS_API.wait_for_multiple_pictures(["Upgrade_Error_ref"], 5, ["[Upgrade_Error_new]"], [80])
                                if(result_error == 0):
                                    NOS_API.test_cases_results_info.isTestOK = False  
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.sw_upgrade_nok_error_message)
                                    NOS_API.set_error_message("Não Actualiza")
                                    error_codes = NOS_API.test_cases_results_info.sw_upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.sw_upgrade_nok_error_message
                                    test_result = "FAIL"

                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                    return

                            if(video_height == "576" or video_height == "1080"):
                                NOS_API.SET_720 = True
                            else:
                                NOS_API.SET_720 = False

                            if not(video_height == "576"):
                                threshold = TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD
                            else:
                                threshold = NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD
                            
                            ## Depends on resolution set appropriate picture and macro
                            if (TEST_CREATION_API.compare_pictures("menu_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menublack_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menu_" + video_height + "_eng_ref", "menu", "[MENU_" + video_height + "]", threshold) ):
                                #############################################
                                if(NOS_API.SET_720):
                                    ## Set resolution to 720p and navigate to the signal level settings
                                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                    TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                    time.sleep(3)
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                    if(video_height != "720"):
                                        time.sleep(1)
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                        TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                        time.sleep(3)
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                        if (video_height != "720"):
                                            NOS_API.set_error_message("Resolução")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                            test_result = "FAIL"
                                        
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                            
                                            return 
                                
                                NOS_API.test_cases_results_info.channel_boot_up_state = True
                            else:
                                if(video_height == "720"):
                                    result = NOS_API.wait_for_multiple_pictures(["installation_boot_up_ref", "installation_boot_up_ref_NOS", "installation_boot_up_eng_ref"], 8, ["[Inst_Mode]", "[Inst_Mode]", "[Inst_Mode_Eng]"], [80, 80, 80])
                                    if not(result == 0 or result == 1 or result == 2):
                                        TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                        TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                        time.sleep(2)

                                        if not(NOS_API.grab_picture("menu")):
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
        
        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                            return 

                                        ## Depends on resolution set appropriate picture and macro
                                        if (TEST_CREATION_API.compare_pictures("menu_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menublack_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menu_" + video_height + "_eng_ref", "menu", "[MENU_" + video_height + "]", threshold)):
                                            #############################################
                                            if(NOS_API.SET_720):
                                                ## Set resolution to 720p and navigate to the signal level settings
                                                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                                TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                                time.sleep(3)
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                if(video_height != "720"):
                                                    time.sleep(1)
                                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                                    TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                                    time.sleep(3)
                                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                    if (video_height != "720"):
                                                        NOS_API.set_error_message("Resolução")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                                        error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                                        error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                                        test_result = "FAIL"
                                                    
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                        
                                                        return 
                                            
                                            NOS_API.test_cases_results_info.channel_boot_up_state = True
                                        else:
                                            if not(NOS_API.grab_picture("menu_1")):
                                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                NOS_API.set_error_message("Video HDMI")
                                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
            
            
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                return
                                            
                                            if(TEST_CREATION_API.compare_pictures("menu", "menu_1")):
                                                if (Repeat_Block == 3):
                                                    TEST_CREATION_API.write_log_to_file("STB Blocks")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.block_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.block_error_message)
                                                    NOS_API.set_error_message("STB bloqueou")
                                                    error_codes = NOS_API.test_cases_results_info.block_error_code
                                                    error_messages = NOS_API.test_cases_results_info.block_error_message
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    test_result = "FAIL"
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                    
                                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                    return
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB Blocks. Try Again")
                                                    Repeat_Block = Repeat_Block + 1
                                                    continue
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                                NOS_API.set_error_message("Video HDMI")
                                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
            
            
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                return                
                                    else:
                                        NOS_API.test_cases_results_info.channel_boot_up_state = False 
                                else:
                                    TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                    TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                    time.sleep(2)

                                    if not(NOS_API.grab_picture("menu")):
                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
    
    
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                        return 

                                    ## Depends on resolution set appropriate picture and macro
                                    if (TEST_CREATION_API.compare_pictures("menu_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menublack_" + video_height + "_ref", "menu", "[MENU_" + video_height + "]", threshold) or TEST_CREATION_API.compare_pictures("menu_" + video_height + "_eng_ref", "menu", "[MENU_" + video_height + "]", threshold)):
                                        #############################################
                                        if(NOS_API.SET_720):
                                            ## Set resolution to 720p and navigate to the signal level settings
                                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                            TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                            time.sleep(3)
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                            if(video_height != "720"):
                                                time.sleep(1)
                                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                                                TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                                time.sleep(3)
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                if (video_height != "720"):
                                                    NOS_API.set_error_message("Resolução")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                                    error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                                    error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                                    test_result = "FAIL"
                                                
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                    
                                                    return 
                                        
                                        NOS_API.test_cases_results_info.channel_boot_up_state = True
                                    else:
                                        if not(NOS_API.grab_picture("menu_1")):
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
        
        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                            return
                                        
                                        if(TEST_CREATION_API.compare_pictures("menu", "menu_1")):
                                            if (Repeat_Block == 3):
                                                TEST_CREATION_API.write_log_to_file("STB Blocks")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.block_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.block_error_message)
                                                NOS_API.set_error_message("STB bloqueou")
                                                error_codes = NOS_API.test_cases_results_info.block_error_code
                                                error_messages = NOS_API.test_cases_results_info.block_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                test_result = "FAIL"
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                
                                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                            
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                return
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB Blocks. Try Again")
                                                Repeat_Block = Repeat_Block + 1
                                                continue
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
        
        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                            return
                                            
                            test_result = "PASS"
                            Repeat_Block = 4
                        else:
                            NOS_API.grabber_stop_video_source()
                            
                            ## Initialize input interfaces of DUT RT-AV101 device 
                            NOS_API.reset_dut()
                            #time.sleep(2)
                            
                            ## Start grabber device with video on SCART video source
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                            #time.sleep(WAIT_TO_SWITCH_SCART)

                            ## Check is signal present on SCART
                            if (NOS_API.is_signal_present_on_video_source()):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                Repeat_Block = 4 
                            else:
                                if (NoBoot == 1):
                                    TEST_CREATION_API.write_log_to_file("No boot")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                    NOS_API.set_error_message("Não arranca")
                                    error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                    error_messages = NOS_API.test_cases_results_info.no_boot_error_message    
                                    Repeat_Block = 4
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB didn't boot. Try Again")
                                    NoBoot = NoBoot + 1
                                    continue
                System_Failure = 2
            else:
                TEST_CREATION_API.write_log_to_file("Wrong MAC")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.wrong_mac_error_code \
                                                               + "; Error message: " + NOS_API.test_cases_results_info.wrong_mac_error_message \
                                                               + "; MAC: " + NOS_API.test_cases_results_info.mac_using_barcode)
                NOS_API.set_error_message("MAC") 
                error_codes = NOS_API.test_cases_results_info.wrong_mac_error_code
                error_messages = NOS_API.test_cases_results_info.wrong_mac_error_message
                System_Failure = 2
       
        except Exception as error:
            if(System_Failure == 0):
                System_Failure = System_Failure + 1 
                NOS_API.Inspection = True
                if(System_Failure == 1):
                    try:
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                    try:
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_off()): 
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)

                        return
                    time.sleep(10)
                    ## Power on STB with energenie
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        test_result = "FAIL"
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                        
                        return
                    time.sleep(10)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    NOS_API.set_error_message("Inspection")
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                    report_file = ""
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    test_result = "FAIL"
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                    
                    return
                
                NOS_API.Inspection = False
            else:
                test_result = "FAIL"
                TEST_CREATION_API.write_log_to_file(error)
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                error_messages = NOS_API.test_cases_results_info.grabber_error_message
                NOS_API.set_error_message("Inspection")
                System_Failure = 2
             
    NOS_API.add_test_case_result_to_file_report(
                    test_result,
                    "- - - - - - - - - - - - - - - - - - - -",
                    "- - - - - - - - - - - - - - - - - - - -",
                    error_codes,
                    error_messages)
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_file = ""
    if (test_result != "PASS"):
        report_file = NOS_API.create_test_case_log_file(
                        NOS_API.test_cases_results_info.s_n_using_barcode,
                        NOS_API.test_cases_results_info.nos_sap_number,
                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                        NOS_API.test_cases_results_info.mac_using_barcode,
                        end_time)
        NOS_API.upload_file_report(report_file)
        NOS_API.test_cases_results_info.isTestOK = False
        
        NOS_API.send_report_over_mqtt_test_plan(
                test_result,
                end_time,
                error_codes,
                report_file)
    
    
    ## Update test result
    TEST_CREATION_API.update_test_result(test_result)

    ## Return DUT to initial state and de-initialize grabber device
    NOS_API.deinitialize()
    