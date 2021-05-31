# -*- encoding: utf-8 -*-
'''
@File    :   qiangke.py
@Time    :   2021/02/25 14:17:18
@Author  :   Daniel-ChenJH
@Email   :   13760280318@163.com
@Version    :   2.0
@Descriptions :   Course-Bullying-in-SJTU
                    上海交通大学全自动抢课脚本,请保证已经安装了最新版本的Chrome浏览器（90.0.4430系列版本）
                    本程序支持准点开抢与抢课已经开始后持续捡漏两种模式。
'''

# The imported libs: 
from selenium import webdriver
from time import sleep,strftime,localtime
from PIL import Image
from pytesseract import image_to_string
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from pytesseract.pytesseract import TesseractNotFoundError
from os import remove, path
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import sys
import signal

# 检测程序异常终止
def signal_handling(signum,frame):
    print('\n')
    print('******************************')
    print ("程序被使用者终止。")    
    print('******************************')
    print('\n')
    sys.exit()

# 将输出同时写入到log文件
class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a+",encoding='utf-8')
 
    def write(self, message):
        if message[0]=='\n':
            self.terminal.write(message)
            self.log.write(message)
        else:
            self.terminal.write('['+datetime.datetime.now().strftime('%H:%M:%S')+'] '+message)
            self.log.write('['+datetime.datetime.now().strftime('%H:%M:%S')+'] '+message)
        self.flush() #每次写入后刷新到文件中，防止程序意外结束
    def flush(self):
        self.log.flush()
 
def quitting():
    print("\nPlease 'Star' the program of Daniel-ChenJH on Github if you think it's a quite good one. ")
    print('\nLink to \'Course-Bullying-in-SJTU\' in Github : https://github.com/Daniel-ChenJH/Course-Bullying-in-SJTU')
    my_file = 'button.png' # 文件路径
    if path.exists(my_file): # 如果文件存在
        remove(my_file) # 则删除
    print('\n')
    input('程序已完成！请立即自行移步至教学信息服务网 https://i.sjtu.edu.cn 查询确认抢课结果！\n\n回车键退出程序……')


def simulater(mode,on_time,kechengs,class_type,account_name,account_password,times):
    start_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

    option = webdriver.ChromeOptions()

    # 无头模式；采用有头模式时将bili调成当前电脑屏幕的缩放比例（1、1.25、1.5或2），并注释掉50~52行
    bili=1
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
    driver = webdriver.Chrome(options=option,executable_path=r'chromedriver.exe')
    driver.set_page_load_timeout(5)
    try:
        driver.get('https://i.sjtu.edu.cn/')
        driver.maximize_window()    
        login = WebDriverWait(driver,2,0.1).until(lambda x:driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/form/div[6]/div/a/img') )
        login.click()
    except TimeoutException:
        driver.execute_script('window.stop()')

    driver.switch_to.default_content()
    flag,flag2=True,True
    count=1
    while(flag):
        try:
            name=driver.find_element_by_xpath('//*[@id="user"]')
            name.clear()
            name.send_keys(account_name)
            password=driver.find_element_by_xpath('//*[@id="pass"]')
            password.clear()
            password.send_keys(account_password)
            
            if flag2:       #如果pytesseract没有问题
                
                captcha=driver.find_element_by_xpath('//*[@id="captcha-img"]')
                photoname='button.png'
                driver.save_screenshot(photoname)

                left = captcha.location['x']*bili
                top = captcha.location['y']*bili
                right = left + captcha.size['width']*bili
                bottom = top + captcha.size['height']*bili

                im = Image.open(photoname)
                im = im.crop((left, top, right, bottom))
                gray = im.convert('L')
                threshold = 180
                table = []
                for i in range(256):
                    if i < threshold:
                        table.append(0)
                    else:
                        table.append(1)
                out = gray.point(table, '1')
                out.save(photoname)
                cap=image_to_string(out)
                captcha=driver.find_element_by_xpath('//*[@id="captcha"]')
                captcha.clear()
                captcha.send_keys(str(cap.strip()))
            else:
                captcha=driver.find_element_by_xpath('//*[@id="captcha"]')
                captcha.clear()
                captcha.send_keys(hand_cap.strip())
            driver.find_element_by_xpath('//*[@id="submit-button"]').click()
            driver.switch_to.default_content()
            lanmu=driver.find_element_by_xpath('/html/body/div[3]/div/nav/ul/li[3]/a') # 用来确保登陆成功
            flag=False
            print('登录成功！\n')
        except TimeoutException:
            driver.refresh()
            driver.switch_to.default_content()
            try:
                lanmu=driver.find_element_by_xpath('/html/body/div[3]/div/nav/ul/li[3]/a') # 用来确保登陆成功
                flag=False
                print('登录成功！\n')      
            except NoSuchElementException:
                flag=True
        
        except TesseractNotFoundError:
            print('There is something wrong with your tesseract')
            print('The captcha can be seen from file: \'button.png\', please type in the captcha: ')
            hand_cap=input('hand_cap=')
            flag2=False
        except NoSuchElementException:
            print('验证码自动识别错误或jaccount信息输入错误，正在尝试第'+str(count+1)+'次...')
            count+=1
            if count%3==0:
                driver.refresh()
                try:
                    captcha = WebDriverWait(driver,3,0.1).until(lambda x:driver.find_element_by_xpath('//*[@id="captcha"]'))
                except TimeoutException:
                    driver.execute_script('window.stop()')

                driver.switch_to.default_content()
            if count>=12:
                driver.quit()
                print('\n大概率是您的jaccount信息输入错误，请检查并修改后重试...')
                quitting()
                return
        except ElementNotInteractableException:
            try:
                driver.refresh()
                sleep(3)
            except TimeoutException:
                driver.execute_script('window.stop()')
            driver.switch_to.default_content()

    origin= driver.current_window_handle
    driver.implicitly_wait(5)
    
    # 准点开抢模式，阻塞程序
    if mode==1:
        while True:
            now_time=datetime.datetime.now()
            if now_time<on_time and int((on_time-now_time).seconds)>2:
                print('未到设定的抢课开放时间，程序等待中')
                if int((on_time-now_time).seconds)>60:
                    sleep(60) 
                elif int((on_time-now_time).seconds)>10:
                    sleep(10)
                else:sleep(2)     
            else:
                if now_time>=on_time:break   
    
    print('程序开始抢课！\n')

    failcount=0
    # 点击下拉栏尝试进入选课页面
    while failcount<50:
        try:
            for j in range(len(kechengs)):
                now=driver.window_handles
                driver.find_element_by_xpath('/html/body/div[3]/div/nav/ul/li[3]/a').click()
                driver.find_element_by_xpath('/html/body/div[3]/div/nav/ul/li[3]/ul/li[3]/a').click()
                WebDriverWait(driver, 2, 0.05).until(EC.new_window_is_opened(now))
            all_window_handles = driver.window_handles
            k=0
            stat={}
            # 此时已经进入选课界面
            for handle in all_window_handles:
                if handle !=origin:
                    stat[handle]=[0,k]
                    k+=1                    
            
            print('持续查询刷新中......')
            # 开始查询刷新
            for q in range(times):
                # 添加状态记录字典 

                temp=list(stat.values())
                st=[]

                for t in range(len(temp)):
                    st.append(temp[t][0])
                if 0 not in st:break    #所有课程都抢课完成

                for handle in all_window_handles:
                    if handle!=origin and stat[handle][0]==0:
                        driver.switch_to.window(handle)
                        if q==0:
                            classfind=False
                            try:
                                inp = WebDriverWait(driver,1,0.1).until(lambda x:driver.find_element_by_xpath('//*[@id="searchBox"]/div/div[1]/div/div/div/div/input') )
                                inp.clear()
                                inp.send_keys(kechengs[stat[handle][1]])
                                go=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/span/button[1]')
                                go.click()

                                typebox=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/ul')
                                types=typebox.find_elements_by_tag_name('a')
                            except NoSuchElementException as e:
                                unavailable=driver.find_element_by_xpath('//*[@id="innerContainer"]/div[4]/div[2]/div/span')
                                if unavailable.is_displayed():
                                    print('\n')
                                    print('程序错误，当前不属于选课阶段，请自行确认抢课开放时间。')
                                    driver.quit()
                                    quitting()
                                    return
                                else:
                                    print('程序好像出现了一些问题……')
                                    print(e)
                                
                            for type in types:
                                if class_type[stat[handle][1]] in type.text:
                                    type.click()
                                    classfind=True
                                    break
                            if not classfind:
                                print(kechengs[stat[handle][1]]+' 的用户指定类别：'+class_type[stat[handle][1]]+'不存在，将跳过此门课程；请检查确认无误后重新运行程序')
                                stat[handle][0]=3
                                continue

                        loc = (By.XPATH, '//html/body/div[1]/div/div/div[5]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[15]')
                        try:
                            WebDriverWait(driver,1,0.1).until(EC.visibility_of_element_located(loc))
                        except TimeoutException:pass
                        driver.implicitly_wait(0.5)
                        
                        # 刷新次数达到500时重启程序
                        if (q+1)%500==0:
                            driver.refresh()
                            sleep(1)
                            driver.implicitly_wait(5)
                            inp=driver.find_element_by_xpath('//*[@id="searchBox"]/div/div[1]/div/div/div/div/input')
                            inp.clear()
                            inp.send_keys(kechengs[stat[handle][1]])
                            
                            # 查询按钮
                            go=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/span/button[1]')
                            go.click()
                            sleep(0.3)
                            typebox=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/ul')
                            types=typebox.find_elements_by_tag_name('a')
                            for type in types:
                                if class_type[stat[handle][1]] in type.text:
                                    type.click()
                                    loc = (By.XPATH, '//html/body/div[1]/div/div/div[5]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[21]')
                                    sleep(1.5)
                                    driver.implicitly_wait(5)
                                    break
                                    
                        rongliang=10+len(driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[5]/div/div[2]/div[1]/div[2]/table/thead/tr/th"))
                        status=driver.find_element_by_xpath('//html/body/div[1]/div/div/div[5]/div/div[2]/div[1]/div[2]/table/tbody/tr/td['+str(rongliang)+']')
                        if status.is_displayed():
                            # 显示已满
                            print(str(kechengs[stat[handle][1]])+'  try_time== '+str(q+1)+' failed '+status.text)
                            go=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/span/button[1]')
                            go.click()
                        else:
                            try:
                                temp=WebDriverWait(driver,1, 0.1).until(lambda driver: driver.find_element_by_xpath('//*[@id="contentBox"]//button'))
                                sleep(0.2)
                                if temp.text!='退选': 
                                    # print(temp.text)
                                    temp.click()
                                    temp2=WebDriverWait(driver,1, 0.1).until(lambda driver: driver.find_element_by_xpath('//*[@id="contentBox"]//button'))
                                    sleep(0.2)
                                    try:
                                        if temp2.text=='退选': 
                                            print('================================ '+str(kechengs[stat[handle][1]])+' , Success! try_time== '+str(q+1)+' ========================\n')
                                            stat[handle][0]=1
                                        else:
                                            print('好像抢课程：'+str(kechengs[stat[handle][1]])+'中出现了些什么问题……请自行登录网站尝试抢课，并对照文件\'readme.txt\'确保无误后再次尝试运行程序!')
                                            stat[handle][0]=3
                                    except:
                                        print('好像抢课程：'+str(kechengs[stat[handle][1]])+'中出现了些什么问题……请自行登录网站尝试抢课，并对照文件\'readme.txt\'确保无误后再次尝试运行程序!')
                                        stat[handle][0]=3
                                else :
                                    print('你已经选上这门课了！'+str(kechengs[stat[handle][1]]))
                                    stat[handle][0]=2
                                all_window_handles=driver.window_handles
                            except Exception as e:
                                print(str(kechengs[stat[handle][1]])+' try_time== '+str(q+1)+' failed '+status.text)
                                print('failed because of :'+str(e)+' Retrying!')
            if False not in st:break
        except Exception as e:
            failcount+=1
            print('程序第'+str(failcount)+'次异常，异常原因：'+str(e)+' 重试中...')
            all_window_handles = driver.window_handles
            for handle in all_window_handles:
                if handle !=origin:
                    driver.switch_to.window(handle)
                    driver.implicitly_wait(0.5)
                    driver.close()
            driver.switch_to.window(origin)
            driver.implicitly_wait(0.5)
            sleep(0.5)       

    if failcount==20:print('好像出了些什么问题,也可能是网站服务器问题……请自行登录网站尝试抢课，并对照文件\'readme.txt\'确保无误后再次尝试运行程序!\n')
    print('ended!\n\n抢课结果:\n\n成功：')
    for k in range(len(kechengs)):
        if stat[all_window_handles[k+1]][0]==1:
            print(kechengs[k]+'成功，程序成功抢课!')
        elif stat[all_window_handles[k+1]][0]==2:
            print(kechengs[k]+'成功，你之前已经选好这门课了!')

    print('\n失败：')
    for k in range(len(kechengs)):       
        if stat[all_window_handles[k+1]][0]==3:
            print(kechengs[k]+'失败，抢课中遇到了一些问题，请自行尝试抢这门课!')
        elif stat[all_window_handles[k+1]][0]==0:
            print(kechengs[k]+'失败，直到程序终止都没能抢到此门课!')    
    end_time=strftime("%Y-%m-%d %H:%M:%S", localtime())

    print('\n')
    print('Start time: '+start_time)
    print('End time: '+end_time)
    driver.quit()

    quitting()
    


if __name__ == '__main__':
    print("\n\nCourse-Bullying-in-SJTU: an On-Time Automatic Class Snatching System\n\nAuthor:\t@Daniel-ChenJH (email address: 13760280318@163.com)\nFirst Published on Februry 25th, 2021 , revised for v2.0 on May 24th, 2021.\n")
    print('\nPlease read file \'readme.txt\' carefully and then edit file \'account.txt\' before running the program!!!\n')
    print('The efficiency of this program depend on your network environment and your PC\'s capability.')
    
    # 检测程序是否异常终止
    signal.signal(signal.SIGINT,signal_handling)

    now_time = datetime.datetime.now()

    # 用户输入读取
    data = []
    for line in open("account.txt","r",encoding='utf-8'):
        data.append(line)               

    mode=int(data[0].strip())
    if mode==1:on_time=datetime.datetime.strptime(data[1].strip(),'%Y-%m-%d %H:%M:%S')
    else:on_time=datetime.datetime.strptime('2000-10-11 04:30:00','%Y-%m-%d %H:%M:%S')

    times=int(data[2].strip())
    account_name=data[3].strip()
    account_password=data[4].strip()
    dataline=5

    # 提升修改jaccount信息
    if account_name=='your_jaccount_id_here' or account_password=='your_jaccount_password_here':
        print('请先修改jaccount信息，再运行程序！')
        sys.exit(0)

    kechengs=[]
    class_type=[]
    for line in data[dataline:]:
        if ',' in line.strip():
            kechengs.append(line.strip().split(',')[0])
            class_type.append(line.strip().split(',')[1])
        elif ' ' in line.strip():
            kechengs.append(line.strip().split(' ')[0])
            class_type.append(line.strip().split(' ')[1])
        elif '，' in line.strip():
            kechengs.append(line.strip().split('，')[0])
            class_type.append(line.strip().split('，')[1])

    sys.stdout = Logger("qiangke_log_file.txt")
    #会同时在控制台输出和写入“log_file.txt”文件中
    print('\n')
    print('\n====================================\nStarting progress in '+now_time.strftime('%Y-%m-%d %H:%M:%S')+' :\n====================================\n')
    print('Welcome, '+account_name+'!')
    # print('Welcome, ******** !')
    print('\n')
    if mode==1:
        print('抢课模式：1.准点开抢\t抢课开始时间设定为：'+on_time.strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print('抢课模式：2.持续捡漏')

    print('目标课程：')
    print(kechengs)
    simulater(mode,on_time,kechengs,class_type,account_name,account_password,times)