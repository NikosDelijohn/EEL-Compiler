# ***************************** #
# Deligiannis Nikos 2681        #
# UoI - Spring Semester 2018    #
# Compilers MYY802 prof G.Manis #
# Project: Compiler for EEL     #
# ***************************** #

# ********************************************** TERMINAL SYNTAX ********************************************** #
#                                                                                                               #
#                                   >python EELC.py [source file] [options]<                                    #
#                                                                                                               #
#       -[filename]: The name of the .eel file (Source Code)                                                    #
#       -[verbose]: Detailed output of Lexical and Syntactical analysis.                                        #
#                   If you do not want a verbosed output simply type '-skip' ! You will be notified about       #
#                   the test results of Lexical and Syntactical Analysis.                                       #
#                   If you want a verbosed output type "-verbose" after the [filename]                          #
#                   Due to wealth of text messages, redirected output is strongly reccomended!!                 #
#                   For example python EELC.py example verbose > output.txt!                                    #
#                                                                                                               #
# *************************************************************************************************************

import sys

# [PHASE: 1] :: Lexical and Syntactical Analysis

#Global Scope Variables 

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

global max_word_size
max_word_size = 30  # An Alpharithmetic can't be over 30 char's long
global line
line          = 1   # The current line (used for debugging messages)
global ret_token
ret_token     = 0   # The token lex() will return
global lex_unit
lex_unit      = ""  # The lexical unit lex() will return

global code         # File pointer of the Source Code



# This function is used by lex() in some cases we need to get the previous character 
def backtrack():
  global code
  position = code.tell()
  code.seek(position - 1)

# Lexical Analysis #

def lex():

  global lex_unit     # Linking the Global Variables
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

      ret_token = token_dict["alphaTK"]     #Default case, its an alpharithmetic (e.g. variableA)
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

      if(unit.isalpha()):                     #[A]
        print("""
        ****************************** LEX ERROR ******************************
          
          -Invalid Sequence detected
            --After you cannot have numbers with alpharithmetics in them
              ---Example: Sequence "123abc" is not acceptable

          -Error spotted at Line: %d

        ****************************** LEX ERROR ******************************
        LEX()""" %(line))
        exit()

      tmp_num = int(lex_unit)                #[B] :: [NOTE] :: No need to check if the number is >= -32767 ! Grammar will provide the sign 
      if tmp_num >= 32767:                        
        print("""
        ****************************** LEX ERROR ******************************

        -Invalid Number
          --Acceptable numbers are:
            ---Numbers greater or equal to -32767 [ >= -32767]
            ---Numbers lower or equal to 32767 [<= 32767]

        -Error spotted at Line: %d

        ****************************** LEX ERROR ******************************
        LEX()""" %(line))
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
        print("""
        ****************************** LEX ERROR ******************************

        -You marked the end of a comment section '*/'
        -You havend though marked the start of it '*/'

        -Error spotted at Line: %d

        ****************************** LEX ERROR ******************************
        LEX()""" %(line))
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

      if unit == '*':                       # [A]: Comment initializer found! Keep reading until you find '*/'

        tmp_flag = 0

        tmp_err = line                      # Used in case of an error!

        while(tmp_flag == 0):

          unit = code.read(1)

          if unit == '\n': line = line + 1

          if unit == '*':

            unit = code.read(1)

            if not unit :                      # Reached EOF without closing comments
              print("""
              ****************************** LEX ERROR ******************************

              -EOF Reached while reading comments
                --A Comment section has not been terminated

              -Comments initiated at Line: %d
              -Error spotted at Line: %d

              ****************************** LEX ERROR ******************************
              LEX()""" %(tmp_err,line))
              exit()

            if(unit == '/') : tmp_flag = 1

          if not unit :                      # Reached EOF without closing comments
            print("""
            ****************************** LEX ERROR ******************************

            -EOF Reached while reading comments
              --A Comment section has not been terminated

            -Comments initiated at Line: %d
            -Error spotted at Line: %d

            ****************************** LEX ERROR ******************************
            LEX()""" %(tmp_err,line))
            exit()

        return lex()                      


      elif unit == '/':                       # [B]: Comment the whole line

        tmp_flag = 0

        while(tmp_flag == 0):

          unit = code.read(1)

          if unit == '\n': tmp_flag = 1        # End of line reached! Stop!

        return lex()

      else:                                   # [C]: Division operator. Baktrack required 

        backtrack()
        ret_token = token_dict["divTK"]
        return token_dict["divTK"]

    if unit == '=':

      lex_unit = lex_unit + unit
      ret_token = token_dict["eqTK"]
      return token_dict["eqTK"]

    if unit == ';':
      #print("Semicolon")
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

      if unit == '=':           # [A]

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

      if unit == "=":     # [A]

        lex_unit = lex_unit + unit
        ret_token = token_dict["leqTK"]
        return token_dict["leqTK"]

      if unit == ">":     # [B]

        lex_unit = lex_unit + unit
        ret_token = token_dict["difTK"]
        return token_dict["difTK"]

      # [C]

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

      if unit == "=":     # [A]

        lex_unit = lex_unit + unit
        ret_token = token_dict["greqTK"]
        return token_dict["greqTK"]

      backtrack()
      ret_token = token_dict["greaTK"]
      return token_dict["greaTK"]

 # -------------------[State 8 of the FSM]------------------- #    
 # -Uknown symbol found. Error!                               #
 # ---------------------------------------------------------- #

    print("""[Lex()]::\
      ***** ERROR *****
        -Uknown character found!
        """)
    print("[Lex()]:: Error found ~at line %d"%(line))
    exit()

  lex_unit = "EOF"
  ret_token = token_dict["eofTK"]
  return token_dict["eofTK"]

# Syntax Analysis #

# -- <PROGRAM> ::= PROGRAM ID <BLOCK> ENDPROGRAM -- #
def PROGRAM():
  
  if sys.argv[2] == "-verbose" : print(" ===========> START OF SYNTAX !! <=========== ")
  if sys.argv[2] == "-verbose" : print("0.<PROGRAM>")

  global ret_token

  if ret_token == token_dict["progTK"]:

    if sys.argv[2] == "-verbose" : print ("\tPROGRAM\t" + lex_unit)
    lex()

    if ret_token == token_dict["alphaTK"]:

      if sys.argv[2] == "-verbose" : print ("\tPROGRAM\t" + lex_unit)
      lex()

      if sys.argv[2] == "-verbose" : print ("*** PROGRAM ==> BLOCK ***")
      BLOCK()
      
      if ret_token == token_dict["eprogTK"]:
        
        if sys.argv[2] == "-verbose" : print ("\tPROGRAM\t" + lex_unit)
        lex()  # EOF is expected

        if sys.argv[2] == "-verbose" : 

          if ret_token == token_dict["eofTK"]:

            print(" ===========> END OF FILE REACHED <=========== ")

        
      else:
        print("""
        ****************************** SYN ERROR ******************************

        -Invalid Syntax
          --Every program shall end with word "endprogram" writen!
          --Instead you typed something else or forgot to type it!

        -Error spotted at Line: %d
 
        ****************************** SYN ERROR ******************************
        PROGRAM()"""%(line))

        exit()

    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --Program name expected after "program"
        --Instead you typed something else or forgot to type it!

      -Error spotted at Line %d
        
      ****************************** SYN ERROR ******************************
      PROGRAM()"""%(line))
      exit()

  else:
    print("""
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --Every program shall begin with word "program".
      --Instead You typed something else or forgot to type it!

    -Error spotted at Line: %d

    ****************************** SYN ERROR ****************************** 
    PROGRAM()"""%(line))

    exit()

def BLOCK():

  if sys.argv[2] == "-verbose" : print("1.<BLOCK>")

  if sys.argv[2] == "-verbose" : print("*** BLOCK ==> DECLARATIONS ***")
  DECLARATIONS()
  if sys.argv[2] == "-verbose" : print("*** BLOCK ==> SUBPROGRAMS ***")
  SUBPROGRAMS()
  if sys.argv[2] == "-verbose" : print("*** BLOCK ==> STATEMENTS ***")
  STATEMENTS()

# -- <DECLARATIONS> ::= e | DECLARE <VARLIST> ENDDECLARE -- #
def DECLARATIONS():

  if sys.argv[2] == "-verbose" : print("2.<DECLARATIONS>")
  
  global ret_token

  if ret_token == token_dict["decTK"]:

    if sys.argv[2] == "-verbose" : print("\tDECLARATIONS\t" + lex_unit)
    lex()

    if sys.argv[2] == "-verbose" : print("*** DECLARATIONS ==> VARLIST ***")
    VARLIST()               

    if ret_token == token_dict["edecTK"]:

      if sys.argv[2] == "-verbose" : print("\tDECLARATIONS\t" + lex_unit)
      lex()
          

    else:
      print("""      
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --After declaring the variables "enddeclare" is expected 
        --Instead You typed something else or forgot to type it.
      
      -Error spotted at Line: %d
      
      ****************************** SYN ERROR ******************************
      DECLARATIONS()""" %(line))

      exit()

  # e : No Declarations is acceptable

# -- <VARLIST> ::= e | ID (, ID)* -- #
def VARLIST():

  if sys.argv[2] == "-verbose" : print("3.<VARLIST>")

  global ret_token

  if ret_token == token_dict["alphaTK"]:

    if sys.argv[2] == "-verbose" : print("\tVARLIST\t" + lex_unit)
    lex()

    while(ret_token == token_dict["commaTK"]):

      if sys.argv[2] == "-verbose" : print("\tVARLIST\t" + lex_unit)
      lex()
      
      if ret_token == token_dict["alphaTK"]:

        if sys.argv[2] == "-verbose" : print("\tVARLIST\t" + lex_unit)
        lex()   
        
      else:
        print("""          
        ****************************** SYN ERROR ******************************

        -Invalid Syntax
          --After comma (',') you have to type a variable's name!
            ---[NOTE]: Read EEL's documentation file to see which
                       words are allowed to be used as variable names! 

        -Error spotted at Line: %d
          
        ****************************** SYN ERROR ******************************
        VARLIST()""" %(line))

        exit()

  # e : No Variables is acceptable

# -- <SUBPROGRAMS> ::= (<PROCORFUNC>)* -- #
def SUBPROGRAMS():

  if sys.argv[2] == "-verbose" : print("4.<SUBPROGRAMS>")

  global ret_token

  #Sneak Peek
  while(ret_token == token_dict["procTK"] or ret_token == token_dict["funTK"]):

    if sys.argv[2] == "-verbose" : print("*** SUBPROGRAMS ==> PROCORFUNC***")
    PROCORFUNC()

  # e : Kleene-Star includes e! So missing Function or Procedure is acceptable

# -- <PROCORFUNC> ::= PROCEDURE ID <PROCORFUNCBODY> ENDPROCEDURE | 
#                     FUNCTION ID <PROCORFUNCBODY> ENDFUNCTION -- #
def PROCORFUNC():

  if sys.argv[2] == "-verbose" : print("5.<PROCORFUNC>")

  global ret_token

  if ret_token == token_dict["procTK"]:

    if sys.argv[2] == "-verbose" : print("\tPROCORFUNC\t" + lex_unit)
    lex()

    if ret_token == token_dict["alphaTK"]:

      if sys.argv[2] == "-verbose" : print("\tPROCORFUNC\t" + lex_unit)
      lex()
      
      if sys.argv[2] == "-verbose" : print("*** PROCORFUNC ==> PROCORFUNCBODY ***")
      PROCORFUNCBODY()
      
      if ret_token == token_dict["eprocTK"]:

        if sys.argv[2] == "-verbose" : print("\tPROCORFUNC\t" + lex_unit)
        lex()

      else: 
        print("""          
        ****************************** SYN ERROR ******************************
        -Invalid Syntax
          --After declaring the procedure, you must type "endprocedure"
          --Instead you typed something else or forgot to type it!
            
        -Error spotted at Line: %d

        ****************************** SYN ERROR ******************************
        PROCORFUNC()""" %(line))
        exit()

    else:
      print("""      
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --You must name the procedure you want to type!
        --Instead you typed something else or forgot to type it!

      -Error spotted at Line: %d
      
      ****************************** SYN ERROR ******************************
      PROCORFUNC()""" %(line))
      exit()

  # No need to display an error message. If there was no procedure Token we wouldn't be here.

  elif ret_token == token_dict["funTK"]:

    if sys.argv[2] == "-verbose" : print("\tPROCORFUNC\t" + lex_unit)
    lex()
    
    if ret_token == token_dict["alphaTK"]:

      if sys.argv[2] == "-verbose" : print("\tPROCORFUNC\t" + lex_unit)
      lex()
      
      if sys.argv[2] == "-verbose" : print("*** PROCORFUNC ==> PROCORFUNCBODY ***")
      PROCORFUNCBODY()

      if ret_token == token_dict["efunTK"]:

        if sys.argv[2] == "-verbose" : print("\tPROCORFUNC\t" + lex_unit)
        lex()

      else:
        print("""
        ****************************** SYN ERROR ******************************

        -Invalid Syntax
              --After declaring the function, you must type "endfunction".
              --Instead you typed something else or forgot to type it!

            -Error spotted at Line: %d

        ****************************** SYN ERROR ******************************
        PROCORFUNC()""" %(line))

        exit()

    else:
      print("""      
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --You must name the function you want to type!
        --Instead you typed something else or forgot to type it!

      -Error spotted at Line: %d 
      
      ****************************** SYN ERROR ******************************
      PROCORFUNC()""" %(line))

      exit()  
  # No need to display an error message. If there was no function Token we wouldn't be here.

# -- <PROCORFUNCBODY() ::= <FORMALPARS> <BLOCK> -- #
def PROCORFUNCBODY():

  if sys.argv[2] == "-verbose" : print("6.<PROCORFUNCBODY>")

  if sys.argv[2] == "-verbose" : print("*** PROCORFUNCBODY ==> FORMALPARS ***")
  FORMALPARS()
  if sys.argv[2] == "-verbose" : print("*** PROCORFUNCBODY ==> BLOCK ***")
  BLOCK()

# -- <FORMALPARS> ::= (<FORMALPARLIST>) -- #
def FORMALPARS():

  if sys.argv[2] == "-verbose" : print("7.<FORMALPARS>")

  global ret_token

  if ret_token == token_dict["lbrTK"]:

    if sys.argv[2] == "-verbose" : print("\tFORMALPARS\t" + lex_unit)
    lex()

    if sys.argv[2] == "-verbose" : print("*** FORMALPARS ==> FORMALPARLIST ***")
    FORMALPARLIST()

    if ret_token == token_dict["rbrTK"]:

      if sys.argv[2] == "-verbose" : print("\tFORMALPARS\t" + lex_unit)
      lex()
      
    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --After declaring the procedure's/function's
            parameters you have to type ')'
        --Instead you typed something else or forgot to type it!

      -Error spotted at Line: %d
        
      ****************************** SYN ERROR ******************************
      FORMALPARS()""" %(line))
      
      exit() 

  else:
    print("""
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --To start declaring the procedure's/function's 
          parameters you have to type '(' !
      --Instead you typed something else or forgot to type it!

    -Error spotted at Line: %d

    ****************************** SYN ERROR ******************************
    FORMALPARS()""" %(line))

    exit() 

# -- <FORMALPARLIST> ::= <FORMALPARITEM> (, <FORMALPARITEM> )* | e -- #
def FORMALPARLIST():

  if sys.argv[2] == "-verbose" : print("8.<FORMALPARLIST>")

  global ret_token

  # Sneak Peek
  if (ret_token == token_dict["inTK"] or ret_token == token_dict["inoutTK"]):

    if sys.argv[2] == "-verbose" : print("*** FORMALPARLIST ==> FORMALPARITEM ***")
    FORMALPARITEM()

    while(ret_token == token_dict["commaTK"]):

      if sys.argv[2] == "-verbose" : print("\tFORMALPARLIST\t" + lex_unit)
      lex()

      if sys.argv[2] == "-verbose" : print("*** FORMALPARLIST ==> FORMALPARITEM ***")
      FORMALPARITEM()

  # e : Not deremining parameters is acceptable.

# -- <FORMALPARITEM> ::= IN ID | INOUT ID -- #
def FORMALPARITEM():

  if sys.argv[2] == "-verbose" : print("9.<FORMALPARITEM>")

  global ret_token

  if ret_token == token_dict["inTK"]:

    if sys.argv[2] == "-verbose" : print("\tFORMALPARITEM\t" + lex_unit)
    lex()

    if ret_token == token_dict["alphaTK"]:

      if sys.argv[2] == "-verbose" : print("\tFORMALPARITEM\t" + lex_unit)
      lex()
      

    else:
      print("""        
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --After declaring the variable's scope (in) you have to 
            name the variable (e.g in temp)
        --Instead you typed something else or forgot to type it!
      
      -Error spotted at Line: %d

      ****************************** SYN ERROR ******************************
      FORMALPARITEM()""" %(line))

      exit() 

  elif ret_token == token_dict["inoutTK"]:

    if sys.argv[2] == "-verbose" : print("\tFORMALPARITEM\t" + lex_unit)
    lex()

    if ret_token == token_dict["alphaTK"]:

      if sys.argv[2] == "-verbose" : print("\tFORMALPARITEM\t" + lex_unit)
      lex()

    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --After declaring the variable's scope (in) you have to 
            name the variable (e.g in temp)
        --Instead you typed something else or forgot to type it!
      
      -Error spotted at Line: %d
        
      ****************************** SYN ERROR ******************************
      FORMALPARITEM()""" %(line))
      exit()

# -- <STATEMENTS> ::= <STATEMENT> (;<STATEMENT>)* -- #
def STATEMENTS():

  if sys.argv[2] == "-verbose" : print("10.<STATEMENTS>")

  global ret_token
  
  if sys.argv[2] == "-verbose" : print("*** STATEMENTS ==> STATEMENT ***")
  STATEMENT()

  while ret_token == token_dict["semiTK"]:

    if sys.argv[2] == "-verbose" : print("\tSTATEMENTS\t" + lex_unit)
    lex()

    if sys.argv[2] == "-verbose" : print("*** STATEMENTS ==> STATEMENT ***")
    STATEMENT()

  if ret_token == token_dict["alphaTK"]  or ret_token == token_dict["ifTK"] or ret_token == token_dict["repTK"] or ret_token == token_dict["whileTK"] or ret_token == token_dict["exitTK"] or ret_token == token_dict["swiTK"] or ret_token == token_dict["fcaseTK"] or ret_token == token_dict["callTK"] or ret_token == token_dict["retTK"] or ret_token == token_dict["inputTK"] or ret_token == token_dict["printTK"]:
    print("""        
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --After Statement ';' is expected (unless its the final one)
      --Instead you typed something else or forgot to type it!
      
    -Error spotted at Line: %d

    ****************************** SYN ERROR ******************************
    STATEMENTS()""" %(line))
    exit() 

# -- <STATEMENT> ::= e | <ASSIGNMENT-STAT> | <IF-STAT> | <REPEAT-STAT> | <WHILE-STAT> | <EXIT-STAT> 
#                      | <SWITCH-STAT> | <FORCASE-STAT> | <CALL-STAT> | <RETURN-STAT> | <INPUT-STAT>
#                      | <PRINT-STAT> -- #
def STATEMENT():

  if sys.argv[2] == "-verbose" : print("11. <STATEMENT>")

  global ret_token

  # Sneak Peeks!
  if ret_token == token_dict["alphaTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> ASSIGNMENT_STAT ***")
    ASSIGNMENT_STAT()
  elif ret_token == token_dict["ifTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> IF_STAT ***")
    IF_STAT()
  elif ret_token == token_dict["repTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> REPEAT_STAT ***")
    REPEAT_STAT()
  elif ret_token == token_dict["whileTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> WHILE_STAT ***")
    WHILE_STAT()
  elif ret_token == token_dict["exitTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> EXIT_STAT ***")
    EXIT_STAT()
  elif ret_token == token_dict["swiTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> SWITCH_STAT ***")
    SWITCH_STAT()
  elif ret_token == token_dict["fcaseTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> FORCASE_STAT ***")
    FORCASE_STAT()
  elif ret_token == token_dict["callTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> CALL_STAT ***")
    CALL_STAT()
  elif ret_token == token_dict["retTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> RETURN_STAT ***")
    RETURN_STAT()
  elif ret_token == token_dict["inputTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> INPUT_STAT ***")
    INPUT_STAT()
  elif ret_token == token_dict["printTK"]:
    if sys.argv[2] == "-verbose" : print("*** STATEMENT ==> PRINT_STAT ***")
    PRINT_STAT()
  elif ret_token == "": 
    # e : Not typing a statement is acceptable.
    pass

# -- <ASSIGNMENT-STAT> ::= ID := <EXPRESSION> -- #
def ASSIGNMENT_STAT():

  if sys.argv[2] == "-verbose" : print("12.<ASSIGNMENT-STAT>")

  global ret_token

  if ret_token == token_dict["alphaTK"]:

    if sys.argv[2] == "-verbose" : print("\tASSIGNMENT_STAT\t" + lex_unit)
    lex()
    

    if ret_token == token_dict["assigTK"]:

      if sys.argv[2] == "-verbose" : print("\tASSIGNMENT_STAT\t" + lex_unit)
      lex()
      
      if sys.argv[2] == "-verbose" : print("*** ASSIGNMENT_STAT ==> EXPRESSION ***")
      EXPRESSION()

    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --Assignment operator ':=' not found!

      -Error spotted at Line: %d
          
      ****************************** SYN ERROR ******************************
      ASSIGNMENT_STAT()""" %(line))
        
      exit() 

  # No need to display an error message here. If there was no alpha Token we wouldn't be here.

# -- <IF-STAT> ::= IF <CONDITION> THEN <STATEMENTS> <ELSEPART> ENDIF -- #
def IF_STAT():

  if sys.argv[2] == "-verbose" : print("13.<IF-STAT>")

  global ret_token

  if sys.argv[2] == "-verbose" : print("\tIF_STAT\t" + lex_unit)
  lex()
  
  if sys.argv[2] == "-verbose" : print("*** IF_STAT ==> CONDTITION ***")
  CONDITION()

  if ret_token == token_dict["thenTK"]:

    if sys.argv[2] == "-verbose" : print("\tIF_STAT\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** IF_STAT ==> STATEMENTS ***")
    STATEMENTS()

    if sys.argv[2] == "-verbose" : print("*** IF_STAT ==> ELSEPART ***")
    ELSEPART()

    if ret_token == token_dict["eifTK"]:

      if sys.argv[2] == "-verbose" : print("\tIF_STAT\t" + lex_unit)
      lex()
      

    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --"endif" Commited word missing from if statement.
        --Instead you typed something else or forgot to type it!
          ---Example: if ... then ... endif

      -Error spotted at Line: %d
        
      ****************************** SYN ERROR ******************************
      IF_STAT()""" %(line))

      exit()
  
  else:
    print("""
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --"then" Commited word missing from if statement.
      --Instead you typed something else or forgot to type it!
        ---Example: if ... then ... endif

    -Error spotted at Line: %d
        
    ****************************** SYN ERROR ******************************
    IF_STAT()""" %(line))

    exit()
      
# -- <ELSEPART> ::= e | ELSE <STATEMENTS> -- #
def ELSEPART():

  if sys.argv[2] == "-verbose" : print("14.<ELSEPART>")

  global ret_token

  if ret_token == token_dict["elseTK"]:

    if sys.argv[2] == "-verbose" : print("\tELSEPART\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** ELSEPART ==> STATEMENTS ***")
    STATEMENTS()

  # e : Not determining an else part is acceptable.

# -- <REPEAT-STAT> ::= REPEAT <STATEMENTS> ENDREPEAT -- #
def REPEAT_STAT():

  if sys.argv[2] == "-verbose" : print("15.<REPEAT-STAT>")

  global ret_token

  if ret_token == token_dict["repTK"]:

    if sys.argv[2] == "-verbose" : print("\tREPEAT_STAT\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** REPEAT_STAT ==> STATEMENTS ***")
    STATEMENTS()

    if ret_token == token_dict["erepTK"]:

      if sys.argv[2] == "-verbose" : print("\tREPEAT_STAT\t" + lex_unit)
      lex()
      

    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --"endrepeat" Commited word missing from repeat statement.
        --Instead you typed something else or forgot to type it!
          ---Example: repeat ... endrepeat

      -Error spotted at Line: %d
        
      ****************************** SYN ERROR ******************************
      REPEAT_STAT()""" %(line))
      exit()

  # No need to display an error message. If there was no repeat Token we wouldn't be here.

# -- <EXIT-STAT> ::= EXIT -- #
def EXIT_STAT():

  if sys.argv[2] == "-verbose" : print("16.<EXIT-STAT>")

  global ret_token

  if ret_token == token_dict["exitTK"]:

    if sys.argv[2] == "-verbose" : print("\tEXIT_STAT\t" + lex_unit)
    lex()
    

  # No need to display an error message. If there was no exit Token we wouldn't be here.

# -- <WHILE-STAT> ::= WHILE <CONDITION> <STATEMENTS> ENDWHILE -- #
def WHILE_STAT():

  if sys.argv[2] == "-verbose" : print("17.<WHILE-STAT>")

  global ret_token

  if ret_token == token_dict["whileTK"]:

    if sys.argv[2] == "-verbose" : print("\tWHILE_STAT\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** WHILE_STAT ==> CONDITION ***")
    CONDITION()

    if sys.argv[2] == "-verbose" : print("*** WHILE_STAT ==> STATEMENTS ***")
    STATEMENTS()

    if ret_token == token_dict["ewhileTK"]:

      if sys.argv[2] == "-verbose" : print("\tWHILE_STAT\t" + lex_unit)
      lex()
      
  # No need to display an error message. If there was no while Token we wouldn't be here.

# -- <SWITCH-STAT> ::= SWITCH <EXPRESSION> ( CASE <EXPRESSION> : <STATEMENTS )+ ENDSWITCH -- #
def SWITCH_STAT(): 

  if sys.argv[2] == "-verbose" : print("18.<SWITCH-STAT>")

  global ret_token

  if ret_token == token_dict["swiTK"]:

    if sys.argv[2] == "-verbose" : print("\tSWITCH_STAT\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** SWITCH_STAT ==> EXPRESSION ***")
    EXPRESSION()
    

    if ret_token == token_dict["caseTK"]:

      if sys.argv[2] == "-verbose" : print("\tSWITCH_STAT\t" + lex_unit)
      lex() 
      
      if sys.argv[2] == "-verbose" : print("*** SWITCH_STAT ==> EXPRESSION ***")
      EXPRESSION()
     
      if ret_token == token_dict["colonTK"]:

        if sys.argv[2] == "-verbose" : print("\tSWITCH_STAT\t" + lex_unit)
        lex()
        
        if sys.argv[2] == "-verbose" : print("*** SWITCH_STAT ==> STATEMENTS ***")
        STATEMENTS()

        # Sneak Peek
        while ret_token == token_dict["caseTK"]:

          if sys.argv[2] == "-verbose" : print("\tSWITCH_STAT\t" + lex_unit)
          lex()

          if sys.argv[2] == "-verbose" : print("*** SWITCH_STAT ==> EXPRESSION ***")
          EXPRESSION()

          if ret_token == token_dict["colonTK"]:

            if sys.argv[2] == "-verbose" : print("\tSWITCH_STAT\t" + lex_unit)
            lex()

            if sys.argv[2] == "-verbose" : print("*** SWITCH_STAT ==> STATEMENTS ***")
            STATEMENTS()

          else:
            print("""
            ****************************** SYN ERROR ******************************

            -Invalid Syntax
              --After declaring case's expression colon ':' is expected!
              --Instead you forgot to type it or typed something else!
                ---Example: switch ... case ... : .... endswitch

            -Error spotted at Line: %d

            ****************************** SYN ERROR ******************************
            SWITCH_STAT()""" %(line))
            exit()

        if ret_token == token_dict["eswiTK"]:

          if sys.argv[2] == "-verbose" : print("\tSWITCH_STAT\t" + lex_unit)
          lex()
          

        else:
          print("""
          ****************************** SYN ERROR ******************************

          -Invalid Syntax
            --"endswitch" Commited word missing from switch statement!
            --Instead you forgot to type it or typed something else!

          -Error spotted at Line: %d
        
          ****************************** SYN ERROR ******************************
          SWITCH_STAT()""" %(line))
          exit()

      else:
        print("""
        ****************************** SYN ERROR ******************************
        
        -Invalid Syntax
          --After declaring case's expression colon ':' is expected!
          --Instead you forgot to type it or typed something else!
            ---Example: switch ... case ... : .... endswitch

        -Error spotted at Line: %d
        
        ****************************** SYN ERROR ******************************
        SWITCH_STAT()""" %(line))
        exit()

    else:
      print("""
      ****************************** SYN ERROR ******************************

        -Invalid Syntax
          --After declaring the switch at least one case is required!
          --Instead you forgot to type it or typed something else!
            ---Example: switch ... case ... : .... endswitch

        -Error spotted at Line: %d

      ****************************** SYN ERROR ******************************
      SWITCH_STAT()""" %(line))
      exit()

  # No need to display an error message. If there was no switch Token we wouldn't be here.

# -- <FORCASE-STAT> ::= FORCASE ( WHEN <CONDITION> : <STATEMENTS> )+ ENDFORCASE -- #
def FORCASE_STAT():

  if sys.argv[2] == "-verbose" : print("19.<FORCASE-STAT>")

  global ret_token

  if ret_token == token_dict["fcaseTK"]:

    if sys.argv[2] == "-verbose" : print("\tFORCASE_STAT\t" + lex_unit)
    lex()

    if ret_token == token_dict["whenTK"]:

      if sys.argv[2] == "-verbose" : print("\tFORCASE_STAT\t" + lex_unit)
      lex()
      
      if sys.argv[2] == "-verbose" : print("*** FORCASE_STAT ==> CONDITION ***")
      CONDITION()

      if ret_token == token_dict["colonTK"]:

        if sys.argv[2] == "-verbose" : print("\tFORCASE_STAT\t" + lex_unit)
        lex()
        
        if sys.argv[2] == "-verbose" : print("*** FORCASE_STAT ==> STATEMENTS ***")
        STATEMENTS()

        # Sneak Peek
        while ret_token == token_dict["whenTK"]:

          if sys.argv[2] == "-verbose" : print("\tFORCASE_STAT\t" + lex_unit)
          lex()
          
          if sys.argv[2] == "-verbose" : print("*** FORCASE_STAT ==> CONDITION ***")
          CONDITION()

          if ret_token == token_dict["colonTK"]:

            if sys.argv[2] == "-verbose" : print("\tFORCASE_STAT\t" + lex_unit)
            lex()

            if sys.argv[2] == "-verbose" : print("*** FORCASE_STAT ==> STATEMENTS ***")
            STATEMENTS()

          else:
            print("""
            ****************************** SYN ERROR ******************************
            -Invalid Syntax
              --After declaring forcase's condition colon ':' is expected
              --Instead you forgot to type it or typed something else!
                ---Example: forcase when ... : ... endforcase

            -Error spotted at Line: %d

            ****************************** SYN ERROR ******************************
            FORCASE_STAT()""" %(line))
            exit()

        if ret_token == token_dict["efcaseTK"]: 

          if sys.argv[2] == "-verbose" : print("\tFORCASE_STAT\t" + lex_unit)
          lex()
          

        else:
          print("""
          ****************************** SYN ERROR ******************************

          -Invalid Syntax
            --"endforcase" Commited word missing from forcase statement!
            --Instead you forgot to type it or typed something else!

          -Error spotted at Line: %d
        
          ****************************** SYN ERROR ******************************
          FORCASE_STAT()""" %(line))
          exit()

      else:
        print("""
        ****************************** SYN ERROR ******************************

        -Invalid Syntax
          --After declaring forcase's condition colon ':' is expected
          --Instead you forgot to type it or typed something else!
            ---Example: forcase when ... : ... endforcase

        -Error spotted at Line: %d

        ****************************** SYN ERROR ******************************
        FORCASE_STAT()""" %(line))
        exit()

    else: 
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --"when" Commited word expected after forcase!
        --Instead you forgot to type it or typed something else!
          ---Example: forcase when ... : ... endforcase

      -Error spotted at Line: %d

      ****************************** SYN ERROR ******************************
      FORCASE_STAT()""" %(line))
      exit()

# -- <CALL-STAT> ::= CALL ID <ACTUALPARS> -- #
def CALL_STAT():

  if sys.argv[2] == "-verbose" : print("20.<CALL-STAT>")

  global ret_token 

  if ret_token == token_dict["callTK"]:

    if sys.argv[2] == "-verbose" : print("\tCALL_STAT\t" + lex_unit)
    lex()
    
    if ret_token == token_dict["alphaTK"]:

      if sys.argv[2] == "-verbose" : print("\tCALL_STAT\t" + lex_unit)
      lex()
      
      if sys.argv[2] == "-verbose" : print("*** CALL_STAT ==> ACTUALPARS ***")
      ACTUALPARS()

    else: 
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --Function's/Procedure's name is expected after call!
        --Instead you forgot to type it or typed something else!
            ---Example: call function1( ... )

      -Error spotted at Line: %d

      ****************************** SYN ERROR ******************************
      CALL_STAT()""" %(line))

      exit()

# -- <RETURN-STAT> ::= RETURN <EXPRESSION> -- #
def RETURN_STAT():

  if sys.argv[2] == "-verbose" : print("21.<RETURN-STAT>")

  global ret_token

  if ret_token == token_dict["retTK"]:

    if sys.argv[2] == "-verbose" : print("\tRETURN_STAT\t" + lex_unit)
    lex() 
    
    if sys.argv[2] == "-verbose" : print("*** RETURN_STAT ==> EXPRESSION ***")
    EXPRESSION()

  # No need to display an error message. If there was no return Token we wouldn't be here.

# -- <PRINT-STAT> ::= PRINT <EXPRESSION> -- #
def PRINT_STAT():

  if sys.argv[2] == "-verbose" : print("22.<PRINT-STAT>")

  global ret_token

  if ret_token == token_dict["printTK"]:

    if sys.argv[2] == "-verbose" : print("\tPRINT_STAT\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** PRINT_STAT ==> EXPRESSION ***")
    EXPRESSION()
  # No need to display an error message. If there was no print Token we wouldn't be here.

# -- <ACTUALPARS> ::= ( <ACTUALPARLIST> ) -- #
def ACTUALPARS():

  if sys.argv[2] == "-verbose" : print("23.<ACTUALPARS>")

  global ret_token

  if ret_token == token_dict["lbrTK"]:

    if sys.argv[2] == "-verbose" : print("\tACTUALPARS\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** ACTUALPARS ==> ACTUALPARLIST ***")
    ACTUALPARLIST()

    if ret_token == token_dict["rbrTK"]:

      if sys.argv[2] == "-verbose" : print("\tACTUALPARS\t" + lex_unit)
      lex()

    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --After declaring the parameters right bracket character ')'
          is required
        --Instead you forgot to type it or typed something else!
  
      -Error spotted at Line: %d

      ****************************** SYN ERROR ******************************
      ACTUALPARS()""" %(line))
      exit()

  else:
    print("""
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --To start declaring the parameters left bracket character '('
        is required
      --Instead you forgot to type it or typed something else!
  
    -Error spotted at Line: %d

    ****************************** SYN ERROR ******************************
    ACTUALPARS()""" %(line))
    exit()

# -- <ACTUALPARLIST> ::= <ACTUALPARITEM> (, <ACTUALPARITEM> )* | e -- #
def ACTUALPARLIST():

  if sys.argv[2] == "-verbose" : print("24.<ACTUALPARLIST>")

  global ret_token

  # Sneak Peek
  if ret_token == token_dict["inTK"] or ret_token == token_dict["inoutTK"]:

    if sys.argv[2] == "-verbose" : print("*** ACTUALPARLIST ==> ACTUALPARITEM ***")
    ACTUALPARITEM()

    while ret_token == token_dict["commaTK"]:

      if sys.argv[2] == "-verbose" : print("\tACTUALPARLIST\t" + lex_unit)
      lex()

      if sys.argv[2] == "-verbose" : print("*** ACTUALPARLIST ==> ACTUALPARITEM ***")
      ACTUALPARITEM()

  # e : Not defining an actual parameter is acceptable.

# -- <ACTUALPARITEM> ::= IN <EXPRESSION> | INOUT ID -- #
def ACTUALPARITEM():

  if sys.argv[2] == "-verbose" : print("25.<ACTUALPARITEM>")

  global ret_token

  if ret_token == token_dict["inTK"]:

    if sys.argv[2] == "-verbose" : print("\tACTUALPARITEM\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** ACTUALPARITEM ==> EXPRESSION ***")
    EXPRESSION()

  elif ret_token == token_dict["inoutTK"]:

    if sys.argv[2] == "-verbose" : print("\tACTUALPARITEM\t" + lex_unit)
    lex()

    if ret_token == token_dict["alphaTK"]:

      if sys.argv[2] == "-verbose" : print("\tACTUALPARITEM\t" + lex_unit)
      lex()

    else: 
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --Passing by reference without declaring variable name detected!       

      -Error spotted at Line: %d

      ****************************** SYN ERROR ******************************
      ACTUALPARITEM()""" %(line))

      exit()

# -- <CONDITION> ::= <BOOLTERM> ( OR <BOOLTERM> )* -- #
def CONDITION():

  if sys.argv[2] == "-verbose" : print("26.<CONDITION>")

  global ret_token 

  if sys.argv[2] == "-verbose" : print("*** CONDITION ==> BOOLTERM ***")
  BOOLTERM()

  while ret_token == token_dict["orTK"]:

    if sys.argv[2] == "-verbose" : print("\tCONDITION\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** CONDITION ==> BOOLTERM ***")
    BOOLTERM()

# -- <BOOLTERM> ::= <BOOLFACTOR> ( AND <BOOLFACTOR> )* -- #
def BOOLTERM():

  if sys.argv[2] == "-verbose" : print("27.<CONDITION>")

  global ret_token

  if sys.argv[2] == "-verbose" : print("*** BOOLTERM ==> BOOLFACTOR ***")
  BOOLFACTOR()

  while ret_token == token_dict["andTK"]:

    if sys.argv[2] == "-verbose" : print("\tBOOLTERM\t" + lex_unit)
    lex()

    if sys.argv[2] == "-verbose" : print("*** BOOLTERM ==> BOOLFACTOR ***")
    BOOLFACTOR()

# -- <BOOLFACTOR> ::= NOT [ <CONDITION> ] | [ <CONDITION> ] | <EXPRESSION> <RELATIONAL-OPER> <EXPRESSION> 
#                                         | TRUE | FALSE -- #
def BOOLFACTOR():
  
  if sys.argv[2] == "-verbose" : print("28.<BOOLFACTOR>")

  global ret_token
  
  if ret_token == token_dict["notTK"]:

    if sys.argv[2] == "-verbose" : print("\tBOOLFACTOR\t" + lex_unit)
    lex()

    if ret_token == token_dict["blbrTK"]:

      if sys.argv[2] == "-verbose" : print("\tBOOLFACTOR\t" + lex_unit)
      lex()
      
      if sys.argv[2] == "-verbose" : print("*** BOOLFACTOR ==> CONDITION ***")
      CONDITION()

      if ret_token == token_dict["brbrTK"]:

        if sys.argv[2] == "-verbose" : print("\tBOOLFACTOR\t" + lex_unit)
        lex()

      else:
        print("""
        ****************************** SYN ERROR ******************************

        -Invalid Syntax
          --After declaring a condition you have to put ']'
          --Instead you forgot to type it or typed something else!
            ---Example: not [a operator b]

        -Error spotted at Line: %d

        ****************************** SYN ERROR ******************************
        BOOLFACTOR()""" %(line))

        exit()

    else:
        print("""
        ****************************** SYN ERROR ******************************

        -Invalid Syntax
          --Before declaring a condition you have to put '['
          --Instead you forgot to type it or typed something else!
            ---Example: not [a operator b]

        -Error spotted at Line: %d

        ****************************** SYN ERROR ******************************
        BOOLFACTOR()""" %(line))

        exit()

  elif ret_token == token_dict["blbrTK"]:

    if sys.argv[2] == "-verbose" : print("\tBOOLFACTOR\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("*** BOOLFACTOR ==> CONDITION ***")
    CONDITION()

    if ret_token == token_dict["brbrTK"]:

      if sys.argv[2] == "-verbose" : print("\tBOOLFACTOR\t" + lex_unit)
      lex()

    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --After declaring a condition you have to put ']'
        --Instead you forgot to type it or typed something else!
          ---Example: not [a operator b]

      -Error spotted at Line: %d

      ****************************** SYN ERROR ******************************
      BOOLFACTOR()""" %(line))

      exit()

  # Sneak Peek
  elif ret_token == token_dict["plusTK"] or ret_token == token_dict["minusTK"] or ret_token == token_dict["numberTK"] or ret_token == token_dict["lbrTK"] or ret_token == token_dict["alphaTK"]:

    if sys.argv[2] == "-verbose" : print("*** BOOLFACTOR ==> EXPRESSION ***")
    EXPRESSION()
    if sys.argv[2] == "-verbose" : print("*** BOOLFACTOR ==> RELATIONAL_OPER ***")
    RELATIONAL_OPER()
    if sys.argv[2] == "-verbose" : print("*** BOOLFACTOR ==> EXPRESSION ***")
    EXPRESSION()

  elif ret_token == token_dict["trueTK"]:

    if sys.argv[2] == "-verbose" : print("\tBOOLFACTOR\t" + lex_unit)
    lex()

  elif ret_token == token_dict["falseTK"]:

    if sys.argv[2] == "-verbose" : print("\tBOOLFACTOR\t" + lex_unit)
    lex()

# -- <EXPRESSION> ::= <OPTIONAL-SIGN> <TERM> ( <ADD-OPER> <TERM> )* -- #
def EXPRESSION(): 

  if sys.argv[2] == "-verbose" : print("29.<EXPRESSION>")

  global ret_token

  if sys.argv[2] == "-verbose" : print("*** EXPRESSION ==> OPTIONAL_SIGN ***")
  OPTIONAL_SIGN()
  if sys.argv[2] == "-verbose" : print("*** EXPRESSION ==> TERM ***")
  TERM()

  #Sneak Peek
  while( ret_token == token_dict["plusTK"] or ret_token == token_dict["minusTK"] ):

    if sys.argv[2] == "-verbose" : print("*** EXPRESSION ==> ADD_OPER ***")
    ADD_OPER()
    if sys.argv[2] == "-verbose" : print("*** EXPRESSION ==> TERM ***")
    TERM()

# -- <TERM> ::= <FACTOR> ( <MUL-OPER> <FACTOR> )* -- #
def TERM():

  if sys.argv[2] == "-verbose" : print("30.<TERM>")

  global ret_token

  if sys.argv[2] == "-verbose" : print("*** TERM ==> FACTOR ***")
  FACTOR()

  #Sneak Peek
  while(ret_token == token_dict["mulTK"] or ret_token == token_dict["divTK"]):

    if sys.argv[2] == "-verbose" : print("*** TERM ==> MUL_OPER ***")
    MUL_OPER()
    if sys.argv[2] == "-verbose" : print("*** TERM ==> FACTOR ***")
    FACTOR()

# -- <FACTOR> ::= COSTANT | ( <EXPRESSION> ) | ID <IDTAIL> -- #
def FACTOR():

  if sys.argv[2] == "-verbose" : print("31.<FACTOR>")

  global ret_token

  if ret_token == token_dict["numberTK"]:

    if sys.argv[2] == "-verbose" : print("\tFACTOR\t" + lex_unit)
    lex()

  elif ret_token == token_dict["lbrTK"]:

    if sys.argv[2] == "-verbose" : print("\tFACTOR\t" + lex_unit)
    lex()
    
    if sys.argv[2] == "-verbose" : print("\tFACTOR\t" + lex_unit)
    EXPRESSION()

    if ret_token == token_dict["rbrTK"]:

      if sys.argv[2] == "-verbose" : print("\tFACTOR\t" + lex_unit)
      lex()


    else:
      print("""
      ****************************** SYN ERROR ******************************

      -Invalid Syntax
        --After declaring an expression you have to put ')'
        --Instead you forgot to type it or typed something else!
          ---Example: ( expression )

      -Error spotted at Line: %d

      ****************************** SYN ERROR ******************************
      FACTOR()""" %(line))

      exit()

  elif ret_token == token_dict["alphaTK"]:

    if sys.argv[2] == "-verbose" : print("\tFACTOR\t" + lex_unit)
    lex()

    if sys.argv[2] == "-verbose" : print("*** FACTOR ==> IDTAIL ***")
    IDTAIL()

  else:
    print("""
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --Invalid FACTOR used!
        ---[NOTE]: Read EEL's documentation file to see which
                   options are available for factor usage.

    -Error spotted at Line: %d

    ****************************** SYN ERROR ******************************
    FACTOR()""" %(line))

    exit()

# -- <IDTAIL> ::= e | <ACTUALPARS> -- #
def IDTAIL():

  if sys.argv[2] == "-verbose" : print("32.<IDTAIL>")

  global ret_token

  if ret_token == token_dict["lbrTK"]:

    if sys.argv[2] == "-verbose" : print("*** IDTAIL ==> ACTUALPARS ***")
    ACTUALPARS()

  # e : No statements after an ID is acceptable.

# -- <RELATIONAL-OPER> ::= = | <= | >= | > | < | <> -- #
def RELATIONAL_OPER():

  if sys.argv[2] == "-verbose" : print("33.<RELATIONAL-OPER>")

  global ret_token 

  if ret_token == token_dict["eqTK"]:

    if sys.argv[2] == "-verbose" : print("\tRELATIONAL_OPER\t" + lex_unit)
    lex()

  elif ret_token == token_dict["leqTK"]:

    if sys.argv[2] == "-verbose" : print("\tRELATIONAL_OPER\t" + lex_unit)
    lex()

  elif ret_token == token_dict["greqTK"]:
    
    if sys.argv[2] == "-verbose" : print("\tRELATIONAL_OPER\t" + lex_unit)
    lex()

  elif ret_token == token_dict["greaTK"]:

    if sys.argv[2] == "-verbose" : print("\tRELATIONAL_OPER\t" + lex_unit)
    lex()

  elif ret_token == token_dict["lessTK"]:

    if sys.argv[2] == "-verbose" : print("\tRELATIONAL_OPER\t" + lex_unit)
    lex()

  elif ret_token == token_dict["difTK"]:

    if sys.argv[2] == "-verbose" : print("\tRELATIONAL_OPER\t" + lex_unit)
    lex()

  else:
    print("""
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --Invalid RELATIONAL OPERATOR used!
        ---[NOTE]: Read EEL's documentation file to see which
                   options are available for relational op usage!

    -Error spotted at Line: %d

    ****************************** SYN ERROR ******************************
    RELATIONAL_OPER()""" %(line))
    exit()

# -- <ADD-OPER> ::= + | - -- #
def ADD_OPER():

  if sys.argv[2] == "-verbose" : print("34.<ADD-OPER>")

  global ret_token

  if ret_token == token_dict["plusTK"]:

    if sys.argv[2] == "-verbose" : print("\tADD_OPER\t" + lex_unit)
    lex()

  elif ret_token == token_dict["minusTK"]:

    if sys.argv[2] == "-verbose" : print("\tADD_OPER\t" + lex_unit)
    lex()

  else:
    print("""
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --Invalid ADDITION OPERATOR used!
        ---[NOTE]: Read EEL's documentation file to see which
                   options are available for add op usage!

    -Error spotted at Line: %d

    ****************************** SYN ERROR ******************************
    MUL_OPER()""" %(line))
    exit()

# -- <MUL-OPER> ::= * | / -- #
def MUL_OPER():

  if sys.argv[2] == "-verbose" : print("35.<MUL-OPER>")

  global ret_token

  if ret_token == token_dict["mulTK"]:

    if sys.argv[2] == "-verbose" : print("\tMUL_OPER\t" + lex_unit)
    lex()

  elif ret_token == token_dict["divTK"]:

    if sys.argv[2] == "-verbose" : print("\tMUL_OPER\t" + lex_unit)
    lex()
  else:
    print("""
    ****************************** SYN ERROR ******************************

    -Invalid Syntax
      --Invalid MULTIPLICATION OPERATOR used!
        ---[NOTE]: Read EEL's documentation file to see which
                   options are available for mul op usage!

    -Error spotted at Line: %d

    ****************************** SYN ERROR ******************************
    MUL_OPER()""" %(line))
    exit()

#  -- <OPTIONAL-SIGN> ::= e | <ADD-OPER> -- #
def OPTIONAL_SIGN():

  if sys.argv[2] == "-verbose" : print("36.<OPTIONAL-SIGN>")

  global ret_token

  if ret_token == token_dict["plusTK"] or ret_token == token_dict["minusTK"]:

    if sys.argv[2] == "-verbose" : print("*** OPTIONAL_SIGN ==> ADD_OPER ***") 
    ADD_OPER()

  # e : Not using an add operator is acceptable.


# *********** [MAIN FUNCTION] *********** #
if __name__ == '__main__':

  try:
    
    if sys.argv[2] != "-verbose" and sys.argv[2] != "-skip" : raise IndexError
    if ".eel" in sys.argv[1] : raise IOError

    global code 
    #global line
    eel_source_code = sys.argv[1]
    code = open(eel_source_code+".eel")

    # Lexical Test #
    if sys.argv[2] == "-verbose" : print(" ===========> START OF LEX !! <=========== ")
    a = lex()
    verbose_iterator = 0;
    if sys.argv[2] == "-verbose" : print(str(verbose_iterator)+"."+" "+ str(a) + "\t\t" + lex_unit)

    while(a != token_dict["eofTK"]):

      a = lex()
      verbose_iterator = verbose_iterator + 1;
      if sys.argv[2] == "-verbose" : print(str(verbose_iterator)+"."+" "+ str(a) + "\t\t" + lex_unit)

    if sys.argv[2] == "-skip" : print("\n\tLEX Test:\t[ OK! ]")
    
    # Reset the File Pointer and Line Counter
    code.seek(0,0)
    line = 1 

    # Syntax Test #
    
    lex()
    PROGRAM()
    if sys.argv[2] == "-skip" : print("\tSYN Test:\t[ OK! ]\n")

    code.close()

  except IndexError: 
    print("""
Usage: python EELC.py [source file name] [options]
Where possible options include:

  -verbose\t Output messages about what the compiler is doing. 
          \t Redirection is reccomended due to wealth of text messages.
          \t [ e.g >python EELC.py example -verbose > output.txt ] 

  -skip   \t Output messages only for the progression of the analysis.
          \t Outputs "OK!" messages on success.
          """)
  except IOError:
    print("""
Usage: python EELC.py [source file name] [options]
  
  - ".eel" Ending is not required on [source file name]!

  - [ e.g >python EELC.py example -skip] )
    """)

