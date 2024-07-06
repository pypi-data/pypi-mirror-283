#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: Feb 2024
# Last Modified: Feb 2024
#=================================================================
"""
Pre-requisite: 
base_frame.py
Used Input:
N/A
Expected Output:
Detailed windows based on user selection
Description:
This script defines individual checking option in a new ‘class’ object following logic stated in section 4.1.

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================


import tkinter as tk
import threading

from vision_oslo_extension.shared_contents import SharedVariables, Local_Shared, SharedMethods
from vision_oslo_extension.base_frame import BasePage

# Battery EMU Assessment
class A01(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 1: Battery EMU Assessment',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This function requires the excel spreadsheet with proper pre-defined information. See manual for detailed requirements',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Excel spreadsheet in .xlsx format is required before click RUN',font = controller.text_font)
        explain1.pack()
        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Option 1 & 2 require "Import "Excel - For Quick BEMU Assessment" if needed ',font = controller.text_font)
        explain2.pack()
        explain21 = tk.Label(master=self.headframe, text = 'NOTE: Option 3 & 4 require "Import "Excel - For Detail BEMU Assessment" if needed ',font = controller.text_font)
        explain21.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Preliminary Assessment (Import Excel - For Quick BEMU Assessment). (Only require .oof file)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Update spreadsheet only (Import Excel - For Quick BEMU Assessment). (Require all .d4 files)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: Detailed Modelling Auto Assessment (Import Excel - For Detail BEMU Assessment). (Only require .oof file)', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Update spreadsheet only (Import Excel - For Detail BEMU Assessment). (Require all .ds1 files)',value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        label02 = tk.Label(master=self.inputframe, text = 'Below required for Option 1 and Option 3',font = controller.text_font)
        label02.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 2,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 2,column = 3)

        button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_batch_processing(option1,input1,input2,input3),width = 20, height =2)
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Support", command=lambda: controller.show_frame("PageFive"))
        button2.grid(row = 0, column = 1)


    def run_batch_processing(self,option1,input1,input2,input3):
        try:
            # so that sim_name is updated when clicked
            sim_name = SharedVariables.sim_variable.get() # call variables saved in a shared places.
            main_option = SharedVariables.main_option
            time_start = input1.get()
            time_end = input2.get()
            option_select = option1.get()
            text_input = input3.get()
            low_v = Local_Shared.low_threshold
            high_v = Local_Shared.high_threshold
            time_step = Local_Shared.time_step

            # Run the batch processing function in a separate thread
            thread = threading.Thread(target=SharedMethods.common_thread_run,
                                      args=("battery_processing.py",sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step))
            thread.start()
        
        except Exception as e:
            print("Error in threading...Contact Support / Do not carry out multiple tasking at the same time. ", e)

# Connectivity
class A02(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 14: Output to Data Files',font = controller.sub_title_font)
        head.pack()

        explain = tk.Label(master=self.headframe, text = 'Directs seveval outputs plus train summary output', font = controller.text_font)
        explain.pack()

        #button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_post_processing(),width = 20, height =2)
        button = tk.Button(master=self.excuteframe, text="RUN!", command=lambda: controller.show_frame("PageFour"),width = 20, height =2)
        button.pack()


        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)


    def run_post_processing(self):
        try:
            # so that sim_name is updated when clicked
            sim_name = SharedVariables.sim_variable.get() # call variables saved in a shared places.
            main_option = SharedVariables.main_option
            time_start = Local_Shared.time_start
            time_end = Local_Shared.time_end
            option_select = Local_Shared.option_select
            text_input = Local_Shared.text_input
            low_v = Local_Shared.low_threshold
            high_v = Local_Shared.high_threshold
            time_step = Local_Shared.time_step

        except Exception as e:
            print("Error in post_processing.main:", e)

# Plotting
class A03(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 14: Output to Data Files',font = controller.sub_title_font)
        head.pack()

        explain = tk.Label(master=self.headframe, text = 'Directs seveval outputs plus train summary output', font = controller.text_font)
        explain.pack()

        #button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_post_processing(),width = 20, height =2)
        button = tk.Button(master=self.excuteframe, text="RUN!", command=lambda: controller.show_frame("PageFour"),width = 20, height =2)
        button.pack()


        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)


    def run_post_processing(self):
        try:
            # so that sim_name is updated when clicked
            sim_name = SharedVariables.sim_variable.get() # call variables saved in a shared places.
            main_option = SharedVariables.main_option
            time_start = Local_Shared.time_start
            time_end = Local_Shared.time_end
            option_select = Local_Shared.option_select
            text_input = Local_Shared.text_input
            low_v = Local_Shared.low_threshold
            high_v = Local_Shared.high_threshold
            time_step = Local_Shared.time_step

        except Exception as e:
            print("Error in post_processing.main:", e)

