function X = genpaihfh(FNAME)
%
% 倍音1つに情報を埋め込むのは，雜音耐性でキツい．
% % mes=0(+), PN=[1001]([-,+,+,-]) 
% % → mes_PN =[-,+,+,-] % を [ 2-a, 3+a, 4+a, 5-a] * f0 で表現
%

%
% gen,decで共有する情報
%
paihfh_common_parameter;

% genだけに必要な情報
paih_gen_parameter;

% check
if AIDA > 1/BPS
  input('AIDA * BPS is recommended to be larger than 1 !');
end

% 二次的に計算される情報
embnum = double(moji);  % convert each char to int ('J' -> 74)
bitstr = dec2bin(embnum);  % convert int(dec) to int(bin) (74 -> 1001 
010)
[n, cn] = size(bitstr); %n: number of char, cn:num of bitlen
b = reshape(bitstr', cn*n, 1); % vectorize
% str2num is converting char b into double
mes = str2num(b)'  %

LEN = ceil(length(mes)/BPS);
MUL = length(PN);

%=============================================
phasem_old = 2*pi*rand(MUL,1);
phase_old = 0;
t_mod_old = 0;
siren_paih=zeros(LEN*FS,1);
Nmean = 3;
Fh_mean = zeros(MUL,Nmean);
for t=0:1/FS:ceil(LEN)
  t_mod = mod(t,2*DUR);
  if (t_mod < AIDA)
    BASE = ((AIDA+t_mod)*PEE+(AIDA-t_mod)*POO)/(2*AIDA);
  elseif (AIDA <= t_mod && t_mod < DUR-AIDA)
      BASE = PEE;
  elseif (DUR-AIDA <= t_mod && t_mod < DUR+AIDA)
    BASE = ((DUR+AIDA-t_mod)*PEE + (t_mod-DUR+AIDA)*POO)/(2*AIDA);
  elseif (DUR+AIDA <= t_mod && t_mod < 2*DUR-AIDA)
    BASE = POO;
  else     BASE = ((t_mod-2*DUR+AIDA)*PEE + (2*DUR+AIDA-t_mod)*POO)/( 
2*AIDA);
  endif
    phase_base = 2*pi*BASE*mod(t_mod-t_mod_old,2*DUR);
  siren_base= sin(phase_base+phase_old);
  phase_old = phase_base+phase_old;
  now_bit = floor(t*BPS)+1;
  siren_mes = 0;
  for m = 1:MUL
    if now_bit <= length(mes)
      Fh(m,Nmean) = g*(power(-1,PN(m))*power(-1,mes(now_bit)));
    else
      Fh(m,Nmean) = 0;
    end

    Fh_mean = 0;count_Fh=0;
    for imean = 1:Nmean
      if Fh(m,imean) ~= 0
        Fh_mean = Fh_mean + Fh(m,imean);
        count_Fh = count_Fh + 1;
      end
    end
        if count_Fh ~= 0
      Fh_mean = Fh_mean/count_Fh;
    end
    Fh_mean = (1+m)+Fh_mean;

    if(1)
      if mod(round(t*FS+1),round(FS/BPS)) == 0.0
        figure(1);
        plot(t,...
             phase_base*Fh_mean/(2*pi*mod(t_mod-t_mod_old,2*DUR)),'rx 
');
        hold on;grid on;
        plot(t,...
             phase_base*(1+m)/(2*pi*mod(t_mod-t_mod_old,2*DUR)),'gd') 
;
      end
    end
        Gh = Gain/Fh_mean;
    siren_mes_m(m) = Gh*sin(phasem_old(m)+phase_base*Fh_mean);
    phasem_old(m) = phasem_old(m)+phase_base*Fh_mean;
    siren_mes = siren_mes + siren_mes_m(m);
    %figure(1);
    %subplot(MUL,1,m);plot(siren_mes_m(m,max(1,round(t*FS+1)-1000):ro 
und(t*FS+1)));
  end
  TEMP = Fh(:,2:Nmean);
  Fh(:,1:Nmean-1) = TEMP;

  t_mod_old = t_mod;
  %input('hit some key');
  siren_paih(round(t*FS+1)) = siren_base + siren_mes;
  if(1)
    if mod(round(t*FS+1),round(FS/BPS)) == 0.0
      figure(1);plot(t,BASE,'bo');hold on;grid on;
      %input('hit any key');
    end
  end
  %  input('hit some key');

end

maxi = 1/32767;
for i=1:length(siren_paih)
  if maxi < abs(siren_paih(i));
    maxi = abs(siren_paih(i));
  end
end
for i=1:length(siren_paih)
  siren_paih(i) = 0.5*siren_paih(i)/maxi;
end
wavwrite(siren_paih,FS,16,FNAME)

figure(1);
xlabel(['Time \rm{[s]}']);
ylabel(['Frequency \rm{[Hz]}']);
print('Fh.eps','-depsc2'); hold off;
close all;
