offs=0.5;
ori=-1;

for (x=0; x<getWidth(); x++) {
	v=newArray(getHeight());
	for (y=getHeight()-1; y>=0; y--) {
		v[y]=getPixel(x, y);
	}
	for (y=getHeight()-1; y>=0; y--) {
		cy=y+ori*floor(x/2);
		while (cy<0) {
			cy+=getHeight();
		}
		cy=cy%getHeight();
		setPixel(x, cy, v[y]);
	}
	updateDisplay();
}
