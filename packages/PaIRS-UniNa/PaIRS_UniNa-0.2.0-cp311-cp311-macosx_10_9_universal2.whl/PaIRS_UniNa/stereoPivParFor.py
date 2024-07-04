from typing import Tuple#,Callable
from .PaIRS_pypacks import *
from .procTools import *
from .pivParFor import WrapperOutFromPIV
from .readcfg import readCalFile
#if Flag_DEBUG_PARPOOL:   import debugpy



def initStereoPIV(eventFerma,iImg,procId,data:dataTreePar,*args,**kwargs):  
  ''' this  function is called once per processor before the main function 
  eventferma is passed to the function called by PIV in order to stop the processing ''' 
  #prTimeLock(0,f"  initPIV")
  
  StereoPIV=data2StereoPIV(data)
  try:
    StereoPIV.evalCommonZone() #todo maybe this should be done also before for plotting the common zone
  except ValueError as exc:
    pri.Error.white(f"{exc=}, {type(exc)=}")
  

  StereoPIV.Inp.FlagLog=0
  #vect=[]
  #for v in data.PRO.Vect:      vect.append(v.astype(np.intc))
      
  #StereoPIV.SetVect([v.astype(np.intc) for v in data.PRO.Vect])
  data.compMin.Imin=[np.zeros(1),np.zeros(1)]
  if data.FlagMIN:
    filename=data.filename_proc[StepTypes.min]
    if filename:
      try:
          with open(filename, 'rb') as file:
              data_min:dataTreePar = pickle.load(file)
          data.copyfromfields(data_min,['compMin'])
      except Exception as inst:  
          raise (inst)
          #data.FlagMIN=False        
        

  #fatto in modo esplicito da vedere
  #StereoPIV.Inp.FlagNumThreads=1# of threads used in the processing use 0 for the number of logical processors 
  StereoPIV.Media=MediaPIV(stepType=StepTypes.spiv)#data.mediaPIV
  StereoPIV.WraOut =WrapperOutFromPIV(0,eventExit=eventFerma)
  StereoPIV.fun=PaIRS_lib.GetPyFunction(StereoPIV.WraOut) 
  StereoPIV.initAlloc(StereoPIV.fun)
  (flagOut,VarOut)  =procStereoPIV(iImg,procId ,StereoPIV,data,*args,**kwargs)
  return (flagOut,VarOut,StereoPIV)
def exitNoLog(flagOut,varOut):
  ''' exit without printing the log '''
  varOut[0]=-1
  return (flagOut,varOut)
def procStereoPIV(i,procId ,StereoPIV,data:dataTreePar,numUsedThreadsPIV,*args,**kwargs):
  ''' main proc function called for all the images one time per processor 
    k=0 always
    In output flagOut and varOut[0] can be:
      Already processed:      varOut[0]=-1 flagOut=FLAG_PROC[k]|FLAG_READ[k]|FLAG_FINALIZED[k]
      Error reading:          varOut[0]=i  flagOut=FLAG_READ_ERR[k]
      Error processing:       varOut[0]=i  flagOut=FLAG_READ[k]
      Process stoped by user: varOut[0]=-1 flagOut=FLAG_READ[k]
      Error saving:           varOut[0]=i  flagOut=FLAG_PROC[k]|FLAG_READ[k]
      Read and processed:     varOut[0]=i  flagOut=FLAG_PROC[k]|FLAG_READ[k]|FLAG_FINALIZED[k]|FLAG_CALLBACK_INTERNAL
    Use:
    numCallBackTotOk+=sum(1 if x&FLAG_CALLBACK_INTERNAL else 0 for x in flagOut) 
        to evaluate the number of total internal callbacks
    numProcOrErrTot=sum(1 if f else 0 for f  in flagOut)   
        to evaluate the number of total images processed (after a possible pause)
    numFinalized=sum(1 if f&FLAG_FINALIZED[0]  else 0 for f  in flagOut)   
        to evaluate the number of total images correctly  processed   

    where FLAG_FINALIZED_OR_ERR = [ p|e for (p,e) in zip(FLAG_FINALIZED,FLAG_READ_ERR)]
    numProcOrErrTot=sum(1 if (f&FLAG_FINALIZED_OR_ERR[0])or(not f&FLAG_PROC[0])  else 0 for f  in flagOut)    
    to delete images 
    pa='C:\desk\dl\apairs\jetcross\'
    no='zR2jet0_0004a'
    I =imread([pa no '.png']);
    I=I*0+1;
    imwrite(I,[pa no 'black.png']);
  '''
  
  flagOut=0#data.list_pim[i] #0 to be processed, -1 error, 1 correctly processed
  
  varOut=[i,'',[]] # The log will be written unless exitNoLog. If FLAG_CALLBACK_INTERNAL will be set then also the internal part will be called. 
  
  #if PIV.WraOut.flagFerma!=0: return (flagOut,VarOut)
  j=i*2
  kConst=0#useless. In preProc the flags are different for the first and second image in this case we only use the first (i.e. k=0)
  try:
    varOut[1]+=f'{data.list_Image_Files[j]}-{data.list_Image_Files[j+1]}'
    if data.list_eim[j] and data.list_eim[j+1]:  
      if  data.list_pim[i]&FLAG_FINALIZED[kConst]:
        flagOut=FLAG_READ[kConst]|FLAG_PROC[kConst]|FLAG_FINALIZED[kConst]  # It has been already processed. Exit without calling the callback  core part
        #☻prTimeLock(0,f"{i} --> {data.list_Image_Files[j]}   {data.list_Image_Files[j+1]}  {hex(flagOut)}")
        return exitNoLog(flagOut,varOut)
      else:
        if StereoPIV.WraOut.eventExit.is_set():    return exitNoLog(flagOut,varOut)# non si può mettere prima
        # reading images and transforming 
        #prTimeLock(0,f"{i} --> {data.list_Image_Files[j]}   {data.list_Image_Files[j+1]}")
        imgs = [[None] * 2 for i in range(2)]
        # tbd
        #if i==2:1/0
        try:
          for c in range(2):
            for k in range(2):
              if StereoPIV.WraOut.eventExit.is_set(): return exitNoLog(flagOut,varOut)
              if c==0:
                nameImg=data.inpPath+data.list_Image_Files[j+k]
              else:
                nameImg=data.inpPath+data.list_Image_Files[j+k].replace('_cam0','_cam1')
              imgs[c][k]=np.ascontiguousarray(Image.open(nameImg),dtype= np.uint16)
              """
                if data.FlagMIN                
                  if data.FlagTR and i%2:
                    I1[k]=I1[k]-data.compMin.Imin[[1,0][k]]
                  else:
                    I1[k]=I1[k]-data.compMin.Imin[k]
                    #todo mettere la seconda img
              #todo al contrario della PIV le img sono uint16 capire se sia il caso di cambiare anche li
                """
            #iProc=transfIm(data.OUT,flagTransf=0,Images=I1)
        except Exception as inst:
          flagOut|=FLAG_READ_ERR[kConst]
          if data.list_pim[i]&FLAG_READ_ERR[kConst]:varOut[0]=-1# no log already written
          varOut[1]+=f"\n!!!!!!!!!! Error while reading the image {data.list_Image_Files[j+k]}:\n{inst}\n" 
          prLock(f'{varOut[1]}')
          return (flagOut,varOut) #we can exit directly! Not calling the internal part of the callback in case of error
        
        # no exception reading images and transforming running the process 
        flagOut|=FLAG_READ[kConst]
        #infoPrint.white(os.getpid())
        try:
          if StereoPIV.WraOut.eventExit.is_set(): return (flagOut,varOut)
          err=StereoPIV.run(imgs)
        except Exception as inst:
          #raise (inst)
          if ( data.list_pim[i] &FLAG_READ[kConst]):varOut[0]=-1# no log already written
          #dum=str(inst.__cause__).split('\n')[3] #solved
          dum='\n'.join(str(inst.args[0]).split('\n')[3:])
          #varOut[1]+=f"\n!!!!!!!!!! Error while processing the above image pair: {dum}"  
          varOut[1]+=f"\n!!!!!!!!!! Error while processing data:\n{dum}\n"  
          #prLock(f'{varOut[1]}')
          return (flagOut,varOut) #we can exit directly! Not calling the internal part of the callback in case of error
        try:# no exception running the process 
          if err==-1000: #interrotto 
              return exitNoLog(flagOut,varOut) #we can exit directly no log ! 
          else:
            # Finalizing the process (means  transformations and saving data)
            flagOut|=FLAG_PROC[kConst]# per completezza aggiungo anche processato
            #x,y,u,v=transfVect(data.OUT,StereoPIV) # No transformation for Spiv          #[StereoPIV.x,StereoPIV.y,StereoPIV.z,StereoPIV.u,StereoPIV.v,StereoPIV.w]
            nameFields=StereoPIV.Media.namesPIV.instVelFields
            #otherVars=[getattr(StereoPIV,f) for f in nameFields[4:] ]
            #campoVel=[x,y,u,v] +transfIm(data.OUT,flagTransf=1,Images=otherVars,flagRot=1)
            campoVel=[getattr(StereoPIV,f) for f in nameFields ]
            nameVar=StereoPIV.Media.namesPIV.instVel
            StereoPIV.Media.sum(campoVel)  
            try:
              saveResults(data,i+1,campoVel,nameVar)
            except Exception as inst:   
              varOut[1]+=f"\n!!!!!!!!!! Error while saving the results:\n{str(inst)}\n"   
              #prLock(f'{varOut[1]}')
              varOut[0]=i# In any case the log will be written. If FLAG_CALLBACK_INTERNAL will be set then also the internal part will be called. 
              return (flagOut,varOut) #we can exit directly! Not calling the internal part of the callback in case of error
            varOut[1]+="\n"+printPIVLog(StereoPIV.PD0)+printPIVLog(StereoPIV.PD1)
            flagOut|=FLAG_FINALIZED[kConst]
            varOut[0]=i# In any case the log will be written. If FLAG_CALLBACK_INTERNAL will be set then also the internal part will be called. 
            flagOut|=FLAG_CALLBACK_INTERNAL# Verrà chiamata la callback
        except Exception as inst:
          varOut[1]+=f"\n!!!!!!!!!! Error while finalizing the PIV process:\n{str(inst)}\n"  
          #prLock(f'{varOut[1]}')
          return (flagOut,varOut)
    else:#if data.list_eim[j] and data.list_eim[j+1]:  
      flagOut|=FLAG_READ_ERR[kConst]
      if  data.list_pim[i]&FLAG_READ_ERR[kConst]:varOut[0]=-1# no log already written
      jj=j+1 if data.list_eim[j] else j
      varOut[1]+=f"\n!!!!!!!!!! Error while reading the image {data.list_Image_Files[jj]}:\nThe image file is missing!\n"
      #prLock(f'{varOut[1]}')
  except :
    flagOut|=FLAG_GENERIC_ERROR
    varOut[0]=i# In any case the log will be written. If FLAG_CALLBACK_INTERNAL will be set then also the internal part will be called. 
    varOut[1]+=printException(flagMessage=True)
  
  # to del  ma il resto dove va
  #varOut=[i,stampa,[]] if flagOut&FLAG_FINALIZING_PROC_OK[0] else [-1,stampa,[]]
  if (not procId%numUsedThreadsPIV) and flagOut&FLAG_FINALIZED[0]: # copiare l'img nella coda è un operazione onerosa. TA ha deciso che si copia solo quando serve
    #prLock(f'procMIN Main proc i={i}')
    varOut[2]=campoVel#VarOut=[i,stampa,Var]
  

  
  return (flagOut,varOut)

def finalStereoPIV(procId, PIV,data,*args,finalPIVPIppo=4 ,**kwargs):
  #prLock(f'finalPIV  procId={procId}')
  return PIV.Media

def saveAndMean(procId,flagHasWorked,med,data,*args,**kwargs):
  ''' saveAndMean is the wrapUp function called once per processor  '''
  if flagHasWorked:
    data.mediaPIV.sumMedia(med)
  return data.mediaPIV

def callBackStereoPIV(flag,perc,procId,flagOut,name,VarOut,signal_res):
  ''' 
    flag=true new data False just check exit
    perc= precentage done
    flagOutFromTasks,varOutFromTask Out varibles from task  e.g.:
      flagOut=1 #0 to be processed, -1 error, 1 correctly processed
      varOutFromTask whatever for now a string
      name current element in names
    to stop the process the return value should be True otherwise sleep  
  '''
  global FlagStopWorkers
  
  if flag:
    i=VarOut[0]
    stampa=VarOut[1]
    Var=VarOut[2]
    #pr(f'Callback {i}         getpid {os.getpid()}      {len(Var)}')
    #prLock(f'Callback {i}         getpid {os.getpid()}   ')
    signal_res.emit(procId,i,flagOut,Var,stampa)
    VarOut[2]=[]#altrimenti salvo le img 
    '''
    if i==0:
      callBackPIV.flagStop=True
    if(callBackPIV.flagStop):
      if i>=2:
        callBackPIV.flagStop=False
        FlagStopWorkers[0]=True
        return True
    #''' 
  if FlagStopWorkers[0]:
    return True
  else:
    return False     
