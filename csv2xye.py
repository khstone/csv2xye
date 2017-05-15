import numpy as np
from matplotlib import pyplot as plt

mult = 1e6   #A multiplicative factor to make the numbers reasonable (adjust as desired)
def readfile():
	while True:
		try:
			filename = raw_input("Please enter the csv file to convert:  ")
			csv = open(filename)
			break
		except:
			print "Cannot open that file, please try again..."
	
	line = csv.readline()
	temp = line.split(',')
	for i in range(0, np.size(temp)):
		print i, temp[i].strip()
	
	xi = int(raw_input("Enter channel number to use for x:  "))
	yi = int(raw_input("Enter channel number to use for y:  "))
	i0i = int(raw_input("Enter channel number to use for I0:  "))
	
	x = []
	y = []
	i0 = []
	line = csv.readline()
	while line:
		temp = line.split(",")
		x = np.append(x, float(temp[xi]))
		y = np.append(y, float(temp[yi]))       
		i0 = np.append(i0, float(temp[i0i]))
		line = csv.readline()
	csv.close()
	return np.around(x,4), y, i0

fullx = []
fully = []
fulli0 = []
while True:
	newx, newy, newi0 = readfile()
	if len(fullx) <= 1:
		fullx = newx
		fully = newy
		fulli0 = newi0
	else:
		for i in xrange(0, len(newx)):
			if newx[i] in fullx:
				j = where(fullx == newx[i])
				fully[j] += newy[i]
				fulli0[j] += newi0[i]
			else:
				fullx = np.append(fullx, newx[i])
				fully = np.append(fully, newy[i])
				fulli0 = np.append(fulli0, newi0[i])
	indexing = np.argsort(fullx)
	fullx = fullx[indexing]
	fully = fully[indexing]
	fulli0 = fulli0[indexing]
	more = raw_input("File read, do you want to merge more data files with this one (Y/N)?")
	if more not in ['y','Y','yes','Yes','YES']:
		break

goodpts = np.where(fulli0 > 1.0)   # remove points where the beam may have been down
        
x = fullx[goodpts]
y = fully[goodpts]
i0 = fulli0[goodpts]

uy = np.sqrt(y)
ui0 = np.sqrt(i0)

y2 = np.zeros_like(y)
uy2 = np.zeros_like(y)
for i in xrange(0, np.size(y)):  #make sure that no detector channel is 0 (ad hoc adjustment, but keeps things well behaved)
	y2[i] = max(y[i], 1.0)
	uy2[i] = max(np.sqrt(y[i]), 1.0)

outname = raw_input("Enter the name of the file to save this as, without extensions...")

outfile = open(outname + '.xye', "w")
for i in xrange(0, np.size(x)):
	outfile.write(str(x[i]) + "\t" + str(mult*y2[i]/i0[i]) + "\t" + str(mult*np.sqrt((uy2[i]/y2[i])**2 + (ui0[i]/i0[i])**2)*(y2[i]/i0[i])) + "\n")
    #outfile.write(str(x[i]) + "\t" + str(mult*y[i]) + "\t" + str(sqrt(mult*y[i])) + "\n")
outfile.close()

outfile = open(outname + ".fxye", "w")
outfile.write('Title'.ljust(80) + '\n')
outfile.write('# Comments go here...'.ljust(80) + '\n')
outfile.write(("BANK 1 %i %i CONST %f %f 0.0 0.0 FXYE" % (int(np.size(x)), int(np.size(x)),x[0]*100.,(x[1] - x[0])*100.)).ljust(80) + '\n')
for i in xrange(0, np.size(x)):
	outfile.write(("%15.6f    %15.6G    %15.6G" % (x[i]*100., mult*y2[i]/i0[i], mult*np.sqrt((uy2[i]/y2[i])**2 + (ui0[i]/i0[i])**2)*(y2[i]/i0[i]))).ljust(80) + '\n')
	#outfile.write(str(x[i]*100) + "\t" + str(y2[i]/i0[i]) + "\t" + str(sigma[i]) + "\n")
outfile.close()

plt.figure()
plt.plot(x, mult * y2/i0)

plt.show()
