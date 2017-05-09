from Spectroscopy.models import Spectrum
from decouple import config
import tempfile



def uploadSpectrum(myfile, sn, mjd, notes):
    #f=open(file.file, 'r')
    #f=file
    with tempfile.TemporaryFile() as tmp:
        for chunk in myfile.chunks():
            tmp.write(chunk)
        tmp.seek(0)


        w=[]
        for line in tmp:
            l=line.strip().split(' ')
            w.append([float(l[0]), float(l[1])])

        Sp=Spectrum.objects.create(sn=sn, MJD=mjd, notes=notes, spectrum=w)
    return 1
