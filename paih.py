def str_ord(s:str):
    """convert Strings to decimal numbers 

    Args:
        s (str): strings

    Returns:
        (list): decimal numbers (lengh: string length)

    Example:
        >>> x = 'aA'
        >>> y = str_ord(x)
        >>> print(y)
        [97, 65]
        >>> x = 'あア'
        >>> y = str_ord(x)
        >>> print(y)
        [12354, 12450]
    """
    m = map(ord,s)
    l = list(m)
    return l

def str_bool(s:str,encoding='utf-8'):
    hb = s.encode(encoding)
    ordlist = [int("{:0d}".format(c)) for c in hb ]
    binlist = list(map(bin,ordlist))
    z = list(map(bin_bool,binlist))
    return z


def str_bool2(s:str):
    """convert Strings to list of boolean list
    
    Args:
        s (str): Strings
    Returns:
        (list of list): binary numbers ()
    
    Example:
        >>> x = 'aA'
        >>> Y = str_bool(x)
        >>> print(Y)

    """
    #from . import str_ord,bin_bool
    ordlist = str_ord(s)
    binlist = list(map(bin,ordlist))
    z = list(map(bin_bool,binlist))
    return z

def bin_bool(s:str):
    """convert binary representation '0b+' to boolean list
     
    Args:
        s (str): binary representation 
    Returns:
        (list of boolean): 
    
    Example:
        >>> s = '0b10'
        >>> y = [True, False]
    """
    # '0b10'は文字列で，eval('0b10')=2
    # 先頭の2文字'0b'を抜いた'10'はeval('10')=10
    s = s[2:]
    z = [bool(int(c)) for c in s]
    return z

def flatten(l:list):
    return [item for sublist in l for item in sublist]

def str_seq(message):
    booleanStr = str_bool(message)
    booleanSeq = flatten(booleanStr)
    return booleanSeq

def genPN(length:int,seed):
    import numpy as np
    rng = np.random.default_rng(seed)
    pn = rng.integers(2,size=(length,))
    return pn

def genPAIHv0(message:str,SecDuration:float,FreqSampling:float=44100,bps:float=10):
    """Generate Japanese Ambulance Siren (PeePoo) in PAIHv0.
    ピーポーサイレンのタイミング0.65[s]ごとにm倍音をgain(<0)[dB]で加える.
    ※ピーポーサイレンは，(Pee,Poo)=(970,780)[Hz], それぞれ0.65[s]交替
    mはペイロードビットに従って以下のように決める．
    '0' -> 1/2
    '1' -> 2
    """
    import numpy as np
    PeePooTime:float = 0.65 #仮のPeePoo長[s]
    PeePooHz = {'Pee':970,'Poo':780}
    WatGain = 0.5
    payload = str_seq(message) # 固定 ペイロード長

    # (eq1) N = bps*PeePooTime [bit]　が整数（Pee1つに入るbit数が整数）ならば，
    # (eq2) L = (PeePooTime*FreqSampling [sample]) // N 
    #   = FreqSampling/bps が　1ビット埋め込みあたりのフレーム長[sample] 
    # eq1からNを求め，
    # (eq2)から　L= FreqSampling*PeePooTime/N　が整数となるようにLを求め，
    # Pee1つのフレーム長[sample] M = PeePooTime*FreqSampling=L*Nを求める
    # bps = N/PeePooTIme = N/(M/FreqSampling) = N*FreqSampling/M  (実数)とfix
    #
    N:int = max((bps * PeePooTime)//1,1) ##
    #
    L:int = (FreqSampling * PeePooTime)//N 
    #
    PeePoo_frame:int = (L*N)//1
    # fix bps
    fixed_bps = N*FreqSampling/PeePoo_frame
    print('bps fixed:',bps,'->',fixed_bps)
    bps = fixed_bps
    
    Code_frame:int = FreqSampling//bps 

    # 埋め込み処理が行われるサンプル数と指定された秒数サンプル数とを比べる
    len_fromEmbed = len(payload)*Code_frame
    len_fromDuration = (SecDuration*FreqSampling)//1
    if len_fromEmbed > len_fromDuration:
        print(bpsを下げるかdurationを長くしてください)
    else:
        rep = int(np.ceil(len_fromDuration/len_fromEmbed))
        payload = payload*rep
    
    # Time, origHz, payload, stegHz のdataframeを作る
    # origHz = {0:Pee,1:Poo}
    # paylaod = {0,1}
    # stegHz = origHz+payload = {00,01,10,11}
    # 00~11の4種類の信号を作り，切り替わるタイミングで振幅クロスフェード
    initOrigPhase=0
    initWatPhase=np.pi/2
    orig = np.zeros(len_fromDuration,)
    orig_c = np.zeros(len_fromDuration,)
    wat = np.zeros(len_fromDuration,)
    wat_c = np.zeros(len_fromDuration,)
    for i in range(len_fromDuration):
        if i == 0: 
            # 初期位相を決めるsin,cos値
            orig[i] = np.sin(initOrigPhase)
            orig_c[i] = np.cos(initOrigPhase)
            wat[i] = WatGain*np.sin(initWatPhase)
            wat_c[i] = WatGain*np.cos(initWatPhase)
        else:
            if i%(2*PeePoo_frame) < PeePoo_frame: # Pee
                origFreq = PeePooHz['Pee']
            else: # Poo
                origFreq = PeePooHz['Poo']

            code = payload[int(i//Code_frame)]
            if code == 0:
                watFreq = 2*origFreq
            else:
                watFreq = 1/2*origFreq
        
            orig[i] = np.sin(2*np.pi*origFreq/FreqSampling + np.arctan2(orig[i-1],orig_c[i-1]))
            orig_c[i] = np.cos(2*np.pi*origFreq/FreqSampling + np.arctan2(orig[i-1],orig_c[i-1]))

            wat[i] = WatGain * np.sin(2*np.pi*watFreq/FreqSampling + np.arctan2(wat[i-1]/WatGain,wat_c[i-1]/WatGain))
            wat_c[i] = WatGain * np.cos(2*np.pi*watFreq/FreqSampling + np.arctan2(wat[i-1]/WatGain,wat_c[i-1]/WatGain))
    
    steg = orig+wat
    return steg,Code_frame

def decPAIHv0(steg,Code_frame):
    len_steg = len(steg)

    i_start = 0
    while i_start < len_steg:
        i = int(i_start/Code_frame)
        i_end = min(i_start + Code_frame,len_steg)
        len_frame = i_end-i_start         
        x = steg[i_start:i_end]
        xx = fft.rfft(x)
        f0,k = max(xx)
        if xx[int(2*k)] > xx[int(k/2)]:
            code[i] = 0
        else:
            code[i] = 1
    
    # reshape 8bit list
    code = code.reshape((-1,8))
    
    # bool_str :bool-8bit to str

    # return message


"""
新手法アイデア：あるスペクトルを同じ聞こえ方のするスペクトルに変換
- Bark聴覚フィルタ内に実数倍音を加える．
def  
"""

