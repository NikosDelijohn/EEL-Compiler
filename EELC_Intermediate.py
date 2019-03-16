# + ------------------------- + #
# Deligiannis Nikos 2681        #
# UoI - Spring Semester 2018    #
# 		CSE Department          #
# Compilers MYY802 prof G.Manis #
# Project: Compiler for EEL     #
# + ------------------------- + #

import sys
import signal
import os

# Just in case someone is curious!
def handler(signum, frame):
  print ("\n")
  print (Colors.HIGHL + "Compilation shall not be stopped" + Colors.RESET)
  print ("\n")


# [PHASE: 1] :: Lexical and Syntactical Analysis 	Due 14/3/2018
# [PHASE: 2] :: Intermediate Code Generation 	 		Due 18/4/2018

#Classes
class Colors:
  RED   	= "\033[1;31m"  
  BLUE  	= "\033[1;34m"
  CYAN  	= "\033[1;36m"
  GREEN 	= "\033[0;32m"
  YELLOW	= "\033[93m"
  BOLD    = "\033[;1m"
  RESET 	= "\033[0;0m"
  HIGHL 	= "\033[;7m"

class Quad:

	def __init__(self, label, op, arg_1, arg_2, res):

		self.label	= label 
		self.op   	= op
		self.arg_1 	= arg_1
		self.arg_2 	= arg_2
		self.res 	= res

	def __str__(self):

		return "(" + str(self.label) + ": " + str(self.op) + ", " + str(self.arg_1) + ", " \
			+ str(self.arg_2) + ", " + str(self.res) + ")" 


# + ------------------------------------ + #
# 										   #														
#	  Global Variables Declaration 		   #
#										   #
# + ------------------------------------ + #

token_dict = dict(alphaTK  = 1,  # Alpharithmetic - String (e.g Compiler)
                  numberTK = 2,  # Any Number (e.g 65)
                  plusTK   = 3,  # +
                  minusTK  = 4,  # -
                  mulTK    = 5,  # *
                  divTK    = 6,  # /
                  lessTK   = 7,  # <
                  greaTK   = 8,  # >
                  leqTK    = 9,  # <= 
                  greqTK   = 10, # >= 
                  eqTK     = 11, # =
                  difTK    = 12, # <>
                  assigTK  = 13, # :=
                  semiTK   = 14, # ;
                  commaTK  = 15, # , 
                  colonTK  = 16, # :
                  lbrTK    = 17, # (
                  rbrTK    = 18, # )
                  blbrTK   = 19, # [
                  brbrTK   = 20, # ]
                  #Commited Words#
                  progTK   = 100, # program
                  eprogTK  = 101, # endprogram
                  decTK    = 102, # declare
                  edecTK   = 103, # enddeclare
                  ifTK     = 104, # if
                  thenTK   = 105, # then
                  elseTK   = 106, # else
                  eifTK    = 107, # endif
                  whileTK  = 108, # while
                  ewhileTK = 109, # endwhile
                  repTK    = 110, # repeat
                  erepTK   = 111, # endrepeat
                  exitTK   = 112, # exit
                  swiTK    = 113, # switch
                  caseTK   = 114, # case
                  eswiTK   = 115, # endswitch
                  fcaseTK  = 116, # forcase
                  whenTK   = 117, # when
                  efcaseTK = 118, # endforcase
                  procTK   = 119, # procedure
                  eprocTK  = 120, # endprocedure
                  funTK    = 121, # function
                  efunTK   = 122, # endfunction
                  callTK   = 123, # call
                  retTK    = 124, # return
                  inTK     = 124, # in 
                  inoutTK  = 125, # inout
                  andTK    = 126, # and
                  orTK     = 127, # or
                  notTK    = 128, # not 
                  trueTK   = 129, # true 
                  falseTK  = 130, # false
                  inputTK  = 131, # input
                  printTK  = 132, # print 
                  #Special Tokens#
                  eofTK    = 200, # End of File
                  errTK    = 201, # Error         || Won't be used
                  cmtTK    = 202) # Comment(s)    || Won't be used

max_word_size = 30  	# An Alpharithmetic can't be over 30 char's long
line          = 1   	# The current line (used for debugging messages)
ret_token     = 0   	# The token lex() will return
lex_unit      = ""  	# The lexical unit lex() will return
label_cc 			= 0			# The counter for the label generation/showcase
tmp_cc 				= 0 		# The counter for the tmp unique var generation
code_quads 		= list()# The list of the program stored in quads
program_name 	="" 	 	# The name of the main program				
to_ansi_c_problem = 0 # Used to display Error messages during Int ansi c generation
eel_source_code ="" 	# The source code filename
global code         	# File pointer of the Source Code



# + ------------------------------------ + #
# 										   #														
#	 Intermediate Code Related Funcs	   #
#										   #
# + ------------------------------------ + #

# Shows (does not alter) the next label value (string format)
def next_quad():

	global label_cc
	return str(label_cc)

# Generates a new Quad and increases the label_cc value by 1
def gen_quad(op, x, y, res):

	global label_cc
	global code_quads

	tmp_label = label_cc
	label_cc = label_cc + 1
	ret_quad = Quad(str(tmp_label), str(op), str(x), str(y), str(res))
	code_quads.append(ret_quad)
	
	return ret_quad

# Generates a new unique temp variable that will be used for the intermediate code generation
def new_temp():

	global tmp_cc

	ret_tmp = "T_"+str(tmp_cc)

	tmp_cc = tmp_cc + 1

	return ret_tmp

# Returns an empty list
def empty_list():

	return list()

# Generates and returns a list with one item in it
def make_list(item):

	ret_list = list()
	ret_list.append(item)

	return ret_list

# Merges the two lists
def merge_list(list_a, list_b):

	if list_a and list_b : 

		ret_list = list_a + list_b
		return ret_list

	elif list_a and not list_b:

		ret_list = list_a
		return list_a

	elif list_b and not list_a:

		ret_list = list_b
		return list_b

# For every quad in quadlist alters the .res field into res
def back_patch(quadlist, res):

	global code_quads

	if quadlist:
		
		for quad in code_quads:
		
			if quad.label in quadlist:

				quad.res = res

# + ------------------------------------ + #
# 			                               #											
#				Error Display & 		   #
#		File Generation Related Funcs	   #
#										   #
# + ------------------------------------ + #

#Used by everyone for errors
def error_display(arg,output,line):

	if(arg == 1):		#Lex Related Error Display
		print('[' + Colors.RED 	+ "LexError" + Colors.RESET + ']')
		print(Colors.BOLD + output + Colors.RESET)
		print(Colors.BLUE	+ "Error spotted ~at line: " + str(line) + Colors.RESET)
	elif(arg == 2): #Lex, Comments - EOF Related Error Display
		print('[' + Colors.RED 	+ "LexError" + Colors.RESET + ']')
		print(Colors.BOLD + output + Colors.RESET)
		print(Colors.BLUE	+ "Comments start ~at Line: " + str(line) + Colors.RESET)
	elif(arg == 3): #Syn Related Error Display
		print('[' + Colors.GREEN + "SynError" + Colors.RESET + ']')
		print(Colors.BOLD + output + Colors.RESET)
		print(Colors.BLUE + "Error spotted ~at line: " + str(line) + Colors.RESET)
	elif(arg == 4): #IOError
		print('[' + Colors.CYAN + "IOError" + Colors.RESET + ']')
		print(Colors.BOLD + output + Colors.RESET)


def generate_intermediate_int():

	global code_quads
	global eel_source_code

	file = str(eel_source_code).split('.')[0]+".int"
	int_file = open(file,"w")

	int_file.write("This file was generated automatically from EEL Compiler.\n")
	int_file.write("Intermediate code in quadruples of " + "\"" + eel_source_code + "\".\n\n")

	for quad in code_quads:

		int_file.write(str(quad))
		int_file.write("\n")

	int_file.close()

# Creates the ANSI C equivalent of a quadruple
def to_ansi_c(quad):

	global progam_name
	global to_ansi_c_problem 

	ret_str = ""

	if quad.op == "begin_block":

		if quad.res == program_name:

			ret_str = "void main()\n{"
			declare = find_declarations()
			ints 		= make_declare_string(declare)
			ret_str = ret_str + ints + "\n\tL_" + quad.label + ": "

		else: #Problem here. This won't work

			to_ansi_c_problem = 1

	elif quad.op == "halt" :

		ret_str = "\tL_" + quad.label + ": exit(0);" 

	elif quad.op == "end_block":

		ret_str = "\tL_" + quad.label + ": {}\n}\n"

	elif quad.op == ":=" :

		ret_str = "\tL_" + quad.label + ": " + quad.res + " = " + quad.arg_1 + ";"

	elif quad.op in ("+","-","*","/"):

		ret_str = "\tL_" + quad.label + ": " + quad.res + " = " + quad.arg_1 + " " + \
		quad.op + " " + quad.arg_2 + ";"

	elif quad.op in ("<>", "=", "<", ">", "<=", ">="):

		if 		quad.op == "<>": relop = "!="
		elif  quad.op == "=" : relop = "=="
		else: relop = quad.op

		ret_str = "\tL_" + quad.label + ": if ( " + quad.arg_1 + " " + relop + " " + \
		quad.arg_2 + " ) goto L_" + quad.res + ";" 

	elif quad.op == "jump":

		ret_str = "\tL_" + quad.label + ": goto L_" + quad.res + ";" 

	elif quad.op == "return":

		ret_str = "\tL_" + quad.label + ": return (" + quad.arg_1 + " );"

	elif quad.op == "print":

		ret_str = "\tL_" + quad.label + ': printf( "'+str(quad.arg_1)+' %d\\n" , ' + quad.arg_1 + " );"

	elif quad.op == "input":
	
		ret_str = "\tL_" + quad.label + ': printf("Input: '+str(quad.arg_1)+' ");'+' scanf( " %d", &' + quad.arg_1 + " );" + \
							" if ( ( " + quad.arg_1 + " < -32767 ) || ( " + quad.arg_1 + " > +32767 ) ) " + \
						  " { puts(\"[Error]: Too large/small number ( |Number| <= 32767 ) \"); exit(0); } "
	elif quad.op == "call": #Problem here. This won't work

		to_ansi_c_problem = 1 

	return ret_str

# Finds which variables to declare in C file
def find_declarations():

	global code_quads

	ret_list = []

	for quad in code_quads:

		if quad.op != "call" and quad.op != "begin_block" and quad.arg_2 not in ("in","inout","ret"):
			if quad.op == "end_block" : break
			if isinstance(quad.arg_1,str) and not quad.arg_1.isdigit() and quad.arg_1 not in ret_list: ret_list.append(quad.arg_1)
			if isinstance(quad.arg_2,str) and not quad.arg_2.isdigit() and quad.arg_2 not in ret_list: ret_list.append(quad.arg_2)
			if isinstance(quad.res 	,str) and not quad.res.isdigit()   and quad.res   not in ret_list: ret_list.append(quad.res)

	for pos in ret_list:

		if pos == "_" : ret_list.remove(pos)

	ret_list.sort()

	return ret_list

# Create the declaration string of integers
def make_declare_string(declare):

	ret_string = "int "

	for var in declare:

		ret_string = ret_string + var + ","

	ret_string = "\n\t" + ret_string[:-1] + ";" #Cut the last comma
	return ret_string 

# Create the C file
def generate_intermediate_ansi_c():

	global code_quads
	global eel_source_code

	file = str(eel_source_code).split('.')[0]+".c"
	c_file = open(file,"w")

	c_file.write("/*\n * This file was generated automatically from EEL Compiler. \n")
	c_file.write(" * This is the equivalent Code in ANSI C of " + "\"" + eel_source_code + "\". \n */\n")
	c_file.write("#include <stdio.h>\n#include <stdlib.h>\n\n")

	declare = find_declarations()
		
	for quad in code_quads:

		equiv = to_ansi_c(quad)
		
		if equiv: 

			c_file.write(equiv + " \n")

	c_file.write("\n/* Equivalent Quads \n")
	for quad in code_quads:

		c_file.write(" * " + str(quad) + "\n")

	c_file.write(" */")

	c_file.close()


# + ------------------------------------ + #
# 										   #														
#	   Lexical Analysis Related Funcs      #
#										   #
# + ------------------------------------ + #

def backtrack():

  global code
  position = code.tell()
  code.seek(position - 1)

def lex():

  global lex_unit 
  lex_unit = "" 
  global line         
  global ret_token
  global code

  while True:

    unit = code.read(1)
    
    if not unit       : 
      
      break # EOF reached break the loop.
  
    if unit == '\n'   : line = line + 1 

    if unit == '\t'   : continue # Ignore TABs

    if unit.isspace() : continue

  # -------------------[State 1 of the FSM]------------------- #
  # -Character found. Keep reading until you read him whole    #
  # -Check for commited words. Else return alphaTK.            #
  # -Must be <= 30 characters long.                            #
  # -IMPORTANT: Backtrack is required after while()            #
  # ---------------------------------------------------------- #
  
    if unit.isalpha(): 

      alpha_flag = 0
      lex_unit = lex_unit + unit

      unit = code.read(1)

      while ( (unit.isalpha() or unit.isdigit() ) and len(lex_unit) <= max_word_size ):

        lex_unit = lex_unit + unit

        unit = code.read(1)

      if unit == '\n' : line = line + 1

      if(lex_unit != "endprogram"): #and unit != '\n'):
        backtrack()

      if lex_unit == "program":
        ret_token = token_dict["progTK"]
        return token_dict["progTK"]
      if lex_unit == "endprogram":
        ret_token = token_dict["eprogTK"]
        return token_dict["eprogTK"]
      if lex_unit == "declare":
        ret_token = token_dict["decTK"]
        return token_dict["decTK"]
      if lex_unit == "enddeclare":
        ret_token = token_dict["edecTK"]
        return token_dict["edecTK"]
      if lex_unit == "if":
        ret_token = token_dict["ifTK"]
        return token_dict["ifTK"]          
      if lex_unit == "then":
        ret_token = token_dict["thenTK"]
        return token_dict["thenTK"]
      if lex_unit == "else":
        ret_token = token_dict["elseTK"]
        return token_dict["elseTK"]
      if lex_unit == "endif":
        ret_token = token_dict["eifTK"]
        return token_dict["eifTK"]
      if lex_unit == "while":
        ret_token = token_dict["whileTK"]
        return token_dict["whileTK"]
      if lex_unit == "endwhile":
        ret_token = token_dict["ewhileTK"]
        return token_dict["ewhileTK"]
      if lex_unit == "repeat":
        ret_token = token_dict["repTK"]
        return token_dict["repTK"]
      if lex_unit == "endrepeat":
        ret_token = token_dict["erepTK"]
        return token_dict["erepTK"]
      if lex_unit == "exit":
        ret_token = token_dict["exitTK"]
        return token_dict["exitTK"]
      if lex_unit == "switch":
        ret_token = token_dict["swiTK"]
        return token_dict["swiTK"]
      if lex_unit == "case":
        ret_token = token_dict["caseTK"]
        return token_dict["caseTK"]
      if lex_unit == "endswitch":
        ret_token = token_dict["eswiTK"]
        return token_dict["eswiTK"]
      if lex_unit == "forcase":
        ret_token = token_dict["fcaseTK"]
        return token_dict["fcaseTK"]
      if lex_unit == "when":
        ret_token = token_dict["whenTK"]
        return token_dict["whenTK"]
      if lex_unit == "endforcase":
        ret_token = token_dict["efcaseTK"]
        return token_dict["efcaseTK"]
      if lex_unit == "procedure":
        ret_token = token_dict["procTK"]
        return token_dict["procTK"]
      if lex_unit == "endprocedure":
        ret_token = token_dict["eprocTK"]
        return token_dict["eprocTK"]
      if lex_unit == "function":
        ret_token = token_dict["funTK"]
        return token_dict["funTK"]
      if lex_unit == "endfunction":
        ret_token = token_dict["efunTK"]
        return  token_dict["efunTK"]
      if lex_unit == "call":
        ret_token = token_dict["callTK"]
        return token_dict["callTK"]
      if lex_unit == "return":
        ret_token = token_dict["retTK"]
        return token_dict["retTK"]
      if lex_unit == "in":
        ret_token = token_dict["inTK"]
        return token_dict["inTK"]
      if lex_unit == "inout":
        ret_token = token_dict["inoutTK"]
        return token_dict["inoutTK"]
      if lex_unit == "and":
        ret_token = token_dict["andTK"]
        return token_dict["andTK"]
      if lex_unit == "or":
        ret_token = token_dict["orTK"]
        return token_dict["orTK"]
      if lex_unit == "not":
        ret_token = token_dict["notTK"]
        return token_dict["notTK"]
      if lex_unit == "true":
        ret_token = token_dict["trueTK"]
        return token_dict["trueTK"]
      if lex_unit == "false":
        ret_token = token_dict["falseTK"]
        return token_dict["falseTK"]
      if lex_unit == "input":
        ret_token = token_dict["inputTK"]
        return token_dict["inputTK"]
      if lex_unit == "print":
        ret_token = token_dict["printTK"]
        return token_dict["printTK"]

      ret_token = token_dict["alphaTK"] #Default case, its an alpharithmetic (e.g. variableA)
      return token_dict["alphaTK"]

  # -------------------[State 2 of the FSM]------------------- #
  # -Digit is found. Read the whole number!                    #
  # -Constrains:  A. number <= 32767                           #
  #               B. alphabetics not allowed after digit       #
  # -IMPORTANT: Backtrack is required at the end!              #
  # ---------------------------------------------------------- #

    if unit.isdigit():

      lex_unit = lex_unit + unit

      unit = code.read(1)

      while (unit.isdigit()):

        lex_unit = lex_unit + unit

        unit = code.read(1)

      if unit == '\n' : line = line + 1

      if(unit.isalpha()):               
      	error = "Found \"" + lex_unit + unit + "\"." + " A number must not be followed by character(s)."
      	error_display(1,error,line)
        exit()

      tmp_num = int(lex_unit) #Grammar will provide the sign 
      if tmp_num > 32767:                        
        error = "Found \"" + str(tmp_num) + "\"." + " Maximum allowed integer value is 32767."
        error_display(1,error,line)
        exit()

      backtrack()
      ret_token = token_dict["numberTK"]
      return token_dict["numberTK"]

    if unit == '+':
      
      lex_unit = lex_unit + unit
      ret_token = token_dict["plusTK"]
      return token_dict["plusTK"]

    if unit == '-':

      lex_unit = lex_unit + unit
      ret_token = token_dict["minusTK"]
      return token_dict["plusTK"]

  # -------------------[State 3 of the FSM]------------------- #
  # -Symbol '*' found. Must see what follows in case of error! #
  # -If what follows is '/' then error (closing comments)      #
  # -else return '*' + token                                   #
  # -IMPORTANT: Backtrack is required at the end!              #
  # ---------------------------------------------------------- #

    if unit == '*':

      lex_unit = lex_unit + unit
      
      unit = code.read(1)

      if unit == '/':
      	error = "Found \"" + lex_unit + unit + "\"." + " A comment section was not initialized \"/*\"."
      	error_display(1,error,line)
        exit()

      backtrack()
      ret_token = token_dict["mulTK"]
      return token_dict["mulTK"]

    if unit == ',':
      lex_unit = lex_unit + unit
      ret_token = token_dict["commaTK"]
      return token_dict["commaTK"]

  # -------------------[State 4 of the FSM]------------------- #
  # -Symbol '/' found. Must see what follows!                  #
  # -Three possible scenarios to begin with                    #
  #     [A]: /*  Comment initializer                           #
  #     [B]: //  Comment until new line                        #
  #     [C]: /   Division operator                             #
  # -IMPORTANT: Backtrack is required in case [C]              #
  # -IMPORTANT: In case of comments, lex() has call itself     #
  #             to return the next lex_unit and token!!        #
  # ---------------------------------------------------------- #

    if unit == '/':

      lex_unit = lex_unit + unit

      unit = code.read(1)

      if unit == '*':          

        tmp_flag = 0

        tmp_err = line # Used in case of an error!

        while(tmp_flag == 0):

          unit = code.read(1)

          if unit == '\n': line = line + 1

          if unit == '*':

            unit = code.read(1)

            if not unit : # Reached EOF without closing comments
              error = "Reached EOF while reading comments. A comment section was not terminated"
              error_display(2,error,tmp_err)
              exit()

            if(unit == '/') : tmp_flag = 1

          if not unit : # Reached EOF without closing comments
           	error = "Reached EOF while reading comments. A comment section was not terminated"
           	error_display(2,error,tmp_err)
          	exit()

        return lex() #Recursively provide the next unit                     


      elif unit == '/':                       
        tmp_flag = 0

        while(tmp_flag == 0):

          unit = code.read(1)

          if unit == '\n': tmp_flag = 1 

        return lex() #Recursively provide the next unit

      else:                                   

        backtrack()
        ret_token = token_dict["divTK"]
        return token_dict["divTK"]

    if unit == '=':

      lex_unit = lex_unit + unit
      ret_token = token_dict["eqTK"]
      return token_dict["eqTK"]

    if unit == ';':

      lex_unit = lex_unit + unit
      ret_token = token_dict["semiTK"]
      return token_dict["semiTK"]

    if unit == '(':

      lex_unit = lex_unit + unit
      ret_token = token_dict["lbrTK"]
      return token_dict["lbrTK"]

    if unit == ')':

      lex_unit = lex_unit + unit
      ret_token = token_dict["rbrTK"]
      return token_dict["rbrTK"]

    if unit == '[':

      lex_unit = lex_unit + unit
      ret_token = token_dict["blbrTK"]
      return token_dict["blbrTK"]

    if unit == ']':

      lex_unit = lex_unit + unit
      ret_token = token_dict["brbrTK"]
      return token_dict["brbrTK"]
    
  # -------------------[State 5 of the FSM]------------------- # 
  # -Symbol ':' found. We must check if:                       #
  #     [A]: Symbol '=' follows                                #
  #     [B]: alphabetical or digit follows                     #
  # -IMPORTANT: Backtrack required for [B]!                    #
  # ---------------------------------------------------------- #

    if unit == ':':

      lex_unit = lex_unit + unit

      unit = code.read(1)

      if unit == '=':         

        lex_unit = lex_unit + unit
        ret_token = token_dict["assigTK"]
        return token_dict["assigTK"]

      backtrack()
      ret_token = token_dict["colonTK"]
      return token_dict["colonTK"]

  # -------------------[State 6 of the FSM]------------------- #
  # -Symbol '<' found. We must check again if:                 #
  #     [A]: Symbol '=' follows (lower equal operator '<=')    #
  #     [B]: Symbol '>' follows (different operatior  '<>')    #
  #     [C]: else (lower operator '<')                         #
  # -IMPORTANT: Backtrack required for [C]!                    #
  # ---------------------------------------------------------- #

    if unit == '<':

      lex_unit = lex_unit + unit

      unit = code.read(1)

      if unit == "=":    

        lex_unit = lex_unit + unit
        ret_token = token_dict["leqTK"]
        return token_dict["leqTK"]

      if unit == ">":     

        lex_unit = lex_unit + unit
        ret_token = token_dict["difTK"]
        return token_dict["difTK"]

      backtrack()
      ret_token = token_dict["leqTK"]
      return token_dict["leqTK"]

  # -------------------[State 7 of the FSM]------------------- #
  # -Symbol '>' found. We must check if:                       #
  #     [A]: Symbol '=' follows (greater equal operator '>=')  #
  #     [B]: else (greater operator '>')                       #
  # -IMPORTANT: Backtrack required for [B]                     #
  # ---------------------------------------------------------- #

    if unit == '>':

      lex_unit = lex_unit + unit

      unit = code.read(1)

      if unit == "=":     
        lex_unit = lex_unit + unit
        ret_token = token_dict["greqTK"]
        return token_dict["greqTK"]

      backtrack()
      ret_token = token_dict["greaTK"]
      return token_dict["greaTK"]

 # -------------------[State 8 of the FSM]------------------- #    
 # -Uknown symbol found. Error!                               #
 # ---------------------------------------------------------- #

    error = "Found \"" + unit + "\". Uknown character or symbol."
    error_display(1,error,line)
    exit()

  lex_unit = "EOF"
  ret_token = token_dict["eofTK"]
  return token_dict["eofTK"]

# + ------------------------------------ + #
# 																				 #														
#				Syntactical Analysis &						 #
#			Intermediate Code Generation			 	 #
#																					 #
# + ------------------------------------ + #

# -- <PROGRAM> ::= PROGRAM ID <BLOCK> ENDPROGRAM -- # [SYN: Done]
def PROGRAM():
  
  global ret_token
  global program_name
  global line

  name = None 

  if ret_token == token_dict["progTK"]:

    lex()

    if ret_token == token_dict["alphaTK"]:

      program_name = name = lex_unit
      lex()

      BLOCK(name)
      
      if ret_token == token_dict["eprogTK"]:
        
        lex()	# EOF is expected

        if ret_token == token_dict["eofTK"]:

        	pass #EOF reached

      else:
      	error = "Expected \"endprogram\". Instead found \"" + lex_unit +"\"."
      	error_display(3,error,line)
        exit()

    else:
    	error = "Expected program name after \"program\". Instead found \"" + lex_unit + "\"."
    	error_display(3,error,line)
    	exit()

  else:
    error = "Expected \"program\". Instead found \"" + lex_unit + "\"."
    error_display(3,error,line)
    exit()

# -- <BLOCK> ::= <DECLARATIONS><SUBPROGRAMS><STATEMENTS> -- # [SYN: Done, INT: Done]
def BLOCK(name):

	global program_name
	global line

	DECLARATIONS()
	SUBPROGRAMS()
	gen_quad("begin_block","_","_",name)
	STATEMENTS()
	if name == program_name: 
  		gen_quad("halt","_","_","_")
	gen_quad("end_block","_","_",name)

# -- <DECLARATIONS> ::= e | DECLARE <VARLIST> ENDDECLARE -- # [SYN: Done]
def DECLARATIONS():
  
  global ret_token
  global line

  if ret_token == token_dict["decTK"]:

    lex()

    VARLIST()               

    if ret_token == token_dict["edecTK"]:

      lex()
 
    else:
      error = "Expected \"enddeclare\". Instead found \"" + lex_unit + "\". \
      \nPerhaps you missed a \",\" ?"
      error_display(3,error,line)
      exit()

  # e : No Declarations is acceptable

# -- <VARLIST> ::= e | ID (, ID)* -- # [SYN: Done]
def VARLIST():

  global ret_token
  global line

  if ret_token == token_dict["alphaTK"]:

    lex()

    while(ret_token == token_dict["commaTK"]):

      lex()
      
      if ret_token == token_dict["alphaTK"]:

        lex()   
        
      else:
      	error = error = "Expected variable name after \",\"." + " Instead found \"" + lex_unit + "\"."
      	error_display(3,error,line)
        exit()

  # e : No Variables is acceptable

# -- <SUBPROGRAMS> ::= (<PROCORFUNC>)* -- # [SYN: Done]
def SUBPROGRAMS():

  global ret_token
  global line

  #Sneak Peek
  while(ret_token == token_dict["procTK"] or ret_token == token_dict["funTK"]):

    PROCORFUNC()

  # e : Kleene-Star includes e! So missing Function or Procedure is acceptable

# -- <PROCORFUNC> ::= PROCEDURE ID <PROCORFUNCBODY> ENDPROCEDURE | 
#                     FUNCTION ID <PROCORFUNCBODY> ENDFUNCTION -- # [SYN: Done]
def PROCORFUNC():

  global ret_token
  global line
  toPROCORFUNCBODY = None

  if ret_token == token_dict["procTK"]:

    lex()

    if ret_token == token_dict["alphaTK"]:

      toPROCORFUNCBODY = lex_unit
      lex()
      
      PROCORFUNCBODY(toPROCORFUNCBODY)
      
      if ret_token == token_dict["eprocTK"]:

        lex()

      else:
      	error = "Expected \"endprocedure\". Instead found \"" + lex_unit +"\"." 
        error_display(3,error,line)
        exit()

    else:
    	error = "Expected procedure name after \"procedure\". Instead found \"" + lex_unit +"\"." 
    	error_display(3,error,line)
    	exit()

  # No need to display an error message. If there was no procedure Token we wouldn't be here.

  elif ret_token == token_dict["funTK"]:

    lex()
    
    if ret_token == token_dict["alphaTK"]:

      toPROCORFUNCBODY = lex_unit
      lex()

      PROCORFUNCBODY(toPROCORFUNCBODY)

      if ret_token == token_dict["efunTK"]:

        lex()

      else:
      	error = "Expected \"endfunction\". Instead found \"" + lex_unit +"\"." 
        error_display(3,error,line)
        exit()

    else:
    	error = "Expected function name after \"function\". Instead found \"" + lex_unit +"\"." 
    	error_display(3,error,line)
    	exit()
  # No need to display an error message. If there was no function Token we wouldn't be here.

# -- <PROCORFUNCBODY() ::= <FORMALPARS> <BLOCK> -- # [SYN: Done]
def PROCORFUNCBODY(name):

	global line

	FORMALPARS(name)
	BLOCK(name)

# -- <FORMALPARS> ::= (<FORMALPARLIST>) -- # [SYN: Done]
def FORMALPARS(name):

  global ret_token
  global line

  if ret_token == token_dict["lbrTK"]:

    lex()

    FORMALPARLIST(name)

    if ret_token == token_dict["rbrTK"]:

      lex()
      
    else:
    	error = "Expected \")\" after parameter declarations. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

  else:
  	error = "Expected \"(\" before parameter declarations. Instead found \"" + lex_unit +"\"."
  	error_display(3,error,line)
  	exit() 

# -- <FORMALPARLIST> ::= <FORMALPARITEM> (, <FORMALPARITEM> )* | e -- # [SYN: Done]
def FORMALPARLIST(fp_name):

  global ret_token
  global line

  # Sneak Peek
  if (ret_token == token_dict["inTK"] or ret_token == token_dict["inoutTK"]):

    FORMALPARITEM(fp_name)

    while(ret_token == token_dict["commaTK"]):

      lex()

      FORMALPARITEM(fp_name)

      if ret_token == token_dict["alphaTK"]: # Can be exploited! Will be Catched and Displayed "above"
      	error = "Expected \"in\" or \"inout\" for parameter declaration. Instead found \"" + lex_unit +"\"."
      	error_display(3,error,line)
      	exit()

  elif (ret_token == token_dict["alphaTK"]): # Can be exploited! Will be Catched and Displayed "above"
  	error = "Expected \"in\" or \"inout\" for parameter declaration. Instead found \"" + lex_unit +"\"."
  	error_display(3,error,line)
  	exit()

  # e : Not deremining parameters is acceptable.

# -- <FORMALPARITEM> ::= IN ID | INOUT ID -- # [SYN: Done]
def FORMALPARITEM(fp_name):

  global ret_token
  global line

  if ret_token == token_dict["inTK"]:

    lex()

    if ret_token == token_dict["alphaTK"]:

      lex()
      
    else:
    	error = "Expected variable name after \"in\". Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit() 

  elif ret_token == token_dict["inoutTK"]:

    lex()

    if ret_token == token_dict["alphaTK"]:

      lex()

    else:
    	error = "Expected variable name after \"in\". Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

# -- <STATEMENTS> ::= <STATEMENT> (;<STATEMENT>)* -- #
def STATEMENTS():

  global ret_token
  global line
  to_exit_if_exit = []

  is_exit = STATEMENT()
  if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit,is_exit)

  while ret_token == token_dict["semiTK"]:

    lex()

    is_exit = STATEMENT()
    if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)

  if ret_token == token_dict["alphaTK"] or \
  	 ret_token == token_dict["ifTK"] 		or \
  	 ret_token == token_dict["repTK"] 	or \
  	 ret_token == token_dict["whileTK"] or \
  	 ret_token == token_dict["exitTK"] 	or \
  	 ret_token == token_dict["swiTK"] 	or \
  	 ret_token == token_dict["fcaseTK"] or \
  	 ret_token == token_dict["callTK"] 	or \
  	 ret_token == token_dict["retTK"] 	or \
  	 ret_token == token_dict["inputTK"] or \
  	 ret_token == token_dict["printTK"]:
    
  	error = "Expected \";\" after statement. Instead found \"" + lex_unit +"\"." + \
  	"\nOnly the final statement of a block must not have \";\"."
  	error_display(3,error,line)
  	exit()

  return to_exit_if_exit

# -- <STATEMENT> ::= e | <ASSIGNMENT-STAT> | <IF-STAT> | <REPEAT-STAT> | <WHILE-STAT> | <EXIT-STAT> 
#                      | <SWITCH-STAT> | <FORCASE-STAT> | <CALL-STAT> | <RETURN-STAT> | <INPUT-STAT>
#                      | <PRINT-STAT> -- # [SYN: Done, INT: Done] 
def STATEMENT():

  global ret_token
  global line
  to_exit_if_exit = []

  # Sneak Peeks!
  if ret_token == token_dict["alphaTK"]:
   
    tmp_id_1 = lex_unit
    tmp_id_2 = ASSIGNMENT_STAT()
    gen_quad(":=",tmp_id_2,"_",tmp_id_1)

  elif ret_token == token_dict["ifTK"]: 		to_exit_if_exit = IF_STAT()
  elif ret_token == token_dict["repTK"]: 		REPEAT_STAT()
  elif ret_token == token_dict["whileTK"]:	to_exit_if_exit = WHILE_STAT()
  elif ret_token == token_dict["exitTK"]:   return EXIT_STAT()
  elif ret_token == token_dict["swiTK"]:	  to_exit_if_exit = SWITCH_STAT()
  elif ret_token == token_dict["fcaseTK"]:  to_exit_if_exit = FORCASE_STAT()
  elif ret_token == token_dict["callTK"]:   CALL_STAT()
  elif ret_token == token_dict["retTK"]:    RETURN_STAT()
  elif ret_token == token_dict["inputTK"]:  INPUT_STAT()
  elif ret_token == token_dict["printTK"]:  PRINT_STAT()
  elif ret_token == "": 										pass # e : Not typing a statement is acceptable. 


  return to_exit_if_exit

# -- <ASSIGNMENT-STAT> ::= ID := <EXPRESSION> -- # [SYN: Done, INT: Done]
def ASSIGNMENT_STAT():

  global ret_token
  global line

  if ret_token == token_dict["alphaTK"]:

    lex()
    
    if ret_token == token_dict["assigTK"]:

      lex()
      
      to_caller = EXPRESSION()

      return to_caller

    else:
    	error = "Expected \":=\" for assignment. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

  # No need to display an error message here. If there was no alpha Token we wouldn't be here.

# -- <IF-STAT> ::= IF <CONDITION> THEN <STATEMENTS> <ELSEPART> ENDIF -- # [SYN: Done, INT: Done]
def IF_STAT():

  global ret_token
  global line
  to_exit_if_exit = []

  lex()
  
  (c_true,c_false) = CONDITION()
  back_patch(c_true,next_quad())

  if ret_token == token_dict["thenTK"]:

    lex()
    
    is_exit = STATEMENTS()
    if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)
    iflist = make_list(next_quad())
    gen_quad("jump","_","_","_")
    back_patch(c_false,next_quad())

    is_exit = ELSEPART()
    if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)
    back_patch(iflist,next_quad())

    if ret_token == token_dict["eifTK"]:

      lex()
      
    else:
    	error = "Expected \"endif\" at the end of if statement. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()
  
  else:
  	error = "Expected \"then\" after if statement. Instead found \"" + lex_unit +"\"."
  	error_display(3,error,line)
  	exit()

  return to_exit_if_exit
      
# -- <ELSEPART> ::= e | ELSE <STATEMENTS> -- #
def ELSEPART():

  global ret_token
  global line
  to_exit_if_exit = []

  if ret_token == token_dict["elseTK"]:

    lex()
    
    is_exit = STATEMENTS()
    if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)

  # e : Not determining an else part is acceptable.

  return to_exit_if_exit

# -- <REPEAT-STAT> ::= REPEAT <STATEMENTS> ENDREPEAT -- # [SYN: Done, INT: Done]
def REPEAT_STAT():

  global ret_token
  global line
  exit_list = []

  if ret_token == token_dict["repTK"]:

    lex()
    jump_back = next_quad()
    is_exit = STATEMENTS()
    exit_list = merge_list(exit_list, is_exit)
    gen_quad("jump","_","_", jump_back)

    if ret_token == token_dict["erepTK"]:

    	back_patch(exit_list,next_quad())
    	lex()
     
    else:
    	error = "Expected \"endrepeat\" at the end of repeat statement. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

  # No need to display an error message. If there was no repeat Token we wouldn't be here.

# -- <EXIT-STAT> ::= EXIT -- # [SYN: Done, INT: Done]
def EXIT_STAT():

  global ret_token
  global line

  if ret_token == token_dict["exitTK"]:

    lex()
    back_to_repeat = make_list(next_quad())
    gen_quad("jump","_","_","_")

    return back_to_repeat

    

  # No need to display an error message. If there was no exit Token we wouldn't be here.

# -- <WHILE-STAT> ::= WHILE <CONDITION> <STATEMENTS> ENDWHILE -- # [SYN: Done, INT: Done]
def WHILE_STAT():

  global ret_token
  global line

  jump_back = next_quad()

  to_exit_if_exit = []

  if ret_token == token_dict["whileTK"]:

    lex()
    
    (c_true, c_false) = CONDITION()
    
    back_patch(c_true,next_quad())
    is_exit = STATEMENTS()
    if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)
    gen_quad("jump","_","_",jump_back)
    back_patch(c_false,next_quad())

    if ret_token == token_dict["ewhileTK"]:

      lex()

    else:
    	error = "Expected \"endwhile\" at the end of while statement. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

  return to_exit_if_exit
      
  # No need to display an error message. If there was no while Token we wouldn't be here.

# -- <SWITCH-STAT> ::= SWITCH <EXPRESSION> ( CASE <EXPRESSION> : <STATEMENTS )+ ENDSWITCH -- # [SYN: Done, INT: Done]
def SWITCH_STAT(): 

  global ret_token
  global line
  to_exit_if_exit = []
  jump_out = empty_list()

  if ret_token == token_dict["swiTK"]:

    lex()
    
    tmp_exp_1 = EXPRESSION()
    
    if ret_token == token_dict["caseTK"]:

      lex() 
      
      tmp_exp_2 = EXPRESSION()
      true_1 = make_list(next_quad())
      gen_quad("=",tmp_exp_1,tmp_exp_2,"_")
      false_1 = make_list(next_quad())
      gen_quad("jump","_","_","_")
     
      if ret_token == token_dict["colonTK"]:

        lex()

        back_patch(true_1, next_quad())
        is_exit = STATEMENTS()
        if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)
        jump_out_tmp = make_list(next_quad())
        gen_quad("jump","_","_","_")
        jump_out = merge_list(jump_out, jump_out_tmp)
        back_patch(false_1, next_quad())

        # Sneak Peek
        while ret_token == token_dict["caseTK"]:

          lex()

          tmp_exp_2 = EXPRESSION()
          true_2 = make_list(next_quad())
          gen_quad("=",tmp_exp_1,tmp_exp_2,"_")
          false_2 = make_list(next_quad())
          gen_quad("jump","_","_","_")

          if ret_token == token_dict["colonTK"]:

            lex()

            back_patch(true_2, next_quad())
            is_exit = STATEMENTS()
            if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)
            jump_out_tmp = make_list(next_quad())
            gen_quad("jump","_","_","_")
            jump_out = merge_list(jump_out, jump_out_tmp)
            back_patch(false_2, next_quad())

          else:
          	error = "Expected \":\" after case expression. Instead found \"" + lex_unit +"\"."
          	error_display(3,error,line)
          	exit()

        if ret_token == token_dict["eswiTK"]:

          lex()

          back_patch(jump_out,next_quad())
          
        else:
        	error = "Expected \"endswitch\" at the end of switch statement. Instead found \"" + lex_unit +"\"."
        	error_display(3,error,line)
        	exit()

      else:
      	error = "Expected \":\" after case expression. Instead found \"" + lex_unit +"\"."
      	error_display(3,error,line)
        exit()

    else:
    	error = "Expected \"case\" after switch expression. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()
  
  return to_exit_if_exit

  # No need to display an error message. If there was no switch Token we wouldn't be here.

# -- <FORCASE-STAT> ::= FORCASE ( WHEN <CONDITION> : <STATEMENTS> )+ ENDFORCASE -- # [SYN: Done, INT: Done]
def FORCASE_STAT():

  global ret_token
  global line

  flag = new_temp()
  jump_back = next_quad()
  gen_quad(":=","0","_",flag)

  to_exit_if_exit = []

  if ret_token == token_dict["fcaseTK"]:

    lex()

    if ret_token == token_dict["whenTK"]:

      lex()
      
      (c_true,c_false) = CONDITION()
      back_patch(c_true, next_quad())
      
      if ret_token == token_dict["colonTK"]:

        lex()
        
        is_exit = STATEMENTS()
        if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)
        #gen_quad("jump","_","_",jump_back)
        gen_quad(":=","1","_",flag)
        back_patch(c_false,next_quad())

        # Sneak Peek
        while ret_token == token_dict["whenTK"]:

          lex()
          
          (c2_true,c2_false) = CONDITION()
          back_patch(c2_true, next_quad())


          if ret_token == token_dict["colonTK"]:

            lex()

            is_exit = STATEMENTS()
            if is_exit: to_exit_if_exit = merge_list(to_exit_if_exit, is_exit)
            #gen_quad("jump","_","_",jump_back)
            gen_quad(":=","1","_",flag)
            back_patch(c2_false,next_quad())

          else:
          	error = "Expected \":\" after forcase condition. Instead found \"" + lex_unit +"\"."
          	error_display(3,error,line)
          	exit()

        if ret_token == token_dict["efcaseTK"]: 
 
          gen_quad("=","1",flag,jump_back)
          j_out = make_list(next_quad())
          gen_quad("jump","_","_","_")
          back_patch(j_out,next_quad())
          lex()
          

        else:
          error = "Expected \"endforcase\" at the end of forcase. Instead found \"" + lex_unit +"\"."
          error_display(3,error,line)
          exit()

      else:
      	error = "Expected \":\" after forcase condition. Instead found \"" + lex_unit +"\"."
        error_display(3,error,line)
        exit()

    else:
    	error = "Expected \"when \" after forcase. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

  return to_exit_if_exit

# -- <CALL-STAT> ::= CALL ID <ACTUALPARS> -- # [SYN: Done, INT: Done]
def CALL_STAT():

  global ret_token 

  if ret_token == token_dict["callTK"]:

    lex()
    
    if ret_token == token_dict["alphaTK"]:

    	tmp_id = lex_unit
    	lex()
      
    	my_quads = ACTUALPARS()
  
    	for par in my_quads:
    		if '%i' in par: 
    			gen_quad("par",par.split('%')[0], "in","_")
    		elif '%o' in par:
    			gen_quad("par",par.split('%')[0],"inout","_")
    	gen_quad("call",tmp_id,"_","_")

    else: 
      error = "Expected function/procedure name call. Instead found \"" + lex_unit +"\"."
      error_display(3,error,line)
      exit()

# -- <RETURN-STAT> ::= RETURN <EXPRESSION> -- # [SYN: Done, INT: Done]
def RETURN_STAT():

  global ret_token

  if ret_token == token_dict["retTK"]:

    lex() 
    
    tmp_exp = EXPRESSION()
    gen_quad("return",tmp_exp,"_","_")

  # No need to display an error message. If there was no return Token we wouldn't be here.

# -- <PRINT-STAT> ::= PRINT <EXPRESSION> -- #	[SYN: Done, INT: Done]
def PRINT_STAT():

  global ret_token

  if ret_token == token_dict["printTK"]:

    lex()
    
    tmp_exp = EXPRESSION()
    gen_quad("print",tmp_exp,"_","_")

  # No need to display an error message. If there was no print Token we wouldn't be here.

# -- <INPUT-STAT> ::= INPUT ID -- # [SYN: Done, INT: Done]
def INPUT_STAT():

	global ret_token

	if ret_token == token_dict["inputTK"]:

		lex()
		
		if ret_token == token_dict["alphaTK"]:

			gen_quad("input",lex_unit,"_","_")
			lex()

		else:
			error = "Expected variable name. Instead Found \"" + lex_unit + "\"."
			error_display(3,error,line)
			exit()

# -- <ACTUALPARS> ::= ( <ACTUALPARLIST> ) -- #
def ACTUALPARS():

  global ret_token

  if ret_token == token_dict["lbrTK"]:

    lex()
    
    to_caller = ACTUALPARLIST()
    

    if ret_token == token_dict["rbrTK"]:

      lex()
      return to_caller

    else:
    	error = "Expected \")\" after parameter declaration. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

  else:
  	error = "Expected \"(\" before parameter declaration. Instead found \"" + lex_unit +"\"."
  	error_display(3,error,line)
  	exit()

# -- <ACTUALPARLIST> ::= <ACTUALPARITEM> (, <ACTUALPARITEM> )* | e -- # [SYN: Done, INT: Done]
def ACTUALPARLIST():

  to_actualpars = []
  global ret_token

  # Sneak Peek
  if ret_token == token_dict["inTK"] or ret_token == token_dict["inoutTK"]:

    to_caller = ACTUALPARITEM()
    to_actualpars.append(to_caller)
    while ret_token == token_dict["commaTK"]:

      lex()

      to_caller = ACTUALPARITEM()
      to_actualpars.append(to_caller)

    return to_actualpars
      
  else:
  	error = "Expected \"in/inout\" before parameter name. Instead found \"" + lex_unit +"\"."
  	error_display(3,error,line)
  	exit()

  # e : Not defining an actual parameter is acceptable.

# -- <ACTUALPARITEM> ::= IN <EXPRESSION> | INOUT ID -- # [SYN: Done, INT: Done]
def ACTUALPARITEM():

  global ret_token
  
  if ret_token == token_dict["inTK"]:

    lex()
 
    tmp_exp = EXPRESSION() +'%i'


    #gen_quad("par",tmp_exp,"in","_")
    

  elif ret_token == token_dict["inoutTK"]:

    lex()

    if ret_token == token_dict["alphaTK"]:
    	tmp_exp = lex_unit +'%o'

    	lex()

    	#gen_quad("par",tmp_exp,"inout","_")

  return tmp_exp

# -- <CONDITION> ::= <BOOLTERM> ( OR <BOOLTERM> )* -- # [SYN: Done, INT: Done]
def CONDITION():

  global ret_token 

  (b1_true, b1_false) = BOOLTERM()
  (c_true, c_false) = (b1_true, b1_false)

  while ret_token == token_dict["orTK"]:

    lex()
    back_patch(c_false, next_quad())
    (b2_true, b2_false) = BOOLTERM()
    c_true = merge_list(c_true, b2_true)
    c_false = b2_false

  return (c_true,c_false)

# -- <BOOLTERM> ::= <BOOLFACTOR> ( AND <BOOLFACTOR> )* -- # [SYN: Done, INT: Done]
def BOOLTERM():

  global ret_token

  (b1_true, b1_false) = BOOLFACTOR()
  (b_true, b_false) = (b1_true, b1_false)

  while ret_token == token_dict["andTK"]:

    lex()

    back_patch(b_true,next_quad())

    (b2_true, b2_false) = BOOLFACTOR()
    b_false = merge_list(b_false, b2_false)
    b_true = b2_true

  return(b_true, b_false)

# -- <BOOLFACTOR> ::= NOT [ <CONDITION> ] | [ <CONDITION> ] | <EXPRESSION> <RELATIONAL-OPER> <EXPRESSION> 
#                                         | TRUE | FALSE -- # [SYN: Done, INT: Done]
def BOOLFACTOR():

  global ret_token
  
  if ret_token == token_dict["notTK"]:

    lex()

    if ret_token == token_dict["blbrTK"]:

      lex()
      
      to_caller = CONDITION()
      to_caller = to_caller[::-1] 

      if ret_token == token_dict["brbrTK"]:

        lex()

      else:
      	error = "Expected \"]\" after condition. Instead found \"" + lex_unit +"\"."
      	error_display(3,error,line)
        exit()

    else:
    	error = "Expected \"[\" before condition. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()


  elif ret_token == token_dict["blbrTK"]:

    lex()
    
    to_caller = CONDITION()

    if ret_token == token_dict["brbrTK"]:

      lex()

    else:
    	error = "Expected \"]\" after condition. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

  # Sneak Peek
  elif ret_token == token_dict["plusTK"] or \
  	ret_token == token_dict["minusTK"] 	 or \
  	ret_token == token_dict["numberTK"]  or \
  	ret_token == token_dict["lbrTK"] 		 or \
  	ret_token == token_dict["alphaTK"]:

    tmp_exp1 = EXPRESSION()
    tmp_op = RELATIONAL_OPER()
    tmp_exp2 = EXPRESSION()

    b_true = make_list(next_quad())
    gen_quad(tmp_op,tmp_exp1,tmp_exp2,"_")
    b_false = make_list(next_quad())
    gen_quad("jump","_","_","_")
    to_caller = (b_true, b_false)
  
  elif ret_token == token_dict["trueTK"]:

    b_true = make_list(next_quad())
    gen_quad("jump","_","_","_")
    b_false = empty_list()
    to_caller = (b_true,b_false)
    lex()

  elif ret_token == token_dict["falseTK"]:

    b_false = make_list(next_quad())
    gen_quad("jump","_","_","_")
    b_true = empty_list()
    to_caller = (b_true,b_false)
    lex()
	
  return to_caller


# -- <EXPRESSION> ::= <OPTIONAL-SIGN> <TERM> ( <ADD-OPER> <TERM> )* -- # [SYN: Done, INT: Done]
def EXPRESSION(): 

  global ret_token

  optsign = OPTIONAL_SIGN()
  term_1 = TERM()

  if optsign:
  	tmp_1 = new_temp()
  	gen_quad(optsign, 0, term_1, tmp_1)
  	term_1 = tmp_1

  #Sneak Peek
  while( ret_token == token_dict["plusTK"] or ret_token == token_dict["minusTK"] ):

    oper = ADD_OPER()
    term_2 = TERM()

    tmp_2 = new_temp()
    gen_quad(oper,term_1,term_2,tmp_2)
    term_1 = tmp_2

  return term_1

# -- <TERM> ::= <FACTOR> ( <MUL-OPER> <FACTOR> )* -- # [SYN: Done, INT: Done]
def TERM():

  global ret_token

  factor_1 = FACTOR()

  #Sneak Peek
  while(ret_token == token_dict["mulTK"] or ret_token == token_dict["divTK"]):

    op = MUL_OPER()
    factor_2 = FACTOR()
    tmp = new_temp()
    gen_quad(op,factor_1,factor_2,tmp)
    factor_1 = tmp

  return factor_1

# -- <FACTOR> ::= COSTANT | ( <EXPRESSION> ) | ID <IDTAIL> -- # [SYN: Done, INT: Done]
def FACTOR():

  global ret_token

  if ret_token == token_dict["numberTK"]:

    to_caller = lex_unit
    lex()

  elif ret_token == token_dict["lbrTK"]:

    lex()
    
    to_caller = EXPRESSION()

    if ret_token == token_dict["rbrTK"]:

      lex()

    else:
    	error = "Expected \")\" after expression. Instead found \"" + lex_unit +"\"."
    	error_display(3,error,line)
    	exit()

  elif ret_token == token_dict["alphaTK"]:																				

    to_caller = lex_unit
    lex()
    
    my_quads = IDTAIL()
 	    
    if my_quads:	# Quads must be generated if tail exists. 
    	
    	#print("Factor :" + str(tail_tmp))
    	ret = new_temp()
    	for par in my_quads:
    		if '%i' in par:
    			gen_quad("par",par.split('%')[0],"in","_")
    		elif '%o' in par:
    			gen_quad("par",par.split('%')[0],"inout","_")
    	gen_quad("par",ret,"ret","_")
    	gen_quad("call",to_caller,"_","_")
    	to_caller = ret

  else:
  	error = "Found \"" + lex_unit + "\". Invalid factor."
  	error_display(3,error,line)
  	exit()

  return to_caller

# -- <IDTAIL> ::= e | <ACTUALPARS> -- #	[SYN: Done, INT: Done]
def IDTAIL():

  global ret_token

  if ret_token == token_dict["lbrTK"]:
    	
    return ACTUALPARS()

  # e : No statements after an ID is acceptable.

# -- <RELATIONAL-OPER> ::= = | <= | >= | > | < | <> -- # [SYN: Done, INT: Done]
def RELATIONAL_OPER():

  global ret_token 

  if ret_token == token_dict["eqTK"]:

    to_caller = lex_unit
    lex()

  elif ret_token == token_dict["leqTK"]:

    to_caller = lex_unit
    lex()

  elif ret_token == token_dict["greqTK"]:
    
    to_caller = lex_unit
    lex()

  elif ret_token == token_dict["greaTK"]:

    to_caller = lex_unit
    lex()

  elif ret_token == token_dict["lessTK"]:

    to_caller = lex_unit
    lex()

  elif ret_token == token_dict["difTK"]:

    to_caller = lex_unit
    lex()

  else:
  	error = "Found \"" + lex_unit + "\". Invalid relational operator."
  	error_display(3,error,line)
  	exit()

  return to_caller

# -- <ADD-OPER> ::= + | - -- # [SYN: Done, INT: Done]
def ADD_OPER():

  global ret_token

  if ret_token == token_dict["plusTK"]:

    to_caller = lex_unit
    lex()

  elif ret_token == token_dict["minusTK"]:

    to_caller = lex_unit
    lex()

  else:
    error = "Found \"" + lex_unit + "\". Invalid addition operator."
    error_display(3,error,line)
    exit()
  return to_caller

# -- <MUL-OPER> ::= * | / -- # [SYN: Done, INT: Done]
def MUL_OPER():

  global ret_token

  if ret_token == token_dict["mulTK"]:

    to_caller = lex_unit
    lex()

  elif ret_token == token_dict["divTK"]:

    to_caller = lex_unit
    lex()

  else:
  	error = "Found \"" + lex_unit + "\". Invalid multiplication operator."
  	error_display(3,error,line)
  	exit()

  return to_caller

#  -- <OPTIONAL-SIGN> ::= e | <ADD-OPER> -- # [SYN: Done, INT: Done]
def OPTIONAL_SIGN():

  global ret_token

  if ret_token == token_dict["plusTK"] or ret_token == token_dict["minusTK"]:

    to_caller = ADD_OPER()

    return to_caller

  # e : Not using an add operator is acceptable.

# + ------------------------------------ + #
# 										   #														
#		      Main Function		           #
#										   #
# + ------------------------------------ + #

def main():

  try:

    global code 
    global line
    global eel_source_code
    global to_ansi_c_problem

    signal.signal(signal.SIGTSTP, handler)

    compilation_options = ["-h","-v","-i","-s","-int"]
    verbose = 0
    generate_intermediate = 0

    if(len(sys.argv) > 3 and sys.argv[1] != "-i"): 
  		raise IndexError
    
    if(sys.argv[1] not in compilation_options):
    	raise IndexError

    if(sys.argv[1] == "-i"):
    	print("\n" + Colors.YELLOW)
    	print("EEL stands for \"Early Experimental Language\" and this is its Compiler (version 2681).")
    	print("You can learn more about EEL and her properties by checking the documentation \"wEELCome.pdf\".")
    	print("This software was developed during UoI@CSE802 class: \"Compilers I\".")
    	print("Instructor: George Manis")
    	print("University of Ioannina - Spring Semester - 2018")
    	print("Copyright (C) 2018 Nick I. Deligiannis")
    	print("\n" + Colors.RESET)
    	exit()
    elif(sys.argv[1] == "-h"):
    	print("Usage: python EELC.py [option] [file.eel]")
    	print("where possible options include:")
    	print("-h \t\t Display this info")
    	print("-i \t\t Information about this compiler")
    	print("-v \t\t Output messages about what the compiler is doing")
    	print("-s \t\t Display nothing (silent compilation)")
    	print("-int \t\t Generate intermediate code files (ANSI C and .int)")
    	print("Only one option at a time.")
    	exit()
    elif(sys.argv[1] == "-v"):
    	verbose = 1
    elif(sys.argv[1] == "-s"):
    	pass
    elif(sys.argv[1] == "-int"):
    	generate_intermediate = 1

    eel_source_code = sys.argv[2]
    code = open(eel_source_code)
    if verbose == 1:
    	print("\n" + Colors.BOLD)
    	print("Loaded EEL Source Code File...")
    	print("Starting Lexical Analysis...")

    # Lexical Test #
    a = lex()
    while(a != token_dict["eofTK"]):

      a = lex()
    
    # Reset the File Pointer and Line Counter
    if verbose == 1 and a == token_dict["eofTK"]:
    	print("\t Lexical Analysis \t[" + Colors.RESET + Colors.GREEN + " OK! " + Colors.RESET + Colors.BOLD + "]")
    	print("Starting Syntax Analysis...")
    code.seek(0,0)
    line = 1 

    # Syntax Test #
    lex()
    PROGRAM()

    if verbose == 1:
    	print("\t Syntax Analysis \t[" + Colors.RESET + Colors.GREEN + " OK! " + Colors.RESET + Colors.BOLD + "]")
    	print("Intermediate Code Created...")
    	if_user = raw_input("Generate Files? [Y/N]: ")
    	if if_user == "Y" or if_user == "y":
    		generate_intermediate = 1
    		

    if generate_intermediate == 1:
    	if verbose == 1 : print("Creating And Writing Files...")
    	generate_intermediate_int()
    	print(Colors.BOLD + "\t .int File \t\t[" + Colors.RESET + Colors.GREEN + " OK! " + Colors.RESET + Colors.BOLD + "]")
    	generate_intermediate_ansi_c()
    	if to_ansi_c_problem == 1:
    		os.remove(eel_source_code.split('.')[0]+".c")
    		print("\t ANSI C File \t\t[" + Colors.RESET + Colors.RED + " FAILED! " + Colors.RESET + Colors.BOLD + "]")
    		print(Colors.RESET + Colors.HIGHL + "\t [Found nested functions. Equivalent ANSI C cannot be generated!]" + Colors.RESET + Colors.BOLD)
    	else:
    		print("\t ANSI C File \t\t[" + Colors.RESET + Colors.GREEN + " OK! " + Colors.RESET + Colors.BOLD + "]")
    	generate_intermediate = 0
    
    if verbose == 1:
    	print("Closing Files...")
   
    code.close()

  except IndexError: 
    print("Usage: python EELC.py [option] [file.eel]")
    print("where possible options include:")
    print("-h \t\t Display this info")
    print("-i \t\t Information about this compiler")
    print("-v \t\t Output messages about what the compiler is doing")
    print("-s \t\t Display nothing (silent compilation)")
    print("-int \t\t Generate intermediate code files (ANSI C and .int)")
    print("Only one option at a time.")

  except IOError:
  	error = "File \"" + sys.argv[2] + "\" not found!"
  	error_display(4,error,None)
  	exit()

  except KeyboardInterrupt:
  	print("\n")
  	print(Colors.HIGHL + "Compilation Terminated by SIGINT (^C) " + Colors.RESET)
  	exit()

if __name__ == '__main__':

	main()

