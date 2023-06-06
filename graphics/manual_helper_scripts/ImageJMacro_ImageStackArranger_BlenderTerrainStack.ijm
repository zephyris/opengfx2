run("8-bit");

x=newArray(4, 324, 644, 964, 1284, 1596, 1916, 2236, 2556, 2876, 3196, 3516, 3836, 4156, 4476, 4788, 5108, 5428, 5748)
y=newArray(-124, -124, -124, -124, -124, -124, -124, -124, -92, -92, -92, -92, -92, -92, -92, -60, -124, -92, -92);

cid=getImageID();
w=getWidth();
h=getHeight();
d=nSlices();
getLut(r, g, b);
outwidth=6008;
outheight=196;
newImage("t", "8-bit white", outwidth, outheight, 1);
setLut(r, g, b);
oid=getImageID();
for (i=0; i<d; i++) {
	selectImage(cid);
	setSlice(i+1);
	makeRectangle(0, 0, w, h);
	run("Copy");
	selectImage(oid);
	makeRectangle(x[i], y[i], w, h);
	run("Paste");
}
