w=512;
bw=4;
bh=2;
n=w*w/(bw*bh);
n/=16;

function drawWrappedPixel(x, y, v) {
	setPixel((x+getWidth())%getWidth(), (y+getHeight())%getHeight(), v);
}

function drawBlock(sx, sy, w, h, v) {
	for (x=0; x<w; x++) {
		for (y=0; y<h; y++) {
			drawWrappedPixel(sx+x, sy+y, v);
		}
	}
}

newImage("Untitled", "8-bit black", w, w, 1);
setColor(128);
fill();
for (i=0; i<n; i++) {
	sx=floor(random()*(w/bw))*2;
	sy=floor(random()*(w/bh));
	sx+=sy%2;
	sx*=bw/2;
	sy*=bh;
	drawBlock(sx, sy, bw, bh, 255);
}
for (i=0; i<n; i++) {
	sx=floor(random()*(w/bw))*2;
	sy=floor(random()*(w/bh));
	sx+=sy%2;
	sx*=bw/2;
	sy*=bh;
	drawBlock(sx, sy, bw, bh, 0);
}

function shear() {
	run("Add Slice");
	for (x=0; x<getWidth(); x+=2) {
		setSlice(1);
		makeRectangle(x, 0, 2, getHeight());
		run("Copy");
		setSlice(2);
		makeRectangle(x, x/2, 2, getHeight());
		run("Paste");
		makeRectangle(x, x/2 - getHeight(), 2, getHeight());		
		run("Paste");
	}
	run("Select None");
	setSlice(1);
	run("Delete Slice");
}

shear();
