function Y = decpaihfh(FNAME)
%
% 倍音1つに情報を埋め込むのは，雜音耐性でキツいのでMUL倍音まで多重
% に使う．
% これは，検出プログラム．
%   %
% gen,decで共有する情報
%
paihfh_common_parameter;

% decだけに必要な情報
paih_dec_parameter;

% 二次的に計算される情報
embnum = double(moji);  % convert each char to int ('J' -> 74)
bitstr = dec2bin(embnum);  % convert int(dec) to int(bin) (74 -> 1001 
010)
[n, cn] = size(bitstr); %n: number of char, cn:num of bitlen
b = reshape(bitstr', cn*n, 1); % vectorize
% str2num is converting char b into double
mes = str2num(b)'  %

MUL = length(PN);

%================================================
%まずwavの情報を取得
FS=44100
[LEN,NCH] = wavread(FNAME,'size');

%

ONEBIT_LEN  = round(FS/BPS);
WINSIZE = 2*round(ONEBIT_LEN/(ITE_WIN))
FFTSIZE = max(32768,WINSIZE);

now_bit_old = 0;
detect = zeros(LEN(1)/ONEBIT_LEN,ITE_WIN);
x_ushiro= wavread(FNAME,[1  WINSIZE/2]);
for i=1:round(LEN/(WINSIZE/2));
  now_bit = floor(i*(WINSIZE/2)/(FS/BPS))+1;
  x_mae = x_ushiro;
  end_i = min(LEN,(i+1)*(WINSIZE/2));
  x_ushiro = wavread(FNAME,[i*(WINSIZE/2)+1  end_i(1)]);
  x = [x_mae;x_ushiro];
  length_x = length(x);
  x = hanning(length_x).*x;
  x_expand = zeros(FFTSIZE,1);
  x_expand(end/2-WINSIZE/2+1:end/2-WINSIZE/2+length_x) = x;
  fft_x = fft(x_expand);
    [tonal_val,tonal_idx] = max(abs(fft_x(1:end/2)));
  tonal = tonal_idx*FS/FFTSIZE;
    for k=1:MUL
    for b = 1:2
      maxi(b) = 0;
      Fh = (1+k)+g*power(-1,b-1);
      for f = -FW:0.01:FW
        if maxi(b) < abs(fft_x(round((Fh+f)*tonal_idx)))
          maxi(b) = abs(fft_x(round((Fh+f)*tonal_idx)));
        end
      end
    end
    if maxi(1) > maxi(2)
      tonal_mes_val(k) = 1;
    else
      tonal_mes_val(k) = -1;
    end
  end

  if DEBUG == 1
    fprintf('x\t:\tPN\n');
    for k = 1:MUL
      fprintf('%2d\t:\t%2d\n', tonal_mes_val(k), power(-1,PN(k)));
    end
  end
    if now_bit != now_bit_old
    c = 1;
    if (now_bit != 1)
      if (now_bit_old <= LEN(1)/ONEBIT_LEN)
        fprintf('====================\n');
        if sum(detect(now_bit_old,:))/ITE_WIN > 0
          mes_out(now_bit_old) = '0'
        elseif sum(detect(now_bit_old,:))/ITE_WIN < 0
          mes_out(now_bit_old) = '1'
        endif
        if mod(now_bit_old,7) == 0;
          nx = now_bit_old/7;
          x = reshape(mes_out(1:7*nx), 7, nx)';
          str = char(bin2dec(x))';
          str(1:min(length(str),70))
        end
        fprintf('====================\n');
      end
    end
  end

  fprintf('detect_mes_val(%d) => ',i);
  detect_mes_val = tonal_mes_val * power(-1,PN')/length(PN);
  if abs(detect_mes_val) > abs(sum(PN)/length(PN))
    if now_bit < LEN(1)/ONEBIT_LEN
      fprintf('%f\t:%d\t',...
              detect_mes_val,power(-1,mes(mod(now_bit-1,length(mes))+ 
1)));
      if detect_mes_val * power(-1,mes(mod(now_bit-1,length(mes))+1)) 
 > 0         %%同符号なら正になる
          fprintf('[o]\n');
          detect(now_bit,c) = detect_mes_val;
      else
        fprintf('[x]\n');
      end
    else
      fprintf('%f\t:- \n',...
              detect_mes_val);
    end
  else
    if now_bit < LEN(1)/ONEBIT_LEN
      fprintf('%f\t:%d\t[!Ambiguous]\t',...
            detect_mes_val,power(-1,mes(mod(now_bit-1,length(mes))+1) 
));
      if detect_mes_val * power(-1,mes(mod(now_bit-1,length(mes))+1)) 
 > 0
        fprintf('[o]\n');
      else
        fprintf('[x]\n');
      end
    else
      fprintf('%f\t:- [!Ambiguous]\n',...
              detect_mes_val);
    end
  end

  c = c +1;   now_bit_old = now_bit;
    t_expand = [0:FFTSIZE-1]/FS;
  subplot(3,1,1);plot(t_expand,x_expand);grid on;
  t_orig = [(i-1)*(WINSIZE/2)+1:end_i(1)]/FS;
  subplot(3,1,2);plot(t_orig,x);grid on;
  subplot(3,1,3);plot([0:Fh*1000*FFTSIZE/FS-1]*FS/FFTSIZE,(abs(fft_x( 
1:Fh*1000*FFTSIZE/FS))));grid on;
  input('hit some key to continue: ');


end


%Edirol R-44 %LS-10
%BME-200
%HM-250
%OKM
