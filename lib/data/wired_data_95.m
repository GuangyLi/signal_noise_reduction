clear all;
clear clc;
close all;

f1=figure(1);
movegui(f1,'west');
set(0, 'CurrentFigure', f1)


google3 = dlmread('Wired Control Data 95%/trial1.txt', ' ', 1, 0);
google3(end)=[];
g3time=0:.003:(length(google3)-1)*.003;
subplot(3,2,1), plot(g3time,google3);
xlim([0 3]);
title("Trial 1");
ylabel('Current (mA)');
xlabel('Time (s)');

google4 = dlmread('Wired Control Data 95%/trial2.txt', ' ', 1, 0);
google4(end)=[];
g4time=0:.003:(length(google4)-1)*.003;
subplot(3,2,2), plot(g4time,google4);
xlim([0 3]);
title("Trial 2");
ylabel('Current (mA)');
xlabel('Time (s)');

google5 = dlmread('Wired Control Data 95%/trial3.txt', ' ', 1, 0);
google5(end)=[];
g5time=0:.003:(length(google5)-1)*.003;
subplot(3,2,3), plot(g5time,google5);
hsp1=get(gca, 'Position');
xlim([0 3]);
title("Trial 3");
ylabel('Current (mA)');
xlabel('Time (s)');

google6 = dlmread('Wired Control Data 95%/trial4.txt', ' ', 1, 0);
google6(end)=[];
g6time=0:.003:(length(google6)-1)*.003;
subplot(3,2,4), plot(g6time,google6);
hsp2=get(gca, 'Position');
xlim([0 3]);
title("Trial 4");
ylabel('Current (mA)');
xlabel('Time (s)');

newleft=(hsp1(1)+hsp2(1))/2;
positionVector = [newleft, 0.1, hsp1(3:4)];

google7 = dlmread('Wired Control Data 95%/trial5.txt', ' ', 1, 0);
google7(end)=[];
g7time=0:.003:(length(google7)-1)*.003;
subplot('Position',positionVector), plot(g7time,google7);
xlim([0 3]);
title("Trial 5");
ylabel('Current (mA)');
xlabel('Time (s)');

currentFigure = gcf;
t=sgtitle("Current Traces for Wired Control Data 95%");
 
%---------------------------------------%
%---------------------------------------%
f2=figure(2);
movegui(f2,'north');
set(0, 'CurrentFigure', f2)

yt1 = dlmread('Wired google.com Data 95%/trial1.txt', ' ', 1, 0);
yt1(end)=[];
yt1time=0:.003:(length(yt1)-1)*.003;
subplot(3,2,1), plot(yt1time,yt1);
xlim([0 3]);
title("Trial 1");
ylabel('Current (mA)');
xlabel('Time (s)');

yt2 = dlmread('Wired google.com Data 95%/trial2.txt', ' ', 1, 0);
yt2(end)=[];
yt2time=0:.003:(length(yt2)-1)*.003;
subplot(3,2,2), plot(yt2time,yt2);
xlim([0 3]);
title("Trial 2");
ylabel('Current (mA)');
xlabel('Time (s)');

yt3 = dlmread('Wired google.com Data 95%/trial3.txt', ' ', 1, 0);
yt3(end)=[];
yt3time=0:.003:(length(yt3)-1)*.003;
subplot(3,2,3), plot(yt3time,yt3);
xlim([0 3]);
title("Trial 3");
ylabel('Current (mA)');
xlabel('Time (s)');

hsp1=get(gca, 'Position');

yt4 = dlmread('Wired google.com Data 95%/trial4.txt', ' ', 1, 0);
yt4(end)=[];
yt4time=0:.003:(length(yt4)-1)*.003;
subplot(3,2,4), plot(yt4time,yt4);
xlim([0 3]);
title("Trial 4");
ylabel('Current (mA)');
xlabel('Time (s)');

hsp2=get(gca, 'Position');

newleft=(hsp1(1)+hsp2(1))/2;
positionVector = [newleft, 0.1, hsp1(3:4)];

yt5 = dlmread('Wired google.com Data 95%/trial5.txt', ' ', 1, 0);
yt5(end)=[];
yt5time=0:.003:(length(yt5)-1)*.003;
subplot('Position',positionVector), plot(yt5time,yt5);
xlim([0 3]);
title("Trial 5");
ylabel('Current (mA)');
xlabel('Time (s)');



currentFigure = gcf;
t=sgtitle("Current Traces for Wired google.com Data 95%");

%------------------------------------------------------------%
%------------------------------------------------------------%
f3=figure(3);
movegui(f3,'east');
set(0, 'CurrentFigure', f3)

yt1 = dlmread('Wired wikipedia.org Data 95%/trial1.txt', ' ', 1, 0);
yt1(end)=[];
yt1time=0:.003:(length(yt1)-1)*.003;
subplot(3,2,1), plot(yt1time,yt1);
xlim([0 3]);
title("Trial 1");
ylabel('Current (mA)');
xlabel('Time (s)');

yt2 = dlmread('Wired wikipedia.org Data 95%/trial2.txt', ' ', 1, 0);
yt2(end)=[];
yt2time=0:.003:(length(yt2)-1)*.003;
subplot(3,2,2), plot(yt2time,yt2);
xlim([0 3]);
title("Trial 2");
ylabel('Current (mA)');
xlabel('Time (s)');

yt3 = dlmread('Wired wikipedia.org Data 95%/trial3.txt', ' ', 1, 0);
yt3(end)=[];
yt3time=0:.003:(length(yt3)-1)*.003;
subplot(3,2,3), plot(yt3time,yt3);
xlim([0 3]);
title("Trial 3");
ylabel('Current (mA)');
xlabel('Time (s)');

hsp1=get(gca, 'Position');

yt4 = dlmread('Wired wikipedia.org Data 95%/trial4.txt', ' ', 1, 0);
yt4(end)=[];
yt4time=0:.003:(length(yt4)-1)*.003;
subplot(3,2,4), plot(yt4time,yt4);
xlim([0 3]);
title("Trial 4");
ylabel('Current (mA)');
xlabel('Time (s)');

hsp2=get(gca, 'Position');

newleft=(hsp1(1)+hsp2(1))/2;
positionVector = [newleft, 0.1, hsp1(3:4)];

yt5 = dlmread('Wired wikipedia.org Data 95%/trial5.txt', ' ', 1, 0);
yt5(end)=[];
yt5time=0:.003:(length(yt5)-1)*.003;
subplot('Position',positionVector), plot(yt5time,yt5);
xlim([0 3]);
title("Trial 5");
ylabel('Current (mA)');
xlabel('Time (s)');

currentFigure = gcf;
t=sgtitle("Current Traces for Wired wikipedia.org Data 95%");
%-----------------------------------------------------------------------%
f4=figure(4);
movegui(f4,'south');
set(0, 'CurrentFigure', f4)
yt1 = dlmread('Wired cnn.com Data 95%/trial1.txt', ' ', 1, 0);
yt1(end)=[];
yt1time=0:.003:(length(yt1)-1)*.003;
subplot(3,2,1), plot(yt1time,yt1);
xlim([0 4]);
title("Trial 1");
ylabel('Current (mA)');
xlabel('Time (s)');

yt2 = dlmread('Wired cnn.com Data 95%/trial2.txt', ' ', 1, 0);
yt2(end)=[];
yt2time=0:.003:(length(yt2)-1)*.003;
subplot(3,2,2), plot(yt2time,yt2);
xlim([0 4]);
title("Trial 2");
ylabel('Current (mA)');
xlabel('Time (s)');

yt3 = dlmread('Wired cnn.com Data 95%/trial3.txt', ' ', 1, 0);
yt3(end)=[];
yt3time=0:.003:(length(yt3)-1)*.003;
subplot(3,2,3), plot(yt3time,yt3);
xlim([0 4]);
title("Trial 3");
ylabel('Current (mA)');
xlabel('Time (s)');

hsp1=get(gca, 'Position');

yt4 = dlmread('Wired cnn.com Data 95%/trial4.txt', ' ', 1, 0);
yt4(end)=[];
yt4time=0:.003:(length(yt4)-1)*.003;
subplot(3,2,4), plot(yt4time,yt4);
xlim([0 4]);
title("Trial 4");
ylabel('Current (mA)');
xlabel('Time (s)');

hsp2=get(gca, 'Position');

newleft=(hsp1(1)+hsp2(1))/2;
positionVector = [newleft, 0.1, hsp1(3:4)];

yt5 = dlmread('Wired cnn.com Data 95%/trial5.txt', ' ', 1, 0);
yt5(end)=[];
yt5time=0:.003:(length(yt5)-1)*.003;
subplot('Position',positionVector), plot(yt5time,yt5);
xlim([0 4]);
title("Trial 5");
ylabel('Current (mA)');
xlabel('Time (s)');

currentFigure = gcf;
t=sgtitle("Current Traces for Wired cnn.com Data 95%");