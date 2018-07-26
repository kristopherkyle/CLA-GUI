from __future__ import division
import Tkinter as tk
import tkFont
import tkFileDialog
import Tkconstants
import os
import re
import sys
import platform
from threading import Thread
import Queue

dataQueue = Queue.Queue()

#This creates the message for the progress box (and puts it in the dataQueue)
progress = "...Waiting for Data to Process"
dataQueue.put(progress)

#Def1 is the core program; args is information from GUI passed to program
def start_thread(def1, arg1, arg2, arg3): 
	t = Thread(target=def1, args=(arg1, arg2, arg3))
	t.start()

if platform.system() == "Darwin":
	system = "M"
	title_size = 16
	font_size = 14
	geom_size = "425x400"
	color = "#de9460"
elif platform.system() == "Windows":
	system = "W"
	title_size = 14
	font_size = 12
	geom_size = "425x400"
	color = "#de9460"
elif platform.system() == "Linux":
	system = "L"
	title_size = 14
	font_size = 12
	geom_size = "425x400"
	color = "#de9460"

class MyApp: #this is the class for the gui and the text analysis
	def __init__(self, parent):
		
		#Creates font styles: Consider changing to Lucida Grande or Helvetica Neue
		helv14= tkFont.Font(family= "Helvetica Neue", size=font_size)
		times14= tkFont.Font(family= "Lucida Grande", size=font_size)
		helv16= tkFont.Font(family= "Helvetica Neue", size = title_size, weight = "bold", slant = "italic")
				#This defines the GUI parent (ish)
		
		self.myParent = parent
		
		#This creates the header text - Task:work with this to make more pretty!
		self.spacer1= tk.Label(parent, text= "Constructed Response Analysis Tool", font = helv16, background = color)
		self.spacer1.pack()
		
		#This creates a frame for the meat of the GUI
		self.thestuff= tk.Frame(parent, background =color)
		self.thestuff.pack()
		
		self.myContainer1= tk.Frame(self.thestuff, background = color)
		self.myContainer1.pack(side = tk.RIGHT, expand= tk.TRUE)

		self.labelframe2 = tk.LabelFrame(self.myContainer1, text= "Instructions", background = color)
		self.labelframe2.pack(expand=tk.TRUE)
		
		#This creates the list of instructions.
		self.instruct = tk.Button(self.myContainer1, text = "Instructions", justify = tk.LEFT)
		self.instruct.pack()
		self.instruct.bind("<Button-1>", self.instruct_mess)

		self.secondframe= tk.LabelFrame(self.myContainer1, text= "Data Input", background = color)
		self.secondframe.pack(expand=tk.TRUE) 

		self.summary_name = ""
		self.summary_button = tk.Button(self.secondframe)
		self.summary_button.configure(text= "Select List Dictionary")
		self.summary_button.pack()
		self.summary_button.bind("<Button-1>", self.get_summary_text)

		self.summarylabel =tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected list dictionary:", background = color)
		self.summarylabel.pack()

		summary_file_name = "(No List Dictionary Chosen)"
		self.summarylabelchosen = tk.Label(self.summarylabel, height= "1", width= "44", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = summary_file_name)
		self.summarylabelchosen.pack()

		#This Places the first button under the instructions.
		self.button1 = tk.Button(self.secondframe)
		self.button1.configure(text= "Select Input Folder")
		self.button1.pack()
		
		#This tells the button what to do when clicked.	 Currently, only a left-click
		#makes the button do anything (e.g. <Button-1>). The second argument is a function
		#That is defined later in the program.
		self.button1.bind("<Button-1>", self.button1Click)
		
		#Creates default dirname so if statement in Process Texts can check to see
		#if a directory name has been chosen
		self.dirname = ""
		
		#This creates a label for the first program input (Input Directory)
		self.inputdirlabel =tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected input folder:", background = color)
		self.inputdirlabel.pack()
		
		#Creates label that informs user which directory has been chosen
		directoryprompt = "(No Folder Chosen)"
		self.inputdirchosen = tk.Label(self.inputdirlabel, height= "1", width= "44", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = directoryprompt)
		self.inputdirchosen.pack()
		
		#This creates the Output Directory button.
		self.button2 = tk.Button(self.secondframe)
		self.button2["text"]= "Select Output Filename"
		#This tells the button what to do if clicked.
		self.button2.bind("<Button-1>", self.button2Click)
		self.button2.pack()
		self.outdirname = ""
		
		#Creates a label for the second program input (Output Directory)
		self.outputdirlabel = tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected output filename:", background = color)
		self.outputdirlabel.pack()
		
		#Creates a label that informs sure which directory has been chosen
		outdirectoryprompt = "(No Output Filename Chosen)"
		self.outputdirchosen = tk.Label(self.outputdirlabel, height= "1", width= "44", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = outdirectoryprompt)
		self.outputdirchosen.pack()

		self.BottomSpace= tk.LabelFrame(self.myContainer1, text = "Run Program", background = color)
		self.BottomSpace.pack()

		self.button3= tk.Button(self.BottomSpace)
		self.button3["text"] = "Process Texts"
		self.button3.bind("<Button-1>", self.runprogram)
		self.button3.pack()

		self.progresslabelframe = tk.LabelFrame(self.BottomSpace, text= "Program Status", background = color)
		self.progresslabelframe.pack(expand= tk.TRUE)
		
		self.progress= tk.Label(self.progresslabelframe, height= "1", width= "45", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text=progress)
		self.progress.pack()
		
		self.poll(self.progress)
	
	def instruct_mess(self, event):
		import tkMessageBox
		tkMessageBox.showinfo("Instructions", "To process your files, please follow these steps: \n\n1. Select the dictionary you would like to use.\n(must be a spreadsheet saved as a tab-delimited text)\n\n2. Choose the input folder (where your files are).\n\n3. Select your output filename\n\n4. Press the 'Process Texts' button.")

	def entry1Return(self,event):
		input= self.entry1.get()
		self.input2 = input + ".csv"
		self.filechosenchosen.config(text = self.input2)
		self.filechosenchosen.update_idletasks()

	def get_summary_text(self, event):
		import tkFileDialog
		self.summary_name = tkFileDialog.askopenfilename()
		self.displaysummary_file = '.../'+self.summary_name.split('/')[-1]
		self.summarylabelchosen.config(text = self.displaysummary_file)

		print self.summary_name
		
	def button1Click(self, event):
		#import Tkinter, 
		import tkFileDialog
		self.dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
		self.displayinputtext = '.../'+self.dirname.split('/')[-1]
		self.inputdirchosen.config(text = self.displayinputtext)


	def button2Click(self, event):
		#self.outdirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
		self.outdirname = tkFileDialog.asksaveasfilename(parent=root, defaultextension = ".csv", initialfile = "results",title='Choose Output Filename')
		print self.outdirname
		if self.outdirname == "":
			self.displayoutputtext = "(No Output Filename Chosen)"
		else: self.displayoutputtext = '.../' + self.outdirname.split('/')[-1]
		self.outputdirchosen.config(text = self.displayoutputtext)
		
	
	def SubmitFilenameButtonClick(self, event):
		input= self.entry1.get()
		self.input2 = input + ".csv"
		self.filechosenchosen.config(text = self.input2)
		
	def runprogram(self, event):
		self.poll(self.progress)
		start_thread(main, self.dirname, self.outdirname, self.summary_name)

	def poll(self, function):
		
		self.myParent.after(10, self.poll, function)
		try:
			function.config(text = dataQueue.get(block=False))
			
		except Queue.Empty:
			pass

def main(indir, outdir, list_dict):		
		
		import tkMessageBox
		if list_dict is "":
			tkMessageBox.showinfo("Choose List Dictionary!", "Choose List Dictionary!")
		if list_dict[-4:] != ".txt":
			tkMessageBox.showinfo("Dictionary Must Be .txt!", "Your dictionary file must be a tab-delimited .txt!")
		#if self.dirname not in r'*.txt':
			#tkMessageBox.showinfo("Dictionary must be a text file!","Dictionary must be a text file!")
		if indir is "":
			tkMessageBox.showinfo("Supply Information", "Choose Input Directory")
		
		if outdir is "":
			tkMessageBox.showinfo("Choose Output Directory", "Choose Output Directory")
		if indir is not "" and outdir is not "" and list_dict[-4:] == ".txt":
			
			#Analyze Custom List_3 - Kris Kyle 11-10-13
			import glob
			import re

			inputfile = indir + "/*.txt"
			filenames = glob.glob(inputfile)

			variable_spreadsheet = file(list_dict, 'rU').read().split("\n")

			variable_dict = {}
			variable_regex_dict={}
			variable_ngram_regex_dict={}
			variable_list = []

			nvariables = 0
			nlists=0
			
			for line in variable_spreadsheet:
				if line is not "":
					nlists+=1
				else:
					break
			
			for i in range(nlists):
				variable_list.append("")
				
			for line in variable_spreadsheet:
				list = []
				regex_list = []
				ngram_regex_list = []
				
				if nvariables > (nlists-1):
					break
				else:
					entries = line.split("\t")
					for items in entries[1:]:
						if items == "":
							continue
						if items[0] == '*' and items[-1] == '*':
							regex_list.append(re.compile(r'\b.*?' + items[1:-1] + r'.*?\b', re.IGNORECASE))
						elif items[-1] == '*':
							regex_list.append(re.compile(r'\b' + items[0:-1] + r'.*?\b', re.IGNORECASE))
						elif items[0] == '*':
							regex_list.append(re.compile(r'\b.*?' + items[1:] + r'\b', re.IGNORECASE))
						elif '*' not in items and " " not in items:
							list.append(items)
						elif '*' not in items and " " in items:
							ngram_regex_list.append(re.compile(r'\b' + items + r'\b', re.IGNORECASE))
				
				variable_list[nvariables]=entries[0]
				variable_dict[entries[0]] = list
				variable_regex_dict[entries[0]] = regex_list
				variable_ngram_regex_dict[entries[0]] = ngram_regex_list
				nvariables+=1

			output = """filename, nwords,"""
			
			for i in range(nlists):
				output = output + variable_list[i] + ','
			output = output + '\n'
				
			outf=file(outdir, "w")
			outf.write(output)


			def regex_count(dict, ngram_dict, regex_dict, key, text, clean_text):
				punctuation = (".","!","?",",",":",";", "'",'"')
				if key == "":
					blank = ""
					return blank
				else:
					counter = 0
					nwords = len(text.split())
					for item in regex_dict[key]:
						if item == "":
							continue
						counter+= len(re.findall(item, text))
							
					for item in ngram_dict[key]:
						if item == "":
							continue
						counter+= len(re.findall(item, text))
						
					for word in clean_text:
						if word == "":
							continue
						if word[-1] in punctuation:
							word = word[:-1]
						if word in dict[key]:
							counter+=1
					return counter/nwords

			n_filenames = len(filenames)
			progress = 0
			for filename in filenames:
				if system == "M" or system == "L":
					simple_filename = filename.split("/")[-1]
				if system == "W":
					simple_filename = filename.split("\\")[-1]
				
				progress += 1
				update_string  = "Processing: " + str(progress) + " of " + str(n_filenames) + " files"
				dataQueue.put(update_string)
				root.update_idletasks()
				
				text= file(filename, 'rU').read()
				clean_text = re.sub('.', ' ', text)
				clean_text = re.sub("  ", " ", text)
				clean_text = text.lower().split()
				nwords = len(clean_text)
				
				Var = []
				outnumbers='{0}, {1}, {2} \n'
				
				for i in range(nlists):
					Var.append(regex_count(variable_dict, variable_ngram_regex_dict, variable_regex_dict, variable_list[i], text, clean_text))
			
				Var = ''.join(str(Var))
				Var = Var[1:-1]
				outf.write (outnumbers
				.format(simple_filename, nwords, Var))

			outf.flush()#flushes out buffer to clean output file
			outf.close()#close output file    
		
			#Closing Message to let user know that the program did something: (may need to be more sophisticated)	
			nfiles = len(filenames)
			finishmessage = ("Processed " + str(nfiles) + " Files")
			dataQueue.put(finishmessage)
			root.update_idletasks()
			if system == "M":
				tkMessageBox.showinfo("Finished!", "Your files have been processed by CLA!")

class Catcher:
    def __init__(self, func, subst, widget):
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        try:
            if self.subst:
                args = apply(self.subst, args)
            return apply(self.func, args)
        except SystemExit, msg:
            raise SystemExit, msg
        except:
            import traceback
            import tkMessageBox
            ermessage = traceback.format_exc(1)
            ermessage = re.sub(r'.*(?=Error)', "", ermessage, flags=re.DOTALL)
            ermessage = ermessage + "There was a problem processing your files.\nThis is usually do to non-ASCII characters in your files.\nPlease clean your files and try again."
            #tkMessageBox.showerror("Error Message", "There was a problem running your files\nPlease make sure your files only include ASCII characters")
            tkMessageBox.showerror("Error Message", ermessage)
            #traceback.print_exc()
		
root = tk.Tk()
root.wm_title("Custom List Analyzer V.1.1")
root.configure(background = color)
root.geometry(geom_size)

tk.CallWrapper = Catcher
myapp = MyApp(root)
root.mainloop()

