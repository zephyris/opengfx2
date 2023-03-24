scale=4;
newImage("Untitled", "8-bit white", 1502*scale, 192*scale, 1);
for (x=0; x<getWidth(); x++) {
	for (y=0; y<48*scale; y++) {
		if (random()<0.333) {
			setPixel(x, y+48*scale, 0);
		}
	}
}
for (x=0; x<getWidth(); x++) {
	for (y=0; y<48*scale; y++) {
		if (random()<0.666) {
			setPixel(x, y+96*scale, 0);
		}
	}
}
makeRectangle(0, 144*scale, 1502*scale, 192*scale);
setColor(0);
fill();
