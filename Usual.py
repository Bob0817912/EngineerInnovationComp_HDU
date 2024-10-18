RGBDIR={'R':1,'G':2,'B':3}
RGBT=('R','G','B')
TypetoRGB={
    '5':"RGB",
    '6':"RBG",
    '3':"GBR",
    '4':"GRB",
    '1':"BGR",
    '2':"BRG"
}
RGBtoType={"RGB":'5',
           "NGB":'5',
           "RNB":'5',
           "RGN":'5',

           "RBG":'6',
           "NBG":'6',
           "RNG":'6',
           "RBN":'6',

           "GBR":'3',
           "NBR":'3',
           "GNR":'3',
           "GBN":'3',

           "GRB":'4',
           "NRB":'4',
           "GNB":'4',
           "GRN":'4',

           "BGR":'1',
           "NGR":'1',
           "BNR":'1',
           "BGN":'1',

           "BRG":'2',
           "NRG":'2',
           "BNG":'2',
           "BRN":'2'
           }

dir02={
        "123":'a',
        "132":'b',
        "213":'c',
        "231":'d',
        "312":'e',
        "321":'f'

        }
def IntToType(tNum=(0,0,0)):
       s=str(tNum[0])+str(tNum[1])+str(tNum[2])
       return dir02[s]

def Type04(tNum):
    s=RGBT[tNum[0]-1]+RGBT[tNum[1]-1]+RGBT[tNum[2]-1]
    return RGBtoType[s]
def Type_Task05(taskid:str,three_color:str):
    res_str=""
    for ic in taskid:
       res_str+=str(three_color.find(RGBT[ic-1])+1)
    return dir02[res_str]
    
    
def GetReturnType(s):
    res='g'
    try:
        res=RGBtoType[s]
    except:
         res='g'
    return res


