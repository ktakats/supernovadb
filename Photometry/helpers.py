from Photometry.models import Photometry, FILTERCHOICES
from decouple import config

FILTERS=[c[0] for c in FILTERCHOICES]

import tempfile

def uploadPhotometry(myfile, sn):
    #f=open(file.file, 'r')
    #f=file
    with tempfile.TemporaryFile() as tmp:
        for chunk in myfile.chunks():
            tmp.write(chunk)
#    with open(UPLOAD_PATH, 'wr') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)
#    f=open(UPLOAD_PATH, 'r')
        tmp.seek(0)
        header=tmp.readline().split(' ')
        if not header[0]=='MJD':
            tmp.close()
            return -1
        filters=[]
        notes=-1
        for i in range(1, len(header)+1, 2):
            if header[i] in FILTERS:
                filters.append(header[i])
            else:
                noteindex=i
                break

        if noteindex!=len(header)-1:
            f.close()
            return -1

        for line in tmp:
            line=line.split(' ')
            for i,filt in enumerate(filters):
                if line[i*2+1]=="NA" or line[i*2+1]=='999':
                    continue
                if len(line)<=noteindex:
                    note=''
                else:
                    note=' '.join(line[noteindex:])
                Photometry.objects.create(MJD=float(line[0]), Filter=filt, magnitude=float(line[i*2+1]), mag_error=float(line[i*2+2]), notes=note, sn=sn)


    return 1
