from Spectroscopy.models import Spectrum


UPLOAD_PATH='/home/kati/Dropbox/munka/learning/sn_app/test_tools/uploads/tmp.txt'

def uploadSpectrum(f, sn, mjd, notes):
    #f=open(file.file, 'r')
    #f=file
    with open(UPLOAD_PATH, 'wr') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    f=open(UPLOAD_PATH, 'r')


    w=[]
    for line in f:
        l=line.strip().split(' ')
        w.append([float(l[0]), float(l[1])])

    Sp=Spectrum.objects.create(sn=sn, MJD=mjd, notes=notes, spectrum=w)
    f.close()
    return 1
