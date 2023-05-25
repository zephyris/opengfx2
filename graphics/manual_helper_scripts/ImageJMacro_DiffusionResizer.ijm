//Settings groups
//temperate_shoretile_water
probDiffuse=0.6;
diffuseRange=2;
anisotropic=true;

//general_water
//probDiffuse=0.4;
//diffuseRange=2;
//anisotropic=true;

//trees
probDiffuse=0.8;
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
					if (v2!=0 && v2!=255) {
						setPixel(x, y, v2);
						setPixel(x+rx, y+ry, v1);
					}
				}
			}
		}
	}
}
