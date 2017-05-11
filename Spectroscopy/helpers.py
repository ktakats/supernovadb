from Spectroscopy.models import Spectrum
from decouple import config
import tempfile
import math



def uploadSpectrum(myfile, sn, mjd, notes):
    #f=open(file.file, 'r')
    #f=file
    with tempfile.TemporaryFile() as tmp:
        for chunk in myfile.chunks():
            tmp.write(chunk)
        tmp.seek(0)


        w=[]
        s=[]
        for line in tmp:
            l=line.strip().split(' ')
            w.append(int(float(l[0])*1000))
            if not math.isnan(float(l[1])):
                s.append(int(float(l[1])*1000))
            else:
                s.append(99999)

        Sp=Spectrum.objects.create(sn=sn, MJD=mjd, notes=notes, wavelength=w, flux=s)
    return 1
