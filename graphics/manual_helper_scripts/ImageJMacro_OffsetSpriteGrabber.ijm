
//Faces: 805 184
//Signals, base: 1275 16
//Trees, tropical, agave: 1849 14
//Trees, tropical, palm & cacti: 1884 49
//Trees, toyland, all: 1947 63
//FX, power station, sparks: 2055 6
//Airport, windsock: 2676 4
//Airport, radar: 2680 12
//FX, vehicle, smoke: 3073 6
//FX, vehicle, steam: 3079 5
//FX, vehicle, steam: 3084 6
//FX, power station, smoke: 3701 8
//FX, vehicle, breakdown: 3737 4
//Vehicles, aircraft: 3741 168
//Vehicles, ships: 3669 32
//FX, vehicle, helicopter rotor: 3901 4
//FX, bubble factory, bubble: 4748 15

start=805;
number=184;
name="ogfx1_base";
//name="trg1r";

width=256;
height=256;
xoffs=width/2;
yoffs=height/2;

function pad(v, l) {
	s=""+v;
	while(lengthOf(s)<l) {
		s="0"+s;
	}
	return s;
}

function splitline(s) {
	l=lengthOf(s);
	//while (lengthOf(replace(s, "  ", " "))!=l) {
	//	s=replace(s, "  ", " ");
	//}
	a=split(s, " ");
	a[0]=parseInt(a[0]);
	for (i=3; i<9; i++) {
		a[i]=parseInt(a[i]);
	}
	return a;
}

path=getDirectory("");
data=File.openAsString(path+name+".nfo");
tlines=split(data, "\r\n");
lines=newArray();
for (i=0; i<lengthOf(tlines); i++) {
	if (substring(tlines[i], 0, 1)!="\t") {
		if (substring(tlines[i], 0, 1)!="/" && substring(tlines[i], 4, 5)!="|") {
			lines=Array.concat(lines, tlines[i]);
		}
	}
}
cid=0;
cimage="";

for (i=start; i<start+number; i++) {
	data=splitline(lines[i]);
	if (cimage!=data[1]) {
		if (cid!=0) {
			selectImage(cid);
			close();
		}
		open(path+substring(data[1], lengthOf("sprites/"), lengthOf(data[1])));
		cid=getImageID();
		cimage=data[1];
	}
	selectImage(cid);
	makeRectangle(data[3], data[4], data[5], data[6]);
	run("Copy");
	if (i==start) {
		run("Duplicate...", "t");
		run("Copy");
		oid=getImageID();
		run("Canvas Size...", "width="+width+" height="+height+" position=Center");
		makeRectangle(0, 0, getWidth(), getHeight());
		setColor(0);
		fill();
	} else {
		selectImage(oid);
		setSlice(nSlices());
		run("Add Slice");
		setSlice(nSlices());
	}
	print(xoffs+data[3], yoffs+data[4], data[5], data[6]);
	makeRectangle(xoffs+data[7], yoffs+data[8], data[5], data[6]);
	run("Paste");
}
selectImage(cid);
close();
selectImage(oid);
run("Select None");