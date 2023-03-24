version=1;

w=getWidth();
h=getHeight();
src=getImageID();
type=bitDepth();
if (type==24) {
	type="RGB";
} else {
	type=""+type+"-bit";
}

slopefactor=2; //Flat tile
//slopefactor=1.32; //Sloping up top-right
//slopefactor=4; //Sloping down top-right
extraheight=w/slopefactor-w/2;
print(extraheight, floor(extraheight));

newImage("out", ""+type+" black", w*2, h+extraheight, 2);
out=getImageID();
setBatchMode(true);

for (x=0; x<w; x++) {
	for (y=0; y<h; y++) {
		selectImage(src);
		v=getPixel(x, y);
		selectImage(out);
		setSlice(1);
		setPixel(x+y+y%2, h/2-floor(x/slopefactor)+floor(y/2)+extraheight, v);
		setSlice(2);
		setPixel(x+y+x%2, h/2-floor(x/slopefactor)+floor(y/2)+extraheight, v);
	}
}
