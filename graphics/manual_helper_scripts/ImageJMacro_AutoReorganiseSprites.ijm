spacing=16;
minspritearea=20;

//get source image ID
src=getImageID();
run("Select None");
//duplicate and crop to make output
run("Duplicate...", " ");
out=getImageID();
makeRectangle(0, 0, spacing, spacing);
run("Crop");
//duplicate and strip down to black/white not sprite/sprite
selectImage(src);
run("Duplicate...", " ");
tmp=getImageID();
changeValues(0, 254, 0);
r=newArray(256); g=newArray(256); b=newArray(256);
r[0]=255; g[0]=255; b[0]=255;
r[255]=0; g[255]=0; b[255]=0;
setLut(r, g, b);
run("RGB Color");
run("8-bit");
//Find sprites and get coordinates
//remove small sprites
run("Find Maxima...", "prominence=10 output=[Point Selection]");
getSelectionCoordinates(sx, sy);
for (i=0; i<lengthOf(sx); i++) {
	doWand(sx[i], sy[i]);
	getRawStatistics(area);
	if (area<minspritearea) {
		setColor(0);
		fill();
	}
}
//find coords
run("Select None");
run("Find Maxima...", "prominence=10 output=[Point Selection]");
getSelectionCoordinates(sx, sy);
x=newArray(lengthOf(sx)); y=newArray(lengthOf(sx)); w=newArray(lengthOf(sx)); h=newArray(lengthOf(sx));
for (i=0; i<lengthOf(sx); i++) {
	doWand(sx[i], sy[i]);
	getSelectionBounds(cx, cy, cw, ch);
	x[i]=cx; y[i]=cy; w[i]=cw; h[i]=ch;
}

//Brute force left to right, then top to bottom, grabbing sprites into sprite sheet
Array.getStatistics(x, xmin, xmax, xmean, xstdev);
Array.getStatistics(y, ymin, ymax, ymean, ystdev);

selectImage(tmp);
close();

pastex=0;
pastey=0;
for (cy=0; cy<ymax+1; cy++) {
	showProgress(cy/(ymax+2));
	for (cx=0; cx<xmax+1; cx++) {
		for (i=0; i<lengthOf(x); i++) {
			if (x[i]==cx && y[i]==cy) {
				selectImage(src);
				makeRectangle(x[i], y[i], w[i], h[i]);
				run("Copy");
				selectImage(out);
				if (getHeight()<pastey+h[i]+spacing*2) {
					run("Canvas Size...", "width="+getWidth()+" height="+(pastey+h[i]+spacing*2)+" position=Top-Left");
				}
				if (getWidth()<pastex+w[i]+spacing*2) {
					run("Canvas Size...", "width="+pastex+w[i]+spacing*2+" height="+getHeight()+" position=Top-Left");
				}
				makeRectangle(pastex, pastey, w[i]+spacing*2, h[i]+spacing*2);
				setColor(255);
				fill();
				makeRectangle(pastex+spacing, pastey+spacing, w[i], h[i]);
				run("Paste");
				pastex+=w[i]+spacing;
			}
		}
	}
}

selectImage(out);
