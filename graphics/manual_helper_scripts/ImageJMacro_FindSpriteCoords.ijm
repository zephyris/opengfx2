changeValues(0, 254, 0);
r=newArray(256); g=newArray(256); b=newArray(256);
r[0]=255; g[0]=255; b[0]=255;
r[255]=0; g[255]=0; b[255]=0;
setLut(r, g, b);
run("RGB Color");
run("8-bit");
run("Find Maxima...", "prominence=10 output=[Point Selection]");
getSelectionCoordinates(sx, sy);
x=newArray(lengthOf(sx)); y=newArray(lengthOf(sx)); w=newArray(lengthOf(sx)); h=newArray(lengthOf(sx));
for (i=0; i<lengthOf(sx); i++) {
	doWand(sx[i], sy[i]);
	getSelectionBounds(cx, cy, cw, ch);
	x[i]=cx; y[i]=cy; w[i]=cw; h[i]=ch;
}
for (i=0; i<lengthOf(x); i++) {
	Array.getStatistics(x, xmin, xmax, xmean, xstdev);
	j=arrayIndexOf(x, xmin);
	print(x[j], y[j], w[j], h[j]);
	x[j]=getWidth()+1;
}

function arrayIndexOf(a, v) {
	i=-1;
	for (j=0; j<lengthOf(a); j++) {
		if (a[j]==v) {
			return j;
		}
	}
	return i;
}

