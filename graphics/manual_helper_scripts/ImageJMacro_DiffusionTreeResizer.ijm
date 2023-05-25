//Wants an OpenTTDDoS 8-bit image
//Leaf greens on a white background

function diffusion2xResize() {
	//trees
	probDiffuse=1;
	diffuseRange=1;
	anisotropic=false;

	//Resize 2x using nearest neighbour
	run("Size...", "width="+getWidth()*2+" height="+getHeight()*2+" constrain average interpolation=None");
	//Loop through all the pixels for pixel diffusion
	for (x=0; x<getWidth(); x++) {
		for (y=0; y<getHeight(); y++) {
			//Get the value of the current pixel
			v1=getPixel(x, y);
			//If not blue (0) or white (255) randomise whether to diffuse this pixel
			if (v1!=0 && v1!=255 && random()<probDiffuse) {
				//Set the xfactor for anisotropic diffusuion
				//Anisotropic diffusion promoting movement in x is good for many dimetric projections
				if (anisotropic==true) {
					xfac=1;
				} else {
					xfac=2;
				}
				//Find the random x/y offset to diffuse the pixel to
				rx=round(random()*diffuseRange*2*xfac-diffuseRange*xfac);
				ry=round(random()*diffuseRange*2-diffuseRange);
				//Only continue if the x/y offset is nonzero and within the image bounds
				if (rx!=0 && ry!=0) {
					if (x+rx>=0 && x+rx<getWidth() && y+ry>=0 && y+ry<getHeight()) {
						//Get the value of the pixel at the x/y offset
						v2=getPixel(x+rx, y+ry);
						//If it is not blue (0) or white (255) then swap values of the current pixel and the one at the x/y offset
						//if (v2!=0 && v2!=255) {
							setPixel(x, y, v2);
							setPixel(x+rx, y+ry, v1);
						//}
					}
				}
			}
		}
	}
}

diffusion2xResize();
diffusion2xResize();
run("Add Slice");
setColor(255);
makeRectangle(0, 0, getWidth(), getHeight());
fill();

style="leaf";
//style="needle";

for (x=1; x<getWidth()-1; x++) {
	for (y=1; y<getHeight()-1; y++) {
		setSlice(1);
		v=getPixel(x, y);
		rm=true;
		for (a=-1; a<2; a++) {
			for (b=-1; b<2; b++) {
				if (a!=0 || b!=0) {
					if (getPixel(x+a, y+b)!=255) {
						rm=false;
					}
				}
			}
		}
		if (rm==true) {
			setPixel(x, y, 255);
		} else {
			v=getPixel(x, y);
			setZCoordinate(1);
			if (v!=255) {
				valt=maxOf(80, v-1);
				if (style=="leaf") {
					setPixel(x, y, v);
					if (random()<0.5) {
						for (a=-1; a<2; a++) {
							for (b=-1; b<2; b++) {
								if (a==0 || b==0) {
									setPixel(x+a, y+b, v);
								}
							}
						}
					}
				}
				if (style=="needle") {
					da=(random()-0.5)*2+0.5;
					db=1;
					len=random()*2+2;
					r=random();
					for (i=0; i<len; i++) {
						setPixel(x+da*i, y+db*i, v);
					}
				}
			}
		}
	}
}
