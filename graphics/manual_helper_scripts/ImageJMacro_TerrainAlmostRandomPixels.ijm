newImage("Untitled", "8-bit white", 1502, 49, 1);
for (x=0; x<getWidth(); x++) {
	for (y=0; y<getHeight(); y++) {
		if (random()<1/16 && getPixel(x-1, y)==255 && getPixel(x, y-1)==255 &&getPixel(x-1, y-1)==255) {
			v=floor(random()*8);
			setPixel(x, y, v+1);
		}
	}
}
