import sys
import time
from src.args import arguments
from src import compareAlgorithms
from src import extractImage
# from src import terminalActions

# Check input
def checkInput():
    pass

def pullImages(imageStatus, image):
    # Kiểm tra tồn tại image?
    checkExistImage = extractImageAlgs.checkExistImage(image)
    if checkExistImage == 0:
        extractImageAlgs.log(f"\tINFO: {imageStatus} image '{image}' đã tồn tại. Bỏ qua pull image.")
    else:
        extractImageAlgs.log(f"\tINFO: {imageStatus} image '{image}' chưa tồn tại. Thực hiện pull image...")
        exitCodePullImage = extractImageAlgs.pullImage(image)
        if exitCodePullImage != 0:
            sys.exit(100)

def processPullImages(oldImages, newImages):
    print('*** Kiểm tra tồn tại các images...')
    # Kiểm tra old image
    if oldImages == []:
        extractImageAlgs.log('\tINFO: Giá trị old images để trống --> Bỏ qua old images.')
    else:
        extractImageAlgs.log(f"\tINFO: Kiểm tra tồn tại các old image...")
        for oldImage in oldImages:
            pullImages('Old', oldImage)

    # Kiểm tra new image
    extractImageAlgs.log(f"\tINFO: Kiểm tra tồn tại các new image...")
    for newImage in newImages:
        pullImages('New', newImage)

def processCheckAddUser(newImages):
    print('*** Kiểm tra chỉ định USER trong Dockerfile...')
    try:
        for newImage in newImages:
            userValue = extractImageAlgs.processGetUser(newImage)
            if userValue:
                extractImageAlgs.log(f"\tINFO: Image '{newImage}' đã chỉ định USER riêng của dự án - Tên USER: {userValue}")
            else:
                extractImageAlgs.log(f"\tWARNING: Image '{newImage}' chưa chỉ định USER riêng của dự án trên Dockerfile. Cần bổ sung thêm.")
    except Exception as e:
        extractImageAlgs.log(f"\tERROR: {e}")
        sys.exit(100)

def extractFiles2Image(oldImage, newImage):
    global containerID1
    global containerID2
    global storedPaths1
    global storedPaths2
    try:
        if oldImage:
            extractImageAlgs.log(f"\tINFO: Trích xuất old image '{oldImage}'...")
            extractOutput1 = extractImageAlgs.processCopyFromContainerToHost(oldImage)
            storedPaths1.append(extractOutput1[0])
            containerID1.append(extractOutput1[1])
            extractImageAlgs.log(f"\tINFO: Trích xuất old image '{oldImage}' hoàn tất.")
        extractImageAlgs.log(f"\tINFO: Trích xuất new image '{newImage}'...")
        extractOutput2 = extractImageAlgs.processCopyFromContainerToHost(newImage)
        storedPaths2.append(extractOutput2[0])
        containerID2.append(extractOutput2[1])
        extractImageAlgs.log(f"\tINFO: Trích xuất new image '{newImage}' hoàn tất.")

    except Exception as e:
        extractImageAlgs.log(f"\tERROR: Trích xuất file thất bại. ❌")
        print(f"==> Error detail: {e}")
        sys.exit(100)

def processExtractFiles2Image(oldImages, newImages):
    print('*** Trích xuất image...')
    for i in range(len(newImages)):
        if oldImages == []: 
            oldImage = None
        else:
            oldImage = oldImages[i]
        newImage = newImages[i]

        extractFiles2Image(oldImage, newImage)

def getFiles2Folder(storedPath1, storedPath2):
    listFiles = []
    try:
        # Duyệt files thư mục 1
        if not storedPath1:
            filesInDir1 = [['', '', '', 0, '', '']]
            listFiles.append(filesInDir1)
        else:
            extractImageAlgs.log(f"\tINFO: Duyệt files trên thư mục {storedPath1}...")
            filesInDir1 = algorithms.getFiles(storedPath1)
            listFiles.append(filesInDir1)
            extractImageAlgs.log(f"\tINFO: Duyệt thư mục {storedPath1} hoàn tất.")

        # Duyệt files thư mục 2
        extractImageAlgs.log(f"\tINFO: Duyệt files trên thư mục {storedPath2}...")
        filesInDir2 = algorithms.getFiles(storedPath2)
        extractImageAlgs.log(f"\tINFO: Duyệt thư mục {storedPath2} hoàn tất.")
        listFiles.append(filesInDir2)

        return listFiles
    
    except Exception as e:
        extractImageAlgs.log(f"\tERROR: Duyệt file thất bại. ❌")
        print(f"==> Error detail: {e}")
        sys.exit(100)

def processGetFiles2Folder():
    global storedPaths1
    global storedPaths2
    global listFilesArray

    print('*** Duyệt files...')
    for i in range(len(storedPaths2)):
        if storedPaths1 == []:
            storedPath1 = None
        else:
            storedPath1 = storedPaths1[i]
        storedPath2 = storedPaths2[i]
        # Thực hiện duyệt file
        listFiles = getFiles2Folder(storedPath1, storedPath2) 
        listFilesArray.append(listFiles)

def compare(listFiles):
    result = []
    try:
        compareResult = algorithms.compareList(listFiles[0], listFiles[1])
        result.append(listFiles[0])
        result.append(listFiles[1])
        result.append(compareResult)
        return result
    except Exception as e:
        extractImageAlgs.log(f"\tERROR: So sánh file thất bại. ❌")
        print(f"==> Error detail: {e}")
        sys.exit(100)

def processCompare():
    print('*** So sánh files...')
    global results
    global listFilesArray
    for item in listFilesArray:
        result = compare(item)
        results.append(result)
    extractImageAlgs.log(f"\tINFO: So sánh file hoàn tất.")

def processOutput(oldImages, newImages):
    global results
    global fileOutput
    print('*** Xuất file kết quả...')
    try:
        fileOutput = algorithms.writeToExcelFile(results, oldImages, newImages, argValues[2], argValues[3])
        extractImageAlgs.log(f"\tINFO: Xuất file kết quả hoàn tất")
        extractImageAlgs.log(f"\tINFO: Đường dẫn file kết quả: {fileOutput}")
        extractImageAlgs.log(f"\tINFO: Kết nối tới SMB...")
        algorithms.connectSMB(argValues[4])
        time.sleep(0.8)
        extractImageAlgs.log(f"\tINFO: Kết nối SMB thành công")
        extractImageAlgs.log(f"\tINFO: Đẩy file kết quả vào SMB storage...")
        algorithms.saveExcelToSMB(fileOutput, r'\\storage1\DU_LIEU_CHUYEN_RA_NGOAI\Compare_file', argValues[2])
        extractImageAlgs.log(f"\tINFO: Đẩy file kết quả vào SMB storage thành công")
    except Exception as e:
        extractImageAlgs.log(f"\tERROR: Có lỗi trong quá trình lưu file kết quả. ❌")
        print(f"==> Error detail: {e}")
        sys.exit(100)

def processClean(oldImages, newImages):
    global storedPaths1
    global storedPaths2
    global containerID1
    global containerID2
    global fileOutput
    print('*** Dọn dẹp sau kiểm tra...')
    try:
        cleanReturnCodes = extractImageAlgs.clean(containerID1, containerID2, oldImages, newImages, storedPaths1, storedPaths2, fileOutput)
        for cleanReturnCode in cleanReturnCodes:
            if cleanReturnCode != None: 
                if all(element == 0 for element in cleanReturnCode):
                    pass
                else: 
                    sys.exit(100)
            else: 
                sys.exit(100)
        extractImageAlgs.log(f"\tINFO: Dọn dẹp hoàn tất")
    except Exception as e:
        # extractImageAlgs.log(f"\tERROR: {e}")
        sys.exit(100)

if __name__ == "__main__":
    argValues = arguments.argsFunc()
    algorithms = compareAlgorithms
    extractImageAlgs = extractImage

    storedPaths1 = []
    storedPaths2 = []
    containerID1 = []
    containerID2 = []
    listFilesArray = []
    results = []
    fileOutput = ""

    if argValues[0]:
        oldImages = argValues[0].split(',')
    else: oldImages = []
    newImages = argValues[1].split(',')

    print('''
      __           __    ____ __      
 ____/ /  ___ ____/ /__ / _(_) /__ ___
/ __/ _ \/ -_) __/  '_// _/ / / -_|_-<
\__/_//_/\__/\__/_/\_\/_//_/_/\__/___/
                            
                        °˚°°˚°''')
    print(f"""INPUT:
[+] OLD IMAGE:          {argValues[0]}
[+] NEW IMAGE:          {argValues[1]}
[+] PRODUCT NAME:       {argValues[2]}
[+] VERSION:            {argValues[3]}
[+] SMB CONFIG FILE:    {argValues[4]}
""")
    print("BẮT ĐẦU THỰC HIỆN CHECKFILES")
    start = time.time()
    processPullImages(oldImages, newImages)
    processCheckAddUser(newImages)
    processExtractFiles2Image(oldImages, newImages)
    processGetFiles2Folder()
    processCompare()
    processOutput(oldImages, newImages)
    processClean(oldImages, newImages)
    end = time.time()
    print('\nCHECKFILES THÀNH CÔNG !!! ✅')
    print("*** Tổng thời gian chạy: " + str(end - start))
