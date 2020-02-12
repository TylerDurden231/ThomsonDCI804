# -*- coding: utf-8 -*-
# Test name = Interfaces Test
# Test description = Test all interfaces of STB

from datetime import datetime
from time import gmtime, strftime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

## Max record video time in miliseconds
MAX_RECORD_VIDEO_TIME = 2000

## Max record audio time in miliseconds
MAX_RECORD_AUDIO_TIME = 2000

## Recording time in seconds
REC_TIME = 30

THRESHOLD = 70

REC_POWER_THRESHOLD = 52

## Wait time to display first image after factory reset
TIME_COUNTER = 90

## Constant multiplier used for conversion from seconds to milliseconds
MS_MULTIPLIER = 1000

def runTest():

    System_Failure = 0
    
    NOS_API.test_cases_results_info.isTestOK = True
    
     ## Skip this test case if some previous test failed
    if not(NOS_API.test_cases_results_info.isTestOK):
        TEST_CREATION_API.update_test_result(TEST_CREATION_API.TestCaseResult.FAIL)
        return
    
    while (System_Failure < 2):
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"
            test_result_output = False
            test_result_quality = False
            pqm_analyse_check = True
            error_codes = ""
            error_messages = ""
            boot_counter = "-"
            
            HDMI_720p_Result = False

            HDD_DETECTION_Result = False
            
            ERASE_CONTENT_Result = False
            Lock = 0
            erase_counter_folder_Menu = 0
            TimeOut_Folder_Menu = 400
            erase_counter_folder_Content = 0
            TimeOut_Folder_Content = 400
            erase_counter_folder = 0
            TimeOut_Folder = 180
            erase_counter = 0
            space_counter = 0
            TimeOut = 900
            TimeOutSche = 300
            Fixed = False
            delta_time = 0
            delta_time_1 = 0
            delta_time_2 = 0
            delta_time_3 = 0     
            
            REC_START_Result = False
            
            SCART_Result = False
            test_result_SCART_video = False
            
            ANALOG_AUDIO_Result = False
            
            SPDIF_Result = False
            
            VIDEO_RECORD_Result = False
            
            AUDIO_RECORD_Result = False
            
            test_result_sd = False
            
            test_result_telnet = False
            
            test_result_boot = False
            
            test_result_res = False
            test_result_hd = False
            pqm_analyse_check = True
            hd_counter = 0
            sd_ch_counter = 0
            
            error_command_telnet = False
            stb_state = False
            
            cmd0 = 'Show cable modem ' + NOS_API.test_cases_results_info.mac_using_barcode       
            sid = NOS_API.get_session_id()
            
            ## Initialize grabber device
            NOS_API.initialize_grabber()

            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
            
            if(System_Failure == 1):
                if not(NOS_API.is_signal_present_on_video_source()):
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
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                        
                
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    return
            
                TEST_CREATION_API.send_ir_rc_command("[Exit_HDD_Folder_Loop]")
                TEST_CREATION_API.send_ir_rc_command("[LEFT]")
                TEST_CREATION_API.send_ir_rc_command("[LEFT]")     
                TEST_CREATION_API.send_ir_rc_command("[QUICK_EXIT]")                                 
                time.sleep(2)
                
                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                if(video_height != "720"):
                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                    if(video_height != "720"):
                        time.sleep(1)
                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_T804]")
                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "720"):
                            NOS_API.set_error_message("Resolução")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                       + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
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
                            return
            
                time.sleep(2)
                
            ## Set volume to max
            TEST_CREATION_API.send_ir_rc_command("[VOL_MIN]")
            
            ## Set volume to half, because if vol is max, signal goes in saturation
            TEST_CREATION_API.send_ir_rc_command("[VOL_PLUS_HALF]")
            
            ## Zap to service
            TEST_CREATION_API.send_ir_rc_command("[CH_1]")

            time.sleep(NOS_API.MAX_ZAP_TIME)
            
            if not (NOS_API.is_signal_present_on_video_source()):
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
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                    
            
                ## Update test result
                TEST_CREATION_API.update_test_result(test_result)
            
                ## Return DUT to initial state and de-initialize grabber device
                NOS_API.deinitialize()
                return
                
            ## Record video with duration of recording (10 seconds)
            NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)

            ## Instance of PQMAnalyse type
            pqm_analyse = TEST_CREATION_API.PQMAnalyse()

            ## Set what algorithms should be checked while analyzing given video file with PQM.
            # Attributes are set to false by default.
            pqm_analyse.black_screen_activ = True
            pqm_analyse.blocking_activ = True
            pqm_analyse.freezing_activ = True

            # Name of the video file that will be analysed by PQM.
            pqm_analyse.file_name = "video"

            ## Analyse recorded video
            analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)

            if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                pqm_analyse_check = False
                NOS_API.set_error_message("Video HDMI")
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code \
                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code)                    
                error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code
                error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message

            if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                pqm_analyse_check = False
                NOS_API.set_error_message("Video HDMI")
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code \
                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message)
                        
                if (error_codes == ""):
                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                else:
                    error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                        
                if (error_messages == ""):
                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                else:
                    error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message        
                        
            if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                pqm_analyse_check = False
                NOS_API.set_error_message("Video HDMI")
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                if (error_codes == ""):
                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                else:
                    error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                        
                if (error_messages == ""):
                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                else:
                    error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
            
            if not(pqm_analyse_check): 
                NOS_API.set_error_message("Video HDMI")
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
                return
            
            if not(analysed_video): 
                TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                error_messages = NOS_API.test_cases_results_info.grabber_error_message
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
                return 
            else:           
                test_result_output = True
     
        ######################################################## HDMI 720p Video Quality #######################################################################
       
            if(test_result_output):
                
                video_result = 0

                try:
                    
                    ## Perform grab picture
                    try:
                        TEST_CREATION_API.grab_picture("HDMI_video")
                    except: 
                        time.sleep(5)
                        try:
                            TEST_CREATION_API.grab_picture("HDMI_video")
                        except:
                            
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

                    ## Compare grabbed and expected image and get result of comparison
                    video_result = NOS_API.compare_pictures("HDMI_video_ref", "HDMI_video", "[HALF_SCREEN]")

                except Exception as error:
                    ## Set test result to INCONCLUSIVE
                    TEST_CREATION_API.write_log_to_file(str(error))
                    test_result = "FAIL"
                    TEST_CREATION_API.write_log_to_file("There is no signal on HDMI 720p interface.")
                    NOS_API.set_error_message("Video HDMI")
        
                ## Check video analysis results and update comments
                if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    ## Set test result to PASS
                    test_result_quality = True
                else:
                    TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on HDMI 720p.")
                    NOS_API.set_error_message("Video HDMI")
                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                    + "; V: " + str(video_result))
                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message

                ################################################################ HDMI 720p Video Audio ########################################################################
           
                if(test_result_quality):            
            
                ## Good Audio Comparison start ######
                
                    ### Record audio from digital output (HDMI)
                    #TEST_CREATION_API.record_audio("HDMI_audio", MAX_RECORD_AUDIO_TIME)
                    #
                    ### Compare recorded and expected audio and get result of comparison
                    #audio_result_1 = NOS_API.compare_audio("HDMI_audio_ref1", "HDMI_audio")
                    #audio_result_2 = NOS_API.compare_audio("HDMI_audio_ref2", "HDMI_audio")
                    #
                    #if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result_2 < TEST_CREATION_API.AUDIO_THRESHOLD):
                    #
                    #    TEST_CREATION_API.send_ir_rc_command("[CH+]")
                    #    TEST_CREATION_API.send_ir_rc_command("[CH-]")
                    #    time.sleep(NOS_API.MAX_ZAP_TIME)
                    #    
                    #    TEST_CREATION_API.record_audio("HDMI_audio", MAX_RECORD_AUDIO_TIME)
                    #
                    #    ## Compare recorded and expected audio and get result of comparison
                    #    audio_result_1 = NOS_API.compare_audio("HDMI_audio_ref1", "HDMI_audio")
                    #    audio_result_2 = NOS_API.compare_audio("HDMI_audio_ref2", "HDMI_audio")           
                    #
                    #
                    #if (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                    
                ## Good Audio Comparison end ######
                
                ## No Audio Comparison start ######
                
                    ## Record audio from digital output (HDMI)
                    TEST_CREATION_API.record_audio("HDMI_audio", MAX_RECORD_AUDIO_TIME)
            
                    ## Compare recorded and expected audio and get result of comparison
                    audio_result_1 = NOS_API.compare_audio("HDMI_audio_ref1", "No_Both_ref")
                    #audio_result_2 = NOS_API.compare_audio("HDMI_audio_ref2", "HDMI_audio")
                    
                    ## Check is audio present on channel
                    if (TEST_CREATION_API.is_audio_present("HDMI_audio")):
                    
                        if (audio_result_1 > TEST_CREATION_API.AUDIO_THRESHOLD):
                        
                            TEST_CREATION_API.send_ir_rc_command("[CH+]")
                            TEST_CREATION_API.send_ir_rc_command("[CH-]")
                            time.sleep(NOS_API.MAX_ZAP_TIME)
                            
                            TEST_CREATION_API.record_audio("HDMI_audio", MAX_RECORD_AUDIO_TIME)
                
                            ## Compare recorded and expected audio and get result of comparison
                            audio_result_1 = NOS_API.compare_audio("HDMI_audio_ref1", "HDMI_audio")
                            audio_result_2 = NOS_API.compare_audio("HDMI_audio_ref2", "HDMI_audio")           

                        if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD):         
                            
                            HDMI_720p_Result = True
                        else:
                            TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                            NOS_API.set_error_message("Audio HDMI")
                            NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                    + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                    + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                    + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                          
                    else:
                        TEST_CREATION_API.write_log_to_file("Audio is not present on hdmi 720p interface.")
                        NOS_API.set_error_message("Audio HDMI")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message \
                                                            + "; Audio is not present on hdmi_576p interface")
                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code
                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message
                   
                ################################################################ HDD DEtection ################################################################################
                
                if(HDMI_720p_Result):
                
                    TEST_CREATION_API.send_ir_rc_command("[HDD_MENU_T804]")
                    time.sleep(1.5)

                    ## Perform grab picture
                    TEST_CREATION_API.grab_picture("hdd_menu")

                    video_result = NOS_API.compare_pictures("hdd_menu_ref", "hdd_menu", "[HDD_MENU]")
                    
                    ## Check is HDD menu is opened
                    if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):

                        video_result = NOS_API.compare_pictures("hdd_menu_ref1", "hdd_menu", "[HDD_DETECTION]")
                        
                        try:
                            hdd_space = int(TEST_CREATION_API.OCR_recognize_text("hdd_menu", "[HDD_SPACE]", "", "hdd_space"))
                        except Exception as error:
                            TEST_CREATION_API.write_log_to_file(str(error))
                            hdd_space = 0
                        
                        ## Check if hdd is detected
                        if (video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            if (hdd_space > 50):
                                ## Set test result to PASS
                                HDD_DETECTION_Result = True
                            else:
                                TEST_CREATION_API.write_log_to_file("HDD with too much content.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.too_much_content_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.too_much_content_error_message)
                                NOS_API.set_error_message("HDD")
                                error_codes = NOS_API.test_cases_results_info.too_much_content_error_code
                                error_messages = NOS_API.test_cases_results_info.too_much_content_error_message
                                
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
                                return
                            NOS_API.test_cases_results_info.hdd_detection = True
                        else:
                            TEST_CREATION_API.write_log_to_file("Hdd is not detected")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdd_not_detected_error_code \
                                                                   + "; Error message: " + NOS_API.test_cases_results_info.hdd_not_detected_error_message \
                                                                   + "; V: " + str(video_result))
                            error_codes = NOS_API.test_cases_results_info.hdd_not_detected_error_code
                            error_messages = NOS_API.test_cases_results_info.hdd_not_detected_error_message
                            NOS_API.set_error_message("HDD")
                    else:
                        TEST_CREATION_API.write_log_to_file("Hdd menu is not opened.")
                        NOS_API.set_error_message("HDD")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                        error_messages = NOS_API.test_cases_results_info.navigation_error_message
                       
                    ################################################################ Erase content from HDD #######################################################################
                        
                    if(HDD_DETECTION_Result):
                    
                        if not(NOS_API.grab_picture("empty_recorded_list")):            
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
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
                            return
                        ## Empty all recorded content from HDD
                        if not(TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[HDD_MENU_LEFT]")):                                       
                            ## Delete next recorded content
                            TEST_CREATION_API.send_ir_rc_command("[Recorded_Folder]")
                            
                            if not(NOS_API.grab_picture("empty_recorded_folder")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
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
                                return
                            if not(TEST_CREATION_API.compare_pictures("empty_recorded_folder_ref", "empty_recorded_folder", "[Folder_Home]")):
                                TEST_CREATION_API.send_ir_rc_command("[Folder_Home]")
                                if not(NOS_API.grab_picture("empty_recorded_folder")):                
                                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    
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
                                    return
                            start_time_2 = time.localtime()
                            while not((TEST_CREATION_API.compare_pictures("empty_recorded_folder_ref", "empty_recorded_folder", "[Folder_Check]")) or (delta_time_2 >= TimeOut_Folder_Menu)):
                                if (erase_counter_folder_Menu == 2):
                                    erase_counter_folder_Menu = 0
                                    if not(TEST_CREATION_API.compare_pictures("empty_recorded_folder_ref", "empty_recorded_folder", "[Check_not_folder_loop_1]") and TEST_CREATION_API.compare_pictures("empty_recorded_folder_ref", "empty_recorded_folder", "[Check_not_folder_loop_2]")):
                                        TEST_CREATION_API.send_ir_rc_command("[Exit_HDD_Folder_Loop]")                     
                                        Fixed = True
                                
                                ## Perform grab picture
                                TEST_CREATION_API.send_ir_rc_command("[Erase_Folder]")
                                
                                if not(NOS_API.grab_picture("empty_recorded_folder_1")):
                                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    
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
                                    return
                                
                                if (TEST_CREATION_API.compare_pictures("empty_recorded_folder_1", "empty_recorded_folder", "[Folder_Block]")):
                                    if (TEST_CREATION_API.compare_pictures("empty_recorded_folder_lock_ref", "empty_recorded_folder_1", "[Lock]")):
                                        TEST_CREATION_API.send_ir_rc_command("[Unlock]")
                                        TEST_CREATION_API.send_ir_rc_command("[Erase_Folder]")
                                        Lock = 1
                                    if not(NOS_API.grab_picture("empty_recorded_folder_Lock")):
                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        
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
                                        return
                                    if (TEST_CREATION_API.compare_pictures("empty_recorded_folder_1", "empty_recorded_folder_Lock", "[Folder_Block]")):
                                        TEST_CREATION_API.send_ir_rc_command("[DVR]")
                                        time.sleep(5)
                                        TEST_CREATION_API.send_ir_rc_command("[Check_Serie]")
                                        if not(NOS_API.grab_picture("empty_recorded_list_block")):
                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            
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
                                            return
                                        while (TEST_CREATION_API.compare_pictures("Erase_Serie_ref", "empty_recorded_list_block", "[Erase_Serie_1]")):
                                            TEST_CREATION_API.send_ir_rc_command("[Double_OK]")
                                            time.sleep(3)
                                            TEST_CREATION_API.send_ir_rc_command("[Check_Serie]")
                                            if not(NOS_API.grab_picture("empty_recorded_list_block")):            
                                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                NOS_API.set_error_message("Video HDMI")
                                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                
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
                                                return
                                        time.sleep(8)
                                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                                        start_time_1 = time.localtime()
                                        while not((TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list_block", "[RECORDED_CONTENT_AREA]")) or (delta_time_1 >= TimeOut_Folder_Content)):
                                            if (erase_counter_folder_Content == 2):
                                                erase_counter_folder_Content = 0
                                                if not(TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list_block", "[Check_not_loop_1]") and TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list_block", "[Check_not_loop_2]")):
                                                    TEST_CREATION_API.send_ir_rc_command("[Exit_HDD_Loop]")
                                                    time.sleep(1)
                                                    TEST_CREATION_API.send_ir_rc_command("[Mega_UP]")
                                                    TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                                                    time.sleep(1)
                                                    TEST_CREATION_API.send_ir_rc_command("[DVR_1]")
                                                    time.sleep(1)
                                                    TEST_CREATION_API.send_ir_rc_command("[Erase_Folder_block]")
                                                    Fixed = True
                                            
                                            ## Delete next recorded content
                                            if (Lock == 1):
                                                TEST_CREATION_API.send_ir_rc_command("[Erase_Content_block]")
                                            else:
                                                TEST_CREATION_API.send_ir_rc_command("[Erase_Content_block_NL]")
                                            
                                            ## Perform grab picture
                                            if not(NOS_API.grab_picture("empty_recorded_list_block")):
                                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                NOS_API.set_error_message("Video HDMI")
                                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                
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
                                                return
                                
                                            erase_counter_folder_Content = erase_counter_folder_Content + 1       
                                            delta_time_1 = (time.mktime(time.localtime()) - time.mktime(start_time_1))
                                        
                                        if (delta_time_1 >= TimeOut_Folder_Content):
                                            TEST_CREATION_API.write_log_to_file("Doesn't Erase HDD")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdd_erase_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdd_erase_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdd_erase_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdd_erase_error_message
                                            NOS_API.set_error_message("HDD")
                                            
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
                                            return
                                    
                                    TEST_CREATION_API.send_ir_rc_command("[Folder_Home]")
                                
                                if not(NOS_API.grab_picture("empty_recorded_folder")):
                                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    
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
                                    return
                             
                                erase_counter_folder_Menu = erase_counter_folder_Menu + 1       
                                delta_time_2 = (time.mktime(time.localtime()) - time.mktime(start_time_2))
                            
                            if (delta_time_2 >= TimeOut_Folder_Menu):
                                TEST_CREATION_API.write_log_to_file("Doesn't Erase HDD")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdd_erase_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdd_erase_error_message)
                                error_codes = NOS_API.test_cases_results_info.hdd_erase_error_code
                                error_messages = NOS_API.test_cases_results_info.hdd_erase_error_message
                                NOS_API.set_error_message("HDD")
                                
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
                                return
                             
                            TEST_CREATION_API.send_ir_rc_command("[HDD_MENU_1]")
                            if not(NOS_API.grab_picture("empty_recorded_list")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
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
                                return
                            
                        start_time_3 = time.localtime()
                        while not((TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[HDD_MENU_LEFT]")) or (delta_time_3 >= TimeOut_Folder)):
                            if (erase_counter_folder == 2):
                                erase_counter_folder = 0
                                if not(TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[Check_not_loop_1]") and TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[Check_not_loop_2]")):
                                    TEST_CREATION_API.send_ir_rc_command("[Exit_HDD_Loop]")
                                    TEST_CREATION_API.send_ir_rc_command("[Mega_UP]")
                                    Fixed = True
                                    
                            TEST_CREATION_API.send_ir_rc_command("[Erase_Serie_Folder]")         
                            if not(NOS_API.grab_picture("empty_recorded_list")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
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
                                return
                        
                            erase_counter_folder = erase_counter_folder + 1       
                            delta_time_3 = (time.mktime(time.localtime()) - time.mktime(start_time_3))
                        
                        if (delta_time_3 >= TimeOut_Folder):
                            TEST_CREATION_API.write_log_to_file("Doesn't Erase HDD")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdd_erase_error_code \
                                                                   + "; Error message: " + NOS_API.test_cases_results_info.hdd_erase_error_message)
                            error_codes = NOS_API.test_cases_results_info.hdd_erase_error_code
                            error_messages = NOS_API.test_cases_results_info.hdd_erase_error_message
                            NOS_API.set_error_message("HDD")
                            
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
                            return
                        
                        start_time = time.localtime()
                        ## Empty all recorded content from HDD
                        while not((TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[RECORDED_CONTENT_AREA]")) or (delta_time >= TimeOut)):
                            if (TEST_CREATION_API.compare_pictures("Lock_Content_ref", "empty_recorded_list", "[Lock_Content]") or TEST_CREATION_API.compare_pictures("Lock_Content_ws_ref", "empty_recorded_list", "[Lock_Content]")):
                                TEST_CREATION_API.send_ir_rc_command("[DELETE_A_CONTENT_BLOCK]")
                                TEST_CREATION_API.send_ir_rc_command("[UP]")
                                if not(NOS_API.grab_picture("empty_recorded_list")):
                                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    
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
                                    return
                                continue
                            
                            if (erase_counter == 3):
                                erase_counter = 0
                                
                                if not(TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[Check_not_loop_1]") and TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[Check_not_loop_2]") and TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[Check_not_loop_3]") == False and TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list", "[Check_not_loop_4]") == False):
                                                        
                                    TEST_CREATION_API.send_ir_rc_command("[Exit_HDD_Loop]")
                                    TEST_CREATION_API.send_ir_rc_command("[Mega_UP]")
                                    Fixed = True
                            ## Delete next recorded content
                            TEST_CREATION_API.send_ir_rc_command("[DELETE_A_CONTENT]")
                            TEST_CREATION_API.send_ir_rc_command("[UP]")
                            ## Perform grab picture
                            if not(NOS_API.grab_picture("empty_recorded_list")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
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
                                return
                            
                            erase_counter = erase_counter + 1       
                            delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                            
                        if (delta_time < TimeOut):
                            TEST_CREATION_API.send_ir_rc_command("[Down]")
                            if not(NOS_API.grab_picture("empty_recorded_list_sche")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
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
                                return
                            start_time = time.localtime()
                            erase_counter = 0
                            delta_time = 0
                            
                            while not(TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list_sche", "[RECORDED_CONTENT_AREA]") or delta_time >= TimeOutSche):
                                
                                if (erase_counter == 3):
                                    erase_counter = 0
                                    
                                    if not (TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list_sche", "[Check_not_loop_1]") and TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "empty_recorded_list_sche", "[Check_not_loop_2]")):
                                        TEST_CREATION_API.send_ir_rc_command("[Exit_HDD_Loop]")
                                        TEST_CREATION_API.send_ir_rc_command("[Mega_UP]")
                                        TEST_CREATION_API.send_ir_rc_command("[Down]")
                                        
                                        Fixed = True
                                ## Delete next recorded content
                                TEST_CREATION_API.send_ir_rc_command("[DELETE_A_CONTENT_SCHED]")
                        
                                ## Perform grab picture
                                if not(NOS_API.grab_picture("empty_recorded_list_sche")):
                                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    
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
                                    return
                                
                                erase_counter = erase_counter + 1       
                                delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                                
                        if (delta_time >= TimeOut):
                            TEST_CREATION_API.write_log_to_file("Doesn't Erase HDD")
                            NOS_API.set_error_message("HDD")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdd_erase_error_code \
                                                                   + "; Error message: " + NOS_API.test_cases_results_info.hdd_erase_error_message)
                            error_codes = NOS_API.test_cases_results_info.hdd_erase_error_code
                            error_messages = NOS_API.test_cases_results_info.hdd_erase_error_message
                            
                        while ((space_counter < 2) and (delta_time < TimeOut)):
                            ## Perform grab picture
                            if not(NOS_API.grab_picture("hdd_space")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
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
                                return
                            
                            try:
                                hdd_space = int(TEST_CREATION_API.OCR_recognize_text("hdd_space", "[HDD_SPACE]", "", "hdd_space"))
                            except Exception as error:
                                TEST_CREATION_API.write_log_to_file(str(error))
                                hdd_space = 0

                            if (hdd_space > 90):
                                ERASE_CONTENT_Result = True
                                break
                            else:
                                if (space_counter == 1):
                                    TEST_CREATION_API.write_log_to_file("HDD size NOK")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdd_size_nok_error_code \
                                                                           + "; Error message: " + NOS_API.test_cases_results_info.hdd_size_nok_error_message  \
                                                                           + "; OCR: " + str(hdd_space))
                                    error_codes = NOS_API.test_cases_results_info.hdd_size_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdd_size_nok_error_message
                                    NOS_API.set_error_message("HDD")
                                    break
                                else:
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(10)
                                    TEST_CREATION_API.send_ir_rc_command("[DVR_1]") 
                                    time.sleep(4)
                                    
                                    if not(NOS_API.grab_picture("hdd_space")):
                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        
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
                                        return
                                    video_result = NOS_API.compare_pictures("hdd_menu_ref", "hdd_space", "[HDD_MENU]")
                                    ## Check is HDD menu is opened
                                    if not(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                        time.sleep(3)
                                        TEST_CREATION_API.send_ir_rc_command("[DVR_1]")
                                        time.sleep(4)
                            space_counter = space_counter + 1

                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                        if (Fixed):
                            time.sleep(2)
                            TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                        
                        ################################################################ Recording Started ############################################################################
                        
                        if(ERASE_CONTENT_Result):           
                       
                            ## Zap to service
                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                            #TEST_CREATION_API.send_ir_rc_command(NOS_API.CHANNEL)
                            time.sleep(1)
                            TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                            ## Start recording
                            TEST_CREATION_API.send_ir_rc_command("[REC]")

                            ## Perform grab picture
                            TEST_CREATION_API.grab_picture("rec")

                            video_result_1 = NOS_API.compare_pictures("rec_ref", "rec", "[REC_ICON]")
                            video_result_2 = NOS_API.compare_pictures("rec1_ref", "rec", "[REC_ICON]")

                            ## Check if recording is started
                            if (video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):

                                ## Use this variable in script Video Recording Content to check is recording started or not
                                NOS_API.test_cases_results_info.recording_started = True
                                REC_START_Result = True

                            else:

                                ## Use this variable in script Video Recording Content to check is recording started or not
                                NOS_API.test_cases_results_info.recording_started = False

                                TEST_CREATION_API.write_log_to_file("Recording is not started")

                                    
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recording_error_code \
                                                                               + "; Error message: " + NOS_API.test_cases_results_info.recording_error_message \
                                                                               + "; V: " + str(video_result_1))
                                error_codes = NOS_API.test_cases_results_info.recording_error_code
                                error_messages = NOS_API.test_cases_results_info.recording_error_message
                                NOS_API.set_error_message("HDD")
                                                                                         
                            ################################################################ SCART Test ###################################################################################
                            
                            if(REC_START_Result):
                            
                                NOS_API.grabber_stop_video_source()
                                time.sleep(1)
                                NOS_API.grabber_stop_audio_source()
                                time.sleep(1) 
                            
                                ## Initialize input interfaces of DUT RT-AV101 device 
                                NOS_API.reset_dut()
                                #time.sleep(2)

                                ## Start grabber device with video on default video source
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                                time.sleep(3)
                                
                                if not(NOS_API.is_signal_present_on_video_source()):                                    
                                    NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                    time.sleep(2)
                                if (NOS_API.is_signal_present_on_video_source()):
                                    ## Check if video is playing (check if video is not freezed)
                                    if (NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.CVBS2)):
                                        video_result = 0

                                        try:
                                            ## Perform grab picture
                                            try:
                                                TEST_CREATION_API.grab_picture("SCART_video")
                                            except: 
                                                time.sleep(5)
                                                try:
                                                    TEST_CREATION_API.grab_picture("SCART_video")
                                                except:
                                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on Scart")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                                                    NOS_API.set_error_message("Video Scart")
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
                                                

                                            ## Compare grabbed and expected image and get result of comparison
                                            video_result = NOS_API.compare_pictures("SCART_video_ref", "SCART_video", "[HALF_SCREEN_576p]")

                                        except Exception as error:
                                           ## Set test result to INCONCLUSIVE
                                           TEST_CREATION_API.write_log_to_file(str(error))
                                           test_result = "FAIL"
                                           TEST_CREATION_API.write_log_to_file("There is no signal on SCART interface.")
                                           NOS_API.set_error_message("Video Scart")

                                        ## Check video analysis results and update comments
                                        if (video_result >= NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD):
                                           ## Set test result to PASS
                                           test_result_SCART_video = True
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on SCART interface.")
                                            NOS_API.set_error_message("Video Scart")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.scart_noise_error_message \
                                                                                + "; V: " + str(video_result))
                                            error_codes = NOS_API.test_cases_results_info.scart_noise_error_code
                                            error_messages =  NOS_API.test_cases_results_info.scart_noise_error_message

                                    else:
                                        TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on SCART interface.")
                                        NOS_API.set_error_message("Video Scart")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_freezing_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.scart_image_freezing_error_message \
                                                                                + "; Video is not playing on SCART interface")
                                        error_codes = NOS_API.test_cases_results_info.scart_image_freezing_error_code
                                        error_messages = NOS_API.test_cases_results_info.scart_image_freezing_error_message
                                else:
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on Scart")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                                    NOS_API.set_error_message("Video Scart")
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
                               
    ############################################################################# SCART Audio ##################################################################################
                           
                                if(test_result_SCART_video):
                                
                                    NOS_API.grabber_stop_video_source()
                                    time.sleep(0.5)
                                    
                                    ## Start grabber device with audio on SCART audio source
                                    TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.LINEIN2)
                                    time.sleep(3)
                                
                                
                                    ## Record audio from digital output (SCART)
                                    TEST_CREATION_API.record_audio("SCART_audio", MAX_RECORD_AUDIO_TIME)
                                    
                                ## Good Audio Comparison start ####
                                
                                #
                                #    ## Compare recorded and expected audio and get result of comparison
                                #    audio_result_1 = NOS_API.compare_audio("SCART_audio_ref1", "SCART_audio")
                                #    audio_result_2 = NOS_API.compare_audio("SCART_audio_ref2", "SCART_audio")
                                #    
                                #    if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result_2 < TEST_CREATION_API.AUDIO_THRESHOLD):
                                #        ## Record audio from digital output (SCART)
                                #        TEST_CREATION_API.record_audio("SCART_audio", MAX_RECORD_AUDIO_TIME)
                                #  
                                #        ## Compare recorded and expected audio and get result of comparison
                                #        audio_result_1 = NOS_API.compare_audio("SCART_audio_ref1", "SCART_audio")
                                #        audio_result_2 = NOS_API.compare_audio("SCART_audio_ref2", "SCART_audio")
                                #        
                                #        if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result_2 < TEST_CREATION_API.AUDIO_THRESHOLD):
                                #            
                                #            NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                #            
                                #            ## Record audio from digital output (SCART)
                                #            TEST_CREATION_API.record_audio("SCART_audio", MAX_RECORD_AUDIO_TIME)
                                #        
                                #            ## Compare recorded and expected audio and get result of comparison
                                #            audio_result_1 = NOS_API.compare_audio("SCART_audio_ref1", "SCART_audio")
                                #            audio_result_2 = NOS_API.compare_audio("SCART_audio_ref2", "SCART_audio")
                                #  
                                #    if (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                #        
                                #        ## Check is audio present on channel
                                #        if (TEST_CREATION_API.is_audio_present("SCART_audio")):
                                #            SCART_Result = True
                                #            
                                #        else:
                                #            TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                #            NOS_API.set_error_message("Audio Scart")
                                #            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                #                                                    + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message \
                                #                                                    + "; Audio is not present on SCART interface")
                                #            error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                #            error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                #    else:
                                #        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SCART interface.")
                                #        NOS_API.set_error_message("Audio Scart")
                                #        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code  \
                                #                                                    + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_code  \
                                #                                                    + "; Error messages: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message \
                                #                                                    + ";\n" + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message)
                                #        error_codes = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_code
                                #        error_messages = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_message
                                #                  
                                    
                                    
                                ## Good Audio Comparison end ####
                                    
                                    
                                ## No Audio Comparison start ####
                                    
                                    ## Compare recorded and expected audio and get result of comparison
                                   ## Compare recorded and expected audio and get result of comparison
                                    audio_result_1 = NOS_API.compare_audio("No_Left_ref", "SCART_audio", "[AUDIO_ANALOG]")
                                    audio_result_2 = NOS_API.compare_audio("No_right_ref", "SCART_audio", "[AUDIO_ANALOG]")
                                    audio_result_3 = NOS_API.compare_audio("No_Both_ref", "SCART_audio", "[AUDIO_ANALOG]")
                        
                                    if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            
                                        ## Check is audio present on channel
                                        if (TEST_CREATION_API.is_audio_present("SCART_audio")):
                                            #test_result = "PASS"
                                            SCART_Result = True
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message)
                                            error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                            NOS_API.set_error_message("Audio Scart") 
                                    else:
                                        time.sleep(3)
                                        
                                        NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                        
                                        ## Record audio from digital output (SCART)
                                        TEST_CREATION_API.record_audio("SCART_audio1", MAX_RECORD_AUDIO_TIME)
                                    
                                        ## Compare recorded and expected audio and get result of comparison
                                        audio_result_1 = NOS_API.compare_audio("No_Left_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                        audio_result_2 = NOS_API.compare_audio("No_right_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                        audio_result_3 = NOS_API.compare_audio("No_Both_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                    
                                        if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                    
                                            ## Check is audio present on channel
                                            if (TEST_CREATION_API.is_audio_present("SCART_audio1")):
                                                SCART_Result = True
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message)
                                                error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                                error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                                NOS_API.set_error_message("Audio Scart") 
                                        else:           
                                            TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SCART interface.")
                                            NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code  \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_code  \
                                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_message)
                                            error_codes = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_code
                                            error_messages = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_message
                                            NOS_API.set_error_message("Audio Scart") 
                                            
                            
                                ## No Audio Comparison end ####
                                                                                                        
    #################################################################################################### Analog Audio ###################################################################################################################
                                
                                if(SCART_Result):
                                
                                    NOS_API.grabber_stop_audio_source()
                                    time.sleep(1)
                                    
                                    ## Start grabber device with audio on analog audio source
                                    TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.LINEIN)

                                    ## Zap to service
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    #TEST_CREATION_API.send_ir_rc_command(NOS_API.CHANNEL)

                                    ## Record audio from analog output
                                    TEST_CREATION_API.record_audio("analog_audio", MAX_RECORD_AUDIO_TIME)

                                    
                                    
                                ## Good Audio Comparison start ####    
                                    
                                #    ## Compare recorded and expected audio and get result of comparison
                                #    audio_result1 = NOS_API.compare_audio("analog_audio_ref1", "analog_audio")
                                #    audio_result2 = NOS_API.compare_audio("analog_audio_ref2", "analog_audio")
                                #    
                                #    if (audio_result1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result2 < TEST_CREATION_API.AUDIO_THRESHOLD):
                                #    
                                #        ## Record audio from analog output
                                #        TEST_CREATION_API.record_audio("analog_audio", MAX_RECORD_AUDIO_TIME)
                                #
                                #        ## Compare recorded and expected audio and get result of comparison
                                #        audio_result1 = NOS_API.compare_audio("analog_audio_ref1", "analog_audio")
                                #        audio_result2 = NOS_API.compare_audio("analog_audio_ref2", "analog_audio")
                                #    
                                #        if (audio_result1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result2 < TEST_CREATION_API.AUDIO_THRESHOLD):
                                #        
                                #            NOS_API.display_dialog("Confirme os cabos de Audio Analogico e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                #            
                                #            ## Record audio from analog output
                                #            TEST_CREATION_API.record_audio("analog_audio", MAX_RECORD_AUDIO_TIME)
                                #        
                                #            ## Compare recorded and expected audio and get result of comparison
                                #            audio_result1 = NOS_API.compare_audio("analog_audio_ref1", "analog_audio")
                                #            audio_result2 = NOS_API.compare_audio("analog_audio_ref2", "analog_audio")
                                #    
                                #    if (audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                #
                                #        ## Check is audio present on channel
                                #        if (TEST_CREATION_API.is_audio_present("analog_audio")):
                                #            ANALOG_AUDIO_Result = True
                                #          
                                #        else:
                                #            TEST_CREATION_API.write_log_to_file("Audio is not present on analog interface.")
                                #            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code \
                                #                                                   + "; Error message: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message \
                                #                                                   + "; Audio is not present on analog interface")
                                #            error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code
                                #            error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message
                                #    else:
                                #        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on analog interface.")
                                #        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_code  \
                                #                                                   + ";\n" + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_code  \
                                #                                                   + "; Error messages: " + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message \
                                #                                                   + ";\n" + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message)
                                #        error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_code
                                #        error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_message
                                #                
                                ## Good Audio Comparison end ####   

                                ## No Audio Comparison start ####
                                
                                    ## Compare recorded and expected audio and get result of comparison
                                    audio_result1 = NOS_API.compare_audio("No_Left_ref", "analog_audio", "[AUDIO_ANALOG]")
                                    audio_result2 = NOS_API.compare_audio("No_right_ref", "analog_audio", "[AUDIO_ANALOG]")
                                    audio_result3 = NOS_API.compare_audio("No_Both_ref", "analog_audio", "[AUDIO_ANALOG]")
                                    
                                    if not(audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                    
                                        ## Check is audio present on channel
                                        if (TEST_CREATION_API.is_audio_present("analog_audio")):
                                           ANALOG_AUDIO_Result = True
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Audio is not present on analog interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code \
                                                                                   + "; Error message: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message)
                                            error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message
                                            NOS_API.set_error_message("Audio Analogico")
                                    else:
                                        time.sleep(3)
                                        
                                        NOS_API.display_dialog("Confirme os cabos Audio Analogico e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                        
                                        ## Record audio from analog output
                                        TEST_CREATION_API.record_audio("analog_audio1", MAX_RECORD_AUDIO_TIME)
                                    
                                        ## Compare recorded and expected audio and get result of comparison
                                        audio_result1 = NOS_API.compare_audio("No_Left_ref", "analog_audio1", "[AUDIO_ANALOG]")
                                        audio_result2 = NOS_API.compare_audio("No_right_ref", "analog_audio1", "[AUDIO_ANALOG]")
                                        audio_result3 = NOS_API.compare_audio("No_Both_ref", "analog_audio1", "[AUDIO_ANALOG]")
                                    
                                        if not(audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                    
                                            ## Check is audio present on channel
                                            if (TEST_CREATION_API.is_audio_present("analog_audio1")):
                                                ANALOG_AUDIO_Result = True
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Audio is not present on analog interface.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message)
                                                error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code
                                                error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message
                                                NOS_API.set_error_message("Audio Analogico")
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on analog interface.")
                                            NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_code  \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_code  \
                                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_message)
                                            error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_code
                                            error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_message
                                            NOS_API.set_error_message("Audio Analogico")

    ########################################################################################### SPDIF Test ##############################################################################################################################
                                    
                                if(ANALOG_AUDIO_Result):
                                
                                    NOS_API.grabber_stop_audio_source()
                                    time.sleep(1)
                                    
                                    ## Start grabber device with audio on default audio source
                                    TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.SPDIF_OPT)
                                    time.sleep(3)
                                   
                                    ## Record audio from digital output (SPDIF OPT)
                                    TEST_CREATION_API.record_audio("SPDIF_OPT_audio", MAX_RECORD_AUDIO_TIME)

                                ## Good Audio Comparison start ####    
                                    
                                #    ## Compare recorded and expected audio and get result of comparison
                                #    audio_result_1 = NOS_API.compare_audio("SPDIF_OPT_audio_ref1", "SPDIF_OPT_audio")
                                #    audio_result_2 = NOS_API.compare_audio("SPDIF_OPT_audio_ref2", "SPDIF_OPT_audio")
                                #    
                                #    
                                #    if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result_2 < TEST_CREATION_API.AUDIO_THRESHOLD):
                                #        
                                #        ## Record audio from digital output (SPDIF OPT)
                                #        TEST_CREATION_API.record_audio("SPDIF_OPT_audio", MAX_RECORD_AUDIO_TIME)
                                #
                                #        ## Compare recorded and expected audio and get result of comparison
                                #        audio_result_1 = NOS_API.compare_audio("SPDIF_OPT_audio_ref1", "SPDIF_OPT_audio")
                                #        audio_result_2 = NOS_API.compare_audio("SPDIF_OPT_audio_ref2", "SPDIF_OPT_audio")
                                #        
                                #        if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result_2 < TEST_CREATION_API.AUDIO_THRESHOLD):
                                #        
                                #            NOS_API.display_dialog("Confirme o cabo TOSLINK e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                #        
                                #            ## Record audio from digital output (SPDIF OPT)
                                #            TEST_CREATION_API.record_audio("SPDIF_OPT_audio", MAX_RECORD_AUDIO_TIME)
                                #        
                                #            ## Compare recorded and expected audio and get result of comparison
                                #            audio_result_1 = NOS_API.compare_audio("SPDIF_OPT_audio_ref1", "SPDIF_OPT_audio")
                                #            audio_result_2 = NOS_API.compare_audio("SPDIF_OPT_audio_ref2", "SPDIF_OPT_audio")
                                #        
                                #    if (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                #
                                #        ## Check is audio present on channel
                                #        if (TEST_CREATION_API.is_audio_present("SPDIF_OPT_audio")):
                                #            SPDIF_Result = True
                                #           
                                #        else:
                                #            TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF optical interface.")
                                #            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code \
                                #                                                   + "; Error message: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message \
                                #                                                   + "; Audio is not present on SPDIF optical interface")
                                #            error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code
                                #            error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message
                                #    else:
                                #        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SPDIF optical interface.")
                                #        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_code  \
                                #                                                   + ";\n" + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_code  \
                                #                                                   + "; Error messages: " + NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_message \
                                #                                                   + ";\n" + NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_message)
                                #        error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_code
                                #        error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_message
                                
                                ## Good Audio Comparison end ####
                                
                                ## No Audio Comparison start ####
                                    ## Compare recorded and expected audio and get result of comparison
                                    audio_result1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_OPT_audio")

                                    if not(audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD):

                                        ## Check is audio present on channel
                                        if (TEST_CREATION_API.is_audio_present("SPDIF_OPT_audio")):
                                           SPDIF_Result = True
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF coaxial interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code \
                                                                                   + "; Error message: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message)
                                            error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message 
                                            NOS_API.set_error_message("SPDIF")
                                    else:
                                        time.sleep(3)
                                        
                                        NOS_API.display_dialog("Confirme o cabo SPDIF e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                        
                                        ## Record audio from digital output (SPDIF COAX)
                                        TEST_CREATION_API.record_audio("SPDIF_OPT_audio1", MAX_RECORD_AUDIO_TIME)
                                    
                                        ## Compare recorded and expected audio and get result of comparison
                                        audio_result1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_OPT_audio1")
                                    
                                        if not(audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                    
                                            ## Check is audio present on channel
                                            if (TEST_CREATION_API.is_audio_present("SPDIF_OPT_audio1")):
                                                SPDIF_Result = True
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF coaxial interface.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message)
                                                error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code
                                                error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message 
                                                NOS_API.set_error_message("SPDIF")
                                        else:           
                                            TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SPDIF coaxial interface.")
                                            NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_code  \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_code  \
                                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_message \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_message)
                                            error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_code
                                            error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_message + " " +  NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_message
                                            NOS_API.set_error_message("SPDIF")
                                
                                    ################################################################ Video Recording ##############################################################################
                                    
                                    if(SPDIF_Result):
                                    
                                        NOS_API.grabber_stop_audio_source()
                                        time.sleep(1)
                                        
                                        ## Start grabber device with video on default video source
                                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                        TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
                                        
                                        TEST_CREATION_API.send_ir_rc_command("[DVR_1]")

                                        #TEST_CREATION_API.send_ir_rc_command("[PLAY_CONTENT_FROM_HDD]")
                                        if not(NOS_API.grab_picture("HDD_menu")):
                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            
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
                                            return
                                        
                                        if not(TEST_CREATION_API.compare_pictures("hdd_menu_ref", "HDD_menu", "[HDD_MENU]")):
                                            TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                                            time.sleep(1)
                                            TEST_CREATION_API.send_ir_rc_command("[DVR_1]")
                                            if not(NOS_API.grab_picture("HDD_menu")):
                                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                NOS_API.set_error_message("Video HDMI")
                                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                
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
                                                return
                                            
                                            if not(TEST_CREATION_API.compare_pictures("hdd_menu_ref", "HDD_menu", "[HDD_MENU]")):
                                                TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                NOS_API.set_error_message("Navegação")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                                
                                        if(TEST_CREATION_API.compare_pictures("empty_recorded_list_ref", "HDD_menu", "[RECORDED_CONTENT_AREA]")):
                                            ## Use this variable in script Video Recording Content to check is recording started or not
                                            NOS_API.test_cases_results_info.recording_started = False
                                            TEST_CREATION_API.write_log_to_file("Recording is not started")   
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recording_error_code \
                                                                                           + "; Error message: " + NOS_API.test_cases_results_info.recording_error_message \
                                                                                           + "; V: " + str(video_result_1))
                                            error_codes = NOS_API.test_cases_results_info.recording_error_code
                                            error_messages = NOS_API.test_cases_results_info.recording_error_message
                                            NOS_API.set_error_message("HDD")
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
                                        
                                        TEST_CREATION_API.send_ir_rc_command("[PLAY_HDD]")
                                        
                                        if not(NOS_API.grab_picture("Check_Play")):
                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            
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
                                            return
                                        
                                        if(TEST_CREATION_API.compare_pictures("recorded_content_ref", "Check_Play", "[HALF_SCREEN]") == False):
                                            TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                                            time.sleep(4)
                                            TEST_CREATION_API.send_ir_rc_command("[PLAY_CONTENT_FROM_HDD]")
                                            if not(NOS_API.grab_picture("HDD_menu_1")):
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
                                            if(TEST_CREATION_API.compare_pictures("recorded_content_ref", "HDD_menu_1", "[HALF_SCREEN]") == False):
                                                if(TEST_CREATION_API.compare_pictures("HDD_menu_1", "HDD_menu", "[Check_Blocked_Play]") == False):
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
                                                    TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                    NOS_API.set_error_message("Navegação")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                                    error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                    error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                                
                                        if not (NOS_API.is_signal_present_on_video_source()):
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
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                
                                        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                        
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            return
                                            
                                        ## Record video with duration of recording (5 seconds)
                                        NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)

                                        ## Instance of PQMAnalyse type
                                        pqm_analyse = TEST_CREATION_API.PQMAnalyse()

                                        ## Set what algorithms should be checked while analyzing given video file with PQM.
                                        # Attributes are set to false by default.
                                        pqm_analyse.black_screen_activ = True
                                        pqm_analyse.blocking_activ = True
                                        pqm_analyse.freezing_activ = True

                                        # Name of the video file that will be analysed by PQM.
                                        pqm_analyse.file_name = "video"

                                        ## Analyse recorded video
                                        analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)

                                        if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message)
                                            NOS_API.set_error_message("HDD")       
                                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message

                                        if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message)
                                            NOS_API.set_error_message("HDD")
                                            if (error_codes == ""):
                                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                                            else:
                                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                                            
                                            if (error_messages == ""):
                                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                                            else:
                                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message

                                        if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                                            NOS_API.set_error_message("HDD")
                                            if (error_codes == ""):
                                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                            else:
                                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                            
                                            if (error_messages == ""):
                                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                            else:
                                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                        

                                        ## Check if video is playing (check if video is not freezed)
                                        if (NOS_API.is_video_playing()):
                                            video_result = 0

                                            try:
                                                ## Perform grab picture
                                                TEST_CREATION_API.grab_picture("recorded_content")

                                                ## Compare grabbed and expected image and get result of comparison
                                                video_result = NOS_API.compare_pictures("recorded_content_ref", "recorded_content", "[HALF_SCREEN]")

                                            except Exception as error:
                                                ## Set test result to INCONCLUSIVE
                                                TEST_CREATION_API.write_log_to_file(str(error))
                                                test_result = "FAIL"
                                                TEST_CREATION_API.write_log_to_file("There is no signal on HDMI 720p interface.")

                                            ## Check video analysis results and update comments
                                            if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                if (analysed_video): 
                                                    ## Set test result to PASS           
                                                    VIDEO_RECORD_Result = True
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Recorded video is not reproduced correctly on HDMI 720p interface.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                       + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                                       + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                                       + "; V: " + str(video_result))
                                                NOS_API.set_error_message("HDD") 
                                                error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                                error_messages =  NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_noise_error_message

                                        else:
                                            TEST_CREATION_API.write_log_to_file("Recorded video is not playing on HDMI 720p interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                       + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                                                                       + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message \
                                                                                       + "; Recorded video is not playing")
                                            error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                            error_messages =  NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                            NOS_API.set_error_message("HDD") 
                                                                                                                    
                                        ################################################################ Audio Record Test ############################################################################
                                        
                                        if(VIDEO_RECORD_Result):
                                            
                                            time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[REPLAY_CONTENT_FROM_HDD]")
                                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                                            time.sleep(1)

                                            ## Record audio from digital output (HDMI)
                                            TEST_CREATION_API.record_audio("HDMI_audio_rec", MAX_RECORD_AUDIO_TIME)

                                            ### Compare recorded and expected audio and get result of comparison
                                            #audio_result1 = NOS_API.compare_audio("HDMI_audio_ref1", "HDMI_audio_rec")
                                            #audio_result2 = NOS_API.compare_audio("HDMI_audio_ref2", "HDMI_audio_rec")
                                            
                                             ## Compare recorded and expected audio and get result of comparison
                                            audio_result1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_rec")
                                                                                             
                                            #if (audio_result1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result2 < TEST_CREATION_API.AUDIO_THRESHOLD): 
                                            if (audio_result1 > TEST_CREATION_API.AUDIO_THRESHOLD):
                                            
                                                ## Record audio from digital output (HDMI)
                                                TEST_CREATION_API.record_audio("HDMI_audio_rec", MAX_RECORD_AUDIO_TIME)

                                                ## Compare recorded and expected audio and get result of comparison
                                                audio_result1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_rec")
                                                #audio_result2 = NOS_API.compare_audio("HDMI_audio_ref2", "HDMI_audio_rec")
                                            
                                            #if (audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result2 >= TEST_CREATION_API.AUDIO_THRESHOLD):    
                                            if (audio_result1 < TEST_CREATION_API.AUDIO_THRESHOLD):

                                                ## Check is audio present on channel
                                                if (TEST_CREATION_API.is_audio_present("HDMI_audio_rec")):
                                                    ## Set test result to PASS
                                                    AUDIO_RECORD_Result = True
                                                    TEST_CREATION_API.send_ir_rc_command("[STOP]")
                                                    TEST_CREATION_API.send_ir_rc_command("[STOP]")
                                                    ## Exit from playback
                                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_PLAYBACK]")    
                                                else:       
                                                    NOS_API.set_error_message("HDD") 
                                                    TEST_CREATION_API.write_log_to_file("Audio is not present on hdmi 720p interface.")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                           + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code \
                                                                                           + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message \
                                                                                           + "; Audio is not present on hdmi_576p interface")
                                                    error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code
                                                    error_messages = NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message
                                            else:                             
                                                time.sleep(2)
                                                TEST_CREATION_API.send_ir_rc_command("[REPLAY_CONTENT_FROM_HDD]")
                                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                                time.sleep(1)
                                        
                                                ## Record audio from digital output (HDMI)
                                                TEST_CREATION_API.record_audio("HDMI_audio_rec1", MAX_RECORD_AUDIO_TIME)
                                        
                                                ### Compare recorded and expected audio and get result of comparison
                                                #audio_result1 = NOS_API.compare_audio("HDMI_audio_ref1", "HDMI_audio_rec1")
                                                #audio_result2 = NOS_API.compare_audio("HDMI_audio_ref2", "HDMI_audio_rec1")
                                                
                                                audio_result1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_rec1")
                                                
                                                #if (audio_result1 < TEST_CREATION_API.AUDIO_THRESHOLD and audio_result2 < TEST_CREATION_API.AUDIO_THRESHOLD): 
                                                if (audio_result1 > TEST_CREATION_API.AUDIO_THRESHOLD): 
                                                    ## Record audio from digital output (HDMI)
                                                    TEST_CREATION_API.record_audio("HDMI_audio_rec1", MAX_RECORD_AUDIO_TIME)
                                        
                                                    ## Compare recorded and expected audio and get result of comparison
                                                    audio_result1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_rec1")
                                                    #audio_result2 = NOS_API.compare_audio("HDMI_audio_ref2", "HDMI_audio_rec1")
                                                
                                                #if (audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result2 >= TEST_CREATION_API.AUDIO_THRESHOLD): 
                                                if (audio_result1 < TEST_CREATION_API.AUDIO_THRESHOLD):
                                        
                                                    ## Check is audio present on channel
                                                    if (TEST_CREATION_API.is_audio_present("HDMI_audio_rec1")):
                                        
                                                        ## Set test result to PASS
                                                        AUDIO_RECORD_Result = True
                                                        TEST_CREATION_API.send_ir_rc_command("[STOP]")
                                                        TEST_CREATION_API.send_ir_rc_command("[STOP]")
                                                        ## Exit from playback
                                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_PLAYBACK]")
                                                                  
                                                    else:
                                                        NOS_API.set_error_message("HDD") 
                                                        TEST_CREATION_API.write_log_to_file("Audio is not present on hdmi 720p interface.")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message \
                                                                                            + "; Audio is not present on hdmi_576p interface")
                                                        error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code
                                                        error_messages = NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message
                                                else:
                                                    NOS_API.set_error_message("HDD") 
                                                    TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                                    NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                                            + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                                            + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                                            + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                                                    error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                                                    error_messages = NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                                                             
    ######################################################################################################## HD_SD Channel ############################################################################################################
                                        
                                            if(AUDIO_RECORD_Result):
                                                    
                                              ########################################Set 1080p Resolution #######################################
                                                    
                                              ###########################Erase Recorded Content###########################################
                                                TEST_CREATION_API.send_ir_rc_command("[HDD_MENU_T804]")
                                                time.sleep(2.5)
                                                ## Delete recorded content
                                                TEST_CREATION_API.send_ir_rc_command("[DELETE_A_CONTENT]")
                                                time.sleep(2)
                                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                              #############################################################################################	 
                                              
                                                time.sleep(0.7)
                                                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080p_T804]")
                                             
                                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                if(video_height != "1080"):
                                                    time.sleep(1)
                                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080p_T804]")
                                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                    if (video_height != "1080"):
                                                        NOS_API.set_error_message("Resolução")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                                   + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                                        error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                                        error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                                    else:
                                                        test_result_res = True
                                                else:
                                                    test_result_res = True
                                              ###########################################################################################################################
    ################################################################################################ 1080p Video Output ###############################################################################################################
                                                
                                                if(test_result_res):
                                                    ## Zap to service
                                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                    #TEST_CREATION_API.send_ir_rc_command(NOS_API.HD_CHANNEL)
                                                    
                                            
                                                    while (hd_counter < 3):
                                                        video_result = 0
                                                        time.sleep(NOS_API.MAX_ZAP_TIME)
                                                        time.sleep(1)
                                            
                                                        try:
                                                            ## Perform grab picture
                                                            if not(NOS_API.grab_picture("hd_channel")):
                                                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                                NOS_API.set_error_message("Video HDMI")
                                                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                                
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
                                                                return
                                                            
                                                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)

                                                            video_result1 = NOS_API.compare_pictures("hd_channel_ref1", "hd_channel", "[HALF_SCREEN_HD]")                
                                                            video_result2 = NOS_API.compare_pictures("hd_channel_ref2", "hd_channel", "[HALF_SCREEN_HD]")
                                                            video_result3 = NOS_API.compare_pictures("hd_channel_ref3", "hd_channel", "[HALF_SCREEN_HD]")
                                            
                                                        except Exception as error:
                                                            ## Set test result to INCONCLUSIVE
                                                            TEST_CREATION_API.write_log_to_file(str(error))
                                                            test_result = "FAIL"
                                                            TEST_CREATION_API.write_log_to_file("There is no signal on HDMI interface.")
                                                        
                                                        ## Record audio from HDMI
                                                        #TEST_CREATION_API.record_audio("audio_hd_channel", MAX_RECORD_AUDIO_TIME)
                                                        #
                                                        #audio_result_1 = NOS_API.compare_audio("No_Both_ref", "audio_hd_channel")
                                                        #audio_result_2 = NOS_API.compare_audio("audio_hd_channel_ref2", "audio_hd_channel")
                                                        
                                                        
                                                        # Check if STB zap to horizontal polarization channel (check image and audio)
                                                        #if ((video_result1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD) and (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or \
                                                        #    audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD)):
                                                        if (video_result1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                        
                                                            test_result_hd = True
                                                            break
                                            
                                                        else:
                                                            if (hd_counter == 2):
                                                                if(video_result1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                                    TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 1080p interface.")
                                                                    NOS_API.set_error_message("Audio HDMI")
                                                                    NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_code  \
                                                                                                    + ";\n" + NOS_API.test_cases_results_info.hdmi_1080p_signal_interference_error_code  \
                                                                                                    + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_message \
                                                                                                    + ";\n" + NOS_API.test_cases_results_info.hdmi_1080p_signal_interference_error_message)
                                                                    error_codes = NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_1080p_signal_interference_error_code
                                                                    error_messages = NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_1080p_signal_interference_error_message
                                                                else:
                                                                    TEST_CREATION_API.write_log_to_file("STB does not tune to hd channel")
                                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hd_channel_error_code \
                                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hd_channel_error_message \
                                                                                                    + "; V: " + str(video_result))
                                                                    NOS_API.set_error_message("Tuner")
                                                                    error_codes = NOS_API.test_cases_results_info.hd_channel_error_code
                                                                    error_messages = NOS_API.test_cases_results_info.hd_channel_error_message
                                                            else:
                                                                TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                                                                time.sleep(2)
                                                                TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                                                TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")

                                                        hd_counter = hd_counter + 1
                                                 
                                                if(test_result_hd):
                                                    #Get start time
                                                    startTime = time.localtime()
                                                    
                                                    while (True):

                                                        response = NOS_API.send_cmd_to_telnet(sid, cmd0)
                                                        TEST_CREATION_API.write_log_to_file("response:" + str(response))
                                                        if(response != None):
                                                            if(response.find("Error:") != -1):
                                                                error_command_telnet = True
                                                                break
                                                            if(response != "BUSY"):
                                                                stb_state = NOS_API.is_stb_operational(response)
                                                                break
                                                        else:
                                                            NOS_API.set_error_message("Telnet timeout")
                                                            TEST_CREATION_API.write_log_to_file("Don't get response from telnet in 30 minutes")
                                                            error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                            error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                            report_file = ""    
                                                        
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
                                                            return
                                                            
                                                        time.sleep(5)
                                                            
                                                        #Get current time
                                                        currentTime = time.localtime()
                                                        if((time.mktime(currentTime) - time.mktime(startTime)) > NOS_API.MAX_WAIT_TIME_RESPOND_FROM_TELNET):
                                                            NOS_API.set_error_message("Telnet timeout")
                                                            TEST_CREATION_API.write_log_to_file("Don't get response from telnet in 30 minutes")
                                                            error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                            error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                            if (response != None):
                                                                NOS_API.quit_session(sid)
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                            report_file = ""    
                                                        
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
                                                            return
                                                    
                                                    if(error_command_telnet == False):
                                                        if(stb_state == True):
                                                        
                                                            cmd1 = 'Show cable modem ' + NOS_API.test_cases_results_info.mac_using_barcode + ' verbose'
                                                            startTime = time.localtime()    
                                                    
                                                            while (True):
                                                                
                                                                response = NOS_API.send_cmd_to_telnet(sid, cmd1) 
                                                                TEST_CREATION_API.write_log_to_file("response:" + str(response))
                                                                                
                                                                if(response != None and response != "BUSY"):
                                                                    data = NOS_API.parse_telnet_cmd1(response)
                                                                    break
                                                                if(response == None):                    
                                                                    NOS_API.set_error_message("Telnet timeout")
                                                                    TEST_CREATION_API.write_log_to_file("Don't get response from telnet in 30 seconds")
                                                                    
                                                                    error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                                    error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                                    
                                                                    NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                                    report_file = ""    
                                                                    
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
                                                                    return
                                                                
                                                                time.sleep(5)
                                                                
                                                                #Get current time
                                                                currentTime = time.localtime()
                                                                if((time.mktime(currentTime) - time.mktime(startTime)) > NOS_API.MAX_WAIT_TIME_RESPOND_FROM_TELNET):
                                                                    NOS_API.set_error_message("Telnet timeout")
                                                                    TEST_CREATION_API.write_log_to_file("Telnet session expired")
                                                                    error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                                    error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                
                                                                    NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                                    report_file = ""    
                                                                    
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
                                                                    return
                                                                    
                                                            if (data[1] == "Operational"):
                                                                NOS_API.test_cases_results_info.ip = data[0]             
                                                                NOS_API.test_cases_results_info.tx = data[2] 
                                                                
                                                                try:
                                                                    NOS_API.test_cases_results_info.tx = float(NOS_API.test_cases_results_info.tx[:(NOS_API.test_cases_results_info.tx.find('d'))])
                                                                except Exception as error:
                                                                    ## Set test result to INCONCLUSIVE
                                                                    TEST_CREATION_API.write_log_to_file(str(error))
                                                                    NOS_API.test_cases_results_info.tx = "-"
                                                            
                                                                if (NOS_API.test_cases_results_info.tx != "-" and NOS_API.test_cases_results_info.tx < REC_POWER_THRESHOLD):
                                                                    NOS_API.test_cases_results_info.tx = str(NOS_API.test_cases_results_info.tx)
                                                                    
                                                                    ## Send the command: "show controllers cable-downstream <Value underlined in yellow>" and get results
                                                                    cmd2 = 'show controllers cable-downstream ' + data[3]
                                                                    #Get start time
                                                                    startTime = time.localtime()
                                                                    
                                                                    while (True):
                                                                        response = NOS_API.send_cmd_to_telnet(sid, cmd2) 
                                                                        TEST_CREATION_API.write_log_to_file("response cmd2:" + str(response))
                                                                        if(response != None and response != "BUSY"):
                                                                            data1 = NOS_API.parse_telnet_cmd2(response)        
                                                                            break
                                                                        if(response == None):   
                                                                            NOS_API.set_error_message("Telnet timeout")
                                                                            TEST_CREATION_API.write_log_to_file("Don't get response from telnet in 30 seconds")
                                                                            error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                                            
                                                                            NOS_API.add_test_case_result_to_file_report(
                                                                                    test_result,
                                                                                    "- - - - "  + NOS_API.test_cases_results_info.tx + " - - - - - - - - - - - "  + NOS_API.test_cases_results_info.ip + " " + NOS_API.test_cases_results_info.modulation + " " + NOS_API.test_cases_results_info.freq + "|" + NOS_API.test_cases_results_info.freq_upstream + " -",
                                                                                    "- - - - <52 - - - - - - - - - - - - - - -",
                                                                                    error_codes,
                                                                                    error_messages)
                                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                                            report_file = ""    
                                                                            
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
                                                                            return
                                                                        
                                                                        time.sleep(5)
                                                                        
                                                                        #Get current time
                                                                        currentTime = time.localtime()
                                                                        if((time.mktime(currentTime) - time.mktime(startTime)) > NOS_API.MAX_WAIT_TIME_RESPOND_FROM_TELNET):
                                                                            NOS_API.set_error_message("Telnet timeout")
                                                                            TEST_CREATION_API.write_log_to_file("Don't get response from telnet in 30 seconds")
                                                                            error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                
                                                                            NOS_API.add_test_case_result_to_file_report(
                                                                                        test_result,
                                                                                        "- - - - "  + NOS_API.test_cases_results_info.tx + " - - - - - - - - - - - "  + NOS_API.test_cases_results_info.ip + " " + NOS_API.test_cases_results_info.modulation + " " + NOS_API.test_cases_results_info.freq + "|" + NOS_API.test_cases_results_info.freq_upstream + " -",
                                                                                        "- - - - <52 - - - - - - - - - - - - - - -",
                                                                                        error_codes,
                                                                                        error_messages)
                                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                                            report_file = ""    
                                                                            
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
                                                                            return
                                                                            
                                                                    
                                                                    NOS_API.test_cases_results_info.freq = data1[0]
                                                                    try:
                                                                        ## Convert frequency for downstream from Hz to MHz
                                                                        NOS_API.test_cases_results_info.freq = int(NOS_API.test_cases_results_info.freq)/1000000.0
                                                                        NOS_API.test_cases_results_info.freq = str(int(NOS_API.test_cases_results_info.freq))
                                                                    except Exception as error:
                                                                        ## Set test result to INCONCLUSIVE
                                                                        TEST_CREATION_API.write_log_to_file(str(error))
                                                                        NOS_API.test_cases_results_info.freq = "-"
                                                                        
                                                                    NOS_API.test_cases_results_info.modulation = data1[1]
                                                                    
                                                                    ## Send the command: "show controllers cable-upstream <Value underlined in purple on first image>" and get results
                                                                    cmd3 = 'show controllers cable-upstream ' + data[4]
                                                                    #Get start time
                                                                    startTime = time.localtime()
                                                                    while (True):
                                                                        response = NOS_API.send_cmd_to_telnet(sid, cmd3)
                                                                        TEST_CREATION_API.write_log_to_file("response cmd3:" + str(response))
                                                                        if(response != None and response != "BUSY"):
                                                                            data2 = NOS_API.parse_telnet_cmd3(response)        
                                                                            break
                                                                        if(response == None):   
                                                                            NOS_API.set_error_message("Telnet timeout")
                                                                            TEST_CREATION_API.write_log_to_file("Don't get response from telnet in 30 seconds")
                                                                            error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                
                                                                            NOS_API.add_test_case_result_to_file_report(
                                                                                    test_result,
                                                                                    "- - - - "  + NOS_API.test_cases_results_info.tx + " - - - - - - - - - - - "  + NOS_API.test_cases_results_info.ip + " " + NOS_API.test_cases_results_info.modulation + " " + NOS_API.test_cases_results_info.freq + "|" + NOS_API.test_cases_results_info.freq_upstream + " -",
                                                                                    "- - - - <52 - - - - - - - - - - - - - - -",
                                                                                    error_codes,
                                                                                    error_messages)
                                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                                            report_file = ""    
                                                                            
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
                                                                            return
                                                                        
                                                                        time.sleep(5)
                                                                        
                                                                        #Get current time
                                                                        currentTime = time.localtime()
                                                                        if((time.mktime(currentTime) - time.mktime(startTime)) > NOS_API.MAX_WAIT_TIME_RESPOND_FROM_TELNET):
                                                                            NOS_API.set_error_message("Telnet timeout")
                                                                            TEST_CREATION_API.write_log_to_file("Don't get response from telnet in 30 seconds")
                                                                            error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                
                                                                            NOS_API.add_test_case_result_to_file_report(
                                                                                        test_result,
                                                                                        "- - - - "  + NOS_API.test_cases_results_info.tx + " - - - - - - - - - - - "  + NOS_API.test_cases_results_info.ip + " " + NOS_API.test_cases_results_info.modulation + " " + NOS_API.test_cases_results_info.freq + "|" + NOS_API.test_cases_results_info.freq_upstream + " -",
                                                                                        "- - - - <52 - - - - - - - - - - - - - - -",
                                                                                        error_codes,
                                                                                        error_messages)
                                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                                            report_file = ""    
                                                                            
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
                                                                            return
                                                            
                                                                    NOS_API.test_cases_results_info.freq_upstream = data2[0]
                                                                    
                                                                    try:
                                                                        ## Convert frequency for upstream from Hz to MHz
                                                                        NOS_API.test_cases_results_info.freq_upstream = int(NOS_API.test_cases_results_info.freq_upstream)/1000000.0
                                                                        NOS_API.test_cases_results_info.freq_upstream = str(NOS_API.test_cases_results_info.freq_upstream)
                                                                    except Exception as error:
                                                                        ## Set test result to INCONCLUSIVE
                                                                        TEST_CREATION_API.write_log_to_file(str(error))
                                                                        NOS_API.test_cases_results_info.freq_upstream = "-"
                                                                    
                                                                    test_result_telnet = True
                                                                else:
                                                                    TEST_CREATION_API.write_log_to_file("TX value is less than threshold")
                                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.tx_fail_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.tx_fail_error_message)
                                                                    NOS_API.set_error_message("CM Docsis")
                                                                    error_codes = NOS_API.test_cases_results_info.tx_fail_error_code
                                                                    error_messages = NOS_API.test_cases_results_info.tx_fail_error_message 
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("STB State is not operational")
                                                                NOS_API.set_error_message("CM Docsis")
                                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ip_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.ip_error_message)
                                                                error_codes = NOS_API.test_cases_results_info.ip_error_code
                                                                error_messages = NOS_API.test_cases_results_info.ip_error_message            
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB State is not operational")
                                                            NOS_API.set_error_message("CM Docsis")
                                                            error_codes = NOS_API.test_cases_results_info.ip_error_code
                                                            error_messages = NOS_API.test_cases_results_info.ip_error_message  
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.ip_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.ip_error_message)                                                
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("Invalid telnet command")
                                                        NOS_API.set_error_message("Invalid command")
                                                        error_codes = NOS_API.test_cases_results_info.ip_error_code
                                                        error_messages = NOS_API.test_cases_results_info.ip_error_message  
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.ip_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.ip_error_message)
                                                                                                
                                                    NOS_API.quit_session(sid)
                                                    
                                                    if(test_result_telnet):
                                                        if not(NOS_API.display_custom_dialog("O display est\xe1 ligado?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                                            TEST_CREATION_API.write_log_to_file("Display NOK")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.display_nok_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.display_nok_error_message)
                                                            NOS_API.set_error_message("Display")
                                                            error_codes = NOS_API.test_cases_results_info.display_nok_error_code
                                                            error_messages = NOS_API.test_cases_results_info.display_nok_error_message
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - "  + NOS_API.test_cases_results_info.tx + " - - - - - - - - - - - "  + NOS_API.test_cases_results_info.ip + " " + NOS_API.test_cases_results_info.modulation + " " + NOS_API.test_cases_results_info.freq + "|" + NOS_API.test_cases_results_info.freq_upstream + " -",
                                                                        "- - - - <52 - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                            report_file = ""    
                                                            
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
                                                            return
                                                            
                                                        if (NOS_API.display_custom_dialog("O Led Rede est\xe1 aceso?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):

                                                            if (NOS_API.is_signal_present_on_video_source()):
                                                                ## Set STB in initial state
                                                                TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                                            
                                                                ## Navigate to the factory reset
                                                                TEST_CREATION_API.send_ir_rc_command("[FACTORY_RESET_T804]")
                                                                
                                                                if (NOS_API.is_signal_present_on_video_source()):
                                                                    if not(NOS_API.grab_picture("factory_reset")):
                                                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                                        NOS_API.set_error_message("Video HDMI")
                                                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                                        
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
                                                                        return
                                                                        
                                                                    if not(TEST_CREATION_API.compare_pictures("factory_reset_ref", "factory_reset", "[FACTORY_RESET]")):
                                                                        TEST_CREATION_API.send_ir_rc_command("[INIT]")
                                                                        TEST_CREATION_API.send_ir_rc_command("[FACTORY_RESET_T804]")
                                                                        
                                                                        if not(NOS_API.grab_picture("factory_reset_1")):
                                                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                                            NOS_API.set_error_message("Video HDMI")
                                                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                                            
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
                                                                            return
                                                                            
                                                                        if not(TEST_CREATION_API.compare_pictures("factory_reset_ref", "factory_reset_1", "[FACTORY_RESET]")):
                                                                            TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                                            NOS_API.set_error_message("Navegação")
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                                                            error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                                                            
                                                                    ## Perform factory reset
                                                                    TEST_CREATION_API.send_ir_rc_command("[OK_WITHOUT_DELAY]")
                                                                    time.sleep(5)
                                                                    if (NOS_API.is_signal_present_on_video_source()):
                                                                        if not(NOS_API.grab_picture("factory_reset_after_OK")):
                                                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                                            NOS_API.set_error_message("Video HDMI")
                                                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                                            
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
                                                                            return
                                                                          
                                                                        if (TEST_CREATION_API.compare_pictures("factory_reset_ref", "factory_reset_after_OK", "[FACTORY_RESET]")):
                                                                            ## Perform factory reset
                                                                            TEST_CREATION_API.send_ir_rc_command("[OK_WITHOUT_DELAY]")
                                                                            
                                                                            if (NOS_API.is_signal_present_on_video_source()):
                                                                                if not(NOS_API.grab_picture("factory_reset_after_OK_1")):
                                                                                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                                                    NOS_API.set_error_message("Video HDMI")
                                                                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                                                    
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
                                                                                    return
                                                                                  
                                                                                if (TEST_CREATION_API.compare_pictures("factory_reset_ref", "factory_reset_after_OK_1", "[FACTORY_RESET]")):
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
                                                                                    return
                                                                                
                                                                ## Convert start time to milliseconds
                                                                start_time_in_ms = int(time.time() * MS_MULTIPLIER)
                                                            
                                                                ## Check is FTI displayed after factory reset
                                                                if (NOS_API.wait_for_multiple_pictures(["fti_ref"], TIME_COUNTER, ["[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                                                            
                                                                    ## Get time(in milliseconds) required to display first image after factory reset
                                                                    boot_counter = int(time.time() * MS_MULTIPLIER) - start_time_in_ms
                                                            
                                                                    TEST_CREATION_API.write_log_to_file("Duration of displaying first image after factory reset: " + str(boot_counter) + "ms", "measured_time.txt")
                                                                    NOS_API.update_test_slot_comment("Duration of displaying first image after factory reset: " + str(boot_counter) + "ms")
                                                                    NOS_API.test_cases_results_info.boot_measured_time = str(boot_counter)
                                                                    ## Set test result to PASS
                                                                    test_result_boot = True
                                                                else:
                                                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                                    if(video_height == "720"): 
                                                                        if not(NOS_API.grab_picture("factory_reset_black")):
                                                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                                            NOS_API.set_error_message("Video HDMI")
                                                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                                            
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
                                                                            return
                                                                            
                                                                        if(TEST_CREATION_API.compare_pictures("black_screen_720_ref", "factory_reset_black", "[FULL_SCREEN]")):
                                                                            test_result_boot = True
                                                                        else:
                                                                            TEST_CREATION_API.write_log_to_file("Time out is over")
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                                                            NOS_API.set_error_message("Factory Reset")
                                                                            error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message
                                                                    else:
                                                                        TEST_CREATION_API.write_log_to_file("Time out is over")
                                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                                                        NOS_API.set_error_message("Factory Reset")
                                                                        error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                                                        error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message
                                                                
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                                NOS_API.set_error_message("Video HDMI")   
                                                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                        
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("Led Net NOK")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.led_net_nok_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.led_net_nok_error_message)
                                                            NOS_API.set_error_message("Led's")
                                                            error_codes = NOS_API.test_cases_results_info.led_net_nok_error_code
                                                            error_message = NOS_API.test_cases_results_info.led_net_nok_error_message
                                                            
                                                            
                                                        ##################################################### Factory Reset ########################################################################
                                                        if(test_result_boot):
                                                            if (NOS_API.display_custom_dialog("O Led Power est\xe1 Verde?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                                                NOS_API.display_custom_dialog("Pressiona a tecla 'Power' da STB e de seguida pressiona Continuar", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                                                time.sleep(2)
                                                                if (NOS_API.is_signal_present_on_video_source()):
                                                                    time.sleep(2)
                                                                    if (NOS_API.is_signal_present_on_video_source()):
                                                                        TEST_CREATION_API.write_log_to_file("Power button NOK")
                                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_button_nok_error_code \
                                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_button_nok_error_message)  
                                                                        NOS_API.set_error_message("Botões")
                                                                        error_codes = NOS_API.test_cases_results_info.power_button_nok_error_code
                                                                        error_message = NOS_API.test_cases_results_info.power_button_nok_error_message
                                                                    else:
                                                                        if (NOS_API.display_custom_dialog("O Led Power Vermelho ligou?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                                                            test_result = "PASS"
                                                                            if (NOS_API.configure_power_switch()):
                                                                                NOS_API.power_off()
                                                                                time.sleep(3)
                                                                        else:
                                                                            TEST_CREATION_API.write_log_to_file("Led Power Red NOK")
                                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.led_power_red_nok_error_code \
                                                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.led_power_red_nok_error_message)
                                                                            NOS_API.set_error_message("Led's")
                                                                            error_codes = NOS_API.test_cases_results_info.led_power_red_nok_error_code
                                                                            error_messages = NOS_API.test_cases_results_info.led_power_red_nok_error_message 
                                                                else:
                                                                    if (NOS_API.display_custom_dialog("O Led Power Vermelho ligou?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                                                        test_result = "PASS"
                                                                        if (NOS_API.configure_power_switch()):
                                                                            NOS_API.power_off()
                                                                            time.sleep(3)
                                                                    else:
                                                                        TEST_CREATION_API.write_log_to_file("Led Power Red NOK")
                                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.led_power_red_nok_error_code \
                                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.led_power_red_nok_error_message)
                                                                        NOS_API.set_error_message("Led's")
                                                                        error_codes = NOS_API.test_cases_results_info.led_power_red_nok_error_code
                                                                        error_messages = NOS_API.test_cases_results_info.led_power_red_nok_error_message     
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("Led POWER green NOK")
                                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.led_power_green_nok_error_code \
                                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.led_power_green_nok_error_message)
                                                                NOS_API.set_error_message("Led's")
                                                                error_codes = NOS_API.test_cases_results_info.led_power_green_nok_error_code
                                                                error_message = NOS_API.test_cases_results_info.led_power_green_nok_error_message
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
                    "- - - - " + NOS_API.test_cases_results_info.tx + " - - - - - - - - - - - " + NOS_API.test_cases_results_info.ip + " " + NOS_API.test_cases_results_info.modulation + " " + NOS_API.test_cases_results_info.freq + "|" + NOS_API.test_cases_results_info.freq_upstream + " " + str(boot_counter),
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
        

    ## Update test result
    TEST_CREATION_API.update_test_result(test_result)

    ## Return DUT to initial state and de-initialize grabber device
    NOS_API.deinitialize()
  