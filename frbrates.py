mport numpy as np

def printline():
    print("===================================================================")

def printheader():
    printline()
    print("Survey        gain   Tsys     Smin     FoV   days/event events/day")
    print("             [K/Jy]   [K]    [Jyms]   [sqdeg]   ")

def printfooter():
    printline()
    print(" ")

# ============================================================================
# define a survey type, and populate a list with survey parameters
# bandwith * number of poles: BWNp
survey_type = [("name", "S32"),
               ("BWNp","float"),
               ("Tsys","float"),
               ("collecting area", "float"),
               ("gain","float"),
               ("FoV","float")]


def gain(area, f=0.5):
  k = 1.38e-23
  return (area/k)*f /2. * 1E-26 #K/Jy
def fov(wav, diam):
  #area of circular field of view
  return np.pi * ((180/np.pi) * wav/(diam)/2)**2

surveys = np.zeros(14, dtype=survey_type)
surveys[0] = "Parkes",  340*2,  25, (64/2.)**2 * np.pi , gain((64/2.)**2 * np.pi),  fov(3e8/1.4e9, 64) * 13 # for 13 beams of Parkes
surveys[1] = "UTMOST",  32,  300,  1600*11, gain(1600*11, 0.25) ,9.0
surveys[2] = "DSA10",   250*2,  65, (4.5/2.)**2 * np.pi ,gain((4.5/2.)**2 * np.pi), fov(3e8/1.4e9, 4.5) * 10 #https://arxiv.org/pdf/1906.08699.pdf
surveys[3] = "DSA256",  250*2,  65,  (4.5/2.)**2 * np.pi ,gain((4.5/2.)**2 * np.pi), fov(3e8/1.4e9, 4.5) * 256
surveys[4] = "CHIME",   400*2,  50, 8000, gain(8000), 200 #https://iopscience.iop.org/article/10.3847/1538-4357/aad188
surveys[5] = "PALFA",   300*2, 30, (300/2)**2 * np.pi , gain((300/2)**2 * np.pi), fov(3e8/1.375e9, 300) # http://www.naic.edu/ao/scientist-user-portal/astronomy/receivers
surveys[6] = "MeerKat", 770*2, 20,  0.33, gain((13.5/2)**2*np.pi, 0.8), 42 # Manisha Caleb. (https://pos.sissa.it/277/001/pdf)
surveys[7] = "ASKAP",   300*2,  50,  4072/36, gain((12/2)**2 *np.pi, 0.8), 30.0 # https://www.atnf.csiro.au/projects/askap/specs.html
surveys[8] = "ASKAP36", 300*2,  50,  4072, gain((12/2)**2 *np.pi, 0.8), 30*36
surveys[9] = "Apertif", 750*2, 55, 7333,  gain((25/2)**2*np.pi, 0.75), 8 #https://arxiv.org/pdf/1007.5141.pdf. Aeff/Tsys = 100
surveys[10] = "UTMOST-2D", 45*2, 70, 1.4*11*66, gain(66*1.4*11,0.63), 30 #From Cherie
surveys[11] = "Wagtail", 45*2, 70, (0.2*0.2), gain(0.04, 0.5), 3600 #if we took UTMOST2D antennas and made a tiny array
surveys[12] = "ATA", 1400, 45, 1227, gain((6.1/2)**2 *np.pi), fov(3e8/0.8e9, 6.1) *42 #Wael's telescope
surveys[13] = "GBT", 580*20, 20,(100/2)**2 *np.pi , gain((100/2)**2*np.pi), fov(3e8/1.44e9, 100)

#print( fov(21e-2, 64) )


# f -> efficiency of the collection.
f = 0.5
k = 1.38e-23
area = np.pi*(64.0/2.0)**2
gain = area*f/2.0/k*1E-26
print("Parkes gain = ",gain)

# From Scott Ransom's notes
f = 0.7
area = 5500 / f
#f = 0.7
gain = area*f/2.0/k*1E-26
print("GBT gain = ",gain)


area = 18000.0  # m^2
gain = area*f/2.0/k*1E-26
print("Molonglo gain = ",gain)

area = 1.4*11  # m^2
gain = area*f/2.0/k*1E-26
print("NS cassette gain = ",gain)
print("NS cassette SEFD = ",100.0/gain/1e6," MJy")

area = 0.2*0.2  # m^2
gain = area*f/2.0/k*1E-26
print("Wagtail gain = ",gain)
print("Wagtail SEFD = ",100.0/gain/1e6," MJy")

area = 113.0  # m^2
gain = area*f/2.0/k*1E-26
print("ASKAP single dish gain = ",gain)

f = 0.7
area = np.pi*(13.5/2.0)**2
gain = area*f/2.0/k*1E-26
print("Meerkat single dish gain = ",gain)

# normalisation is to the Parkes FRB detection rate in days per event
parkes_daysperevent = 15 # days/event

# normalisation is to the Molonglo FRB detection rate in days per event
molonglo_daysperevent = 60 # days/event

# fluence scaling is to 1 ms events
dt = 1.0E-3  # sec

# SNR min at all telescopes 
SNRmin = 10.0

# figure out Smin at Parkes for the normalisation
TsysP = surveys[0]["Tsys"]
bwnpP = surveys[0]["BWNp"]*1E6   # convert to MHz

gainP = surveys[0]["gain"]
areaP = surveys[0]["FoV"]
SminP = SNRmin*TsysP/gainP/np.sqrt(bwnpP*dt)

# figure out Smin at Molonglo for the normalisation
TsysM = surveys[1]["Tsys"]
bwnpM = surveys[1]["BWNp"]*1E6   # convert to MHz
gainM = surveys[1]["gain"]
areaM = surveys[1]["FoV"]
SminM = SNRmin*TsysM/gainM/np.sqrt(bwnpM*dt)

# slope of the logNlogF relation
alpha = 1.5

printheader()
for i in range(len(surveys)):
    name = surveys[i]["name"]
    Tsys = surveys[i]["Tsys"]
    bwnp = surveys[i]["BWNp"]*1E6
    gain = surveys[i]["gain"]
    area = surveys[i]["FoV"]
    Smin = SNRmin*Tsys/gain/np.sqrt(bwnp*dt)
    daysperevent = parkes_daysperevent*(areaP/area)*(Smin/SminP)**alpha
    print('{:10s} {:9.4f} {:7.1f} {:7.2f} {:9.3f} {:8.2f} {:9.2f}'.format(name, gain, Tsys, Smin, area, daysperevent, 1.0/daysperevent))
printfooter()
