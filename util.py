import reedsolo
from qrcodegen import QrCode
import contentspace

_hamming = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3,
       4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4,
       4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2, 2, 3, 2,
       3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5,
       4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4,
       5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3,
       3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2,
       3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6,
       4, 5, 5, 6, 5, 6, 6, 7, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5,
       6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 3, 4, 4, 5, 4, 5,
       5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6,
       7, 7, 8]
codesperversion = [19,34,55,80,108,136,156,194,232,274,324,370,428,461,523,589,647,721,795,861,932,1006,1094,1174,1276,1370,1468,1531,1631,1735,1843,1955,2071,2191,2306,2434,2566,2702,2812,2956]
pads = [236,17]
version = 3
errblocks = 15
stringy = 'https://en.wikipedia.org/wiki/QR_code'
# given two equally sized lists of integers in [0,255], compute the hamming distance 
def hamming_dist(l1, l2):
    sum = 0
    for i in range(len(l1)):
        sum += _hamming[l1[i] ^ l2[i]]
    return sum

def xored(l1, l2):
    l = list(l1)
    for i in range(len(l1)):
        l[i] ^= l2[i]
    return l

def str_to_qr(string):
    if(len(string) > 255):
        print("not sure what to do with this yet")
        return None
    # a cheap hack
    wrapped = list(bytes.fromhex('4{:02x}{:s}0'.format(len(string), string.encode('utf-8').hex())))
    need = codesperversion[version-1]-len(wrapped)
    for i in range(need):
        wrapped.append(pads[i%2])
    return bytearray(wrapped)

def qr_to_str(qr):
    return bytes.fromhex(qr.hex()[3:-1].strip())


def encode(data, nerr):
    return reedsolo.rs_encode_msg(data, nerr)

def qr_dist_same(str1, str2, nerr):
    s1 = list(encode(str_to_qr(str1), nerr))
    s2 = list(encode(str_to_qr(str2), nerr))
    return hamming_dist(s1, s2), xored(s1, s2), s1,  s2

def optimal_change(s1, s2, tochange, j):
    hammingdists = list(tochange)
    for i in range(len(s1)):
        hammingdists[i] = _hamming[tochange[i]]
    hammingindices = sorted(range(len(hammingdists)), key = lambda k: hammingdists[k], reverse=True)
    s2c = list(s2)
    for i in range(j):
        s2c[hammingindices[i]] = s1[hammingindices[i]]
    return s2c

def test_against_caps_random(base_string, numerr, maxchanges, candidate_string, attempts):
    from random import choice
    s1 = list(encode(str_to_qr(base_string), numerr))
    best_str = candidate_string
    best_hamming = hamming_dist(s1, list(encode(str_to_qr(candidate_string), numerr)))
    for i in range(attempts):
        test_str = ''.join(choice((str.upper, str.lower))(c) for c in candidate_string)
        test_str_proc = list(encode(str_to_qr(test_str), numerr))
        test_str_best_ham = hamming_dist(s1,optimal_change(s1, test_str_proc, xored(s1, test_str_proc), maxchanges))
        if test_str_best_ham < best_hamming:
            best_str = test_str
            best_hamming = test_str_best_ham
    return best_str, best_hamming

def print_qr(qrcode: QrCode) -> None:
	"""Prints the given QrCode object to the console."""
	border = 4
	for y in range(-border, qrcode.get_size() + border):
		for x in range(-border, qrcode.get_size() + border):
			print("\u2588 "[1 if qrcode.get_module(x,y) else 0] * 2, end="")
		print()
	print()

reedsolo.init_tables(0x11d)


original_proc = list(encode(str_to_qr(stringy),errblocks))
def wrapped(original,new):
    new_proc = list(encode(str_to_qr(new),errblocks))
    return hamming_dist(original_proc,optimal_change(original_proc, new_proc, xored(original_proc, new_proc), errblocks//2))
beststr = contentspace.permute(stringy,wrapped)
message = bytearray(optimal_change(original_proc,list(encode(str_to_qr(beststr),errblocks)),xored(original_proc,list(encode(str_to_qr(beststr),errblocks))),errblocks//2))
#message = bytearray(original_proc)
#print(list(message))
qr = QrCode(3,QrCode.Ecc.LOW,message,msk=1)
print_qr(qr)

#print(test_against_caps_random('www.wikipedia.org', 7, 3, 'www.wikiwnjia.org', 10000))

#str_to_qr('www.wikipedia.org')
#ham, tochange, s1, s2 = qr_dist_same('www.wikipedia.org','www.wijipedaa.org', 7)
#j = 3
#s2c = optimal_change(s1,s2,tochange,j)
#rmes, recc, errata_pos = reedsolo.rs_correct_msg(s2c, 7)
#print(s1)
#print(s2)
#print(s2c)
#print("====")
#print(hamming_dist(s2c, s1))
#print(qr_to_str(rmes))
