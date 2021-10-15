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
    booleanStr = str_bool(str)
    booleanSeq = flatten(booleanStr)
    return booleanSeq

def genPN(length:int,seed):
    import numpy as np
    rng = np.random.default_rng(seed)
    pn = rng.integers(2,size=(length,))
    return pn

def genPAIHv0(message,SecDuration,FreqSampling=44100,bps=10):
    """Generate Japanese Ambulance Siren (PeePoo) in PAIHv0.
    ピーポーサイレンのタイミング0.65[s]ごとにm倍音をgain(<0)[dB]で加える.
    ※ピーポーサイレンは，(Pee,Poo)=(970,780)[Hz], それぞれ0.65[s]交替
    mはペイロードビットに従って以下のように決める．
    '0' -> 1/2
    '1' -> 2
    """
    import numpy as np
    # bps : 仮のbps[bit/s]
    PeePooTime = 0.65 #仮のPeePoo長[s]
    paiload = str_seq(message) @# 固定 ペイロード長

    # (eq1) N = bps*PeePooTime [bit]　が整数（Pee1つに入るbit数が整数）ならば，
    # (eq2) L = (PeePooTime*FreqSampling [sample]) // N 
    #   = FreqSampling/bps が　1ビット埋め込みあたりのフレーム長[sample] 
    # eq1からNを求め，
    # (eq2)から　L= FreqSampling*PeePooTime/N　が整数となるようにLを求め，
    # Pee1つのフレーム長[sample] M = PeePooTime*FreqSampling=L*Nを求める
    # bps = N/PeePooTIme = N/(M/FreqSampling) = N*FreqSampling/M  (実数)とfix
    bps = (np.round(bps*PeePooTime))//PeePooTime


    # 埋め込未処理が行われるサンプル数と指定された秒数サンプル数とを比べる
    len_fromEmbed = length(paiload)*len_frame
    len_fromDuration = (SecDuration*FreqSampling)//1
    if len_fromEmbed > len_fromDuration:
        print(bpsを下げるかdurationを長くしてください)
    


"""
新手法アイデア：あるスペクトルを同じ聞こえ方のするスペクトルに変換
- Bark聴覚フィルタ内に実数倍音を加える．
def  
"""