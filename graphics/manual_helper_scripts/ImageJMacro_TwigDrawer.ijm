getSelectionBounds(x, y, w, h);
area=w*h;
for (i=0; i<area/10; i++) {
	cx=floor(random()*w)+x;
	cy=floor(random()*h)+y;
	v=getPixel(cx, cy);
	if (v!=0) {
		d=floor(random()*5);
		for (j=1; j<=7; j++) {
			if (d==0) {
				dx=-1;
				dy=0;
			} else if (d==1) {
				dx=-1;
				dy=-1;
				} else if (d==2) {
				dx=0;
				dy=-1;
			} else if (d==3) {
				dx=1;
				dy=-1;
			} else if (d==4) {
				dx=1;
				dy=0;
			} else if (d==5) {
				dx=1;
				dy=1;
			} else if (d==6) {
				dx=0;
				dy=1;
			} else if (d==7) {
				dx=-1;
				dy=1;
			}
			rch=random();
			if (rch>0.9) {
				d++;
			} else if (rch<0.1) {
				d--;
			}
			if (d<0) {
				d+=5;
			}
			if (d>=5) {
				d-=5;
			}
			cx+=dx;
			cy+=dy;
			vt=getPixel(cx, cy);
			if (vt!=0) {
				j=7;
			} else {
				setPixel(cx, cy, v);
			}
		}
	}
}
