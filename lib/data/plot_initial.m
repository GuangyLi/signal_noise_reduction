screenoff = dlmread('screen off.txt', '	', 1, 0);
screenoff(end)=[];
%disp(screenoff);
sotime=[0:.003:(length(screenoff)-1)*.003];
%plot(sotime,screenoff);

hold on;

homescreen = dlmread('home screen.txt', '	', 1, 0);
homescreen(end)=[];
hstime=[0:.003:(length(homescreen)-1)*.003];
%plot(hstime,homescreen);


youtube = dlmread('youtube.txt', '	', 1, 0);
youtube(end)=[];
yttime=[0:.003:(length(youtube)-1)*.003];
%plot(yttime,youtube);

musicscreenoff = dlmread('music screen off.txt', '	', 1, 0);
musicscreenoff(end)=[];
msotime=[0:.003:(length(musicscreenoff)-1)*.003];
%plot(msotime,musicscreenoff);

musicscreenon = dlmread('music screen on.txt', '	', 1, 0);
musicscreenon(end)=[];
msontime=[0:.003:(length(musicscreenon)-1)*.003];
%plot(msontime,musicscreenon);

chrome = dlmread('chrome.txt', '	', 1, 0);
chrome(end)=[];
ctime=[0:.003:(length(chrome)-1)*.003];
%plot(ctime,chrome);

gpu = dlmread('gpu.txt', '	', 1, 0);
gpu(end)=[];
disp(length(gpu));
gputime=[0:.003:(length(gpu)-1)*.003];
plot(gputime,gpu);
xlim([0,8.75]);
title('Current Trace of Different Applications');
ylabel("Current (mA)");
xlabel("Time (s)"); 

lgd=legend({'GPU Benchmark'});
 
%lgd=legend({'Screen Off','Home Screen','Youtube',...
 %   'Music Screen Off','Music Screen On','Chrome','GPU Benchmark'});



