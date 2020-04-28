from PIL import Image
import random
import pickle

def compress(file):
    im = Image.open(file)
    img = im.resize((315, 315))
    pixelMap = img.load()
    pv = []
    table=[]

    for i in range(img.size[1]):
        t = []
        for j in range(img.size[0]):
            t.append(pixelMap[j, i][0])
        pv.append(t)

    i, j = 0, 0
    blocks = []
    while i < 315:                                                                       #105x105 blocks
        if j >= 315:
            i = i + 3
            j = 0
        else:
            blocks.append([pv[i][j], pv[i][j + 1], pv[i][j + 2], pv[i + 1][j], pv[i + 1][j + 1], pv[i + 1][j + 2], pv[i + 2][j],pv[i + 2][j + 1], pv[i + 2][j + 2]])
            j = j + 3

    for i in blocks:
        table.append([round(sum(i)/9),max(i)-min(i),0])

    for i in range(len(blocks)):
        str = ''
        for j in range(9):
            if (blocks[i][j] <= table[i][0] and j != 4):
                str = str + '0'
            elif (blocks[i][j] > table[i][0] and j != 4):
                str = str + '1'
        table[i][2]=int(str,2)

    with open(file.replace('.jpg','')+".txt",'wb') as f:
        pickle.dump(table,f)

    t = 0
    im = Image.new('RGB', (105, 105))
    pixelsNew = im.load()
    for i in range(im.size[1]):
        for j in range(im.size[0]):
            pixelsNew[j, i] = tuple(table[t])
            t = t + 1
    cfile = file.replace(".jpg", " ") + "(compressed).jpg"
    im.save(cfile)
    im.show(cfile)
    return(cfile)

def decompress(file):
    with open(file.replace(' (compressed).jpg','')+".txt",'rb') as f:
        table = pickle.load(f)
    im = Image.new('RGB',(315,315))
    pixelsNew = im.load()
    t=0
    i,j=0,0
    while i < 315:
        if j >= 315:
            i=i+3
            j = 0
        else:
            n=bin(table[t][2]).replace("0b","")
            n=n if len(n)==8 else n.zfill(8)
            a=table[t][0]-random.randint(0,table[t][1]) if n[0]=='0' else table[t][0]+random.randint(0,table[t][1])
            pixelsNew[j, i]=(a,a,a)
            a=table[t][0]-random.randint(0,table[t][1]) if n[1]=='0' else table[t][0]+random.randint(0,table[t][1])
            pixelsNew[j + 1, i]=(a,a,a)
            a=table[t][0]-random.randint(0,table[t][1]) if n[2]=='0' else table[t][0]+random.randint(0,table[t][1])
            pixelsNew[j + 2, i]=(a,a,a)
            a=table[t][0]-random.randint(0,table[t][1]) if n[3]=='0' else table[t][0]+random.randint(0,table[t][1])
            pixelsNew[j, i + 1]=(a,a,a)
            pixelsNew[j+1,i+1]=(table[t][0],table[t][0],table[t][0])
            a=table[t][0]-random.randint(0,table[t][1]) if n[4]=='0' else table[t][0]+random.randint(0,table[t][1])
            pixelsNew[j + 2, i + 1]=(a,a,a)
            a=table[t][0]-random.randint(0,table[t][1]) if n[5]=='0' else table[t][0]+random.randint(0,table[t][1])
            pixelsNew[j, i + 2]=(a,a,a)
            a=table[t][0]-random.randint(0,table[t][1]) if n[6]=='0' else table[t][0]+random.randint(0,table[t][1])
            pixelsNew[j + 1, i + 2]=(a,a,a)
            a=table[t][0]-random.randint(0,table[t][1]) if n[7]=='0' else table[t][0]+random.randint(0,table[t][1])
            pixelsNew[j + 2, i + 2]=(a,a,a)
            j=j+3
            t=t+1
    dfile = file.replace(" (compressed).jpg", " ") + "(decompressed).jpg"
    im.save(dfile)
    im.show(dfile)
    return(dfile)

if __name__ == '__main__':
    choice=input("1.Compress\n2.Decompress\n0.Exit\n")
    while(choice!='0'):
        if choice=='1':
            #file=input("\nEnter image name\n")
            cfile=compress('Dog.jpg')
            print("\nCompressed image as {}\n".format(cfile))
            choice = input("1.Compress\n2.Decompress\n0.Exit\n")
        if choice=='2':
            #file=input("\nEnter image name\n")
            dfile=decompress('Dog (compressed).jpg')
            print("\nDecompressed image as {}\n".format(dfile))
            choice = input("1.Compress\n2.Decompress\n0.Exit\n")



