import customtkinter
from tkinter import *
from tkinter import messagebox
import predictionDatabase
import numpy as np 
import joblib



class EntryBox():
  

    def __init__(self, placeText, x, y):
        program = SalaryNow()
        self.entryBox = customtkinter.CTkEntry(app, font=program.style["fontLow"], text_color=program.style["white"], fg_color=program.style["blackLight"], border_color=program.style["greyDark"], border_width=2 , width=135, height=50, placeholder_text=placeText, placeholder_text_color=program.style["greyLight"])
        self.entryBox.place(x=x, y=y)
    
    def checkLimit(self, entryBox, max, min, name):
        if not ((min <= int(entryBox)) and (int(entryBox) <= max)):
            msg = ('Select ' + name + ' between ' + str(min) + ' - ' + str(max) + '.')
            messagebox.showerror('Error', msg)

        return int(entryBox)
    
    def isEmpty(self, entryBox, name, max, min):
            if not entryBox:
                messagebox.showerror('Error', name + ' box is empty.')

            return SalaryNow().checkLimit(entryBox, min, max, name)


class ComboBox():


    def createCombo(self):
        program = SalaryNow()
        comboBox = customtkinter.CTkComboBox(app, font=program.style["fontLow"], text_color=program.style["white"], fg_color=program.style["blackLight"], dropdown_hover_color=program.style["purpleDark"], button_color=program.style["purpleDark"], border_color=program.style["greyDark"], border_width=2 , width=300, height=50, variable=varDepart, values=self.departments, state='readonly')
        comboBox.place(x=50, y=160)
        varDepart.set('   Department')

    def getOption(self, comboBox):
        for option in range(len(SalaryNow().departments)):
            if SalaryNow().departments[option] == comboBox:
                return option

    def isDefault(self, comboBox):
        if comboBox == '   Department':
            messagebox.showerror('Error', 'Select one of the Department options')
            return None 

        return SalaryNow().getOption(comboBox)



class Button():

    def createButton(self, text, width, command, x, fgColor):
        program = SalaryNow()
        button = customtkinter.CTkButton(app, text=text, font=program.style["fontUp"], text_color=program.style["white"], fg_color=fgColor, height=50 , width=width, hover_color=program.style["grey"], command=command)
        button.place(x=x, y=320)


class RadioButton():

    def createRadio(self, text, y, value):
        program = SalaryNow()
        radioButton = customtkinter.CTkRadioButton(app, text=text, fg_color=program.style["purpleDark"], hover_color=program.style["purpleDark"], font=program.style["fontLow"], variable=varGen, value=value, text_color=program.style["white"])
        radioButton.place(x=230, y=y)


class SalaryNow(EntryBox, ComboBox, Button, RadioButton):


    def __init__(self):

        self.style = {
        
            "fontUp" : ('FS Albert Arabic', 16, 'bold'),
            "fontLow" : ('FS Albert Arabic', 14),
            "fontTitle" : ('Joscelynn Demo', 34),
            "purpleDark" : '#7132c1',
            "white" : '#fff',
            "black" : '#1d1e1e',
            "grey" :  '#3c3d43',
            "purpleLight" : '#9820ca',
            "greyDark" : '#2e3346',
            "greyLight" : '#5c5c5c',
            "blackLight" : '#1b1d28'

        }

        self.titleSalary = customtkinter.CTkLabel(app, font=self.style["fontTitle"], text='Salary', text_color=self.style["white"])
        self.titleSalary.place(x=124, y=25)

        self.titleNow = customtkinter.CTkLabel(app, font=self.style["fontTitle"], text='Now', text_color=self.style["purpleLight"])
        self.titleNow.place(x=221, y=25)

        self.departments = ['   Engineering', '   Finance', '   Media', '   Operations', '   Other', '   Product', '   Sales', '   Tech']


    def combine(self):
        testData = [[]]

        genderIn = varGen.get()
        ageIn = program.isEmpty(age.get(), 'Age', 18, 60)
        departmentIn = program.isDefault(varDepart.get())
        experienceIn = program.isEmpty(experience.get(), 'Experience (years)', 0, 42)
        tenureIn = program.isEmpty(tenure.get(), 'Tenure (months)', 0, 504)

        testData[0].append(genderIn)
        testData[0].append(ageIn)
        testData[0].append(departmentIn)
        testData[0].append(experienceIn)
        testData[0].append(tenureIn)

        return testData, ageIn, genderIn, departmentIn, experienceIn, tenureIn

    def predict(self, testData):
        model = joblib.load('../predictor/salary_predictor.pkl')
        gross = model.predict(testData).tolist() 
        gross = gross[0]
        gross = round(gross, 3)
        return gross
        
    def id(self, testData):  
            input = ''
            for num in testData[0]:
                input += str(num)
            hash = 0
            for char in input:
                hash = (hash * 71) + ord(char)
                hash = hash % (10**7)
            if predictionDatabase.id_exists(hash) == True:
                messagebox.showerror('Error', 'ID already exists.')
                messagebox.showerror('Error', 'Input different values.')
            else:
                return hash 

    def insertData(self, id, age, gender, department, experience, tenure, gross):
        predictionDatabase.append_prediction(id, age, gender, department, experience, tenure, gross) 

    def viewPredict(self, gross):
        program = SalaryNow()

        program.createButton('Generate', 300, program.main, 50, program.style["black"])

        program.createButton(("£" + str(gross)), 200, program.empty, 50, program.style["black"])
        program.createButton('Retry', 100, program.main, 250, program.style["purpleDark"])

    def empty(self):
        pass

    def main(self):
        program = SalaryNow()

        testData, ageIn, genderIn, departmentIn, experienceIn, tenureIn = program.combine()
        gross = program.predict(testData)
        id = program.id(testData)
        program.insertData(id, ageIn, genderIn, departmentIn, experienceIn, tenureIn, gross) 
        program.viewPredict(gross)


    






# --- Main -------------------------------------------------------------

app = customtkinter.CTk()
app.geometry('400x420')
app.title(' ・ SalaryNow')
app.config(bg = '#222533')
app.resizable(False, False)

program = SalaryNow()
program.titleSalary
program.titleNow

varGen = IntVar()
varDepart = StringVar()

age = EntryBox("   Age", 50, 80)
age = age.entryBox

experience = EntryBox("   Experience", 215, 80)   
experience = experience.entryBox

tenure = EntryBox(" Tenure (months)", 50, 240) 
tenure = tenure.entryBox
              
department = program.createCombo()

male = program.createRadio('Male', 240, 0)
female = program.createRadio('Female', 270, 1)

generate = program.createButton('Generate', 300, program.main, 50, program.style["purpleDark"])

app.mainloop()







