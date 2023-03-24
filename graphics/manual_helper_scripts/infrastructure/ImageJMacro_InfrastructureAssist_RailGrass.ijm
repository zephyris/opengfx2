z=4;

a1=newArray(0, 0, 65, 34);
a2=newArray(958, 0, 65, 43);
a3=newArray(478, 0, 65, 26);
a4=newArray(240, 0, 65, 26);
a5=newArray(718, 0, 65, 43);

b1=newArray(638, 0, 65, 43);
b2=newArray(320, 0, 65, 34);
b3=newArray(80, 0, 65, 34);
b4=newArray(160, 0, 65, 26);
b5=newArray(1118, 0, 65, 34);
b6=newArray(558, 0, 65, 26);
b7=newArray(878, 0, 65, 34);
b8=newArray(1038, 0, 65, 43);

src=getImageID();
newImage("Untitled", "RGB black", 1691*z, 42*z, 1);
tgt=getImageID();
cx=0;
for (i=0; i<12; i++) {
	pasteImage(src, tgt, a1[0]*z, a1[1]*z, cx*z, 0*z, a1[2]*z, a1[3]*z);
	cx+=a1[2];
}

pasteImage(src, tgt, b1[0]*z, b1[1]*z, cx*z, 0*z, b1[2]*z, b1[3]*z);
cx+=b1[2];
pasteImage(src, tgt, b2[0]*z, b2[1]*z, cx*z, 0*z, b2[2]*z, b2[3]*z);
cx+=b2[2];
pasteImage(src, tgt, b3[0]*z, b3[1]*z, cx*z, 0*z, b3[2]*z, b3[3]*z);
cx+=b3[2];
pasteImage(src, tgt, b4[0]*z, b4[1]*z, cx*z, 0*z, b4[2]*z, b4[3]*z);
cx+=b4[2];
pasteImage(src, tgt, b5[0]*z, b5[1]*z, cx*z, 0*z, b5[2]*z, b5[3]*z);
cx+=b5[2];
pasteImage(src, tgt, b6[0]*z, b6[1]*z, cx*z, 0*z, b6[2]*z, b6[3]*z);
cx+=b6[2];
pasteImage(src, tgt, b7[0]*z, b7[1]*z, cx*z, 0*z, b7[2]*z, b7[3]*z);
cx+=b7[2];
pasteImage(src, tgt, b8[0]*z, b8[1]*z, cx*z, 0*z, b8[2]*z, b8[3]*z);
cx+=b8[2];

pasteImage(src, tgt, a2[0]*z, a2[1]*z, cx*z, 0*z, a2[2]*z, a2[3]*z);
cx+=a2[2];
pasteImage(src, tgt, a3[0]*z, a3[1]*z, cx*z, 0*z, a3[2]*z, a3[3]*z);
cx+=a3[2];
pasteImage(src, tgt, a4[0]*z, a4[1]*z, cx*z, 0*z, a4[2]*z, a4[3]*z);
cx+=a4[2];
pasteImage(src, tgt, a5[0]*z, a5[1]*z, cx*z, 0*z, a5[2]*z, a5[3]*z);
cx+=a5[2];
for (i=0; i<2; i++) {
	pasteImage(src, tgt, a1[0]*z, a1[1]*z, cx*z, 0*z, a1[2]*z, a1[3]*z);
	cx+=a1[2];
}

function pasteImage(src, tgt, sx, sy, tx, ty, w, h) {
	selectImage(src);
	makeRectangle(sx, sy, w, h);
	run("Copy");
	selectImage(tgt);
	makeRectangle(tx, ty, w, h);
	run("Paste");
}
