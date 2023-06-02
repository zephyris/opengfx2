slices=6;
dy=2;
h=56;
w=48;
pad=8;

newImage("Untitled", "8-bit black", w, h, slices);

//3 points per line
for (a=0; a<3; a++) {
	//for loop range of dy*slices
	for (b=0; b<slices*dy; b++) {
		sx=random()*(w-pad*2)+pad;
		sy=-b;
		sz=0;
		for (y=0; y<h+slices*dy; y++) {
			setPixel(sx, sy, 255);
			setSlice(sz%slices+1);
			r=random();
			if (r<0.33) {
				sx--;
			} else if (r>0.66) {
				sx++;
			}
			sy+=2;
			sz++;
		}
	}
}
