import subprocess
import cv2
import numpy as np
import statistics
import math
import time

#from PIL import Image, ImageDraw



#画面録画
#fps = 30
# 録画する動画のフレームサイズ（webカメラと同じにする）
#size = (1920, 1080)
# 出力する動画ファイルの設定
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#video = cv2.VideoWriter('output.avi', fourcc, fps, size)


#mat = cv2.imread(r"C:\Users\mayuk\Documents\stolip.png")
#cv2.imshow("image", mat)
#cv2.waitKey()

#print("a")


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # カメラ画像の横幅を1920#1280に設定#646
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960) # カメラ画像の縦幅を1080720に設定#484


avg=None
bef_toplist = None
bef_ss=None

# 閾値の設定
#threshold = 100


p =1228800#921600 #2073600 #312664
#1280×960
wide=1280
#1280
high=960
#720
#p = 1228800


def reset_standard():
    global basetop
    global basetop2
    global avg

    avg = gray.copy().astype("float")

    base = np.asarray(avg)
    base = base.flatten()  # 元データ
    
    p = len(base)
    basedata = []  # 移動平均
    basetop = []  # 頂点位置
    
    for a in range(p):

        if a==0:
            now_sum=sum(base[0:3])
            d=now_sum/3
        elif a==1 or a==2:
            now_sum=bef_sum+base[a+2]
            d = now_sum/(a+3)            
        elif a==p-2 or a==p-1:
            now_sum=bef_sum-base[a-3]
            if a==p-2:
                d = now_sum/4
            else:
                d = now_sum/3
        else:
            now_sum=bef_sum-base[a-3]+base[a+2]
            d = now_sum/5

        basedata.append(d)
        bef_sum = now_sum

       
    #print("basedata")

    count = 1
    start = 0
    before = -999999
    trend = 0  # 上がっていたら１下がっていたら０     
    for e in range(p):
        now = basedata[e]
        if before == now:
            count += 1
        elif before > now:
            if trend == 1:
                if count > 1:
                    if (start+e-1)/2 >= 3 and (start+e-1)/2 <= (p-1)-3:
                        basetop.append(int((start+e-1)/2))#
                else:
                    if e-1 >= 3 and e-1 <= (p-1)-3:
                        basetop.append(e-1)
            trend = 0
            count = 1
            start = 0
        elif before < now and before >= 100:
            trend = 1
            count = 1
            start = e

        before = now
    
    #print("basetop")

    ql = []
    for q in range(len(basetop)-1):
        qq = basetop[q+1]-basetop[q]
        ql.append(qq)
        #print(set(ql))
        #print(sum(ql)/len(ql))
    #print("ql")
    basetop2 = basetop[::111]#79#50
    #print("basetop2")
    #print(len(basetop))


#t_range = sum(ql)/len(ql)
#if t_range % 2 == 0:
#t_range = t_range+1

#円は別
#color1 = np.array([255., 255., 255.])
#for tyouten in basetop[::100]:
#yy = int((tyouten//wide)+1)
#xx = int(tyouten-(wide*(yy-1)))
#print(xx,yy)
#cv2.circle(img=avg, center=(xx, yy), radius=5,color=color1, thickness=2, lineType=cv2.LINE_AA)

#avetopbase=np.average(basetop)
#pvabase = statistics.pvariance(basetop)

#ql = []
#qi = []
#for q in range(len(basetop2)-1):
#qq = basetop2[q+1]-basetop2[q]
#ql.append(qq)
#print(set(ql))
#print(sum(ql)/len(ql))


#print(basedata[0:101])
#print(basetop)
# #return

def searching_top():
    global toplist
    xrange = 7
    x = list(range(xrange))  # list(range(35))  # 15  xrange=int(t_range/2)
    toplist = []
    #print(p)
    p = len(data1)
    #print(p)
    #print("data1", len(data1))
    
    for top in basetop2:
        top=int(top)
        if top<=int(xrange/2):
            y = data1[:xrange]
        elif top >= (p-1)-int(xrange/2):  
            y = data1[(p-1)-(xrange-1):]  
            #print("x", len(x))
            #print("y", len(y))
        else:
            y = data1[top-int(xrange/2):top+int(xrange/2)+1]  # int(xrange/2),int(xrange/2)+1
        #print("x",x)
        #print("y",y)
        z = np.polyfit(x, y, 2)
        d = (-z[1]) / (2 * z[0])
    
        if top <= int(xrange/2):  # int(xrange/2)
            toplist.append(d)
        elif top >= (p-1)-int(xrange/2):  # int(xrange/2)
            toplist.append(d+(p-1)-xrange-1)  # xrange-1
        else:
            toplist.append(d+top-int(xrange/2))  # int(xrange/2)


count1 = 0
count2 = 0

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    key = cv2.waitKey(1)
    if key == ord('s'):
        reset_standard()
        color1 = np.array([255., 255., 255.])
        for tyouten in basetop2:  # basetop[::100]:
            yy = int((tyouten//wide)+1)
            xx = int(tyouten-(wide*(yy-1)))
            #print(xx,yy)
            cv2.circle(img=avg, center=(xx, yy), radius=5,color=color1, thickness=2, lineType=cv2.LINE_AA)
    
    if key == ord('b'):
        print("なし",count1,count2,count1/count2)
        print("吹いた")
        count1=0
        count2=0
    if key == ord('e'):
        print("止めた")
        print("あり",count1,count2,count1/count2)
        count1=0
        count2=0

    data1 = gray.copy().astype("float")
    data1 = np.asarray(data1)
    #print(data1)
    data1 = data1.flatten()  # 元データ
    #print(data1)

    # コントラストストレッチ
    #gray1 = cv2.equalizeHist(gray)

    # 二値化(閾値100を超えた画素を255にする。)
    #ret, gray2 = cv2頂点頂点hreshold(gray1, threshold, 255, cv2.THRESH_BINARY)
    # 細線化 THINNING_ZHANGSUEN
    #skeleton1 = cv2.ximgproc.thinning(gray2, thinningType=cv2.ximgproc.THINNING_GUOHALL )
    #skeleton1 = cv2.dilate(gray2, None, iterations=5)
    #skeleton1 = cv2.ximgproc.thinning(skeleton1, thinningType=cv2.ximgproc.THINNING_GUOHALL )

    # 前フレームを保存
  

    if avg is None:
        reset_standard()
        color1 = np.array([255., 255., 255.])

        for tyouten in basetop2:#basetop[::100]:
            yy = int((tyouten//wide)+1)
            xx = int(tyouten-(wide*(yy-1)))
            #print(xx,yy)
            cv2.circle(img=avg, center=(xx, yy), radius=5,color=color1, thickness=2, lineType=cv2.LINE_AA)
        continue

    searching_top()

    if bef_toplist is None:
        bef_toplist=toplist
        continue

    now_toplist=toplist
    

    #print(basedata)
    #print(basetop)
    #basetop2=basetop[::50]

    

    #print(toplist)
    
    #result = np.array(basetop)-np.array(toplist)
    #averesult = np.average(result)
    #pvaresult = statistics.pvariance(result)
    #print("result")
    #print(result)
    #print(sorted(result)[0:10])
    #print("averesult",averesult)
    #print("pvasesult",pvaresult)
    #print(sorted(result)[0:10])
    
    color2 = np.array([255., 255., 255.])
    sa_x=0
    sa_xx=0
    for iti in range(0,len(basetop2)):
        sa=bef_toplist[iti]-now_toplist[iti]
        sa_x+=sa
        sa_xx+=sa**2
        #print(basetop2[iti],toplist[iti])
        sa=int(abs(sa)*100)
        #print(sa)
        #print(sa)
        bt1=basetop2[iti]
        #print(sa)
        #if sa>=1.0:
        yy2 = int((bt1//wide)+1)
        xx2 = int(bt1-(wide*(yy2-1)))
        #print(xx2, yy2)
        if sa <10000:
            cv2.circle(img=gray, center=(xx2, yy2), radius=sa,color=color2, thickness=2, lineType=cv2.LINE_AA)

    #print(len(basetop2))#880
    try:
        sa_x2=(sa_x/len(basetop2))**2 #合計の平均の２乗
        sa_xx2=sa_xx/len(basetop2) #2乗合計の平均
        ss = sa_xx2-sa_x2
        if bef_ss == None:
            bef_ss = ss
        now_ss = ss
        #n=880,880
        #分子の自由度879,分母の自由度879
        #
        #パーセント点 
        #https://keisan.casio.jp/exec/system/1161228871
        #1%基準
        #1.17006201074148931468
        #0.1%基準
        #1.232087743495074646261
        #0.05%基準
        #1.248901820536719497381
        per = 1.2489

        if bef_ss >= now_ss:
            F = bef_ss/now_ss  # round(bef_ss/now_ss,5)
        else:
            F = now_ss/bef_ss #round(now_ss/bef_ss, 5)
            #a = round(2 / 3, 5)小数点第５位まで
        #print(F)
        if F>=2 or F=="inf":
            pass
        else:
            #print(F)
            count2 += 1
            if F > per:
                #print(F)
                #print("違う")
                count1+=1
    except:
        pass


    cv2.imshow("image2",  cv2.convertScaleAbs(avg))  # 前
    cv2.imshow("now", gray)  # 今

    bef_toplist=now_toplist
    bef_ss=now_ss


    time.sleep(0.01)

    if key == 27:
        break

    # 現在のフレームと移動平均との間の差を計算する
    # accumulateWeighted関数の第三引数は「どれくらいの早さで以前の画像を忘れるか」。小さければ小さいほど「最新の画像」を重視する。
    # http://opencv.jp/opencv-2svn/cpp/imgproc_motion_analysis_and_object_tracking.html
    # 小さくしないと前のフレームの残像が残る
    # 重みは蓄積し続ける。
    
    #cv2.imshow("image2",  cv2.convertScaleAbs(avg))#前

    #frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))#差
    #frameDelta_diff = cv2.absdiff(skeleton1, cv2.convertScaleAbs(avg))  # 差

    #alpha = 1000  # コントラスト項目
    #beta = 0    # 明るさ項目
    #frameDelta1 = cv2.convertScaleAbs(frameDelta, alpha=alpha, beta=beta)
    #cv2.accumulateWeighted(gray, avg, 0.9999)



    #cv2.imshow("image1", frameDelta1)#差
    #cv2.imshow("image2", avg)

    #cv2.imshow("now", gray)#今
    #cv2.imshow("Contrast_Stretch", gray1)#コントラストストレッチ
    #cv2.imshow("binarization", gray2)#2値化
    #cv2.imshow("fibrillation", skeleton1)# 細線化
    #cv2.imshow("diff", frameDelta_diff)#差
    
    #video.write(gray)  # 画面録画
    #key = cv2.waitKey(1)
    #if key == 27:
    #    break


#cap.release()
#video.release()
#cv2.destroyAllWindows()



#print(moving_average(data, 4))
