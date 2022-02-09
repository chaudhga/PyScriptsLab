from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('ImgTrain/Orig1.jpg')
wm = 'WeBank.com By GC'
bwm1.read_wm(wm, mode='str')
bwm1.embed('ImgTrain/embedded.png')
len_wm = len(bwm1.wm_bit)
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))


wm_extract = bwm1.extract('ImgTrain/wmgc.jpg', wm_shape=len_wm, mode='str')
print(wm_extract)
