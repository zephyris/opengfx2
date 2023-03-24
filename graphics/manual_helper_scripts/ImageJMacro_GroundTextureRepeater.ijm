makeRectangle(0, 0, getWidth(), 200);
run("Copy");
for (i=0; i<getHeight(); i+=196) {
	makeRectangle(0, i, getWidth(), 200);
	run("Paste");
}
