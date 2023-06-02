wrap=-1;
pad=1;

cid=getImageID();
w=getWidth();
h=getHeight();
d=nSlices();
getLut(r, g, b);
if (wrap==-1) {
	wrap=d;
}
outwidth=(w+pad)*wrap;
if(d%wrap==0) {
	rows=d/wrap;
} else {
	rows=floor(d/wrap)+1;
}
outheight=(h+1)*rows;
newImage("t", "8-bit white", outwidth+pad, outheight+pad, 1);
setLut(r, g, b);
oid=getImageID();
for (i=0; i<d; i++) {
	selectImage(cid);
	setSlice(i+1);
	makeRectangle(0, 0, w, h);
	run("Copy");
	selectImage(oid);
	row=floor(i/wrap);
	makeRectangle(((w+pad)*i)%outwidth+pad, row*(h+pad)+pad, w, h);
	run("Paste");
}
