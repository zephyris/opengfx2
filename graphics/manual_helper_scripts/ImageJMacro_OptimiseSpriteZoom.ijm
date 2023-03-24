path=getDirectory("");
files=getFileList(path);
for (i=0; i<lengthOf(files); i++) {
	if (endsWith(files[i], "_8bpp.png")==true && endsWith(files[i], "_zopt_8bpp.png")==false) {
		open(path+files[i]);
		optimiseSpriteSheet();
		title=substring(files[i], 0, lengthOf(files[i])-lengthOf("_8bpp.png"));
		saveAs("PNG", path+title+"_zopt_8bpp.png");
		close();
	}
}

function optimiseSpriteSheet() {
	//Add a slice to contain the modified sprites
	run("Add Slice");
	makeRectangle(0, 0, getWidth(), getHeight());
	setColor(255);
	fill();
	//Loop through all pixels
	for (x=0; x<getWidth(); x++) {
		for (y=0; y<getHeight(); y++) {
			//If slice one (original) is not white
			setSlice(1);
			if (getPixel(x, y)!=255) {
				//And slice two (new) is white
				setSlice(2);
				if (getPixel(x, y)==255) {
					//Go to slice 1
					setSlice(1);
					//Extend in x direction to check for non-white pixels to find sprite width
					a=0;
					while (getPixel(x+a, y)!=255 && x+a<getWidth()) {
						a++;
					}
					//And the y direction for height
					b=0;
					while (getPixel(x, y+b)!=255 && y+b<getHeight()) {
						b++;
					}
					//Make a selection for the current sprite, and optimise it
					makeRectangle(x, y, a, b);
					optimiseSprite(x, y, a, b);
					//Copy the modified sprite to the new slice
					run("Copy");
					setSlice(2);
					run("Paste");
					//And delete the original sprite from the start slice
					setSlice(1);
					setColor(255);
					fill();
				}
			}
		}
	}
	//Delete the original sprite slice
	setSlice(1);
	run("Delete Slice");
}

function optimiseSprite(x, y, w, h) {
	//Zoom levels to analyse, from most zoomed out to least
	z=newArray(4, 2);
	//Loop through all pixels in the sprite
	for (a=0; a<w; a++) {
		for (b=0; b<h; b++) {
			//If the current pixel is not index 0 or 255
			if (getPixel(x+a, y+h-b)!=0 && getPixel(x+a, y+h-b)!=255) {
				//Loop through zoom levels, but only do the analysis for the first zoom level
				m=false;
				for (i=0; i<lengthOf(z); i++) {
					//If the current pixel is one that will appear in the current zoom out level
					if ((a+1)%z[i]==0 && b%z[i]==0 && m==false) {
						//Flag as analysed, so analysis is not repeated for lower zoom levels
						m=true;
						//Loop through pixels that will be hidden at the current zoom level
						//Make a histogram of the pixel values
						v=newArray(256);
						for (c=0; c<z[i]; c++) {
							for (d=0; d<z[i]; d++) {
								//Add one to the v array corresponding to that pixel value
								v[getPixel(x+a+c, y+h-b-d)]=v[getPixel(x+a+c, y+h-b-d)]+1;
							}
						}
						//Loop through the pixel values and find the most common
						n=0;
						m=0;
						for (j=0; j<256; j++) {
							//If the number of pixels with the current larger is the largest so far
							if (v[j]>n) {
								//Record the new max value, and its index
								n=v[j];
								m=j;
							}
						}
						//If a pixel value is in a majority
						if (n>1) {
							//And is not 0 or 255
							if (m!=0 && m!=255) {
								//Set the current pixel value to the majority value
								setPixel(x+a, y+h-b, m);
							}
						}
						//Update view
						updateDisplay();
					}
				}
			}
		}
	}
}
		
