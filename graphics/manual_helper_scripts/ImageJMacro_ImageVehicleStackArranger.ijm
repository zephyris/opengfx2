//Trains
width=newArray(8, 22, 31, 22, 8, 22, 31, 22);
height=newArray(23, 19, 15, 19, 23, 19, 15, 19);
xoffs=newArray(-3, -15, -17, -7, -3, -15, -17, -7);
yoffs=newArray(-13, -12, -11, -12, -13, -12, -11, -12);
//width=newArray(8, 22, 31, 22);
//height=newArray(23, 19, 15, 19);
//xoffs=newArray(-3, -15, -17, -7);
//yoffs=newArray(-13, -12, -11, -12);

//RVs
//width=newArray(8, 22, 31, 22, 8, 22, 31, 22);
//height=newArray(23, 19, 15, 19, 23, 19, 15, 19);
//xoffs=newArray(-3, -15, -15, -7, -3, -15, -15, -7);
//yoffs=newArray(-15, -10, -9, -10, -15, -10, -9, -10);

//Air
//width=newArray(80, 80, 80, 80, 80, 80, 80, 80);
//height=newArray(80, 80, 80, 80, 80, 80, 80, 80);
//xoffs=newArray(-40, -40, -40, -40, -40, -40, -40, -40);
//yoffs=newArray(-40, -40, -40, -40, -40, -40, -40, -40);

//Sea
width=newArray(96, 96, 96, 96, 96, 96, 96, 96);
height=newArray(96, 96, 96, 96, 96, 96, 96, 96);
xoffs=newArray(-48, -74, -48, -22, -48, -74, -48, -22);
yoffs=newArray(-48, -32, -48, -32, -48, -32, -48, -32);

maxheight=height[0];
for (i=0; i<lengthOf(height); i++) {
	if (height[i]>maxheight) {
		maxheight=height[i];
	}
}
outwidth=0;
for (i=0; i<lengthOf(width); i++) {
	outwidth+=width[i]+1;
}
outwidth+=1;

cid=getImageID();
w=getWidth();
h=getHeight();
d=nSlices();
wrap=lengthOf(height);
getLut(r, g, b);
if (wrap==-1) {
	wrap=d;
}
rows=d/wrap;
outheight=(maxheight+1)*rows;
newImage("t", "8-bit white", outwidth+1, outheight+1, 1);
setLut(r, g, b);
oid=getImageID();
for (i=0; i<d; i++) {
	index=i%wrap;
	if (index==0) {
		curx=0;
	}
	selectImage(cid);
	setSlice(i+1);
	makeRectangle(getWidth()/2+xoffs[index], getHeight()/2+yoffs[index], width[index], height[index]);
	run("Copy");
	selectImage(oid);
	row=floor(i/wrap);
	makeRectangle(curx+1, row*(maxheight+1)+1, width[index], height[index]);
	run("Paste");
	curx+=width[index]+1;
}
