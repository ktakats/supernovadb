from Photometry.models import Photometry

FILTERS=['B', 'V', 'R', 'I']
UPLOAD_PATH='/home/kati/Dropbox/munka/learning/sn_app/test_tools/uploads/tmp.txt'

def uploadPhotometry(f, sn):
    #f=open(file.file, 'r')
    #f=file
    with open(UPLOAD_PATH, 'wr') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    f=open(UPLOAD_PATH, 'r')
    header=f.readline().split(' ')
    if not header[0]=='MJD':
        return -1
    filters=[]
    notes=-1
    for i in range(1, len(header)+1, 2):
        if header[i] in FILTERS:
            filters.append(header[i])
        else:
            noteindex=i
            break

    for line in f:
        line=line.split(' ')
        for i,filt in enumerate(filters):
            if line[i*2+1]=="NA" or line[i*2+1]=='999':
                continue
            if len(line)<=noteindex:
                note=''
            else:
                note=line[noteindex]
            Photometry.objects.create(MJD=float(line[0]), Filter=filt, magnitude=float(line[i*2+1]), mag_error=float(line[i*2+2]), notes=note, sn=sn)

    f.close()
    return 1
