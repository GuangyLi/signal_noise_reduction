%do multiple trials of RiB
music1 = dlmread('music1.txt', ' ', 1, 0);
music1(end)=[];
m1time=0:.003:(length(music1)-1)*.003;
%plot(m1time,music1);

hold on;

music2 = dlmread('music2.txt', ' ', 1, 0);
music2(end)=[];
m2time=0:.003:(length(music2)-1)*.003;
%plot(m2time,music2);

music3 = dlmread('music3.txt', ' ', 1, 0);
music3(end)=[];
m3time=0:.003:(length(music3)-1)*.003;
%plot(m3time,music3);

music4 = dlmread('music4.txt', ' ', 1, 0);
music4(end)=[];
m4time=0:.003:(length(music4)-1)*.003;
%plot(m4time,music4);

music5 = dlmread('music5.txt', ' ', 1, 0);
music5(end)=[];
m5time=0:.003:(length(music5)-1)*.003;
%plot(m5time,music5);

%do multiple trials of same Valkyrie
omusic1 = dlmread('omusic1.txt', ' ', 1, 0);
omusic1(end)=[];
om1time=0:.003:(length(omusic1)-1)*.003;
%plot(om1time,omusic1);

hold on;

omusic2 = dlmread('omusic2.txt', ' ', 1, 0);
omusic2(end)=[];
om2time=0:.003:(length(omusic2)-1)*.003;
%plot(om2time,omusic2);

omusic3 = dlmread('omusic3.txt', ' ', 1, 0);
omusic3(end)=[];
om3time=0:.003:(length(omusic3)-1)*.003;
%plot(om3time,omusic3);

omusic4 = dlmread('omusic4.txt', ' ', 1, 0);
omusic4(end)=[];
om4time=0:.003:(length(omusic4)-1)*.003;
%plot(om4time,omusic4);

omusic5 = dlmread('omusic5.txt', ' ', 1, 0);
omusic5(end)=[];
om5time=0:.003:(length(omusic5)-1)*.003;
%plot(om5time,omusic5);

xlim([0 10])