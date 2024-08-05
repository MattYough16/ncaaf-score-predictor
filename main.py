from tkinter import *
from tkinter import filedialog
from ScorePredictorNCAAF import ScorePredictorNCAAF as SPN
import os
import warnings
warnings.filterwarnings('ignore')

###### Button Functions ######
# Get Path
def get_data_path():
    data_path = filedialog.askdirectory(title="Select Directory to NCAAF Predictor Files")
    in_path.set(data_path)

def get_out_path():
    result_path = filedialog.askdirectory(title="Select Directory for Prediction Results")
    out_path.set(result_path)

def make_predictions():
    predictor = SPN()

    # Get GUI Inputs
    data_path = in_path.get()
    prediction_path = out_path.get()
    season = int(year.get())
    current_week = int(week.get())
    playoff = bPO.get()

    # Make Predictions
    try:
        predictor.predict_scores(data_path, prediction_path, season, current_week, playoff)
        status.delete("1.0", "end")
        status.insert(INSERT, "Predictions Complete")
    except:
        status.delete("1.0", "end")
        status.insert(INSERT, "Missing Data for Season. Can't Complete Predictions")

def update_model():
    predictor = SPN()

    # Get GUI Inputs
    data_path = in_path.get()
    season = int(year.get())
    current_week = int(week.get())
    playoff = bPO.get()

    # Update Model with Current Weeks Data
    predictor_status = predictor.update_model(data_path, season, current_week, playoff)
    status.delete("1.0", "end")
    status.insert(INSERT, predictor_status)

def reset_model():
    predictor = SPN()

    start_year = reset_years1.get()
    end_year = reset_years2.get()
    model_path = in_path.get()

    home_model_fit, away_model_fit = predictor.retrain_model(model_path, start_year, end_year)

    out_string = f"Home Score Fit: {home_model_fit}\nAway Score Fit: {away_model_fit}"

    status.delete("1.0", "end")
    status.insert(INSERT, out_string)

###### GUI ######

# Setting Main Window
root = Tk()
root.title("Welcome to the NCAAF Score Predictor")
root.iconbitmap('Icon.ico')
#root.geometry('750x600')

#############################################################################################################
# Data and Model Path

# Adding a Label for Model Path
sPath_label = Label(root, text = "Predictor Directory")
sPath_label.grid(column =0, row =2)

# Adding a Text Entry Box for Model Path
in_path = StringVar()
spath = Entry(root, width=30, textvariable=in_path)
spath.grid(column =1, row =2)

# Adding Button to Open A Dialogue Box to Select PDF
Path_btn = Button(root, bg = 'red', width = 20, text = "Predictor Directory" ,
             activebackground = 'white', fg = "black", command=get_data_path)
Path_btn.grid(column=2, row=2)

#############################################################################################################
# Prediction Path

# Adding a Label for Model Path
sPath_label = Label(root, text = "Results Directory")
sPath_label.grid(column =0, row =3)

# Adding a Text Entry Box for Model Path
out_path = StringVar()
spath = Entry(root, width=30, textvariable=out_path)
spath.grid(column =1, row =3)

# Adding Button to Open A Dialogue Box to Select PDF
Out_btn = Button(root, bg = 'red', width = 20, text = "Prediction Output Directory" ,
             activebackground = 'white', fg = "black", command=get_out_path)
Out_btn.grid(column=2, row=3)

#############################################################################################################
# Adding a Label for Year
year_label = Label(root, text = "Season (Year)")
year_label.grid(column =0, row =0)

# Adding a Text Entry Box for Year
year = StringVar()
year = Entry(root, width=30, textvariable=year)
year.grid(column =1, row =0)

#############################################################################################################

# Adding a Label for Week
week_label = Label(root, text = "Week of Season")
week_label.grid(column =0, row =1)

# Adding a Text Entry Box for Week
week = StringVar()
week = Entry(root, width=30, textvariable=week)
week.grid(column =1, row =1)

#############################################################################################################

# Adding Button to Make Predictions
Prediction_btn = Button(root, bg = 'red', width = 25, height = 3, text = "Make Predictions" ,
             activebackground = 'white', fg = "black", command=make_predictions)
Prediction_btn.grid(column=0, row=4, rowspan=2)

#############################################################################################################

# Adding Button to Make Predictions
Update_btn = Button(root, bg = 'red', width = 25, height = 3, text = "Update Data" ,
             activebackground = 'white', fg = "black", command=update_model)
Update_btn.grid(column=1, row=4, rowspan=2)

#############################################################################################################

# Status Indicator
status = StringVar()
status = Text(root, width=30, height = 4)
status.grid(column = 2, row=4, rowspan=2)

#############################################################################################################

# Playoff Status Indicator
bPO = IntVar()
check = Checkbutton(root, text = "Check if Playoff Game", variable = bPO, \
                 onvalue = 1, offvalue = 0, height=1, \
                 width = 20)
check.grid(column = 2, row=1)

#############################################################################################################

# Adding a Label for Model Retraining
reset_label = Label(root, text = "Years for Retraining")
reset_label.grid(column = 0, row = 6, pady=50)

# Adding a Text Entry Box for 
reset_years1 = StringVar()
reset_years1 = Entry(root, width=14, textvariable=reset_years1)
reset_years1.grid(column = 1, row = 6, sticky='W', pady=50)

reset_years2 = StringVar()
reset_years2 = Entry(root, width=14, textvariable=reset_years2)
reset_years2.grid(column = 1, row = 6, sticky='E', pady=50)

reset_btn = Button(root, bg = 'red', width = 20, text = "Retrain Model" ,
             activebackground = 'white', fg = "black", command=reset_model)
reset_btn.grid(column=2, row=6, pady=50)

root.mainloop()