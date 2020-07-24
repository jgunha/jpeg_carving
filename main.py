import os
import binascii
import sys

def carving(filename):
    global jpg_count
    jpg_count = 0

    #디렉토리에서 파일 리스트 가져오기
    for path, dirs, files in os.walk(filename):
        for file in files:
            statinfo = os.stat(os.path.join(path,file))
            f_size = statinfo.st_size
            f = open(os.path.join(path, file), 'rb')
            file_read(f,file,f_size)
            f.close()

    print(str(jpg_count) + ' jpg file carving complete')

#파일 데이터 읽어오기
def file_read(f,file,f_size):
    global jpg_count

    sec = f.read(f_size)
    hex_b = binascii.hexlify(sec)
    #jpeg 파일 시그니처 검사
    if hex_b[:8] == b'ffd8ffe0':
        jpg_count += 1
        num = 2
        check = 0
        #파일 이름 중복 제거
        if os.path.isfile("Recovery/" + file.split('.')[0] + ".jpg") == True:
            while check == 0:
                if os.path.isfile("Recovery/" + file.split('.')[0] +'('+str(num)+')'  + ".jpg") == False:
                    output_file = open("Recovery/" + file.split('.')[0] +'('+str(num)+')' +".jpg", "wb")
                    check = 1
                else:
                    num+=1
        else:
            output_file = open("Recovery/" + file.split('.')[0] + ".jpg", "wb")
        output_file.write(sec)
        output_file.close()

def main():
    if len(sys.argv) != 2:
        print('USAGE : python main.py <directory>')
        sys.exit(2)

    if os.path.isdir('Recovery'):
        pass
    else:
        os.mkdir('Recovery')

    filename = sys.argv[1]

    carving(filename)


main()