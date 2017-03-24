from Spectroscopy.models import Spectrum, SpectrumDataPoint

UPLOAD_PATH='/home/kati/Dropbox/munka/learning/sn_app/test_tools/uploads/tmp.txt'

def uploadSpectrum(f, sn, mjd, notes):
    #f=open(file.file, 'r')
    #f=file
    with open(UPLOAD_PATH, 'wr') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    f=open(UPLOAD_PATH, 'r')

    Sp=Spectrum.objects.create(sn=sn, MJD=mjd, notes=notes)


    for line in f:
        line=line.split(' ')
        p=SpectrumDataPoint(spectrum=Sp, wavelength=line[0], flux=line[1])
        print p.flux
        p.save()
    f.close()
    return 1
