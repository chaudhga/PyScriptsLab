import os
import time

from PIL import Image
import imagehash
import blockhash
import blockhash.core



ERICS_SAMPLE = "ImgTrain/Eric_blur.jpg"
ERICS_ORIG = "ImgTrain/Master/2492.jpg"
ERICS_SIMILAR = "ImgTrain/Master/5554.jpg"

GC_ORIG = "ImgTrain/Orig1.jpg"
GC_SAMPLE = "ImgQuery/PC_Crop.jpg"
GC_SAMPLE = "ImgQuery/PC_Phone.jpg"

ihashtable = []

def calculate_hashes(img, hash_funcs=[imagehash.phash, imagehash.average_hash, imagehash.dhash, imagehash.colorhash,
                                      imagehash.whash]):
    hashes = []
    for hash_func in hash_funcs:
        hashes.append(hash_func(Image.open(img)))
    return hashes

# def print_hashes(img1=ERICS_SAMPLE, img2=ERICS_ORIG, img3=ERICS_SIMILAR, hash_func = imagehash.phash):
#     hash1 = hash_func(Image.open(img1))
#     hash2 = hash_func(Image.open(img2))
#     hash3 = hash_func(Image.open(img3))
#     print(hash1)
#     print(hash2)
#     print(hash3)
#     if hash_func != imagehash.crop_resistant_hash:
#         print(hash1 - hash2)
#         print(hash1 - hash3)
    # else:
    #     img2_matches = 0
    #     img3_matches = 0
    #     for i in hash1:
    #         for j in hash2:
    #             if i == j:
    #                 print(j)
    #                 img2_matches += 1
    #         for k in hash3:
    #             if i == k:
    #                 print(k)
    #                 img3_matches += 1
    #     print("matches")
    #     print(img2_matches)
    #     print(img3_matches)


# print("--- Average Hash ---")
# print_hashes(hash_func=imagehash.average_hash)
# print("--- Perceptual Hash ---")
# print_hashes(hash_func=imagehash.phash)
# print("--- Color Hash ---")
# print_hashes(hash_func=imagehash.colorhash)
# print("--- Wavelet Hash ---")
# print_hashes(hash_func=imagehash.colorhash)
# print("--- Diff Hash ---")
# print_hashes(hash_func=imagehash.dhash)
# print("--- Crop Resistant Hash ---")
# print_hashes(hash_func=imagehash.crop_resistant_hash)

def build_ihash_table(path):
    myList = os.listdir(path)
    print('Total Images Detected', len(myList))

    phashtable = {}
    dhashtable = {}
    ahashtable = {}
    chashtable = {}
    whashtable = {}

    for img in myList:
        imagename = os.path.splitext(img)[0]
        hashes = calculate_hashes(f'{path}/{img}')
        if hashes[0] not in phashtable:
            phashtable[hashes[0]] = list()
        phashtable[hashes[0]].extend(imagename)

        if hashes[1] not in ahashtable:
            ahashtable[hashes[1]] = list()
        ahashtable[hashes[1]].extend(imagename)

        if hashes[2] not in dhashtable:
            dhashtable[hashes[2]] = list()
        dhashtable[hashes[2]].extend(imagename)

        if hashes[3] not in chashtable:
            chashtable[hashes[3]] = list()
        chashtable[hashes[3]].extend(imagename)

        if hashes[4] not in whashtable:
            whashtable[hashes[4]] = list()
        whashtable[hashes[4]].extend(imagename)

    ihashtable.extend((phashtable, ahashtable, dhashtable, chashtable, whashtable))

    print(len(phashtable), len(phashtable.values()))
    print(len(ahashtable), len(ahashtable.values()))
    print(len(dhashtable), len(dhashtable.values()))
    print(len(chashtable), len(chashtable.values()))
    print(len(whashtable), len(whashtable.values()))


def match_hash(qhash, htable):
    match = []
    distance = {}
    if qhash in htable:
        return match.append(htable[qhash]), True
    else:
        min_dist = 999
        print("keys in htable:", len(htable.keys()))
        for hkey in htable.keys():
            dist = qhash - hkey
            distance.update({hkey: dist})
            # print("current dist", dist)
            if min_dist >= dist:
                match.extend(htable[hkey])
                min_dist = dist
        return match, False


def find_image(img):
    query_hash = calculate_hashes(img)
    print('Hashes of Query Image:', query_hash)

    for i in range(len(ihashtable)):
        hdict = {}
        hdict = ihashtable[i]
        print("--- Method", i)
        print(len(hdict))
        print("matching ", query_hash[i])
        matches, found = match_hash(query_hash[i], hdict)
        if found:
            print("--- Exact matches:", matches)
        else:
            print("--- Possible matches:", matches)


print("---building hash table ---")
start_time = time.time()
# build_ihash_table('ImgTrain/Sample')
print("---Hash table generation took %s seconds ---" % (time.time() - start_time))
print("---searching image ---")
start_time = time.time()
# find_image('ImgTrain/Eric_blur.jpg')
img = Image.open('ImgTrain/Erics.jpg')
img1 = Image.open('ImgTrain/Master/5554.jpg')
img2 = Image.open('ImgTrain/Master/2492.jpg')
img3 = Image.open('ImgTrain/Orig1.jpg')
w, h = img.size
w1, h1 = img1.size
print(w, h, w1, h1)
qhash = imagehash.dhash(img)
# hash1 = blockhash.core.blockhash(img,8)
# hash2 = blockhash.core.blockhash(img1,8)
# print(hash1)
# print(hash2)

ph1 = imagehash.average_hash(img)
ph2 = imagehash.average_hash(img1)
ph3 = imagehash.average_hash(img2)
ph4 = imagehash.average_hash(img3)
print(ph1)
print(ph2)
print(ph3)
print(ph4)

print(ph2 - ph1)
print(ph3 - ph1)
# print(ph3 - ph2)
print(ph4 - ph1)

print("---Image search took %s seconds ---" % (time.time() - start_time))

# hash1a = imagehash.average_hash(Image.open(ERICS_ORIG))
# hash2a = imagehash.average_hash(Image.open(ERICS_SAMPLE))
# hash3a = imagehash.average_hash(Image.open(ERICS_SIMILAR))
# print("Erics Original:", hash1a)
# print("Erics Profile:", hash2a)
# print("Erics Profile:", hash3a)
#
# print("--- Perceptual Hash ---")
# hash1p = imagehash.phash(Image.open(ERICS_ORIG))
# hash2p = imagehash.phash(Image.open(ERICS_SAMPLE))
# print("Erics Original:", hash1p)
# print("Erics Profile:", hash2p)
#
# print("--- Color Hash ---")
# hash1clr = imagehash.colorhash(Image.open(ERICS_ORIG))
# hash2clr = imagehash.colorhash(Image.open(ERICS_SAMPLE))
# print("Erics Original:", hash1clr)
# print("Erics Profile:", hash2clr)
#
# print("--- Wavelet Hash ---")
# hash1w = imagehash.whash(Image.open(ERICS_ORIG))
# hash2w = imagehash.whash(Image.open(ERICS_SAMPLE))
# print("Erics Original:", hash1w)
# print("Erics Profile:", hash2w)
#
# print("--- Diff Hash ---")
# hash1d = imagehash.dhash(Image.open(ERICS_ORIG))
# hash2d = imagehash.dhash(Image.open(ERICS_SAMPLE))
# print("Erics Original:", hash1d)
# print("Erics Profile:", hash2d)
#
# print("--- Crop Resistant Hash ---")
# hash1crp = imagehash.crop_resistant_hash(Image.open(ERICS_ORIG))
# hash2crp = imagehash.crop_resistant_hash(Image.open(ERICS_SAMPLE))
# print("Erics Original:", hash1crp)
# print("Erics Profile:", hash2crp)

