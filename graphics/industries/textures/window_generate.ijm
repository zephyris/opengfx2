w=512;
l=128;
n=w*w/l;
n/=4;

function drawWrappedPixel(x, y, v) {
	setPixel((x+getWidth())%getWidth(), (y+getHeight())%getHeight(), v);
}

function drawLine(sx, sy, l, w, v) {
	for (i=0; i<l; i++) {
		for (a=0; a<w; a++) {
			drawWrappedPixel(sx+i, sy-i+a, v);
		}
	}
}

newImage("Untitled", "8-bit black", w, w, 1);
setColor(128);
fill();
for (i=0; i<n; i++) {
	sx=random()*w;
	sy=random()*w;
	drawLine(sx, sy, random()*l, random()*3, 255);
}
for (i=0; i<n; i++) {
	sx=random()*w;
	sy=random()*w;
	drawLine(sx, sy, random()*l, random()*3, 0);
}
