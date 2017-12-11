# Variables for pre-processing of responses

#

# each row in xmlManglers consists of:

#  1. the xml tag(s) which contain data to be mangled.  Tags are separated by '|'

#  2. a regular expression identifying text to be found

#  3. optionally two expressions which will be placed before and after the text identified by the regular expression

#     If not entered it will default to "['{% raw rollDate("','",respCreatedDate,stubbedToday)%}']" which rolls dates

#

# You can have as many xmlManger rows as you want.  Each row can have different #templateFixs', or use the default

# Mini regular expression tutorial:

# [0-9]{6} => any 6 digits

# [0-9]{6}|[0-9]{2} => and 6 digits or any 2 digits

# [A-Za-z]{3} => any 3 upper or lower case letters

# JAN|FEB|MAR => JAN or FEB or MAR

#



from stubo.ext.ba.stringSplitter import stringSplitter

import stubo.ext.ba.stubbedInterface as stubbedInterface

import stubo.ext.ba.datePatterns as datePatterns

from stubo.ext.ba.stubbedInterface import composeSuffixedReplaceAllSS



# Variables for pre-processing of responses

# Chris Ash - 24Sep12 - Added EUCN date rolling to roll the date in the ssr freetext

#Shivam Gandhi - 20Aug14 -  Added HBFF date rolling to roll the date in the longFreetext
responseInterface = {'xmlManglers':

    [['(arrDate|depDate|arrivalDate|departureDate|DepartureDate|date|dateOfArrival|dateOfDeparture)', '([0-9]{6}|[0-9]{2}[A-Za-z]{3}[0-9]{4})'],

#        ['Response', '([0-9]{2}(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)([0-9]{2}|' '))'],

        ['PDTDate', '([0-9]{2}(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[0-9]{4})',

        ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ['(creationDate)', '[0-9]{6}', ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

#        ["pnrHeader", stubbedInterface.composeInfixedSS("<depDate>",datePatterns.ddmmyy, "</depDate>(?!\s*<depTime>)")],

#        ["pnrHeader", stubbedInterface.composeInfixedSS("<depDate>",datePatterns.ddmmyy, "</depDate>(?=\s*<depTime>)"), ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

#        ["product", stubbedInterface.composeInfixedSS("<depDate>",datePatterns.ddmmyy, "</depDate>(?!\s*<depTime>)")],

#        ["product", stubbedInterface.composeInfixedSS("<depDate>",datePatterns.ddmmyy, "</depDate>(?=\s*<depTime>)"), ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ["freetext", stubbedInterface.composePrefixedSS(".*RQST.*?" , datePatterns.ddMmMyy)],

        ["freetext", stubbedInterface.composePrefixedSS(".*CAGT.*?" , datePatterns.ddMmMyy)],

        ["freetext", stubbedInterface.composePrefixedSS(".*PAGT.*?" , datePatterns.ddMmMyy)],
        
		["longFreetext", stubbedInterface.composePrefixedSS(".*HBFF.*?" , datePatterns.ddMmMyy)],        

        ["serviceRequest/ssr", stubbedInterface.composePrefixedSS(".*EUCN.*?" , datePatterns.ddMmMyy)],

        ["serviceRequest/ssr", stubbedInterface.composePrefixedSS(".*INFT.*?" , datePatterns.ddMmMyy)],

        ["Cryptic_GetScreen_Reply/CAPI_Screen/Response", stubbedInterface.composePrefixedSS("^(?!FQC).*" , datePatterns.ddMmMyy)],

        ["Cryptic_GetScreen_Reply/CAPI_Screen/Response", stubbedInterface.composePrefixedSS("FQC.*?" , datePatterns.ddMmMyy), ['{% raw rollDate("','",respCreatedStubbedSystemDate,stubbedToday) %}']]

    ],

        'templateFixs': ['{% raw rollDate("','",respCreatedDate,stubbedToday)%}']

    }



###########################################################################

# Variables for processing of matchers

#['Cryptic_GetScreen_Query/Command', '[0-9]{2}(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[0-9]{2}'],

# Chris Ash - 24Sep12 - Added EUCN date rolling to roll the date in the ssr freetext



matcherInterface = {'xmlManglers':

        [['(departureDate|depDate|date|arrDate)', '([0-9]{6}|[0-9]{2}[A-Za-z]{3}[0-9]{4})'],

    ['dateTime', '<year>[0-9]{4}</year><month>[0-9]{2}</month><day>[0-9]{2}</day>',

        ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ['PDTDate', '[0-9]{2}(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[0-9]{4}',

        ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ['freetext', stubbedInterface.composeSuffixedReplaceAllSS("UPGD USING AVIOS" , datePatterns.ddMMM), ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ["serviceRequest/ssr", stubbedInterface.composePrefixedSS(".*EUCN.*?" , datePatterns.ddMmMyy)],

        ["Cryptic_GetScreen_Query/Command", stubbedInterface.composePrefixedSS("IMCST.*" , datePatterns.ddMMM)],

        ["Cryptic_GetScreen_Query/Command", stubbedInterface.composePrefixedSS("IMCXP.*" , datePatterns.ddMMM)],

        ["Cryptic_GetScreen_Query/Command", stubbedInterface.composePrefixedSS("^(?!FQC).*" , datePatterns.ddMmmyyyy)],

        ["Cryptic_GetScreen_Query/Command", stubbedInterface.composePrefixedSS("FQM.*" , datePatterns.ddMmMyy)],

        ["Cryptic_GetScreen_Query/Command", stubbedInterface.composePrefixedSS("FQC.*" , datePatterns.ddMmMyy), ['{% raw rollDate("','",respCreatedStubbedSystemDate,stubbedToday) %}']]

    ]

        }

'''



matcherInterface = {'xmlManglers':\

    [['(arrDate|arrivalDate|departureDate|DepartureDate|date|dateOfArrival|dateOfDeparture)', '([0-9]{6}|[0-9]{2}[A-Za-z]{3}[0-9]{4})', ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ['Response', '([0-9]{2}(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)([0-9]{2}|' '))'],

    ['freetext', stubbedInterface.composeSuffixedReplaceAllSS("UPGD USING AVIOS" , datePatterns.ddMMM), ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ['PDTDate', '([0-9]{2}(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[0-9]{4})',

        ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ['(creationDate)', '[0-9]{6}', ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ["product", stubbedInterface.composeInfixedSS("<depDate>",datePatterns.ddmmyy, "</depDate>(?!<depTime>)")],

        ["product", stubbedInterface.composeInfixedSS("<depDate>",datePatterns.ddmmyy, "</depDate>(?=<depTime>)"), ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']],

        ["Cryptic_GetScreen_Query/Command", stubbedInterface.composePrefixedSS("^(?!FQC).*" , datePatterns.ddMmMyy)],

    ["Cryptic_GetScreen_Query/Command", stubbedInterface.composePrefixedReplaceAllSS("FQC" , datePatterns.ddMmMyy)],

#   ['{% raw rollDate("','",respCreatedStubbedSystemDate,requestStubbedSystemDate) %}']]

        ],

       'templateFixs': ['{{rollDate("','",respCreatedDate,stubbedToday)}}']

    }

'''



#

# Splitter definitions

# 

# Here we define the individual splitters using the methods of the

# stringSplitter class.

#

# Splitters search through a  string using find and pos (position)

# methods. The string can be 'kept' or 'ignored', a mode that is

# controlled by keep and ignore methods. 

# 

# Splitters should be defined to do one specific job - the find and findRE

# methods should also be viewed as assertions - so if any fail the whole

# sequence will fail. 

#

# Stubo will try every splitter in turn - see the splitters list at the

# bottom of this file

#

from stubo.ext.ba.stringSplitter import stringSplitter





# added by JC and CA for booking fee tests (16Feb2012)

# Request = <Cryptic_GetScreen_Query><Command>TWD/TKT125-2490241297</Command></Cryptic_GetScreen_Query>

# Split = <Cryptic_GetScreen_Query><Command>TWD/

def splitter_Cryptic_GetScreen_Query_TWD(matcherValue):



    s=stringSplitter(matcherValue)

    s.findRE('^<Cryptic_GetScreen_Query><Command>TWD/')     # find and assert the XML



    return s.getResult()                                    # capture that, split & return  



# added by JC and CA for booking fee tests (16Feb2012)

# Request = <Cryptic_GetScreen_Query><Command>IMCSS/BAHEL16FEB/EUR2/**-3614-CPH40*ONLINE BKG FEE/P1</Command></Cryptic_GetScreen_Query>

# Split = <Cryptic_GetScreen_Query><Command>IMCSS/BA

def splitter_Cryptic_GetScreen_Query_IMCSS(matcherValue):



    s=stringSplitter(matcherValue)

    s.findRE('^<Cryptic_GetScreen_Query><Command>IMCSS/BA')     # find and assert the XML



    return s.getResult()                                        # capture that, split & return  

    

    

def splitter_Cryptic_GetScreen_Query_FPP_afterslashN_beforecolon(matcherValue):

    """

    Author : John Davenport

    Date   : May 2010

    

    Request = <Cryptic_GetScreen_Query><Command>FPPAXCDSO/676782009988007706/1214/N2412*123456789:06/P2</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FPPAXCDSO/676782009988007706/1214/N:06/P2</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FPP')     # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/N")                                        # find to /N

    s.ignore()                                          # ignore what follows

    s.find(":")                                         # until after the nnnnnnnn

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return

    

def splitter_Cryptic_GetScreen_Query_FOPAX(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FOPAX125-2490015603E1JNB22JUN12/77493651/125-2490015603E1*V/P1</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FOPAX125-2490015603E1*V/P1</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FOPAX')    # find and assert the XML

    s.find("E1")                                         # find to E1

    s.ignore()                                           # ignore what follows

    s.find("E1*")                                         # until after the next E1

    s.keep()                                             # keep what follows

    s.posEnd()                                           # up to the end

    return s.getResult()                                 # capture that, split & return



def splitter_Cryptic_GetScreen_Query_FOINF(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FOINF125-2490015603E1JNB22JUN12/77493651/125-2490015603E1*V/P1</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FOINF125-2490015603E1*V/P1</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FOINF')    # find and assert the XML

    s.find("E1")                                         # find to E1

    s.ignore()                                           # ignore what follows

    s.find("E1*")                                         # until after the next E1

    s.keep()                                             # keep what follows

    s.posEnd()                                           # up to the end

    return s.getResult()                                 # capture that, split & return 

    

def splitter_Cryptic_GetScreen_Query_FO(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FO125-2490015603E1JNB22JUN12/77493651/125-2490015603E1*V/P1</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FO125-2490015603E1*V/P1</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FO')    # find and assert the XML

    s.find("E1")                                         # find to E1

    s.ignore()                                           # ignore what follows

    s.find("E1*")                                         # until after the next E1

    s.keep()                                             # keep what follows

    s.posEnd()                                           # up to the end

    return s.getResult()                                 # capture that, split & return 

    

def splitter_Cryptic_GetScreen_Query_FPP_AfterSlash(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FQPDEL/ABA/D17JUN/CILHR-/ABA/D23JUN/CIDEL- /L/RADT,07MAR12,P,UP</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FQPDEL/ABA</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FPP')     # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/")                                         # find to /

    s.ignore()                                          # ignore what follows

    s.find("</Command>")                                # until after the ,

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return

    

def splitter_Cryptic_GetScreen_Query_FQP_AfterSlash(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FQPDEL/ABA/D17JUN/CILHR-/ABA/D23JUN/CIDEL- /L/RADT,07MAR12,P,UP</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FQPDEL/ABA</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FQP')     # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/")                                         # find to /

    s.ignore()                                          # ignore what follows

    s.find("</Command>")                                # until after the ,

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return



def splitter_Cryptic_GetScreen_Query_FPINFO_afterslashN_beforecolon(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FPINFO/CVI+/CVI/4111111111003771/0115/N2412*13088642:/P1</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FPINFO/CVI+/CVI/4111111111003771/0115</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FPINF')  # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/N")                                        # find to /N

    s.ignore()                                          # ignore what follows

    s.find("</Command>")                                # until after the nnnnnnnn

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return

    

def splitter_Cryptic_GetScreen_Query_FPC_afterslashN_beforecolon(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FPCVI/4111111111003771/0115/N2412*13088642:/L8</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FPCVI/4111111111003771/0115/N:/L8</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FPC')  # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/N")                                        # find to /N

    s.ignore()                                          # ignore what follows

    s.find(":")                                         # until after the nnnnnnnn

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return

    

def splitter_Cryptic_GetScreen_Query_FPC_afterslashN_beforeslash(matcherValue):

    """

    Author : Chris Ash

    Date   : Jan 2013

    

    Request = <Cryptic_GetScreen_Query><Command>FPCVI/4111111111003771/0115/N2412*13088642:/L8</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FPCVI/4111111111003771/0115/N/L8</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FPC')  # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/N")                                        # find to /N

    s.ignore()                                          # ignore what follows

    s.find("/")                                         # until after the slash

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return

    

def splitter_Cryptic_GetScreen_Query_FPO_afterslashN_beforecolon(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FPO/NONREF+/CVI/4111111111111111/0115/N2412*13083942:</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FPO/NONREF+/CVI/4111111111111111/0115/N:</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FPO')     # find and assert the XML

    s.find("/C")                                        # find to /C

    s.find("/N")                                        # find to /N

    s.ignore()                                          # ignore what follows

    s.find(":")                                         # until after the nnnnnnnn

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return



def splitter_Cryptic_GetScreen_Query_FPP_afterslashN_beforeslash(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request = <Cryptic_GetScreen_Query><Command>FPPAXCAX/372701001008260/0116/N2412*12793258/P1</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>FPPAXCAX/372701001008260/0116/N/P1</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>FPP')     # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/N")                                        # find to /N

    s.ignore()                                          # ignore what follows

    s.find("/")                                         # until after the nnnnnnnn

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return
    
    
    
def splitter_Cryptic_GetScreen_Query_TMI_afterslashN_beforeslash(matcherValue):

    """

    Author : Shivam Gandhi

    Date   : 11 Aug,14

    

    Request = <Cryptic_GetScreen_Query><Command>TMI/M1/FP-CAX/372701001008260/0116/N678999*14429299</Command></Cryptic_GetScreen_Query>

    Split = <Cryptic_GetScreen_Query><Command>TMI/M1/FP-CAX/372701001008260/0116/N</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>TMI')     # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/N")                                        # find to /N

    s.ignore()                                          # ignore what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return    
    
    
def splitter_Cryptic_GetScreen_Query_TMI_PaymentReference(matcherValue):

    """

    Author : Shivam Gandhi

    Date   : 11 Aug,14

    

    Request = <Cryptic_GetScreen_Query><Command>TMI/M1/HPayment Reference-14429305</Command></Cryptic_GetScreen_Query> 

    Split = <Cryptic_GetScreen_Query><Command>TMI/M1/HPayment Reference</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>TMI')     # find and assert the XML

    s.find("/")                                         # find to /

    s.find("/HPayment Reference")                       # find to /N

    s.ignore()                                          # ignore what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return 



def splitter_Cryptic_GetScreen_Query_TTI_VXX(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request=<Cryptic_GetScreen_Query><Command>TTI/T4/RGBP368.00/OGBP3.20XA/OGBP1.90XF/OGBP239.00YQ/OGBP3.50YC/OGBP21.40US/OGBP34.49UB/OGBP65.00GB/OGBP1.60AY/OGBP4.50DU/OGBP4.50XY/TGBP149.00/VXX15OCT/C+PD XF IAH3.0/DLONLON/CLON BA HOU172.84BA LON408.04NUC580.88END ROE0.633508 PD XF IAH3.00</Command></Cryptic_GetScreen_Query>

    Split=<Cryptic_GetScreen_Query><Command>TTI/T4/RGBP368.00/OGBP3.20XA/OGBP1.90XF/OGBP239.00YQ/OGBP3.50YC/OGBP21.40US/OGBP34.49UB/OGBP65.00GB/OGBP1.60AY/OGBP4.50DU/OGBP4.50XY/TGBP149.00/VXX

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>TTI/')    # find and assert the XML

    s.find("VXX")                                       # find to vxx

    return s.getResult()                                # and return



def findPoweredPNR_AddMultiElements_FreetextRemover(matcherValue):

    """

    A splitter that removes everything after the first freetext remark

    Date   : Oct 2012

    

    """

    s=stringSplitter(matcherValue)

    s.findRE('^<PoweredPNR_AddMultiElements><pnrActions>')

    s.find('<optionCode>')

    s.find('<traveller>') 

    s.find('<surname>')

    s.find('<origin>')

    s.find('<destination>')

    s.find('<travelProduct>')

    s.find('<depDate>')

    s.find('<freetext>')

    s.ignore()                                 # and ignore what follows

    s.find('</PoweredPNR_AddMultiElements>')   # until here

    s.keep()

    s.posEnd()                                                           

    return s.getResult() 
    
    

def findPoweredQueue_PlaceHBFFPNR(matcherValue):

    """
    
    Request:

	<PoweredQueue_PlacePNR><placementOption><selectionDetails><option>QED</option></selectionDetails></placementOption><targetDetails><targetOffice><sourceType><sourceQualifier1>4</sourceQualifier1></sourceType><originatorDetails><inHouseIdentification1>LONBA07O8</inHouseIdentification1></originatorDetails></targetOffice><queueNumber><queueDetails><number>60</number></queueDetails></queueNumber><categoryDetails><subQueueInfoDetails><identificationType>C</identificationType><itemNumber>0</itemNumber></subQueueInfoDetails></categoryDetails><placementDate><dateTime><year>2014</year><month>06</month><day>27</day><hour>19</hour></dateTime></placementDate></targetDetails><recordLocator><reservation><controlNumber>6HA2AV</controlNumber></reservation></recordLocator></PoweredQueue_PlacePNR>

    Matching Request:

	<PoweredQueue_PlacePNR><placementOption><selectionDetails><option>QED</option></selectionDetails></placementOption><targetDetails><targetOffice><sourceType><sourceQualifier1>4</sourceQualifier1></sourceType><originatorDetails><inHouseIdentification1>LONBA07O8

    A splitter that removes everything after the first Office Id remark

    Date   : Aug 2014

    Shivam Gandhi

    """

    s=stringSplitter(matcherValue)

    s.findRE('^<PoweredQueue_PlacePNR>')
    
    s.find('<inHouseIdentification1>')
    
    s.ignore() 

    s.posEnd()                                                           

    return s.getResult()     


def PoweredPNR_AddMultiElements_pnrActions_BAGA_LongFreeTextSplitter(matcherValue):

    """

    A splitter that removes the longFreetext>BAGA which has a date in it

    Date   : Aug 2014

    Shivam Gandhi

    """

    s=stringSplitter(matcherValue)

    s.findRE('^<PoweredPNR_AddMultiElements><reservationInfo>')
    
    s.find('<dataElementsMaster>')

    s.find('<freetextData>')
    
    s.find('<longFreetext>BAGA')
    
    s.ignore()
    
    s.posEnd()

    return s.getResult() 
                               
                                                        

def PoweredPNR_AddMultiElements_pnrActions_OptionCodeSplitter(matcherValue):

    """

    A splitter that removes one option code

    Date   : June 2011

    Request:

    <PoweredPNR_AddMultiElements><pnrActions><optionCode>20</optionCode></pnrActions></PoweredPNR_AddMultiElements>

    Matching Request:

    <PoweredPNR_AddMultiElements><pnrActions><optionCode>0</optionCode></pnrActions><dataElementsMaster><marker1/><dataElementsIndiv><elementManagementData> more stuff </PoweredPNR_AddMultiElements>

    """

    s=stringSplitter(matcherValue)

    # All three of the finds will have to work for us to be happy

    # as finds are also assertions - if they don't find anything 

    # whole sequence will fail

    s.findRE('^<PoweredPNR_AddMultiElements><pnrActions>')

    s.find('<optionCode>')

    s.ignore()                # and ignore what follows

    s.find('</optionCode>')   # until here

    s.keep()

    s.posEnd()                                                           

    return s.getResult() 



def PoweredPNR_AddMultiElements_pnrActions_FreetextNewItinSplitter(matcherValue):

    """

    A splitter that removes option code and the freetext>NEW ITIN which has a date in it

    Date   : June 2011

    

    """

    s=stringSplitter(matcherValue)

    # All three of the finds will have to work for us to be happy

    # as finds are also assertions - if they don't find anything 

    # whole sequence will fail

    s.findRE('^<PoweredPNR_AddMultiElements><pnrActions>')

    s.find('<optionCode>')

    s.ignore()                # and ignore what follows

    s.find('</optionCode>')   # until here

    s.keep()

    s.find('<freetext>NEW ITIN')

    s.ignore()                # and ignore what follows

    s.find('</freetext>')   # until here

    s.keep()

    s.posEnd()                                                           

    return s.getResult() 






def findPoweredPNR_CAGT_AND_PAGT_AND_RQST_Splitter(matcherValue):

    """

    A splitter that removes CAGT, PAGT & RQST freetext elements

    Author : John Davenport

    Date   : Aug 2010

    >>> findPoweredPNR_CAGT_AND_PAGT_Splitter('<PoweredPNR_AddMultiElements><pnrActions><optionCode>0</optionCode></pnrActions>blah<miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-CAGT-1-LONBA08X1 AA 10AUG10 1030</freetext></remarks></miscellaneousRemark></dataElementsIndiv><dataElementsIndiv><elementManagementData><segmentName>RX</segmentName></elementManagementData><miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-PAGT-1-LONBA08X1 AA 10AUG10 1030</freetext></remarks></miscellaneousRemark>blah</dataElementsMaster></PoweredPNR_AddMultiElements>')

    ['<PoweredPNR_AddMultiElements><pnrActions><optionCode>0</optionCode></pnrActions>blah<miscellaneousRemark><remarks><type>RX</type><freetext>', '</freetext></remarks></miscellaneousRemark></dataElementsIndiv><dataElementsIndiv><elementManagementData><segmentName>RX</segmentName></elementManagementData><miscellaneousRemark><remarks><type>RX</type><freetext>', '</freetext></remarks></miscellaneousRemark>blah</dataElementsMaster></PoweredPNR_AddMultiElements>']

    """

    

    s=stringSplitter(matcherValue)

    #All three of the finds will have to work for us to be happy

    #as finds are also assertions - if they don't find anything 

    #whole sequence will fail

    s.findRE('^<PoweredPNR_AddMultiElements>')

    s.find('<freetext>')

    s.find('TBM2-CAGT')         # we will keep everything up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep what intervenes

    s.find('TBM2-PAGT')         # up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep everything upto

    s.find('RQST:')             # up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep everything upto 

    s.posEnd()                  # the end of the string

    return s.getResult()    



def findPoweredPNR_PAGT_AND_2RQST_Splitter(matcherValue):

    """

    A splitter that removes two PAGT and RQST freetext elements

    Author : John Davenport

    Date   : Aug 2010

    >>> findPoweredPNR_PAGT_AND_RQST_Splitter('<PoweredPNR_AddMultiElements>rubble<miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-PAGT-1-MEX08X1 AA 31JUL12 0952</freetext></remarks></miscellaneousRemark>rubble<freetext>GFF:RQST:31JUL12:0952:UGFM05:0:36022282:MEXICAN:D:MR:N:N:E:N:12500:N:56308435:EC:Y:N:N)</freetext>rubble')

    ['<PoweredPNR_AddMultiElements>rubble<miscellaneousRemark><remarks><type>RX</type><freetext>', '</freetext></remarks></miscellaneousRemark>rubble<freetext>GFF:', '</freetext>rubble']

    

    """

    

    s=stringSplitter(matcherValue)

    #All three of the finds will have to work for us to be happy

    #as finds are also assertions - if they don't find anything 

    #whole sequence will fail

    s.findRE('^<PoweredPNR_AddMultiElements>')

    s.find('<freetext>')

    s.find('TBM2-PAGT')         # we will keep everything up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep what intervenes

    s.find('<freetext>')

    s.find('RQST:')             # up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep everything upto 

    s.find('RQST:')             # up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep everything upto 

    s.posEnd()                  # the end of the string

    return s.getResult()

    

def findPoweredPNR_PAGT_AND_RQST_Splitter(matcherValue):

    """

    A splitter that removes two PAGT and RQST freetext elements

    Author : John Davenport

    Date   : Aug 2010

    >>> findPoweredPNR_PAGT_AND_RQST_Splitter('<PoweredPNR_AddMultiElements>rubble<miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-PAGT-1-MEX08X1 AA 31JUL12 0952</freetext></remarks></miscellaneousRemark>rubble<freetext>GFF:RQST:31JUL12:0952:UGFM05:0:36022282:MEXICAN:D:MR:N:N:E:N:12500:N:56308435:EC:Y:N:N)</freetext>rubble')

    ['<PoweredPNR_AddMultiElements>rubble<miscellaneousRemark><remarks><type>RX</type><freetext>', '</freetext></remarks></miscellaneousRemark>rubble<freetext>GFF:', '</freetext>rubble']

    

    """

    

    s=stringSplitter(matcherValue)

    #All three of the finds will have to work for us to be happy

    #as finds are also assertions - if they don't find anything 

    #whole sequence will fail

    s.findRE('^<PoweredPNR_AddMultiElements>')

    s.find('<freetext>')

    s.find('TBM2-PAGT')         # we will keep everything up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep what intervenes

    s.find('<freetext>')

    s.find('RQST:')             # up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep everything upto 

    s.posEnd()                  # the end of the string

    return s.getResult()



def findPoweredPNR_CAGT_AND_PAGT_Splitter(matcherValue):

    """

    A splitter that removes CAGT and PAGT freetext elements

    Author : John Davenport

    Date   : Aug 2010

    >>> findPoweredPNR_CAGT_AND_PAGT_Splitter('<PoweredPNR_AddMultiElements><pnrActions><optionCode>0</optionCode></pnrActions>blah<miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-CAGT-1-LONBA08X1 AA 10AUG10 1030</freetext></remarks></miscellaneousRemark></dataElementsIndiv><dataElementsIndiv><elementManagementData><segmentName>RX</segmentName></elementManagementData><miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-PAGT-1-LONBA08X1 AA 10AUG10 1030</freetext></remarks></miscellaneousRemark>blah</dataElementsMaster></PoweredPNR_AddMultiElements>')

    ['<PoweredPNR_AddMultiElements><pnrActions><optionCode>0</optionCode></pnrActions>blah<miscellaneousRemark><remarks><type>RX</type><freetext>', '</freetext></remarks></miscellaneousRemark></dataElementsIndiv><dataElementsIndiv><elementManagementData><segmentName>RX</segmentName></elementManagementData><miscellaneousRemark><remarks><type>RX</type><freetext>', '</freetext></remarks></miscellaneousRemark>blah</dataElementsMaster></PoweredPNR_AddMultiElements>']

    """

    

    s=stringSplitter(matcherValue)

    #All three of the finds will have to work for us to be happy

    #as finds are also assertions - if they don't find anything 

    #whole sequence will fail

    s.findRE('^<PoweredPNR_AddMultiElements>')

    s.find('<freetext>')

    s.find('TBM2-CAGT')         # we will keep everything up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep what intervenes

    s.find('TBM2-PAGT')         # up to here

    s.ignore()                  # and ignore this <freetext>

    s.find('</freetext>')       # 

    s.keep()                    # then keep everything upto 

    s.posEnd()                  # the end of the string

    return s.getResult()

    

def findPoweredPNR_PAGTSplitter(matcherValue):

     """

     A splitter that removes a PAGT freetext elements

     Author : John Davenport

     Date   : Aug 2010

     >>> findPoweredPNR_PAGTSplitter('<PoweredPNR_AddMultiElements><pnrActions><optionCode>0</optionCode></pnrActions>blah<miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-PAGT-1-LONBA08X1 AA 10AUG10 1030</freetext></remarks></miscellaneousRemark></dataElementsIndiv><dataElementsIndiv><elementManagementData><segmentName>RX</segmentName></elementManagementData><miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-PAGT-1-LONBA08X1 AA 10AUG10 1030</freetext></remarks></miscellaneousRemark>blah</dataElementsMaster></PoweredPNR_AddMultiElements>')

     ['<PoweredPNR_AddMultiElements><pnrActions><optionCode>0</optionCode></pnrActions>blah<miscellaneousRemark><remarks><type>RX</type><freetext>', '</freetext></remarks></miscellaneousRemark></dataElementsIndiv><dataElementsIndiv><elementManagementData><segmentName>RX</segmentName></elementManagementData><miscellaneousRemark><remarks><type>RX</type><freetext>TBM2-PAGT-1-LONBA08X1 AA 10AUG10 1030</freetext></remarks></miscellaneousRemark>blah</dataElementsMaster></PoweredPNR_AddMultiElements>']

     

     """

       

     s=stringSplitter(matcherValue)

     #All three of the finds will have to work for us to be happy

     #as finds are also assertions - if they don't find anything 

     #whole sequence will fail

     s.findRE('^<PoweredPNR_AddMultiElements>')

     s.find('<freetext>')

     s.find('TBM2-PAGT')         # keep up to here

     s.ignore()                  # and ignore this <freetext>

     s.find('</freetext>')       # 

     s.keep()                    #

     s.posEnd()                  # the end of the string

     return s.getResult()

     

def findPoweredPNR_CAGTSplitter(matcherValue):

    """

    A splitter that removes CAGT freetext element

    Author : John Davenport

    Date   : June 2011

    

    >>> findPoweredPNR_CAGTSplitter('<PoweredPNR_AddMultiElements>blablabla<freetext>TBM2-CAGT-1-LONBA08X1 AA 25MAY10 1306</freetext>morestuff blablabla<freetext>TBM2-PAGT-1-LONBA08X1 AA 25MAY10 1306</freetext>morestuff</PoweredPNR_AddMultiElements>')

    ['<PoweredPNR_AddMultiElements>blablabla<freetext>', '</freetext>morestuff blablabla<freetext>TBM2-PAGT-1-LONBA08X1 AA 25MAY10 1306</freetext>morestuff</PoweredPNR_AddMultiElements>']



    Also for <PoweredPNR_AddMultiElements>...blah <freetext>TBM2-PCCD-1-VI/************1111 EXPY **/** C/******</freetext>.. blah </PoweredPNR_AddMultiElements>

    

    """

    s=stringSplitter(matcherValue)

    # All three of the finds will have to work for us to be happy

    # as finds are also assertions - if they don't find anything 

    # whole sequence will fail

    s.findRE('^<PoweredPNR_AddMultiElements>')

    s.find('<freetext>')

    s.find('TBM2-CAGT')         # we will keep everything up to here

    s.ignore()                  # and ignore what follows

    s.find('</freetext>')       # until here

    s.keep()                    # then keep everything

    s.posEnd()                  # until the end of the string

    return s.getResult()

    

def splitter_Cryptic_GetScreen_Query_TRFU(matcherValue):

    """

    Author : Chris Ash

    Date   : Sep 2012

    

    Request=<Cryptic_GetScreen_Query><Command>TRFU/FP2LB/1421/36001**REFUND</Command></Cryptic_GetScreen_Query>

    Split=<Cryptic_GetScreen_Query><Command>TRFU/**REFUND</Command></Cryptic_GetScreen_Query>

       

    """

    s=stringSplitter(matcherValue)

    s.find('<Cryptic_GetScreen_Query><Command>TRFU')     # find and assert the XML

    s.find("/")                                         # find to /

    s.ignore()                                          # ignore what follows

    s.find("*")                                         # until after the *

    s.keep()                                            # keep what follows

    s.posEnd()                                          # up to the end

    return s.getResult()                                # capture that, split & return



def splitter_FareFlexPricer_Upsell(matcherValue):

    """

    Split out the Session details from the Soap header as this is a web service call

    """

    s=stringSplitter(matcherValue)

    s.find('<wbs:Session>')

    s.ignore()

    s.find('</wbs:Session>')

    s.keep()

    s.posEnd()

    return s.getResult()

def splitter_PoweredFare_InformativePricingWithoutPNR_BookngClass(matcherValue):

    """

    Split out the booking classes as these can change in the request

    """

    s=stringSplitter(matcherValue)

    s.find('<PoweredFare_InformativePricingWithoutPNR>')

    s.find('<bookingClass>').ignore()

    s.posEnd()

    return s.getResult()

def splitter_PoweredTicket_UpdateTST(matcherValue):

    """

    Split out the segments as the hold dateTime as these need to stay static

    """

    s=stringSplitter(matcherValue)

    s.find('<PoweredTicket_UpdateTST>')

    s.find('<segmentInformation>').ignore()

    s.posEnd()

    return s.getResult()

# 

# Splitters list

# 

# Put the splitter definition names in a list here in format:

#

# splitters = [definition, definition, ...]

#

# if none omit splitters or leave it null, i.e. 

#

# splitters = []

#

splitters = [splitter_Cryptic_GetScreen_Query_TWD

                ,splitter_Cryptic_GetScreen_Query_TRFU

                ,splitter_Cryptic_GetScreen_Query_IMCSS

                ,splitter_Cryptic_GetScreen_Query_FOPAX

                ,splitter_Cryptic_GetScreen_Query_FOINF

                ,splitter_Cryptic_GetScreen_Query_FQP_AfterSlash

                ,splitter_Cryptic_GetScreen_Query_FPP_AfterSlash

                ,splitter_Cryptic_GetScreen_Query_FPP_afterslashN_beforecolon

                ,splitter_Cryptic_GetScreen_Query_FPO_afterslashN_beforecolon

                ,splitter_Cryptic_GetScreen_Query_FPINFO_afterslashN_beforecolon

                ,splitter_Cryptic_GetScreen_Query_FPC_afterslashN_beforecolon

                ,splitter_Cryptic_GetScreen_Query_FPC_afterslashN_beforeslash

                ,splitter_Cryptic_GetScreen_Query_FPP_afterslashN_beforeslash

                ,splitter_Cryptic_GetScreen_Query_TTI_VXX

                ,findPoweredPNR_AddMultiElements_FreetextRemover

                ,findPoweredPNR_CAGT_AND_PAGT_AND_RQST_Splitter

                ,findPoweredPNR_PAGT_AND_2RQST_Splitter

                ,findPoweredPNR_PAGT_AND_RQST_Splitter

                ,findPoweredPNR_CAGT_AND_PAGT_Splitter

                ,findPoweredPNR_PAGTSplitter

                ,findPoweredPNR_CAGTSplitter

                ,PoweredPNR_AddMultiElements_pnrActions_FreetextNewItinSplitter

                ,PoweredPNR_AddMultiElements_pnrActions_OptionCodeSplitter

                ,splitter_Cryptic_GetScreen_Query_FO

                ,splitter_FareFlexPricer_Upsell
				
                ,splitter_PoweredFare_InformativePricingWithoutPNR_BookngClass

                ,splitter_PoweredTicket_UpdateTST
                
                ,splitter_Cryptic_GetScreen_Query_TMI_afterslashN_beforeslash
                
                ,splitter_Cryptic_GetScreen_Query_TMI_PaymentReference
                
                ,findPoweredQueue_PlaceHBFFPNR
                
                ,PoweredPNR_AddMultiElements_pnrActions_BAGA_LongFreeTextSplitter

                ]



# 

# Unit Tests - using doctest

# 

# Leave this part alone!

#

# To test run this file from a command prompt:

# python TestInterface.py

# There will be silence if all the tests work

# Alternatively, to see the tests enter

# python TestInterface.py -v

#

def _test():

    import doctest

    doctest.testmod()

    # doctest.testfile("xyz.txt")



if __name__ == '__main__':

    _test()