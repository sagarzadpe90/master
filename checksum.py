
import os
from glob import glob
from datetime import datetime
import socket
import hashlib
import base64
import shutil
import sys
# To find files in directory
def file_finder(rootDirectoryToProcess):
    resList = [y for x in os.walk(rootDirectoryToProcess) for y in glob(os.path.join(x[0], '*.*'))]
    #print(resList)
    return resList

def  get_file_dt(f):
    fTime=os.path.getctime(f)
    return datetime.fromtimestamp(fTime).strftime('%Y-%m-%dT%H:%M-%S:%f')

#to compare two dates
def compare_dt(modifiedAfterDateTime,calc_dt):
    modifiedAfterDateTime=datetime.strptime(modifiedAfterDateTime,'%Y-%m-%dT%H:%M-%S:%f')
    calc_dt=datetime.strptime(calc_dt,'%Y-%m-%dT%H:%M-%S:%f')
    if calc_dt > modifiedAfterDateTime:
        return 1
    else:
        return 0

def calc_hash_base64(file):
    with open(os.path.join(file),"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes);
        #print( "{} - {}".format(file,readable_hash))
        fileHash= readable_hash.hexdigest()
        fileBase64Hash=str(base64.b64encode(readable_hash.digest()))
    return fileHash ,fileBase64Hash

def copyFileDir(fileName,source,dest):
    if not os.path.exists(dest):
        os.makedirs(dest) 
    shutil.copy2(source,os.path.join(dest,fileName) )
    return 0

def run_process(rootDirectoryToProcess,modifiedAfterDateTime,bucketName,targetRelativeKeyPath,bucketRootDirectory):
    currentMin=int(datetime.now().strftime("%M"))
    fileName="D--files-examples_"+ datetime.now().astimezone().strftime("%Z_%Y.%m.%d__H%H--")+ str(currentMin).zfill(2)+".out"
    print(fileName)
    #out=open(fileName,"a")
    resList=file_finder(rootDirectoryToProcess)
    hostname=socket.gethostname()
    with open(os.path.join(targetRelativeKeyPath,fileName),"a") as my_file:
        for fullFilePath in resList:
            fileLastModifiedDateTime=get_file_dt(fullFilePath)
            res=compare_dt(modifiedAfterDateTime,fileLastModifiedDateTime)
            if res==1:
                stTime= datetime.now()
                readable_hash ,fileBase64Sha256Hash=calc_hash_base64(fullFilePath)
                endTime=datetime.now()
                msToHash=endTime-stTime
                msToHash=msToHash.total_seconds() * 1000
                stTime1= datetime.now()        
                #copy_file_aws(fullFilePath,bucketName,bucketRootDirectory)
                copyFileDir(os.path.basename(fullFilePath),fullFilePath,targetRelativeKeyPath)
                endTime1=datetime.now()
                msToCopy=endTime1-stTime1  
                msToCopy=msToCopy.total_seconds() * 1000
                fileProcessedDateTime= datetime.now()
                mssg_string= "{} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {}".format(
                hostname,
                rootDirectoryToProcess,
                modifiedAfterDateTime,
                fileLastModifiedDateTime,
                fullFilePath,
                bucketName,
                targetRelativeKeyPath,
                fileBase64Sha256Hash,
                fileProcessedDateTime,
                msToHash,
                msToCopy)
                #print("{}- \n hash:{}, \n base:{}".format(file,readable_hash ,fileBase64Hash))
                my_file.write(mssg_string + "\n")
                print(mssg_string)
    return 0

if __name__ == "__main__":
    #inputs
    if len(sys.argv) == 6:
        rootDirectoryToProcess=sys.argv[1]
        modifiedAfterDateTime=sys.argv[2]
        bucketName=sys.argv[3]
        targetRelativeKeyPath=sys.argv[4]
        bucketRootDirectory=sys.argv[5]    
        print("rootDirectoryToProcess: {}".format(rootDirectoryToProcess))
        print("modifiedAfterDateTime: {}".format(modifiedAfterDateTime))
        print("bucketName: {}".format(bucketName))
        print("targetRelativeKeyPath: {}".format(targetRelativeKeyPath))
        print("bucketRootDirectory: {}".format(bucketRootDirectory))    
        basePath=os.getcwd()
        #call funtion
        run_process(rootDirectoryToProcess,modifiedAfterDateTime,bucketName,targetRelativeKeyPath,bucketRootDirectory)
    else:
        print("Please provide correct inputs \n Example: \n python checksum.py rootDirectoryToProcess modifiedAfterDateTime bucketName targetRelativeKeyPath bucketRootDirectory")
        print("Inputs->")
        print("rootDirectoryToProcess: root directory Files to search")
        print("modifiedAfterDateTime: Provide date format ('%Y-%m-%dT%H:%M-%S:%f') eg- 2012-01-31T08:59-7:00")
        print("bucketName: Provide correct S3 bucket")
        print("targetRelativeKeyPath: Provide target path ")
        print("bucketRootDirectory: provide root directory name")  
                
        


