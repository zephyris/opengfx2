z=4;

a1=newArray(0, 0, 65, 33);
a2=newArray(65, 0, 65, 33);
a3=newArray(130, 0, 65, 33);
a4=newArray(195, 0, 65, 33);
a5=newArray(260, 0, 65, 33);
a6=newArray(325, 0, 65, 33);
a7=newArray(390, 0, 65, 33);

b1=newArray(0, 33, 65, 41);
b2=newArray(65, 33, 65, 25);
b3=newArray(130, 33, 65, 25);
b4=newArray(195, 33, 65, 41);

src=getImageID();
newImage("Untitled", "RGB color white", 1691*z, 42*z, 2);
tgt=getImageID();
cx=0;
pasteImage(src, tgt, a2[0]*z, a2[1]*z, cx*z, 0*z, a2[2]*z, a2[3]*z);
cx+=a2[2];
pasteImage(src, tgt, a1[0]*z, a1[1]*z, cx*z, 0*z, a1[2]*z, a1[3]*z);
cx+=a1[2];
pasteImage(src, tgt, a3[0]*z, a3[1]*z, cx*z, 0*z, a3[2]*z, a3[3]*z);
cx+=a3[2];
pasteImage(src, tgt, a4[0]*z, a4[1]*z, cx*z, 0*z, a4[2]*z, a4[3]*z);
cx+=a4[2];
pasteImage(src, tgt, a5[0]*z, a5[1]*z, cx*z, 0*z, a5[2]*z, a5[3]*z);
cx+=a5[2];
pasteImage(src, tgt, a6[0]*z, a6[1]*z, cx*z, 0*z, a6[2]*z, a6[3]*z);
cx+=a6[2];
pasteImage(src, tgt, a7[0]*z, a7[1]*z, cx*z, 0*z, a7[2]*z, a7[3]*z);
cx+=a7[2];

for (i=0; i<5; i++) {
	cx+=a1[2];
}

pasteImage(src, tgt, a4[0]*z, a4[1]*z, cx*z, 0*z+8*z, a4[2]*z, a4[3]*z);
cx+=a4[2];
pasteImage(src, tgt, a6[0]*z, a6[1]*z, cx*z, 0*z, a6[2]*z, a6[3]*z);
cx+=a6[2];
pasteImage(src, tgt, a5[0]*z, a5[1]*z, cx*z, 0*z, a5[2]*z, a5[3]*z);
cx+=a5[2];
pasteImage(src, tgt, a3[0]*z, a3[1]*z, cx*z, 0*z, a3[2]*z, a3[3]*z);
cx+=a3[2];

pasteImage(src, tgt, a5[0]*z, a5[1]*z, cx*z, 0*z, a5[2]*z, a5[3]*z);
cx+=a5[2];
pasteImage(src, tgt, a4[0]*z, a4[1]*z, cx*z, 0*z-8*z, a4[2]*z, a4[3]*z);
cx+=a4[2];
pasteImage(src, tgt, a6[0]*z, a6[1]*z, cx*z, 0*z, a6[2]*z, a6[3]*z);
cx+=a6[2];
pasteImage(src, tgt, a3[0]*z, a3[1]*z, cx*z, 0*z, a3[2]*z, a3[3]*z);
cx+=a3[2];

pasteImage(src, tgt, b1[0]*z, b1[1]*z, cx*z, 0*z, b1[2]*z, b1[3]*z);
cx+=b1[2];
pasteImage(src, tgt, b2[0]*z, b2[1]*z, cx*z, 0*z, b2[2]*z, b2[3]*z);
cx+=b2[2];
pasteImage(src, tgt, b3[0]*z, b3[1]*z, cx*z, 0*z, b3[2]*z, b3[3]*z);
cx+=b3[2];
pasteImage(src, tgt, b4[0]*z, b4[1]*z, cx*z, 0*z, b4[2]*z, b4[3]*z);
cx+=b4[2];

pasteImage(src, tgt, a3[0]*z, a3[1]*z, cx*z, 0*z, a3[2]*z, a3[3]*z);
setSlice(2);
pasteImage(src, tgt, a4[0]*z, a4[1]*z, cx*z, 0*z, a4[2]*z, a4[3]*z);
cx+=a4[2];
setSlice(1);
pasteImage(src, tgt, a5[0]*z, a5[1]*z, cx*z, 0*z, a5[2]*z, a5[3]*z);
setSlice(2);
pasteImage(src, tgt, a6[0]*z, a6[1]*z, cx*z, 0*z, a6[2]*z, a6[3]*z);
cx+=a6[2];

function pasteImage(src, tgt, sx, sy, tx, ty, w, h) {
	selectImage(src);
	makeRectangle(sx, sy, w, h);
	run("Copy");
	selectImage(tgt);
	makeRectangle(tx, ty, w, h);
	run("Paste");
}

run("Z Project...", "projection=[Min Intensity]");
selectImage(tgt);
close();
