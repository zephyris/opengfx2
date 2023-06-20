newImage("Untitled", "8-bit ramp", 32, 32, 3);

setSlice(2);
run("Duplicate...", " ");
run("Rotate 90 Degrees Right");
run("Copy");
close();
run("Paste");

run("Canvas Size...", "width=256 height=256 position=Top-Left");
for (x=0; x<8; x++) {
	for (y=0; y<8; y++) {
		for (i=0; i<2; i++) {
			setSlice(i+1);
			makeRectangle(0, 0, 32, 32);
			run("Copy");
			makeRectangle(x*32, y*32, 32, 32);
			run("Paste");
		}
		setSlice(3);
		makeRectangle(x*32, y*32, 32, 32);
		setColor((x+y*8)*256/(8*8));
		fill();
	}
}
run("Select None");

run("Make Composite", "display=Composite");
