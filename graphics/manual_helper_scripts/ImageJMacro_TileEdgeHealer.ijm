r=newArray(getWidth()*getHeight());

for (x=0; x<getWidth(); x++) {
	for (y=0; y<getHeight(); y++) {
		v=getPixel(x, y);
		r[x+y*getWidth()]=v;
		if (v!=0 && v!=255) {
			v1=getPixel(x-1, y-1);
			v2=getPixel(x-2, y-1);
			v3=getPixel(x+1, y-1);
			v4=getPixel(x+2, y-1);
			if (v1==0 && v2==0 && v3==0 && v4==0) {
				r[x+y*getWidth()]=0;
			}
		}
		if (v==0) {
			v1=getPixel(x-1, y-1);
			v2=getPixel(x-2, y-1);
			v3=getPixel(x+1, y-1);
			v4=getPixel(x+2, y-1);
			if (v1!=0 && v2!=0 && v3!=0 && v4!=0 && v1!=255) {
				vr=random();
				if (vr<0.25) {
					r[x+y*getWidth()]=v1;
				} else if (vr<0.5) {
					r[x+y*getWidth()]=v2;
				} else if (vr<0.75) {
					r[x+y*getWidth()]=v3;
				} else {
					r[x+y*getWidth()]=v4;
				}
			}
		}
	}
}
for (x=0; x<getWidth(); x++) {
	for (y=0; y<getHeight(); y++) {
		setPixel(x, y, r[x+y*getWidth()]);
	}
}
