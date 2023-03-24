z=2;

a1=newArray(0, 0, 65, 33);
a2=newArray(958, 0, 65, 41);
a3=newArray(478, 0, 65, 25);
a4=newArray(240, 0, 65, 25);
a5=newArray(718, 0, 65, 41);

src=getImageID();
newImage("Untitled", "RGB black", 1236*z, 42*z, 1);
tgt=getImageID();
cx=0;
for (i=0; i<15; i++) {
	pasteImage(src, tgt, a1[0]*z, a1[1]*z, cx*z, 0*z, a1[2]*z, a1[3]*z);
	cx+=a1[2];
}
pasteImage(src, tgt, a2[0]*z, a2[1]*z, cx*z, 0*z, a2[2]*z, a2[3]*z);
cx+=a2[2];
pasteImage(src, tgt, a3[0]*z, a3[1]*z, cx*z, 0*z, a3[2]*z, a3[3]*z);
cx+=a3[2];
pasteImage(src, tgt, a4[0]*z, a4[1]*z, cx*z, 0*z, a4[2]*z, a4[3]*z);
cx+=a4[2];
pasteImage(src, tgt, a5[0]*z, a5[1]*z, cx*z, 0*z, a5[2]*z, a5[3]*z);
cx+=a5[2];

function pasteImage(src, tgt, sx, sy, tx, ty, w, h) {
	selectImage(src);
	makeRectangle(sx, sy, w, h);
	run("Copy");
	selectImage(tgt);
	makeRectangle(tx, ty, w, h);
	run("Paste");
}
