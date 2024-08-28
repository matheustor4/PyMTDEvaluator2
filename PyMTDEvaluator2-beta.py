import skcriteria
from skcriteria.agg import simple
from skcriteria.preprocessing import invert_objectives, scalers
from skcriteria.agg import similarity 
from skcriteria.pipeline import mkpipe 
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import random
import math
import simpy                            
import numpy as np
import scipy.stats
from decimal import *
import time
from tkinter import *
from tkinter import DISABLED
from tkinter import ttk
from tkinter import scrolledtext
from matplotlib.font_manager import FontProperties
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from tqdm.tk import tqdm
from tktooltip import ToolTip
import sys
import customtkinter as ctk
import tkinter as tk
from customtkinter import filedialog
import xml.etree.ElementTree as ET
ctk.set_appearance_mode("dark") 
# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("green")   


class Scenario():
    
    def __init__(self, trigger, availability, cost, capacity, pas, ttas):
        self.trigger = trigger
        self.availability = availability
        self.cost = cost
        self.capacity = capacity
        self.pas = pas
        self.ttasScn = ttas
    
    def printScenario(self):
        print("Scenario results")
        print("Trigger " + str(self.trigger))
        print("Time for attack success " + self.ttasScn)
        print("Availability " + str(self.availability))
        print("Cost " + str(self.cost))
        print("Capacity " + str(self.capacity))
        print("Probability of Attack Success " + str(self.pas))
    


class Mcdm():
    
    def __init__(self, availWeight, costWeight, capacityWeight, secWeight):
        self.availWeight = availWeight
        self.costWeight = costWeight
        self.capacityWeight = capacityWeight
        self.secWeight = secWeight
        self.scenarios = []
        self.data = []
        self.labels = []
        self.aux = []
        self.finalResult = ""
        self.errorStringMCDMInclusion = ""
        self.internalFlagMCDM = False;

    def checkMCDMFlag(self):
        
        if self.availWeight == 0 and self.costWeight == 0 and self.capacityWeight == 0 and self.secWeight== 0 :
            self.internalFlagMCDM = False
        else:
            self.internalFlagMCDM = True





    def prepareData(self):
        
        for i in range(len(self.scenarios)):
            scenarioLabel = "Tgr " + str(self.scenarios[i].trigger) + " Ttas " + str(self.scenarios[i].ttasScn)
            self.labels.append(scenarioLabel)
            self.aux.append(self.scenarios[i].availability)
            self.aux.append(self.scenarios[i].cost)
            self.aux.append(self.scenarios[i].capacity)
            self.aux.append(self.scenarios[i].pas)
            self.data.append(self.aux)
            self.aux = []



    def includeScenario(self, scenario):
        #print("This is the scenario");
        #scenario.printScenario();
        if(scenario.cost > 0 and scenario.availability > 0 and scenario.capacity > 0 and scenario.pas > 0):
            self.scenarios.append(scenario)
        else:
            self.errorStringMCDMInclusion = self.errorStringMCDMInclusion + "\n MCDM Engine ---- The following scenario was excluded from MCDM (Value=0) \n Trigger =  " 
            self.errorStringMCDMInclusion = self.errorStringMCDMInclusion + str(scenario.trigger) + " Time For attack success " +  str(scenario.ttasScn) + "\n"       
        #print(self.scenarios)
        
    def runMcdm(self):
        
        self.checkMCDMFlag();
        
        if self.internalFlagMCDM:
            self.finalResult = ""
            self.prepareData()
        
            objectives = [max, min, max, min]
        
            print("Avail " + str(self.availWeight) + " Cost " + str(self.costWeight) + " cap " + str(self.capacityWeight) + ' sec ' + str(self.secWeight)) 
        
            if (len(self.scenarios)> 1) :
                dm1 = skcriteria.mkdm(self.data, objectives,
                              alternatives=self.labels,
                              weights=[self.availWeight, self.costWeight, self.capacityWeight, self.secWeight],
                              criteria=["Availability", "Cost", "Capacity", "Prob. of attk. success"])
        
            #print(dm1)
      
                inverter = invert_objectives.InvertMinimize()

                dmt = inverter.transform(dm1)
                print("Original results")
                self.finalResult=self.finalResult + "Original results \n"
                print(dmt)
                self.finalResult=self.finalResult + str(dmt) + "\n"
                scaler = scalers.SumScaler(target="both")
                dmt = scaler.transform(dmt)
        
                print("Transformed results")
                self.finalResult=self.finalResult + "Transformed results \n"
      
                print(dmt)
                self.finalResult=self.finalResult + str(dmt) + "\n"
        
                dec = simple.WeightedSumModel()
        
                rank = dec.evaluate(dmt)
        
                print("------------------")
                self.finalResult=self.finalResult + "------------------\n"

        
                print("Results Weighted Sum Model")
                self.finalResult=self.finalResult + "Results Weighted Sum Model \n"
        
        
                print(rank)
                self.finalResult=self.finalResult + str(rank)+ "\n"
        
                print("-----------------")
                self.finalResult=self.finalResult + "------------------\n"
        
                pipe = mkpipe(
                    invert_objectives.NegateMinimize(),
                    scalers.VectorScaler(target="matrix"), # this scaler transform the matrix
                    scalers.SumScaler(target="weights"), # and this transform the weights
                    similarity.TOPSIS(),)
        
                rank = pipe.evaluate(dmt)
                print("Results TOPSIS")
                self.finalResult=self.finalResult + "Results TOPSIS \n"
        
                print(rank)
                self.finalResult=self.finalResult + str(rank) + "\n"
       
                print(rank.e_)
                self.finalResult=self.finalResult + str(rank.e_) + "\n"
        
                print("Ideal:", rank.e_.ideal)
                self.finalResult=self.finalResult + "Ideal:" + str(rank.e_.ideal) + "\n"
        
                print("Anti-Ideal:", rank.e_.anti_ideal)
                self.finalResult=self.finalResult + "Anti-Ideal:" + str(rank.e_.anti_ideal) + "\n"
               
                print("Similarity index:", rank.e_.similarity)
                self.finalResult=self.finalResult + "Similarity index:" + str(rank.e_.similarity) + "\n"
            
            else:
                if(len(self.scenarios)>0):
                    print("MCDM Engine ---- ERROR: only one scenario left in MCDM after data validation")
                    self.finalResult=self.finalResult + "\n MCDM Engine ---- ERROR: only one scenario left in MCDM after data validation  \n"
                    self.finalResult=self.finalResult + "Trigger " + str(self.scenarios[0].trigger) + " Availability " + str(self.scenarios[0].availability) + " Cost " + str(self.scenarios[0].cost)
                    self.finalResult=self.finalResult + " Capacity " + str(self.scenarios[0].capacity) + " Probability of Attack Success " + str(self.scenarios[0].pas) + " \n" 
                else:
                    print("MCDM Engine ---- ERROR: No scenarios left after data validation")
                    self.finalResult=self.finalResult + "\n MCDM Engine ---- ERROR: No scenarios left after data validation \n ----------- \n"

        else:
            print("Evaluation without MCDM")
            self.finalResult=self.finalResult + "\n Evaluation without MCDM \n ----------- \n"
        

    def getResults(self):
        finalStringResult = self.errorStringMCDMInclusion + self.finalResult
        self.errorStringMCDMInclusion = ""
        return finalStringResult
        
       

class PdfReport():
    
    def __init__(self, summary, countEval):
        self.summary = summary
        self.countEval = countEval
        
        
        
    def generate(self):
        
        stringFileName = "PyMTDEvaluatorReport-" + str(self.countEval) +".pdf"
        
        doc = SimpleDocTemplate(stringFileName,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
        Story=[]
        formatted_time = time.ctime()
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
 
        ptext = '<font size="12">PyMTDEvaluator Report</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
    
        ptext = '<font size="12">%s</font>' % formatted_time
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        aux = self.summary
        results = aux.replace("\n", "<br/>")
        
        ptext = '<font size="12">' + results + '</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
        ptext = '<font size="12">Probability of attack success</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        im = Image('atksucprob.png', 5.4*inch, 4*inch)
        Story.append(im)
        
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
        ptext = '<font size="12">Availability</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        im = Image('availabilityFull.png', 5.4*inch, 4*inch)
        Story.append(im)
        
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
        ptext = '<font size="12">Accumulated cost</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        im = Image('cost.png', 5.4*inch, 4*inch)
        Story.append(im)
        
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
        
        ptext = '<font size="12">Capacity</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        im = Image('capacityFull.png', 5.4*inch, 4*inch)
        Story.append(im)
        
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
         
        ptext = '<font size="12">Availability (example run)</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        im = Image('availability.png', 5.4*inch, 4*inch)
        Story.append(im)
        
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
        ptext = '<font size="12">Capacity (example run)</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        im = Image('capacity.png', 5.4*inch, 4*inch)
        Story.append(im)
        
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
        doc.build(Story)
        

class UserInterface():


    def __init__(self):
        self.fields = ('Downtime per movement (min)', 'Cost per movement ($)', 'Movement Trigger (h)', 'Time for attack success (h)', 'Evaluation Time (h)')
        self.fields2 = ('Movement Trigger (h) - MIN', 'Movement Trigger (h) - MAX', 'Movement Trigger (h) - Step')
        self.fields3 = ('Time for attack success (h) - MIN', 'Time for attack success (h) - MAX', 'Time for attack success (h) - Step')
        self.fields4 = ('Availability (%)', 'Probability of attack success (%)', 'Capacity (%)', 'Cost (%)')
        self.flag = True;
        self.flag2 = True;
        self.flagMCDM = False;
        self.resultsSingleGlobalTime = []
        self.resultsSingleAvailability = []
        self.resultsSingleAtkProb = []
        self.resultsSingleCapacity = []
        self.resultsAtkprob = []
        self.resultsCost = []
        self.resultsCapacity = []
        self.resultsAvailability = []
        self.cubeAvailability = []
        self.cubeCapacity = []
        self.cubeSingleCapacity = []
        self.cubeSingleAvailability = []
        self.cubeSingleAtkProb = []
        self.cubeSingleGlobalTime = []
        self.cubeAtkProb = []
        self.cubeCost=[]
        self.headers = []
        self.headersAtk = []
        self.counter = 0
        self.counter2 = 0
        self.finalSummary="PyMTDEvaluator - Summary of Results \n +++++++++++++++++++++++++++ \n Scenario 0 \n \n ";
        self.markers = ['o', 'v', '1', '8', 'P', '*', 'D', '|', 4, '$a$', '.', '^', '2', 's', 'X', 'd', '+', '_', 5, '$b$', ',', '>', '3', 'p', 'x', 0, 6, '$c$', '<', '4', 'h', 2, 7, '$d$', 'H', '$e$','$f$', '$r$', '$u$', '$m$', 1, 3, 8, 9, 10, 11, 'o', 'v', '1', '8', 'P', '*', 'D', '|', 4, '$a$', '.', '^', '2', 's', 'X', 'd', '+', '_', 5, '$b$', ',', '>', '3', 'p', 'x', 0, 6, '$c$', '<', '4', 'h', 2, 7, '$d$', 'H', '$e$','$f$', '$r$', '$u$', '$m$']
        self.linestyle = ['solid', 'dashed', 'dotted']
        self.colors = ['black', 'blue', 'gray',  'red', 'yellow', 'green', 'orange', 'purple', 'pink', 'brown']
        self.countEval = 0;
        self.pdfFlag = False;
        self.mcdm = Mcdm(0,0,0,0)
        self.interfaceSelectionMain = 0;

        

    def makeform(self, root, fields):
        entries = {}
        for field in self.fields:
            row = Frame(root)
            lab = Label(row, width=27, text=field+": ", anchor='w', font=("Helvetica", 12))
            ent = Entry(row, font=("Helvetica", 12))
            ent.insert(0, "0")
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries[field] = ent
        
        

        return entries


    def makeformExp(self, root, fields):
        entries = {}
        for field in fields:
            row = Frame(root)
            lab = Label(row, width=27, text=field+": ", anchor='w', font=("Helvetica", 12))
            ent = Entry(row, font=("Helvetica", 12))
            ent.insert(0, "0")
            ent.config(state=DISABLED)
            row.pack(side=TOP, fill=X, padx=6, pady=6)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries[field] = ent
        return entries

    def finalPlot(self):
        
        if self.countEval > 0:
            plt.close("all")
        
        
        fig, ax = plt.subplots(tight_layout=True)
        fPlot = plt.figure(1)
        plt.xlabel('Time (h)', fontsize=18)
        plt.ylabel('Probability of attack success', fontsize=16)
        
        self.cubeAvailability.append(self.resultsAvailability)
        self.cubeSingleCapacity.append(self.resultsSingleCapacity)
        self.cubeAtkProb.append(self.resultsAtkprob);
        self.cubeCost.append(self.resultsCost)
        self.cubeSingleAtkProb.append(self.resultsSingleAtkProb)
        self.cubeSingleAvailability.append(self.resultsSingleAvailability)
        self.cubeSingleGlobalTime.append(self.resultsSingleGlobalTime)
        self.cubeCapacity.append(self.resultsCapacity)
        
        self.counter = 0;
        self.counter2 = 0
        
        for i in range(0, len(self.cubeAtkProb)):
            for j in range(0, len(self.cubeAtkProb[i])):
                strPlot = "Scn " + str(i) + "- MovTrigger - " + str(self.headers[self.counter]) + " h - TimeAtkSuc " +  str(self.headersAtk[self.counter]) + " h"
                plt.plot(self.cubeAtkProb[i][j], marker=self.markers[j], label=strPlot.format(j=j), 
                         linestyle=self.linestyle[self.counter2]);
                self.counter = self.counter + 1
                self.counter2 = self.counter2 + 1
                if(self.counter2 > 2):
                    self.counter2 = 0;
        fontP = FontProperties()
        fontP.set_size('small')
        
        plt.legend(loc='upper center', bbox_to_anchor=(0.55, -0.17), ncol=2, fancybox=True, shadow=True, prop=fontP)
        if(self.pdfFlag):
            stringPDFFile = 'atksucprob-' + str(self.countEval) + '.pdf'  
            plt.savefig('atksucprob.png', dpi=100, bbox_inches="tight", pad_inches=0)
            plt.savefig(stringPDFFile, bbox_inches="tight", pad_inches=0)
        
        self.counter = 0
        self.counter2 = 0
        
        fig, ax = plt.subplots(tight_layout=True)
        costPlot = plt.figure(2)
        plt.xlabel('Time (h)', fontsize=18)
        plt.ylabel('Accumulated cost ($)', fontsize=16)
        
        for i in range(0, len(self.cubeCost)):
            for j in range(0, len(self.cubeCost[i])):
                strPlot = "Scn " + str(i) + "- MovTrigger - " + str(self.headers[self.counter]) + " h - TimeAtkSuc " +  str(self.headersAtk[self.counter]) +" h"
                plt.plot(self.cubeCost[i][j], marker=self.markers[j], label=strPlot.format(j=j),
                         linestyle=self.linestyle[self.counter2]);                         
                self.counter = self.counter + 1
                self.counter2 = self.counter2 + 1
                if(self.counter2 > 2):
                    self.counter2 = 0
            
        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(loc='upper center', bbox_to_anchor=(0.55, -0.17), ncol=2, fancybox=True, shadow=True, prop=fontP)
        if(self.pdfFlag):
            stringPDFFile = 'cost-' + str(self.countEval) + '.pdf'  
            plt.savefig('cost.png', dpi=100, bbox_inches="tight", pad_inches=0)
            plt.savefig(stringPDFFile, bbox_inches="tight", pad_inches=0)
        
        self.counter = 0;
        self.counter2 = 0;
        
        fig, ax = plt.subplots(tight_layout=True)
        availPlot = plt.figure(3)
        plt.xlabel('Time (h)', fontsize=18)
        plt.ylabel('Availability (example run)', fontsize=16)
        
        for i in range(0, len(self.cubeSingleAvailability)):
            for j in range(0, len(self.cubeSingleAvailability[i])):
                strPlot = "Scn " + str(i) + "- MovTrigger - " + str(self.headers[self.counter]) + " h - TimeAtkSuc " +  str(self.headersAtk[self.counter]) +" h"
                plt.plot(self.cubeSingleGlobalTime[i][j], self.cubeSingleAvailability[i][j], marker=self.markers[j], label=strPlot.format(j=j),
                         linestyle=self.linestyle[self.counter2]);
                
                self.counter = self.counter + 1
                self.counter2 = self.counter2 + 1
                if(self.counter2 > 2):
                    self.counter2 = 0
        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(loc='upper center', bbox_to_anchor=(0.55, -0.17), ncol=2, fancybox=True, shadow=True, prop=fontP)
        if(self.pdfFlag):
            stringPDFFile = 'availability-' + str(self.countEval) + '.pdf'  
            plt.savefig('availability.png', dpi=100, bbox_inches="tight", pad_inches=0)
            plt.savefig(stringPDFFile, bbox_inches="tight", pad_inches=0)
        
        self.counter = 0;
        self.counter2 = 0
        
        
        fig, ax = plt.subplots(tight_layout=True)
        capacityPlot = plt.figure(4)
        plt.xlabel('Time (h)', fontsize=18)
        plt.ylabel('System Capacity (%) (example run)', fontsize=16)
        
        
        for i in range(0, len(self.cubeSingleCapacity)):
            for j in range(0, len(self.cubeSingleCapacity[i])):
                strPlot = "Scn " + str(i) + "- MovTrigger - " + str(self.headers[self.counter]) + " h - TimeAtkSuc " +  str(self.headersAtk[self.counter]) +" h"
                plt.plot(self.cubeSingleGlobalTime[i][j], self.cubeSingleCapacity[i][j], marker=self.markers[j], label=strPlot.format(j=j),
                         linestyle=self.linestyle[self.counter2]);                         
                self.counter = self.counter + 1
                self.counter2 = self.counter2 + 1
                if(self.counter2 > 2):
                    self.counter2 = 0
        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(loc='upper center', bbox_to_anchor=(0.55, -0.17), ncol=2, fancybox=True, shadow=True, prop=fontP)
        
        if(self.pdfFlag):
            stringPDFFile = 'capacity-' + str(self.countEval) + '.pdf'  
            plt.savefig('capacity.png', dpi=100, bbox_inches="tight", pad_inches=0)
            plt.savefig(stringPDFFile, bbox_inches="tight", pad_inches=0)
        

        self.counter = 0;
        self.counter2 = 0;
        
        fig, ax = plt.subplots(tight_layout=True)
        capacityfullPlot = plt.figure(5)
        plt.xlabel('Time (h)', fontsize=18)
        plt.ylabel('System Capacity (%)', fontsize=16)
        
        
        for i in range(0, len(self.cubeCapacity)):
            for j in range(0, len(self.cubeCapacity[i])):
                strPlot = "Scn " + str(i) + "- MovTrigger - " + str(self.headers[self.counter]) + " h - TimeAtkSuc " +  str(self.headersAtk[self.counter]) +" h"
                plt.plot(self.cubeCapacity[i][j], marker=self.markers[j], label=strPlot.format(j=j),
                         linestyle=self.linestyle[self.counter2]);                         
                self.counter = self.counter + 1
                self.counter2 = self.counter2 + 1
                if(self.counter2 > 2):
                    self.counter2 = 0
        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(loc='upper center', bbox_to_anchor=(0.55, -0.17), ncol=2, fancybox=True, shadow=True, prop=fontP)
        
        if(self.pdfFlag):
            stringPDFFile = 'capacityFull-' + str(self.countEval) + '.pdf'  
            plt.savefig('capacityFull.png', dpi=100, bbox_inches="tight", pad_inches=0)
            plt.savefig(stringPDFFile, bbox_inches="tight", pad_inches=0)
        
        
        self.counter = 0;
        self.counter2 = 0;
        
        fig, ax = plt.subplots(tight_layout=True)
        availabilityFullPlot = plt.figure(6)
        plt.xlabel('Time (h)', fontsize=18)
        plt.ylabel('Availability', fontsize=16)
        
        
        for i in range(0, len(self.cubeAvailability)):
            for j in range(0, len(self.cubeAvailability[i])):
                strPlot = "Scn " + str(i) + "- MovTrigger - " + str(self.headers[self.counter]) + " h - TimeAtkSuc " +  str(self.headersAtk[self.counter]) +" h"
                plt.plot(self.cubeAvailability[i][j], marker=self.markers[j], label=strPlot.format(j=j),
                         linestyle=self.linestyle[self.counter2]);                         
                self.counter = self.counter + 1
                self.counter2 = self.counter2 + 1

                if(self.counter2 > 2):
                    self.counter2 = 0
            
        
        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(loc='upper center', bbox_to_anchor=(0.55, -0.17), ncol=2, fancybox=True, shadow=True, prop=fontP)
        
        if(self.pdfFlag):
            stringPDFFile = 'availabilityFull-' + str(self.countEval) + '.pdf'  
            plt.savefig('availabilityFull.png', dpi=100, bbox_inches="tight", pad_inches=0)
            plt.savefig(stringPDFFile, bbox_inches="tight", pad_inches=0)
        
      
        plt.show(block=False)
        

        self.counter = 0;
        self.counter2 = 0;
        
        self.resultsSingleGlobalTime = [];
        self.resultsSingleAvailability = [];
        self.resultsSingleAtkProb = [];
        self.resultsCost = [];
        self.resultsAtkprob = [];
        self.resultsSingleCapacity = [];
        self.resultsCapacity = [];
        self.resultsAvailability = [];
        
        if (self.pdfFlag):
            pdfGen = PdfReport(self.finalSummary, self.countEval)
            pdfGen.generate();
        
    def resultsSummary(self):
        window = Tk()
        window.title("PyMTDEvaluator - Summary of Results")
        
        txt = scrolledtext.ScrolledText(window,width=105,height=50,font=("Helvetica", 12))
        txt.grid(column=0,row=0)
        txt.insert(INSERT, self.finalSummary)
         
         
        self.countEval = self.countEval + 1
        
        self.finalSummary = self.finalSummary + "\n Scenario " + str(self.countEval) + "\n \n";
        window.update()

        
    def notifyProgressBar(self, _progress):
        print(_progress);
        

    def runEvaluation(self, entries, entriesExp, entriesExp2, entriesMCDM):
        
        
        downtimePerMov = float(entries['Downtime per movement (min)'].get())/60
        costPerMovement = float(entries['Cost per movement ($)'].get())
        evalTime = int(entries['Evaluation Time (h)'].get())
        
        if(self.flagMCDM):
            availWeight = float(entriesMCDM['Availability (%)'].get())/100
            pasWeight = float(entriesMCDM['Probability of attack success (%)'].get())/100
            capacityWeight = float(entriesMCDM['Capacity (%)'].get())/100
            costWeight = float(entriesMCDM['Cost (%)'].get())/100

            if(self.flag2):
                if(self.flag):
                    self.mcdm = Mcdm(0,0,0,0)
                    print("MCDM false")
                    print("Single evaluation - No scenarios for comparison")
                else:
                    self.mcdm = Mcdm(availWeight, costWeight, capacityWeight, pasWeight)
                    print("MCDM true")
            else:
                self.mcdm = Mcdm(availWeight, costWeight, capacityWeight, pasWeight)
                print("MCDM true")

        else:
            self.mcdm = Mcdm(0,0,0,0)
            print("MCDM false")
        
        if(self.flag2):
            if(self.flag):
                print("Single evaluation")
                timeForAtkSucPhase = float(entries['Time for attack success (h)'].get())
                mtdSched = float(entries['Movement Trigger (h)'].get())
                mtdSolver = TransientEvaluator(downtimePerMov, costPerMovement, mtdSched, timeForAtkSucPhase, evalTime, self.countEval)
                mtdSolver.run(1,1)
                self.resultsAvailability.append(mtdSolver.getAvailability())
                self.resultsCapacity.append(mtdSolver.getCapacity())
                self.resultsSingleCapacity.append(mtdSolver.getSingleCapacity())
                self.resultsSingleAtkProb.append(mtdSolver.getSingleAtkProg())
                self.resultsSingleAvailability.append(mtdSolver.getSingleAvailability())
                self.resultsSingleGlobalTime.append(mtdSolver.getSingleGlobalTime())
                self.resultsAtkprob.append(mtdSolver.getAtkProb())
                self.resultsCost.append(mtdSolver.getCost())
                self.headers.append(mtdSched)
                self.headersAtk.append(timeForAtkSucPhase)
                self.mcdm.includeScenario(mtdSolver.getScenario())
                self.finalSummary = self.finalSummary + mtdSolver.getSummary();
                   
            else:
                timeForAtkSucPhase = float(entries['Time for attack success (h)'].get())
                mtdSchedMin = float(entriesExp['Movement Trigger (h) - MIN'].get())
                mtdSchedMax = float(entriesExp['Movement Trigger (h) - MAX'].get())
                mtdSchedStep = float(entriesExp['Movement Trigger (h) - Step'].get())
                print("Experiment only MovTrigger")
                
                totalEvaluationsNeeded = int(round((mtdSchedMax-mtdSchedMin)/mtdSchedStep,0)) + 1
                iterationPbar = 1; 

                control = mtdSchedMin
                while (control <= mtdSchedMax):
                    mtdSolver = TransientEvaluator(downtimePerMov, costPerMovement, control, timeForAtkSucPhase, evalTime, self.countEval)
                    mtdSolver.run(iterationPbar,totalEvaluationsNeeded)
                    iterationPbar+=1;
                    self.resultsAvailability.append(mtdSolver.getAvailability())
                    self.resultsCapacity.append(mtdSolver.getCapacity())
                    self.resultsSingleCapacity.append(mtdSolver.getSingleCapacity())
                    self.resultsSingleAtkProb.append(mtdSolver.getSingleAtkProg())
                    self.resultsSingleAvailability.append(mtdSolver.getSingleAvailability())
                    self.resultsSingleGlobalTime.append(mtdSolver.getSingleGlobalTime())
                    self.resultsAtkprob.append(mtdSolver.getAtkProb())
                    self.resultsCost.append(mtdSolver.getCost())
                    self.headers.append(control)
                    self.headersAtk.append(timeForAtkSucPhase)
                    control = control + mtdSchedStep
                    self.mcdm.includeScenario(mtdSolver.getScenario())
                    self.finalSummary = self.finalSummary + mtdSolver.getSummary();
        else:
            if(self.flag):
                mtdSched = float(entries['Movement Trigger (h)'].get())
                atkDelayMin = float(entriesExp2['Time for attack success (h) - MIN'].get())
                atkDelayMax = float(entriesExp2['Time for attack success (h) - MAX'].get())
                atkDelayStep = float(entriesExp2['Time for attack success (h) - Step'].get())
                print("Experiment only Atk Suc Prob")

                totalEvaluationsNeeded = int(round((atkDelayMax-atkDelayMin)/atkDelayStep,0)) + 1
                iterationPbar = 1; 

                control = atkDelayMin
                while (control <= atkDelayMax):
                    mtdSolver = TransientEvaluator(downtimePerMov, costPerMovement, mtdSched, control, evalTime, self.countEval)
                    mtdSolver.run(iterationPbar,totalEvaluationsNeeded)
                    iterationPbar+=1;
                    self.resultsAvailability.append(mtdSolver.getAvailability())
                    self.resultsCapacity.append(mtdSolver.getCapacity())
                    self.resultsSingleCapacity.append(mtdSolver.getSingleCapacity())
                    self.resultsSingleAtkProb.append(mtdSolver.getSingleAtkProg())
                    self.resultsSingleAvailability.append(mtdSolver.getSingleAvailability())
                    self.resultsSingleGlobalTime.append(mtdSolver.getSingleGlobalTime())
                    self.resultsAtkprob.append(mtdSolver.getAtkProb())
                    self.resultsCost.append(mtdSolver.getCost())
                    self.headers.append(mtdSched)
                    self.headersAtk.append(control)
                    control = control + atkDelayStep
                    self.mcdm.includeScenario(mtdSolver.getScenario())
                    self.finalSummary = self.finalSummary + mtdSolver.getSummary();
                
            else:
                atkDelayMin = float(entriesExp2['Time for attack success (h) - MIN'].get())
                atkDelayMax = float(entriesExp2['Time for attack success (h) - MAX'].get())
                atkDelayStep = float(entriesExp2['Time for attack success (h) - Step'].get())
                mtdSchedMin = float(entriesExp['Movement Trigger (h) - MIN'].get())
                mtdSchedMax = float(entriesExp['Movement Trigger (h) - MAX'].get())
                mtdSchedStep = float(entriesExp['Movement Trigger (h) - Step'].get())
                print("Experiment AtkSucProb + MovTrigger")

                totalEvaluationsNeeded = (int(round((atkDelayMax-atkDelayMin)/atkDelayStep,0)) + 1) * (int(round((mtdSchedMax-mtdSchedMin)/mtdSchedStep,0)) + 1)
                iterationPbar = 1; 


                control = atkDelayMin
                while (control <= atkDelayMax):
                    control2 = mtdSchedMin
                    while (control2 <= mtdSchedMax):
                        mtdSolver = TransientEvaluator(downtimePerMov, costPerMovement, control2, control, evalTime, self.countEval)
                        mtdSolver.run(iterationPbar,totalEvaluationsNeeded)
                        iterationPbar+=1;
                        self.resultsAvailability.append(mtdSolver.getAvailability())
                        self.resultsCapacity.append(mtdSolver.getCapacity())
                        self.resultsSingleCapacity.append(mtdSolver.getSingleCapacity())
                        self.resultsSingleAtkProb.append(mtdSolver.getSingleAtkProg())
                        self.resultsSingleAvailability.append(mtdSolver.getSingleAvailability())
                        self.resultsSingleGlobalTime.append(mtdSolver.getSingleGlobalTime())
                        self.resultsAtkprob.append(mtdSolver.getAtkProb())
                        self.resultsCost.append(mtdSolver.getCost())
                        self.headers.append(control2)
                        self.headersAtk.append(control)
                        control2 = control2 + mtdSchedStep
                        self.mcdm.includeScenario(mtdSolver.getScenario())
                        self.finalSummary = self.finalSummary + mtdSolver.getSummary();
                    control = control + atkDelayStep
                    
                
        
        self.mcdm.runMcdm();
        self.finalSummary = self.finalSummary + '\n' + self.mcdm.getResults() + '\n'
        self.resultsSummary();
        self.finalPlot();
        
    def showModern(self):


        def on_closing():
            self.rootModern.destroy()
            self.rootModern.quit()


        self.rootModern = ctk.CTk();
        self.rootModern.protocol("WM_DELETE_WINDOW", on_closing)

        self.rootModern.title("PyMTDEvaluator 2.0 (beta) - Modern")


        self.downtimeLabel = ctk.CTkLabel(self.rootModern, text="Downtime per movement (min)")
        self.downtimeLabel.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.downtimeToolTip = ToolTip(self.downtimeLabel, msg="Minutes of system downtime due to each MTD movement.")
        
        self.downtimeVar = tk.StringVar(value="0")
        self.downtimeEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", textvariable=self.downtimeVar)
        self.downtimeEntry.grid(row=0, column=1, columnspan=4, padx=20, pady=10, sticky="ew")

        self.costLabel = ctk.CTkLabel(self.rootModern, text="Cost per movement (S)")
        self.costLabel.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.costToolTip = ToolTip(self.costLabel, msg="Monetary cost related to each MTD movement.")

        self.costVar = tk.StringVar(value="0")
        self.costEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", textvariable=self.costVar)
        self.costEntry.grid(row=1, column=1, columnspan=4, padx=20, pady=10, sticky="ew")


        self.triggerLabel = ctk.CTkLabel(self.rootModern, text="Movement trigger (h)")
        self.triggerLabel.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.triggerToolTip = ToolTip(self.triggerLabel, msg="Time (in hours) between MTD movements.")


        self.triggerVar = tk.StringVar(value="0")
        self.triggerEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", textvariable=self.triggerVar)
        self.triggerEntry.grid(row=2, column=1, columnspan=4, padx=20, pady=10, sticky="ew")

        self.timeAtkSucLabel = ctk.CTkLabel(self.rootModern, text="Time for attack success (h)")
        self.timeAtkSucLabel.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.timeAtkSucToolTip = ToolTip(self.timeAtkSucLabel, msg="Expected time (in hours) for the attack to reach success in a system without MTD.")

        self.timeAtkSucVar = tk.StringVar(value="0")
        self.timeAtkSucEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", textvariable=self.timeAtkSucVar)
        self.timeAtkSucEntry.grid(row=3, column=1, columnspan=4, padx=20, pady=10, sticky="ew")

        self.evalTimeLabel = ctk.CTkLabel(self.rootModern, text="Evaluation time (h)")
        self.evalTimeLabel.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.evalTimeToolTip = ToolTip(self.evalTimeLabel, msg="Target time (in hours) for the simulation environment. For example, evaluation time of 24 hours will produce simulation results for the first day of the system under attack.")

        self.evalTimeVar = tk.StringVar(value="0")
        self.evalTimeEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", textvariable=self.evalTimeVar)
        self.evalTimeEntry.grid(row=4, column=1, columnspan=4, padx=20, pady=10, sticky="ew")

       
        # Movement Trigger experiment


        def toggle_sectionMovExp():
            if self.switchMovExpVar.get() == 1:
                self.MovTriggerMinEntry.configure(state=ctk.NORMAL)
                self.MovTriggerMinLabel.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
                self.MovTriggerMinEntry.grid(row=6, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.MovTriggerMaxEntry.configure(state=ctk.NORMAL)
                self.MovTriggerMaxLabel.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
                self.MovTriggerMaxEntry.grid(row=7, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.MovTriggerStepEntry.configure(state=ctk.NORMAL)
                self.MovTriggerStepLabel.grid(row=8, column=0, padx=20, pady=10, sticky="ew")
                self.MovTriggerStepEntry.grid(row=8, column=1, columnspan=4, padx=20, pady=10, sticky="ew")

                self.triggerLabel.grid_forget()
                self.triggerEntry.grid_forget()
                self.triggerEntry.configure(state=ctk.DISABLED)

                self.flag = False;
                
            else:
                self.MovTriggerMinEntry.configure(state=ctk.DISABLED)
                self.MovTriggerMinLabel.grid_forget()
                self.MovTriggerMinEntry.grid_forget()
                self.MovTriggerMaxEntry.configure(state=ctk.DISABLED)
                self.MovTriggerMaxLabel.grid_forget()
                self.MovTriggerMaxEntry.grid_forget()
                self.MovTriggerStepEntry.configure(state=ctk.DISABLED)
                self.MovTriggerStepLabel.grid_forget()
                self.MovTriggerStepEntry.grid_forget()

                self.triggerLabel.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
                self.triggerEntry.grid(row=2, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.triggerEntry.configure(state=ctk.NORMAL)

                self.flag = True;


        self.rootModern.grid_columnconfigure(0, weight=1)

        self.switchMovExpVar = ctk.IntVar(value=0)
        #self.switchMovExp =  ctk.CTkSwitch(self.rootModern, text="Movement Trigger Experiment", command=switcher(), variable=self.switchMovExpVar, onvalue=1, offvalue=0 )
        

        self.switchMovExp =  ctk.CTkSwitch(self.rootModern, text="Movement Trigger Experiment", command=toggle_sectionMovExp, 
                                           variable=self.switchMovExpVar, onvalue=1, offvalue=0 )


        self.switchMovExp.grid(row=5, column=0, columnspan=5, padx=20, pady=10, sticky="")

        self.switchMovToolTip = ToolTip(self.switchMovExp, msg="Conduct a series of evaluations varying the Movement Trigger parameter.")


        self.MovTriggerMinLabel = ctk.CTkLabel(self.rootModern, text="Movement Trigger (h) - Min")
        #self.MovTriggerMinLabel.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        self.MovTriggerMinTimeToolTip = ToolTip(self.MovTriggerMinLabel, msg="First value for Movement Trigger parameter")

        self.MovTriggerMinVar = ctk.StringVar(value="0")
        self.MovTriggerMinEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.MovTriggerMinVar)
        

        self.MovTriggerMaxLabel = ctk.CTkLabel(self.rootModern, text="Movement Trigger (h) - Max")
        self.MovTriggerMaxTimeToolTip = ToolTip(self.MovTriggerMaxLabel, msg="Last value for Movement Trigger parameter")

        self.MovTriggerMaxVar = ctk.StringVar(value="0")
        self.MovTriggerMaxEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.MovTriggerMaxVar)


        self.MovTriggerStepLabel = ctk.CTkLabel(self.rootModern, text="Movement Trigger (h) - Step")
        self.MovTriggerStepToolTip = ToolTip(self.MovTriggerStepLabel, msg="Increment for the Movement Trigger parameter")

        self.MovTriggerStepVar = ctk.StringVar(value="0")
        self.MovTriggerStepEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.MovTriggerStepVar)
        
        # Experiment time to attack success

        def toggle_sectionTtasExp():
            if self.switchTtasExpVar.get() == 1:
                self.TtasMinEntry.configure(state=ctk.NORMAL)
                self.TtasMinLabel.grid(row=10, column=0, padx=20, pady=10, sticky="ew")
                self.TtasMinEntry.grid(row=10, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.TtasMaxEntry.configure(state=ctk.NORMAL)
                self.TtasMaxLabel.grid(row=11, column=0, padx=20, pady=10, sticky="ew")
                self.TtasMaxEntry.grid(row=11, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.TtasStepEntry.configure(state=ctk.NORMAL)
                self.TtasStepLabel.grid(row=12, column=0, padx=20, pady=10, sticky="ew")
                self.TtasStepEntry.grid(row=12, column=1, columnspan=4, padx=20, pady=10, sticky="ew")

                self.timeAtkSucLabel.grid_forget()
                self.timeAtkSucEntry.grid_forget()
                self.timeAtkSucEntry.configure(state=ctk.DISABLED)

                self.flag2 = False;


                
            else:
                self.TtasMinEntry.configure(state=ctk.DISABLED)
                self.TtasMinLabel.grid_forget()
                self.TtasMinEntry.grid_forget()
                self.TtasMaxEntry.configure(state=ctk.DISABLED)
                self.TtasMaxLabel.grid_forget()
                self.TtasMaxEntry.grid_forget()
                self.TtasStepEntry.configure(state=ctk.DISABLED)
                self.TtasStepLabel.grid_forget()
                self.TtasStepEntry.grid_forget()

                self.timeAtkSucLabel.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
                self.timeAtkSucEntry.grid(row=3, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.timeAtkSucEntry.configure(state=ctk.NORMAL)

                self.flag2 = True;

        self.switchTtasExpVar = ctk.IntVar(value=0)
        self.switchTtasExp =  ctk.CTkSwitch(self.rootModern, text="Time for Attack Success Experiment", command=toggle_sectionTtasExp, 
                                           variable=self.switchTtasExpVar, onvalue=1, offvalue=0 )


        self.switchTtasExp.grid(row=9, column=0, columnspan=5, padx=20, pady=10, sticky="")

        self.switchTtasToolTip = ToolTip(self.switchTtasExp, msg="Conduct a series of evaluations varying the Time for attack success parameter.")


        self.TtasMinLabel = ctk.CTkLabel(self.rootModern, text="Time for attack success (h) - Min")
        #self.TtasMinLabel.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        self.TtasMinToolTip = ToolTip(self.TtasMinLabel, msg="First value for Time for attack success parameter")

        self.TtasMinVar = ctk.StringVar(value="0")
        self.TtasMinEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.TtasMinVar)
        

        self.TtasMaxLabel = ctk.CTkLabel(self.rootModern, text="Time for attack success (h) - Max")
        self.TtasMaxToolTip = ToolTip(self.TtasMaxLabel, msg="Last value for Time for attack success parameter")

        self.TtasMaxVar = ctk.StringVar(value="0")
        self.TtasMaxEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.TtasMaxVar)


        self.TtasStepLabel = ctk.CTkLabel(self.rootModern, text="Time for attack success (h) - Step")
        self.TtasStepToolTip = ToolTip(self.TtasStepLabel, msg="Increment for the Time for attack success parameter")

        self.TtasStepVar = ctk.StringVar(value="0")
        self.TtasStepEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.TtasStepVar)

        ### MCDM 


        def toggle_sectionMCDM():
            if self.switchMCDMVar.get() == 1:
                self.MCDMAvailabilityEntry.configure(state=ctk.NORMAL)
                self.MCDMAvailabilityLabel.grid(row=14, column=0, padx=20, pady=10, sticky="ew")
                self.MCDMAvailabilityEntry.grid(row=14, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.MCDMPASEntry.configure(state=ctk.NORMAL)
                self.MCDMPASLabel.grid(row=15, column=0, padx=20, pady=10, sticky="ew")
                self.MCDMPASEntry.grid(row=15, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.MCDMCapacityEntry.configure(state=ctk.NORMAL)
                self.MCDMCapacityLabel.grid(row=16, column=0, padx=20, pady=10, sticky="ew")
                self.MCDMCapacityEntry.grid(row=16, column=1, columnspan=4, padx=20, pady=10, sticky="ew")
                self.MCDMCostEntry.configure(state=ctk.NORMAL)
                self.MCDMCostLabel.grid(row=17, column=0, padx=20, pady=10, sticky="ew")
                self.MCDMCostEntry.grid(row=17, column=1, columnspan=4, padx=20, pady=10, sticky="ew")

                self.flagMCDM = True

               
            else:
                self.MCDMAvailabilityEntry.configure(state=ctk.DISABLED)
                self.MCDMAvailabilityLabel.grid_forget()
                self.MCDMAvailabilityEntry.grid_forget()
                self.MCDMPASEntry.configure(state=ctk.DISABLED)
                self.MCDMPASLabel.grid_forget()
                self.MCDMPASEntry.grid_forget()
                self.MCDMCapacityEntry.configure(state=ctk.DISABLED)
                self.MCDMCapacityLabel.grid_forget()
                self.MCDMCapacityEntry.grid_forget()
                self.MCDMCostEntry.configure(state=ctk.DISABLED)
                self.MCDMCostLabel.grid_forget()
                self.MCDMCostEntry.grid_forget()

                self.flagMCDM = False

        self.switchMCDMVar = ctk.IntVar(value=0)
        self.switchMCDM =  ctk.CTkSwitch(self.rootModern, text="Multi Criteria Decision Making", command=toggle_sectionMCDM, 
                                           variable=self.switchMCDMVar, onvalue=1, offvalue=0 )
        self.switchMCDM.grid(row=13, column=0, columnspan=5, padx=20, pady=10, sticky="")

        self.switchMCDMToolTip = ToolTip(self.switchMCDM, msg="Perform Multi Criteria Decision Making analysis. Below, enter the intented weight (in percentage) for each criteria. The sum of criteria weights should be equal to 100. **The method only works in evaluations with experiments**")

        self.MCDMAvailabilityLabel = ctk.CTkLabel(self.rootModern, text="Availability (%)")
        self.MCDMAvailabilityToolTip = ToolTip(self.MCDMAvailabilityLabel, msg="MCDM - Percentage weight for Availability criteria")

        self.MCDMAvailabilityVar = ctk.StringVar(value="0")
        self.MCDMAvailabilityEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.MCDMAvailabilityVar)

        self.MCDMPASLabel = ctk.CTkLabel(self.rootModern, text="Probability of Attack Success (%)")
        self.MCDMPASToolTip = ToolTip(self.MCDMPASLabel, msg="MCDM - Percentage weight for Probability of Attack Success criteria")

        self.MCDMPASVar = ctk.StringVar(value="0")
        self.MCDMPASEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.MCDMPASVar)

        self.MCDMCapacityLabel = ctk.CTkLabel(self.rootModern, text="Capacity (%)")
        self.MCDMCapacityToolTip = ToolTip(self.MCDMCapacityLabel, msg="MCDM - Percentage weight for Capacity criteria")

        self.MCDMCapacityVar = ctk.StringVar(value="0")
        self.MCDMCapacityEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.MCDMCapacityVar)

        self.MCDMCostLabel = ctk.CTkLabel(self.rootModern, text="Cost (%)")
        self.MCDMCostToolTip = ToolTip(self.MCDMCostLabel, msg="MCDM - Percentage weight for Cost criteria")

        self.MCDMCostVar = ctk.StringVar(value="0")
        self.MCDMCostEntry = ctk.CTkEntry(self.rootModern, placeholder_text="0", state=ctk.DISABLED, textvariable=self.MCDMCostVar)

        ## PDF report generation

        #self.rootModern.grid_columnconfigure(0, weight=1)


        self.pdfSelectionVar = ctk.StringVar(value="off")
        self.pdfCheckBox = ctk.CTkCheckBox(self.rootModern, text="PDF report generation?", variable=self.pdfSelectionVar, onvalue="on", offvalue="off")
        self.pdfCheckToolTip = ToolTip(self.pdfCheckBox, msg="Creates a PDF file containing the PyMTDEvaluator output")
        self.pdfCheckBox.grid(row=18, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")
        self.pdfCheckBox.grid_columnconfigure(0, weight=1)

        
        self.generateSaveXMLButton = ctk.CTkButton(self.rootModern,
                                         text="Save XML", command=(lambda :self.saveXML()))
        self.generateSaveXMLButton.grid(row=19, column=0,
                                        columnspan=1,
                                        padx=20, pady=10,
                                        sticky="ew")
        
        def loadXMLButtonClick():
            self.showXML();
            toggle_sectionMovExp();
            toggle_sectionTtasExp();
            toggle_sectionMCDM()

        self.generateLoadXMLButton = ctk.CTkButton(self.rootModern,
                                        text="Load XML", command=(lambda :loadXMLButtonClick()))
        self.generateLoadXMLButton.grid(row=19, column=1,
                                       columnspan=3,
                                       padx=20, pady=10,
                                       sticky="ew")
        

        self.generateResultsButton = ctk.CTkButton(self.rootModern,
                                         text="Run", command=(lambda :self.runModern()))
        self.generateResultsButton.grid(row=20, column=0,
                                        columnspan=6,
                                        padx=20, pady=10,
                                        sticky="ew")
        

        # Show window

        self.rootModern.mainloop() 


    ## Function - modern
    def runModern(self):
        entsModern = {
            'Downtime per movement (min)': self.downtimeVar,
            'Cost per movement ($)': self.costVar,
            'Movement Trigger (h)': self.triggerVar,
            'Time for attack success (h)': self.timeAtkSucVar,
            'Evaluation Time (h)': self.evalTimeVar
            }
        print(entsModern)
        print("type "+ str(type(entsModern)))

        entsModernExpMov = {
            'Movement Trigger (h) - MIN': self.MovTriggerMinVar,
            'Movement Trigger (h) - MAX': self.MovTriggerMaxVar,
            'Movement Trigger (h) - Step': self.MovTriggerStepVar
            }
        print(entsModernExpMov)

        entsModernExpTtas = {
            'Time for attack success (h) - MIN': self.TtasMinVar,
            'Time for attack success (h) - MAX': self.TtasMaxVar,
            'Time for attack success (h) - Step': self.TtasStepVar
            }
        print(entsModernExpTtas)

        entsModernMCDM = {
            'Availability (%)': self.MCDMAvailabilityVar,
            'Probability of attack success (%)': self.MCDMPASVar,
            'Capacity (%)': self.MCDMCapacityVar,
            'Cost (%)': self.MCDMCostVar
            }
        print(entsModernMCDM)

        if self.pdfSelectionVar.get() == "on":
            self.pdfFlag = True;
        else:
            self.pdfFlag = False;


        self.runEvaluation(entsModern,entsModernExpMov,entsModernExpTtas,entsModernMCDM)


    def selectInterface(self, selectionArg):
        selection = int(selectionArg);
        self.interfaceSelectionMain = selection;
        self.interfaceSelection.destroy();

    def getInterfaceSelection(self):
        return self.interfaceSelectionMain;
    
    
    def xmlVariablesConversion(self, dictXml):
        print("Converting Variables")
        print(dictXml)
        if self.getInterfaceSelection() == 2:
            downtimePerMovement = str(dictXml['downtimePerMovement'])
            self.downtimeVar = ctk.StringVar(value=downtimePerMovement)
            costPerMovement = str(dictXml['costPerMovement'])
            self.costVar = ctk.StringVar(value=costPerMovement)
            movementTrigger = str(dictXml['movementTrigger'])
            self.triggerVar = ctk.StringVar(value=movementTrigger)
            timeForAttackSuccess = str(dictXml['timeForAttackSuccess'])
            self.timeAtkSucVar = ctk.StringVar(value=timeForAttackSuccess)
            evaluationTime = str(dictXml['evaluationTime'])
            self.evalTimeVar = ctk.StringVar(value=evaluationTime)
            switchMovExp = int(dictXml['switchMovExp'])
            self.switchMovExpVar = ctk.IntVar(value=switchMovExp)
            if self.switchMovExpVar.get() == 1:
                self.flag = False;
            else:
                self.flag = True;
            movExpMin = str(dictXml['movExpMin'])
            self.MovTriggerMinVar = ctk.StringVar(value=movExpMin)
            movExpMax = str(dictXml['movExpMax'])
            self.MovTriggerMaxVar = ctk.StringVar(value=movExpMax)
            movExpStep = str(dictXml['movExpStep'])
            self.MovTriggerStepVar = ctk.StringVar(value=movExpStep)
            switchTtasExp = int(dictXml['switchTtasExp'])
            self.switchTtasExpVar = ctk.IntVar(value=switchTtasExp)
            if self.switchTtasExpVar.get() == 1:
                self.flag2 = False;
            else:
                self.flag2 = True;
            ttasExpMin = str(dictXml['ttasExpMin'])
            self.TtasMinVar = ctk.StringVar(value=ttasExpMin)
            ttasExpMax = str(dictXml['ttasExpMax'])
            self.TtasMaxVar = ctk.StringVar(value=ttasExpMax)
            ttasExpStep = str(dictXml['ttasExpStep'])
            self.TtasStepVar = ctk.StringVar(value=ttasExpStep)
            switchMCDMExp = int(dictXml['switchMCDMExp'])
            self.switchMCDMVar = ctk.IntVar(value=switchMCDMExp)
            if self.switchMCDMVar.get() == 1:
                self.flagMCDM = True
            else:
                self.flagMCDM = False
            mcdmAvailability = str(dictXml['MCDMAvailability'])
            self.MCDMAvailabilityVar = ctk.StringVar(value=mcdmAvailability)
            mcdmPAS = str(dictXml['MCDMPAS'])
            self.MCDMPASVar = ctk.StringVar(value=mcdmPAS)
            mcdmCapacity = str(dictXml['MCDMCapacity'])
            self.MCDMCapacityVar = ctk.StringVar(value=mcdmCapacity)
            mcdmCost = str(dictXml['MCDMCost'])
            self.MCDMCostVar = ctk.StringVar(value=mcdmCost)
            pdfSelectionXml = str(dictXml['pdfCheckBox'])
            self.pdfSelectionVar = ctk.StringVar(value=pdfSelectionXml)
        else:
            downtimePerMovement = str(dictXml['downtimePerMovement'])
            self.downtimeVar.set(downtimePerMovement)
            costPerMovement = str(dictXml['costPerMovement'])
            self.costVar.set(costPerMovement)
            movementTrigger = str(dictXml['movementTrigger'])
            self.triggerVar.set(movementTrigger)
            timeForAttackSuccess = str(dictXml['timeForAttackSuccess'])
            self.timeAtkSucVar.set(timeForAttackSuccess)
            evaluationTime = str(dictXml['evaluationTime'])
            self.evalTimeVar.set(evaluationTime)
            switchMovExp = int(dictXml['switchMovExp'])
            self.switchMovExpVar.set(switchMovExp)
            if self.switchMovExpVar.get() == 1:
                self.flag = False;
            else:
                self.flag = True;
            movExpMin = str(dictXml['movExpMin'])
            self.MovTriggerMinVar.set(movExpMin)
            movExpMax = str(dictXml['movExpMax'])
            self.MovTriggerMaxVar.set(movExpMax)
            movExpStep = str(dictXml['movExpStep'])
            self.MovTriggerStepVar.set(movExpStep)
            switchTtasExp = int(dictXml['switchTtasExp'])
            self.switchTtasExpVar.set(switchTtasExp)
            if self.switchTtasExpVar.get() == 1:
                self.flag2 = False;
            else:
                self.flag2 = True;
            ttasExpMin = str(dictXml['ttasExpMin'])
            self.TtasMinVar.set(ttasExpMin)
            ttasExpMax = str(dictXml['ttasExpMax'])
            self.TtasMaxVar.set(ttasExpMax)
            ttasExpStep = str(dictXml['ttasExpStep'])
            self.TtasStepVar.set(ttasExpStep)
            switchMCDMExp = int(dictXml['switchMCDMExp'])
            self.switchMCDMVar.set(switchMCDMExp)
            if self.switchMCDMVar.get() == 1:
                self.flagMCDM = True
            else:
                self.flagMCDM = False
            mcdmAvailability = str(dictXml['MCDMAvailability'])
            self.MCDMAvailabilityVar.set(mcdmAvailability)
            mcdmPAS = str(dictXml['MCDMPAS'])
            self.MCDMPASVar.set(mcdmPAS)
            mcdmCapacity = str(dictXml['MCDMCapacity'])
            self.MCDMCapacityVar.set(mcdmCapacity)
            mcdmCost = str(dictXml['MCDMCost'])
            self.MCDMCostVar.set(mcdmCost)
            pdfSelectionXml = str(dictXml['pdfCheckBox'])
            self.pdfSelectionVar.set(pdfSelectionXml)

   
    def showXML(self):
         
        def selectXmlFile():
            filePath = filedialog.askopenfilename(filetypes=[('XML files', '*.xml')])
            if filePath:
                xmlData = xmlToDict(filePath)
                self.xmlVariablesConversion(xmlData)
                if self.getInterfaceSelection() == 2:
                    self.runModern()
                    selectXmlFile()
                else:
                    print("XML via Modern Interface")
                    #pass

        def xmlToDict(filePath):
            try:
                tree = ET.parse(filePath)
                root = tree.getroot()
                data = {}

                for child in root:
                    data[child.tag] = child.text

                return data
            except FileNotFoundError:
                print(f"File not found: {filePath}")

        rootXML = ctk.CTk()
        rootXML.withdraw() 

        selectXmlFile()

    def saveXML(self):
        xmlFields = {
            'downtimePerMovement': self.downtimeVar.get(),
            'costPerMovement': self.costVar.get(),
            'movementTrigger': self.triggerVar.get(),
            'timeForAttackSuccess': self.timeAtkSucVar.get(),
            'evaluationTime': self.evalTimeVar.get(),
            'switchMovExp': self.switchMovExpVar.get(),
            'movExpMin': self.MovTriggerMinVar.get(),
            'movExpMax': self.MovTriggerMaxVar.get(),
            'movExpStep': self.MovTriggerStepVar.get(),
            'switchTtasExp': self.switchTtasExpVar.get(),
            'ttasExpMin': self.TtasMinVar.get(),
            'ttasExpMax': self.TtasMaxVar.get(),
            'ttasExpStep': self.TtasStepVar.get(),
            'switchMCDMExp': self.switchMCDMVar.get(),
            'MCDMAvailability': self.MCDMAvailabilityVar.get(),
            'MCDMPAS': self.MCDMPASVar.get(),
            'MCDMCapacity': self.MCDMCapacityVar.get(),
            'MCDMCost': self.MCDMCostVar.get(),
            'pdfCheckBox': self.pdfSelectionVar.get()
            }
        
        root = ET.Element("variables")
        for key, value in xmlFields.items():
            child = ET.SubElement(root, key)
            child.text = str(value)

        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding='utf-8', xml_declaration=True, method='xml')


    def interfaceSelection(self):

        self.interfaceSelection = ctk.CTk()
        self.interfaceSelection.title("PyMTDEvaluator 2.0 - Please select your preferred interface")   

        self.selectionVar = tk.StringVar(value="0")
 

        self.selectionLabel = ctk.CTkLabel(self.interfaceSelection, 
                                    text="Interface")
        self.selectionLabel.grid(row=0, column=0, 
                              padx=20, pady=10,
                              sticky="ew")



        self.classicRadioButton = ctk.CTkRadioButton(self.interfaceSelection,
                                  text="Classical",
                                  variable=self.selectionVar,
                                            value="0")
        self.classicRadioButton.grid(row=0, column=1, padx=10,
                                  pady=20, sticky="ew")
 
        self.modernRadioButton = ctk.CTkRadioButton(self.interfaceSelection,
                                      text="Modern",
                                      variable=self.selectionVar,
                                      value="1")
        self.modernRadioButton.grid(row=0, column=2,
                                    padx=20,
                                    pady=10, sticky="ew")
         
        self.chatRadioButton = ctk.CTkRadioButton(self.interfaceSelection,
                                    text="Upload XML file",
                                    variable=self.selectionVar,
                                            value="2")
        self.chatRadioButton.grid(row=0, column=3,
                                  padx=20, pady=10, 
                                  sticky="ew")

        

        self.selectInterfaceButton = ctk.CTkButton(self.interfaceSelection,
                                         text="Select", command=  lambda:  self.selectInterface(self.selectionVar.get()))
        self.selectInterfaceButton.grid(row=1, column=0,
                                        columnspan=5,
                                        padx=20, pady=10,
                                        sticky="ew")


        self.interfaceSelection.mainloop() 


    def show(self):
        root = Tk()
        
        root.title("PyMTDEvaluator 2.0 - Classical")
        ents = self.makeform(root, self.fields)
        
        separator = ttk.Separator(root, orient='horizontal')
        separator.pack(side='top', fill='x')
        
        
      
                
        def click():
            if checker.get() == 1:          
                ents['Movement Trigger (h)'].config(state=DISABLED)
                entsExp['Movement Trigger (h) - MIN'].config(state=NORMAL)
                entsExp['Movement Trigger (h) - MAX'].config(state=NORMAL)
                entsExp['Movement Trigger (h) - Step'].config(state=NORMAL)
                self.flag = False;
            elif checker.get() == 0:        
                ents['Movement Trigger (h)'].config(state=NORMAL)
                entsExp['Movement Trigger (h) - MIN'].config(state=DISABLED)
                entsExp['Movement Trigger (h) - MAX'].config(state=DISABLED)
                entsExp['Movement Trigger (h) - Step'].config(state=DISABLED)
                self.flag = True;
            
        
        checker = IntVar()

        check = Checkbutton(text="Experiment - Movement Trigger", font=("Helvetica", 12), variable=checker, command=click)
        check.pack(side='top', padx=1, pady=5)
        
        entsExp = self.makeformExp(root, self.fields2)


        separator = ttk.Separator(root, orient='horizontal')
        separator.pack(side='top', fill='x')
        
        def click2():
            if checker2.get() == 1:          
                ents['Time for attack success (h)'].config(state=DISABLED)
                entsExp2['Time for attack success (h) - MIN'].config(state=NORMAL)
                entsExp2['Time for attack success (h) - MAX'].config(state=NORMAL)
                entsExp2['Time for attack success (h) - Step'].config(state=NORMAL)
                self.flag2 = False; ### AJUSTAR
            elif checker2.get() == 0:        
                ents['Time for attack success (h)'].config(state=NORMAL)
                entsExp2['Time for attack success (h) - MIN'].config(state=DISABLED)
                entsExp2['Time for attack success (h) - MAX'].config(state=DISABLED)
                entsExp2['Time for attack success (h) - Step'].config(state=DISABLED)
                self.flag2 = True; ### Ajustar
            
        
        checker2 = IntVar()

        check2 = Checkbutton(text="Experiment - Time for attack success", font=("Helvetica", 12), variable=checker2, command=click2)
        check2.pack(side='top', padx=1, pady=5)

        
        entsExp2 = self.makeformExp(root, self.fields3)

        separator = ttk.Separator(root, orient='horizontal')
        separator.pack(side='top', fill='x')
 
       
               
        #MCDM aqui
        def click4():
            if checker4.get() == 1:          
                entsExp3['Availability (%)'].config(state=NORMAL)
                entsExp3['Probability of attack success (%)'].config(state=NORMAL)
                entsExp3['Capacity (%)'].config(state=NORMAL)
                entsExp3['Cost (%)'].config(state=NORMAL)
                self.flagMCDM = True;
            elif checker4.get() == 0:        
                entsExp3['Availability (%)'].config(state=DISABLED)
                entsExp3['Probability of attack success (%)'].config(state=DISABLED)
                entsExp3['Capacity (%)'].config(state=DISABLED)
                entsExp3['Cost (%)'].config(state=DISABLED)
                self.flagMCDM = False;
            
        
        checker4 = IntVar()

        check = Checkbutton(text="Multi-Criteria Decision Making?", font=("Helvetica", 12), variable=checker4, command=click4)
        check.pack(side='top', padx=1, pady=5)
        
               
        entsExp3 = self.makeformExp(root, self.fields4)
        
        separator = ttk.Separator(root, orient='horizontal')
        separator.pack(side='top', fill='x')
        

        
        def click3():
            if checker3.get() == 1:          
                self.pdfFlag = True;
            elif checker3.get() == 0:        
                self.pdfFlag = False;
        

        checker3 = IntVar()

        check3 = Checkbutton(text="PDF report generation?", font=("Helvetica", 12), variable=checker3, command=click3)
        check3.pack(side='top', padx=1, pady=5)
        

        
        b1 = Button(root, text='Run', font=("Helvetica", 12), command=(lambda e=ents, e2=entsExp, e3=entsExp2, e4=entsExp3: self.runEvaluation(e,e2,e3,e4)))
        b1.pack(side='top', fill='x')
        
        root.mainloop()
        
class TransientEvaluator():
    
    def __init__(self, _downtimePerMov, _costPerMovement, _mtdSched, _timeForAtkSuc, _evalTime, _evalCount):
        self.internal = 100
        self.external = 100
        self.downtimeParameter = _downtimePerMov
        self.downtimeForAvailCalc = _downtimePerMov
        self.costParameter = _costPerMovement
        self.migTriggerPlot = _mtdSched
        self.migTriggerMTD = _mtdSched
        self.reconTime = 0
        _variants = 2
        self.variants = []
        for i in range(_variants):
            self.variants.append(0)
        self.downtimeResult = 0
        self.erlangPhase = _timeForAtkSuc/4
        self.timeForAtkPlot = _timeForAtkSuc
        self.target = _evalTime
        self.downtimeTransient = 0;
        
        self.currentPosition = 0
        self.downtime = 0
        self.accumulatedDowntime = 0
        self.globalTime = 0.0000001
        self.recon = False
        self.attackSuccess = False
        self.alive = True
        self.atkProgWOK = 0
        self.attackSuccessWOKnow = False
        
        self.contSuc = 0
        self.contFail = 0
        self.contSucWOK = 0
        self.contFailWOK = 0
        self.contAvail = 0
        self.contUnavail = 0
        
        self.arrCapacity = []
        self.arrAvail = []
        self.arrAvail2 = []
        self.arrContMov = []
        
        self.dataCapacity= []
        self.dataAtk = []
        self.dataAtkWOK = []
        self.dataAvail = []
        self.dataAvail2 = []
        self.dataContMov = []
        
        self.resultsAvail2 = []
        self.resultsAvail2CIP = []
        self.resultsAvail2CIN = []
        self.resultsAvail = []
        self.resultsAvailCIP = []
        self.resultsAvailCIN = []
        self.resultsAtk = []
        self.resultsAtkCIP = []
        self.resultsAtkCIN = []
        self.resultsAtkWOK = []
        self.resultsAtkWOKCIP = []
        self.resultsAtkWOKCIN = []
        self.resultsCapacity= []
        self.resultsCapacityCIP = []
        self.resultsCapacityCIN = []
        self.resultsContMov = []
        self.contMovements = 0
        self.summary="";
        self.countEvaluations = _evalCount;
        self.singleRun = False
        self.singleAtkProgWOK = []
        self.singleAvail = []
        self.singleGlobalTime = []
        self.singleCapacity = []
        self.contUP = 0
        self.contDown = 0
        self.sysAvailable = True
        
        self.scenario = Scenario(0,0,0,0,0, self.timeForAtkPlot);

        self.progressBarVariable = 0;
        #self.pbar=tqdm(total=100)
        self.pbar=0

        #self.window = "window";
        self.window = tk.Tk();
        self.window.title("Tk Window");
        self.window.withdraw();


    def startProgressBar(self, _currentEval, _totalEval):

        pbardesc = "Parameters: MovTrigger = "+ str(self.migTriggerPlot) + " AtkSucProb = " + str(self.timeForAtkPlot) + "\n Progress bar (" + str(_currentEval) + "/" + str(_totalEval) + ")"
        self.pbar = tqdm(total=self.target, desc=pbardesc, leave=False)
        self.progress_var = tk.DoubleVar()  # Track progress for Tkinter bar
        self.progress_bar = ttk.Progressbar(self.window, maximum=self.target, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack()

    def showProgressBar(self):
        print("progress: " + str(self.pbar.n))  # Access current progress from pbar
        self.pbar.update(1)
        self.pbar.refresh()
        self.progress_var.set(self.pbar.n)
        self.window.update()  # Refresh Tkinter UI



    def meanConfidenceInterval(self, data, confidence=0.95):
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        return m, m-h, m+h

    def getSummary(self):
        self.summary = self.summary + "\n +++++++++++++++++++++++++++ \n"
        return self.summary

    def getatkProgWOK(self):
        return self.atkProgWOK

    def getScenario(self):
        return self.scenario

    def getAvailabilitySingle(self):
        if(self.atkProgWOK >= 4):
            a = IntVar();
            a = 0;
            return a;
        else:
            a = IntVar();
            a = 1;
            return a;
    
    def token(self, env):
        eventCounter = 0
        if(self.singleRun):
             f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched" + str(round(self.migTriggerPlot,2)) + "h.tsv"), "w")
             f.close()
             f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
             f.write("Number GlobalTime EventType Status Recon AtkProg Avail \n")
             f.close()
    
        self.atkProgWOK = 0
             
        while True:
            
            if(self.recon):
                time = random.expovariate(1.0/self.erlangPhase)
                if(time < self.migTriggerMTD):
                    if(self.singleRun):
                        eventCounter = eventCounter+1
                        strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "AtkProg" + " " + "next" + " "  + "1" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                        f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                        f.write(strEvent)
                        f.close()
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(self.getAvailabilitySingle())
                    yield env.timeout(time)
                    self.globalTime = self.globalTime + time
                    if(self.singleRun):
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(self.getAvailabilitySingle())
                    
                    self.variants[self.currentPosition] = self.variants[self.currentPosition] + 1
                    
                    
                    self.atkProgWOK = self.atkProgWOK + 1
                    
                    
                    
                    self.migTriggerMTD = self.migTriggerMTD - time
                    if(self.singleRun):
                        strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "AtkProg" + " " + "end" + " "  + "1" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                        f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                        f.write(strEvent)
                        f.close()
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(self.getAvailabilitySingle())
                    
                    if(self.atkProgWOK >= 4):
                        self.atkProgWOK = 4
                        self.attackSuccessWOKnow = True
                        self.sysAvailable = False
                      
                        break
                    
                else:
                    
                    if(self.singleRun):
                        eventCounter = eventCounter+1
                        strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Mov" + " " + "next" + " "  + "1" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                        f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                        f.write(strEvent)
                        f.close()
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(self.getAvailabilitySingle())
                        
                    yield env.timeout(self.migTriggerMTD)
                    self.contMovements = self.contMovements + 1
                    self.globalTime = self.globalTime + self.migTriggerMTD

                    if(self.singleRun):

                        strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Mov" + " " + "end" + " "  + "1" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                        f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                        f.write(strEvent)
                        f.close()
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(self.getAvailabilitySingle())


                    self.migTriggerMTD = self.migTriggerPlot
                    self.recon = False
                    self.currentPosition = self.currentPosition + 1
                    self.atkProgWOK = 0
                    if(self.currentPosition >= len(self.variants)):
                        self.currentPosition = 0
                    self.downtime = random.expovariate(1.0/self.downtimeParameter)

                    if(self.singleRun):
                        eventCounter = eventCounter + 1
                        strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Downt" + " " + "start" + " "  + "0" + " " + str(self.atkProgWOK) +" " + "0" + " \n" ;
                        f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                        f.write(strEvent)
                        f.close()
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(0)
                        

                    self.sysAvailable = False
                    yield env.timeout(self.downtime)
                    self.sysAvailable = True
                  
                  
                    self.globalTime = self.globalTime + self.downtime
                    self.accumulatedDowntime =  self.accumulatedDowntime + self.downtime

                    self.migTriggerMTD = self.migTriggerMTD - self.downtime
                    while(self.migTriggerMTD <0):
                            self.migTriggerMTD = self.migTriggerMTD + self.migTriggerPlot


                    if(self.singleRun):

                        strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Downt" + " " + "end" + " "  + "0" + " " + str(self.atkProgWOK) +" " + "0" + " \n" ;
                        f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                        f.write(strEvent)
                        f.close()
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(0)
                        
                        
                        strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "After" + " " + "start" + " "  + "0" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                        f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                        f.write(strEvent)
                        f.close()
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(self.getAvailabilitySingle())


                        
                for i in range(0, len(self.variants)):
                    if(self.variants[i]>=4):
                        self.attackSuccess = True
                if(self.atkProgWOK >= 4):
                    self.attackSuccessWOKnow = True
            else:
                if (self.reconTime > 0):
                    time = random.expovariate(1.0/self.reconTime)
                    if(self.singleRun):
                        eventCounter = eventCounter+1
                        strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Recon" + " " + "next" + " "  + "0" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                        f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                        f.write(strEvent)
                        f.close()
                        self.singleGlobalTime.append(self.globalTime)
                        self.singleAtkProgWOK.append(self.atkProgWOK)
                        self.singleAvail.append(self.getAvailabilitySingle())

                    if(time < self.migTriggerMTD):
                        if(self.singleRun):
                            self.singleGlobalTime.append(self.globalTime)
                            self.singleAtkProgWOK.append(self.atkProgWOK)
                            self.singleAvail.append(self.getAvailabilitySingle())
                        yield env.timeout(time)
                        self.globalTime = self.globalTime + time
                        if(self.singleRun):
                            self.singleGlobalTime.append(self.globalTime)
                            self.singleAtkProgWOK.append(self.atkProgWOK)
                            self.singleAvail.append(self.getAvailabilitySingle())

                        
                        
                        self.migTriggerMTD = self.migTriggerMTD - time
                        self.recon = True
                        if(self.singleRun):
                            eventCounter = eventCounter+1
                            strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Recon" + " " + "end" + " "  + "1" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                            f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                            f.write(strEvent)
                            f.close()
                            self.singleGlobalTime.append(self.globalTime)
                            self.singleAtkProgWOK.append(self.atkProgWOK)
                            self.singleAvail.append(self.getAvailabilitySingle())
                    else: 
                        if(self.singleRun):
                            eventCounter = eventCounter+1
                            strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Mov" + " " + "next" + " "  + "1" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                            f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                            f.write(strEvent)
                            f.close()
                            self.singleGlobalTime.append(self.globalTime)
                            self.singleAtkProgWOK.append(self.atkProgWOK)
                            self.singleAvail.append(self.getAvailabilitySingle())
                        

                        yield env.timeout(self.migTriggerMTD)
                        
                        self.contMovements = self.contMovements + 1

                        self.globalTime = self.globalTime + self.migTriggerMTD
                        
                        if(self.singleRun):
                            strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Mov" + " " + "end" + " "  + "1" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                            f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                            f.write(strEvent)
                            f.close()
                            self.singleGlobalTime.append(self.globalTime)
                            self.singleAtkProgWOK.append(self.atkProgWOK)
                            self.singleAvail.append(self.getAvailabilitySingle())

                        
                        self.migTriggerMTD = self.migTriggerPlot
                        self.currentPosition = self.currentPosition + 1
                        if(self.currentPosition >= len(self.variants)):
                            self.currentPosition = 0
                        self.atkProgWOK = 0
                        self.downtime = random.expovariate(1.0/self.downtimeParameter)
                        
                        if(self.singleRun):
                            eventCounter = eventCounter + 1
                            strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Downt" + " " + "start" + " "  + "0" + " " + str(self.atkProgWOK) +" " + "0" + " \n" ;
                            f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                            f.write(strEvent)
                            f.close()
                            self.singleGlobalTime.append(self.globalTime)
                            self.singleAtkProgWOK.append(self.atkProgWOK)
                            self.singleAvail.append(0)

                        
                        self.sysAvailable = False
                        yield env.timeout(self.downtime)
                        self.sysAvailable = True
                        
                        self.globalTime = self.globalTime + self.downtime
                        self.accumulatedDowntime =  self.accumulatedDowntime + self.downtime 
                        self.migTriggerMTD = self.migTriggerMTD - self.downtime
                        while(self.migTriggerMTD <0):
                            self.migTriggerMTD = self.migTriggerMTD + self.migTriggerPlot
                        
                        
                        if(self.singleRun):

                            strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "Downt" + " " + "end" + " "  + "0" + " " + str(self.atkProgWOK) +" " + "0" + " \n" ;
                            f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                            f.write(strEvent)
                            f.close()
                            self.singleGlobalTime.append(self.globalTime)
                            self.singleAtkProgWOK.append(self.atkProgWOK)
                            self.singleAvail.append(0)
                        
                        
                            strEvent = str(eventCounter) + " " + str(self.globalTime) + " " + "After" + " " + "start" + " "  + "0" + " " + str(self.atkProgWOK) +" " + str(self.getAvailabilitySingle()) + " \n" ;
                            f = open(("PyMTDEvaluator-EventTrace-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
                            f.write(strEvent)
                            f.close()
                            self.singleGlobalTime.append(self.globalTime)
                            self.singleAtkProgWOK.append(self.atkProgWOK)
                            self.singleAvail.append(self.getAvailabilitySingle())

                        
                    for i in range(0, len(self.variants)):
                        if(self.variants[i]>=4):
                            self.attackSuccess = True
                    if(self.atkProgWOK >= 4):
                        self.attackSuccessWOKnow = True
                    
                else:
                    self.recon = True
        
    
        
    def getAtkProb(self):
        return self.resultsAtkWOK
    
    def getCost(self):
        return self.resultsContMov

    def getCapacity(self):
        return self.resultsCapacity
    
    def getSingleAvailability(self):
        return self.singleAvail
    
    def getSingleAtkProg(self):
        return self.singleAtkProgWOK
    
    def getSingleGlobalTime(self):
        return self.singleGlobalTime
    
    def getSingleCapacity(self):
        return self.singleCapacity
    
    def getAvailability(self):
        return self.resultsAvail
    
    def fill(self, x):
        switcher = {
            0:100,
            1:75,
            2:50,
            3:25,
            4:0       
        }
        
        a = switcher.get(x)
        return a
    
    def resetVariables(self):
        self.currentPosition = 0
        self.downtime = 0
        self.globalTime = 0.0000001
        self.accumulatedDowntime = 0
        self.recon = False
        self.attackSuccessWOKnow = False
        self.attackSuccess = False
        self.arrAvail = []
        self.arrAvail2 = []
        self.arrContMov = []
        self.arrCapacity = []
        self.migTriggerMTD = self.migTriggerPlot
        for i in range(0, len(self.variants)):
            self.variants[i] = 0
        self.atkProgWOK = 0
        self.singleAtkProgWOK = []
        self.singleAvail = []
        self.singleGlobalTime = []
        self.singleCapacity =[]
        self.sysAvailable = True
    
    def singleRunEvaluation(self):
        self.resetVariables();
        random.seed(a=None, version=2) 
        self.singleRun = True
        self.singleGlobalTime.append(0)
        self.singleAtkProgWOK.append(0)
        self.singleAvail.append(1)
                	
        env = simpy.Environment()                       	
        env.process(self.token(env))                  	   	
        env.run(until=self.target)
        if not self.attackSuccessWOKnow:
            self.singleGlobalTime.append(self.target)
            last = len(self.singleAtkProgWOK) -1
            self.singleAtkProgWOK.append(self.singleAtkProgWOK[last])
            last = len(self.singleAvail) -1
            self.singleAvail.append(self.singleAvail[last])
            
        self.singleRun = False
        
        for value in self.singleAtkProgWOK:
            a = self.fill(value)

            self.singleCapacity.append(int(a))

        
        
    
    def run(self, currentEvaluation, totalEvaluation):
        
        
        self.startProgressBar(currentEvaluation, totalEvaluation);

        for i in range(self.external):
            for x in range(self.internal):
                random.seed(a=None, version=2)                  	
                self.currentPosition = 0
                self.downtime = 0
                self.globalTime = 0.0000001
                self.accumulatedDowntime = 0
                self.recon = False
                self.attackSuccessWOKnow = False
                self.attackSuccess = False
                self.arrAvail = []
                self.arrAvail2 = []
                self.arrContMov = []
                self.arrCapacity = []
                self.sysAvailable = True
                self.migTriggerMTD = self.migTriggerPlot
                for i in range(0, len(self.variants)):
                    self.variants[i] = 0
                self.atkProgWOK = 0
                env = simpy.Environment()                       	
                env.process(self.token(env))                  	   	
                env.run(until=0.0001)                     
                
                if(self.attackSuccess):
                    self.contSuc = self.contSuc + 1
                else:
                    self.contFail = self.contFail + 1
                
                if(self.attackSuccessWOKnow):
                    self.contSucWOK = self.contSucWOK + 1
                else:
                    self.contFailWOK= self.contFailWOK + 1
                
                   
                
                if(self.attackSuccessWOKnow):
                    downtimeFail = 0.0001 - self.globalTime
                    totalDowntime = self.accumulatedDowntime + downtimeFail
                    avail2 = (0.0001 - totalDowntime)/0.0001
                    self.arrAvail.append(avail2)
                    
                else:
                    avail2 = (0.0001-self.accumulatedDowntime)/(0.0001)			
                    self.arrAvail.append(avail2)
                    
                capacity = int(self.fill(self.atkProgWOK))
                self.arrCapacity.append(capacity)
                self.arrContMov.append(self.contMovements)
                self.contMovements = 0
            self.probAtkSuc = self.contSuc/(self.contSuc+self.contFail)
            probAtkSucWOK = self.contSucWOK/(self.contSucWOK+self.contFailWOK)
            self.dataAtkWOK.append(probAtkSucWOK)
            
            
            value =(np.mean(self.arrAvail))  * (1-probAtkSucWOK);
            self.dataAvail.append(value)
            
            
            self.dataAtk.append(self.probAtkSuc)
            self.dataAvail2.append(np.mean(self.arrAvail))
            self.dataCapacity.append(np.mean(self.arrCapacity))
            if (len(self.dataContMov)>0):
                if (self.dataContMov[(len(self.dataContMov)-1)] > round(np.mean(self.arrContMov))):
                    self.dataContMov.append(self.dataContMov[(len(self.dataContMov)-1)])
                else:     
                    self.dataContMov.append(round(np.mean(self.arrContMov)))
            else:
                self.dataContMov.append(round(np.mean(self.arrContMov)))

            self.contSuc = 0
            self.contFail = 0
            self.contSucWOK = 0
            self.contFailWOK = 0
            self.contAvail = 0
            self.contUnvail = 0
            
        mean, ciI, ciM = self.meanConfidenceInterval(self.dataAtk, 0.95)
        stringFinal = str('0') + ' ' + str(ciI) + ' ' + str(mean) + ' ' + str(ciM) + '\n'
        self.resultsAtk.append(mean)
        self.resultsAtkCIP.append(ciM)
        self.resultsAtkCIN.append(ciI)
        
        
        f = open(("PyMTDEvaluator-output-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched" + str(round(self.migTriggerPlot,2)) + "h.tsv"), "w")
        f.close()
        f = open(("PyMTDEvaluator-output-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
        f.write("Time CI- Mean CI+ \n")
        f.close()
        f = open(("PyMTDEvaluator-output-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
        f.write(stringFinal)
        f.close()
        
        
        mean, ciI, ciM = self.meanConfidenceInterval(self.dataAtkWOK, 0.95)
        stringFinal = str('0') + ' ' + str(ciI) + ' ' + str(mean) + ' ' + str(ciM) + '\n'
        self.resultsAtkWOK.append(mean)
        self.resultsAtkWOKCIP.append(ciM)
        self.resultsAtkWOKCIN.append(ciI)
        
        
        f = open(("PyMTDEvaluator-output-WOK-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "w")
        f.close()
        f = open(("PyMTDEvaluator-output-WOK-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
        f.write("Time CI- Mean CI+ \n")
        f.close()
        f = open(("PyMTDEvaluator-output-WOK-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
        f.write(stringFinal)
        f.close()
        
        if(len(self.resultsContMov)>0):
            if(self.resultsContMov[(len(self.resultsContMov)-1)] > round(np.mean(self.dataContMov))*self.costParameter):
                self.resultsContMov.append(self.resultsContMov[(len(self.resultsContMov)-1)])
            else:
                   self.resultsContMov.append(round(np.mean(self.dataContMov))*self.costParameter) 
        else:
            self.resultsContMov.append(round(np.mean(self.dataContMov))*self.costParameter)        
        
        mean, ciI, ciM = self.meanConfidenceInterval(self.dataAvail, 0.95)
        stringAvail = str('0') + ' ' + str(ciI) + ' ' + str(mean) + ' ' + str(ciM) + '\n'
        self.resultsAvail.append(mean)
        self.resultsAvailCIP.append(ciM)
        self.resultsAvailCIN.append(ciI)
        
        f = open(("PyMTDEvaluator-output-Avail-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2))  +"h.tsv"), "w")
        f.close()
        f = open(("PyMTDEvaluator-output-Avail-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2))  +"h.tsv"), "a")
        f.write("Time CI- Mean CI+ \n")
        f.close()
        f = open(("PyMTDEvaluator-output-Avail-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2))  +"h.tsv"), "a")
        f.write(stringAvail)
        f.close()
        
        mean, ciI, ciM = self.meanConfidenceInterval(self.dataCapacity, 0.95)
        stringAvail = str('0') + ' ' + str(ciI) + ' ' + str(mean) + ' ' + str(ciM) + '\n'
        self.resultsCapacity.append(mean)
        self.resultsCapacityCIP.append(ciM)
        self.resultsCapacityCIN.append(ciI)
        
        f = open(("PyMTDEvaluator-output-Capacity-Scn"+ str(self.countEvaluations) + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2))  +"h.tsv"), "w")
        f.close()
        f = open(("PyMTDEvaluator-output-Capacity-Scn"+ str(self.countEvaluations) + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2))  +"h.tsv"), "a")
        f.write("Time CI- Mean CI+ \n")
        f.close()
        f = open(("PyMTDEvaluator-output-Capacity-Scn"+ str(self.countEvaluations) + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2))  +"h.tsv"), "a")
        f.write(stringAvail)
        f.close()
        
        self.dataAtk = []
        self.dataAtkWOK = []
        self.dataAvail = []
        self.dataContMov = []
        self.dataCapacity = []
        self.dataAvail2=[]
        
        
        print("MTD evaluation progress")

        for j in range(1, (self.target+1)):
            time.sleep(0.1)
            for i in range(self.external):
                for x in range(self.internal):
                    random.seed(a=None, version=2)                  	
                    self.currentPosition = 0
                    self.downtime = 0
                    self.globalTime = 0.0000001
                    self.accumulatedDowntime = 0
                    self.recon = False
                    self.attackSuccess = False
                    self.attackSuccessWOKnow = False
                    self.sysAvailable = True
                    self.arrAvail = []
                    self.arrAvail2 = []
                    self.arrContMov = []
                    self.arrCapacity = []
                    self.migTriggerMTD = self.migTriggerPlot
                    for i in range(0, len(self.variants)):
                        self.variants[i] = 0
                    self.atkProgWOK = 0
                    env = simpy.Environment()                       	
                    env.process(self.token(env)) 
                    env.run(until=j)                                	
                    if(self.attackSuccess):
                        self.contSuc = self.contSuc + 1
                    else:
                        self.contFail = self.contFail + 1
                        
                        
                    if(self.attackSuccessWOKnow):
                        self.contSucWOK = self.contSucWOK + 1
                    else:
                        self.contFailWOK= self.contFailWOK + 1
                     
                    
                    if(self.attackSuccessWOKnow):
                        downtimeFail = j - self.globalTime
                        totalDowntime = self.accumulatedDowntime + downtimeFail
                        avail2 = (j - totalDowntime)/j
                        self.arrAvail.append(avail2)
                    else:
                        avail2 = (j-self.accumulatedDowntime)/(j)			
                        self.arrAvail.append(avail2) 
                        
                    
                    capacity = int(self.fill(self.atkProgWOK))
                    self.arrCapacity.append(capacity)
                    self.arrContMov.append(self.contMovements)
                    self.contMovements = 0
                self.probAtkSuc = self.contSuc/(self.contSuc+self.contFail)
                probAtkSucWOK = self.contSucWOK/(self.contSucWOK+self.contFailWOK)
                self.dataAtkWOK.append(probAtkSucWOK)
                self.dataAtk.append(self.probAtkSuc)
                
                value =(np.mean(self.arrAvail))  * (1-probAtkSucWOK);
                self.dataAvail.append(value)
                self.dataAvail2.append(np.mean(self.arrAvail))
                self.dataCapacity.append(np.mean(self.arrCapacity))
                if (len(self.dataContMov)>0):
                    if (self.dataContMov[(len(self.dataContMov)-1)] > round(np.mean(self.arrContMov))):
                        self.dataContMov.append(self.dataContMov[(len(self.dataContMov)-1)])
                    else:     
                        self.dataContMov.append(round(np.mean(self.arrContMov)))
                else:
                    self.dataContMov.append(round(np.mean(self.arrContMov)))
                self.contSuc = 0
                self.contFail = 0
                self.contSucWOK = 0
                self.contFailWOK = 0
                self.contAvail = 0
                self.contUnvail = 0
	
            mean, ciI, ciM = self.meanConfidenceInterval(self.dataAtk, 0.95)
            stringFinal = str(j) + ' ' + str(ciI) + ' ' + str(mean) + ' ' + str(ciM) + '\n'
            self.resultsAtk.append(mean)
            self.resultsAtkCIP.append(ciM)
            self.resultsAtkCIN.append(ciI)
           
            if(len(self.resultsContMov)>0):
                if(self.resultsContMov[(len(self.resultsContMov)-1)] > round(np.mean(self.dataContMov))*self.costParameter):
                    self.resultsContMov.append(self.resultsContMov[(len(self.resultsContMov)-1)])
                else:
                   self.resultsContMov.append(round(np.mean(self.dataContMov))*self.costParameter) 
            else:
                self.resultsContMov.append(round(np.mean(self.dataContMov))*self.costParameter)
	
            f = open(("PyMTDEvaluator-output-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
            f.write(stringFinal)
            f.close()
                       
            mean, ciI, ciM = self.meanConfidenceInterval(self.dataAtkWOK, 0.95)
            stringFinal = str(j) + ' ' + str(ciI) + ' ' + str(mean) + ' ' + str(ciM) + '\n'
            self.resultsAtkWOK.append(mean)
            self.resultsAtkWOKCIP.append(ciM)
            self.resultsAtkWOKCIN.append(ciI)
        
            
            f = open(("PyMTDEvaluator-output-WOK-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  +  "-Sched"+ str(round(self.migTriggerPlot,2)) + "h.tsv"), "a")
            f.write(stringFinal)
            f.close()
            
            mean, ciI, ciM = self.meanConfidenceInterval(self.dataAvail, 0.95)
            self.resultsAvail.append(mean)
            self.resultsAvailCIP.append(ciM)
            self.resultsAvailCIN.append(ciI)
            stringAvail = str(j) + ' ' + str(ciI) + ' ' + str(mean) + ' ' + str(ciM) + '\n'
            f = open(("PyMTDEvaluator-output-Avail-Scn"+ str(self.countEvaluations)  + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2))  +"h.tsv"), "a")
            f.write(stringAvail)
            f.close()
            
            mean, ciI, ciM = self.meanConfidenceInterval(self.dataCapacity, 0.95)
            self.resultsCapacity.append(mean)
            self.resultsCapacityCIP.append(ciM)
            self.resultsCapacityCIN.append(ciI)
            stringAvail = str(j) + ' ' + str(ciI) + ' ' + str(mean) + ' ' + str(ciM) + '\n'
            f = open(("PyMTDEvaluator-output-Capacity-Scn"+ str(self.countEvaluations) + "-Atk" + str(self.timeForAtkPlot) + "h"  + "-Sched"+ str(round(self.migTriggerPlot,2))  +"h.tsv"), "a")
            f.write(stringAvail)
            f.close()
            
            self.dataAtk = []
            self.dataAtkWOK = []
            self.dataAvail = []
            self.dataContMov = []
            self.dataCapacity = []
            self.dataAvail2 = []
            
            progressMTD = round((j/self.target)*100) 
            #marksMTD = [0, 25, 50, 75]
            #if progressMTD in marksMTD:
            print(str(progressMTD) +  "% ")
            print("Scenario "+ str(self.countEvaluations) + " MTD Trigger :" + str(self.migTriggerPlot)  + " Time for attack success: " + str(self.timeForAtkPlot));
            self.progressBarVariable = progressMTD;
            self.showProgressBar();
            time.sleep(0.1);
            
        time.sleep(0.1)
        self.pbar.close()
        self.window.destroy()
        
        print("100% ")
      
        downtimeCalc = SteadyStateEvaluator(self.migTriggerPlot, self.downtimeForAvailCalc)
        env2 = simpy.Environment()
        downtimeCalc.compute(env2)
        self.downtimeResult = round(downtimeCalc.getAnnualDowntime(), 2)
        
        ##Results summary
        
        arrayLengthPAS = len(self.resultsAtkWOK)
        lastElementPAS = self.resultsAtkWOK[arrayLengthPAS - 1]

                     
        arrayLength = len(self.resultsContMov)
        lastElement = self.resultsContMov[arrayLength - 1]
        
        self.downtimeTransient = round(((lastElement/self.costParameter)*self.downtimeForAvailCalc*60), 2)
        
        self.summary = self.summary + "\nParameters \n ----------  \nMovement Trigger = " + str(self.migTriggerPlot) + " h \nTime for Attack Success = " + str(self.timeForAtkPlot) + " h \n ------- \nResults \n --------\nExpected downtime due to movements (evaluation time)  = "+ str(self.downtimeTransient) + " min \nExpected annual downtime due to movements = " + str(self.downtimeResult) + " min \nExpected total cost (evaluation time)  = $ " + str(lastElement)  
        
        if (len(self.resultsAtkWOK)>0):
            maxValue = np.max(self.resultsAtkWOK);
            if (maxValue >= 1):
                position = self.resultsAtkWOK.index(max(self.resultsAtkWOK))
                self.summary = self.summary + "\nExpected Threshold = " + str(position) + " h"
            else:
                position = np.argmax(self.resultsAtkWOK)
                self.summary = self.summary + "\nExpected Threshold = " + str(position) + " h"
                
        
        meanC, cinC, cipC = self.meanConfidenceInterval(self.resultsCapacity, 0.95)
        self.summary = self.summary + "\nMean System Capacity 95% CI (during the evaluation time) =  [" + str(round(cinC,5)) + ", " + str(round(meanC,5)) + ", " + str(round(cipC,5)) + "] %"
       
               
        meanA, cinA, cipA = self.meanConfidenceInterval(self.resultsAvail, 0.95)
        self.summary = self.summary + "\nMean System Availability 95% CI (during the evaluation time) =  [" + str(round(cinA,5)) + ", " + str(round(meanA,5)) + ", " + str(round(cipA,5)) + "] "
        #Verificar aqui - Downtime anual ? 
        #self.summary = self.summary + "\nDowntime 95% CI (evaluation time) =  [" + str(round(((1-cipA)*365*24*60),2)) + ", " + str(round(((1-meanA)*365*24*60),2)) + ", " + str(round(((1-cinA)*365*24*60),2)) + "] min"
       
        
        self.summary = self.summary + "\n ---------- \n Pointwise results \n ----------"

        meanCLast = self.resultsCapacity[-1]
        cinCLast = self.resultsCapacityCIN[-1]
        cipCLast = self.resultsCapacityCIP[-1]
               
        self.summary = self.summary + "\nSystem Capacity 95% CI at " + str(self.target) + " h  [" + str(round(cinCLast,5)) + ", " + str(round(meanCLast,5)) + ", " + str(round(cipCLast,5)) + "] %"

        meanALast = self.resultsAvail[-1]
        cinALast = self.resultsAvailCIN[-1]
        cipALast = self.resultsAvailCIP[-1]
               
        self.summary = self.summary + "\nSystem Availability 95% CI at " + str(self.target) + " h  [" + str(round(cinALast,5)) + ", " + str(round(meanALast,5)) + ", " + str(round(cipALast,5)) + "] "

        meanPASLast = self.resultsAtkWOK[-1]
        cinPASLast = self.resultsAtkWOKCIN[-1]
        cipPASLast = self.resultsAtkWOKCIP[-1]
       
        self.summary = self.summary + "\nProbability of Attack Success 95% CI at " + str(self.target) + " h  [" + str(round(cinPASLast,5)) + ", " + str(round(meanPASLast,5)) + ", " + str(round(cipPASLast,5)) + "] "

        
        self.scenario = Scenario(self.migTriggerPlot, meanA, lastElement, meanC, lastElementPAS, self.timeForAtkPlot);
        #self.scenario.printScenario();
        
        self.singleRunEvaluation();
        
        arrayLength = len(self.singleGlobalTime)
        lastElement = self.singleGlobalTime[arrayLength - 1]
        meanAtk, cin, cip = self.meanConfidenceInterval(self.singleAtkProgWOK, 0.95)
        meanCap, cinCap, cipCap = self.meanConfidenceInterval(self.singleCapacity, 0.95)
        self.summary = self.summary + "\n ---------- \nExample run results \n ---------- \nSurvival Time (evaluation time) = " + str(round(lastElement,2)) + " h "
        
        self.summary = self.summary + "\nSystem Capacity 95% CI -while available- (evaluation time) =  [" + str(round(cinCap,2)) + ", " + str(round(meanCap,2)) + ", " + str(round(cipCap,2)) + "] "
        
        
        if (lastElement == self.target):
            self.summary = self.summary + "\nDowntime (evaluation time) = " + str(round(self.downtimeTransient,2)) + "min";
        else:
            downtimeFinal = (self.target - lastElement)*60 + self.downtimeTransient;
            self.summary = self.summary + "\nDowntime (evaluation time) = " + str(round(downtimeFinal,2)) + " min (" + str(round((downtimeFinal/60),2)) + " h)";
        


class SteadyStateEvaluator():

    def __init__(self, _migTrigger, _downtimeParameter):
        self.migTriggerStatic = _migTrigger		
        self.migTrigger = _migTrigger
        self.downtimeParameter = _downtimeParameter 
        self.downtime = 0
        self.accumulatedDowntime = 0
        self.globalTime = 0
        self.warmUpTime = 2000
        self.batchSize = 90
        self.arrAvail = []
        self.dataAvail = 0
        self.availability = 0
        self.row = 0
        self.keep = True;	
        self.arrAvailComp = []
        self.mean = 0
        self.meanCIP = 0
        self.meanCIN = 0
        
        
    def resetVariables(self):
              
        self.migTrigger = self.migTriggerStatic
        self.downtime = 0
        self.accumulatedDowntime = 0
        self.globalTime = 0
        self.warmUpTime = 2000
        self.batchSize = 90
        self.arrAvail = []
        self.dataAvail = 0
        self.availability = 0
        self.row = 0
        self.keep = True;	
        self.arrAvailComp = []
        self.mean = 0
        self.meanCIP = 0
        self.meanCIN = 0

    def getAnnualDowntime(self):

        return (1-self.mean)*365*24*60

		
    def meanConfidenceInterval(self, data, confidence=0.95):
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        return m, m-h, m+h

    def simulation(self, _env):
        self.resetVariables();
        while self.keep: 
            yield _env.timeout(self.migTrigger)
            self.globalTime = self.globalTime + self.migTrigger
            
            self.migTrigger = self.migTriggerStatic	
            generatedDowntime = random.expovariate(1.0/self.downtimeParameter)
            yield _env.timeout(generatedDowntime)
            self.globalTime = self.globalTime + generatedDowntime
            
            self.accumulatedDowntime = self.accumulatedDowntime + generatedDowntime 
            
            
            self.migTrigger = self.migTrigger -  generatedDowntime
            while(self.migTrigger <0):
                self.migTrigger = self.migTrigger + self.migTriggerStatic
            
            if(self.globalTime>self.warmUpTime):
                while self.keep: 
                    yield _env.timeout(self.migTrigger)
                    self.globalTime = self.globalTime + self.migTrigger
                    
                    
                    self.batchSize =  self.batchSize - 1
                    self.migTrigger = self.migTriggerStatic		
                    generatedDowntime = random.expovariate(1.0/self.downtimeParameter)
                    yield _env.timeout(generatedDowntime)
                    self.batchSize = self.batchSize - 1
                    self.globalTime = self.globalTime + generatedDowntime
                    
                    
                    self.accumulatedDowntime =  self.accumulatedDowntime + generatedDowntime 
                    
                    self.migTrigger = self.migTrigger - generatedDowntime
                    while(self.migTrigger <0):
                        self.migTrigger = self.migTrigger + self.migTriggerStatic
                    self.availability = (self.globalTime-self.accumulatedDowntime)/self.globalTime
                    self.arrAvail.append(self.availability)
                    if(self.batchSize <= 0):
                        self.arrAvailComp = self.arrAvail.copy();
                        for x in range(len(self.arrAvailComp)):
                            if(len(self.arrAvailComp)>1):						
                                error = abs(((self.arrAvailComp[0] - self.arrAvailComp[1])/self.arrAvailComp[1])*100)
                                self.arrAvailComp.pop(0)
                                if math.isclose(error, 0, abs_tol=1e-04):	
                                    self.row = self.row + 1
                                if(self.row>30):
                                    self.keep = False
                                    self.mean, self.meanCIN, self.meanCIP = self.meanConfidenceInterval(self.arrAvail, 0.95)
                                    break
								
                        self.row = 0
                        self.batchSize = 90
                        self.arrAvail = [];
				
    def compute(self, envParameter):
        random.seed(a=None, version=2)
        envParameter.process(self.simulation(envParameter))                  	   	
        envParameter.run() 

    def getResults(self):
        return self.mean, self.meanCIP, self.meanCIN 

    def getResultsMean(self):
        return self.mean 
                             
            
if __name__ == '__main__':
    
    mainW = UserInterface()
    mainW.interfaceSelection()

    if mainW.getInterfaceSelection() == 0:
        mainW.show();
    elif mainW.getInterfaceSelection() == 1:
        mainW.showModern();
    else:
        mainW.showXML();
    
    print('app end')
