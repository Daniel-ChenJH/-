# Welcome to Course-Bullying-in-SJTU-v3.1！

## 2021/6/8 紧急更新v3.1 更新说明

1. 为了更好地保护用户隐私，将原来用户名+密码的登录方式改为微信扫二维码+cookie登录方式，**不再需要配置使用pytesseract**。在使用扫码登录模式时，请稍等，二维码将马上弹出。**请在20秒内完成扫码确认，20秒后程序将继续运行**。当距离本地保存的cookie的过期时间不足2小时时，需要重新扫码登录。**因此，用户文件'account.txt'中有关用户名和密码的两行请完全删去。写法例子可见下文。**
2. 对代码进行了优化，稍稍降低了代码运行速度，对各个模式都进行了优化，对模式3的退课环节增加多重保险。针对服务器不稳定时的代码策略进行了优化，提升了程序鲁棒性。
3. 对模式3的**补充说明**：
   1. 当教学信息服务网短时间内流量过大时，会导致服务器出现问题，比如一直加载但上不去、404、Service Unavailable等报错。这种是服务器端的问题，脚本也无能为力。因此，在抢课准点开放时，脚本使用的效率不能保证，强烈建议您同时手动抢课尝试。
   2. **在学校服务器压力较大时段，不建议使用模式3**。模式3带有退课功能，如果因为服务器不稳定而给脚本返回了错误的结果，可能会导致脚本退掉原本已经选上的课，并且没有能选上目标课程。相反，模式1、模式2均为只选不退，因此没有类似风险。
   3. 由于模式3的特殊性以及网页刷新需要一定的加载时间，有可能出现查询到课程A有空余名额，立即前往退掉课程B，返回尝试选课程A时发现已经被人捷足先登的情况。这种情况下，不仅B被退掉了，而且A也没选上。
   4. 由于模式3的特殊性，建议运行模式3时请勿离开，并定时关注程序运行情况。**若有退课行为，建议立即前往教学信息服务网确认。**
   5. **本程序致力于给各用户带来更好的用户体验，也将对其中出现的问题进行优化。模式3目前在本人的电脑上运行正常。但是，考虑到模式3的特殊性以及个人网络环境、电脑配置等方面的差异性，对于模式3的潜在用户，本程序不对其行为及脚本运行结果负任何责任。运行模式3的用户将被默认为对此补充说明已知悉。**

# 模式介绍

## 模式1：准点开抢

**用于准点开放抢课。**

由用户指定开抢的时间，格式为'%Y-%m-%d %H:%M:%S'。范例如：2021-05-24 17:35:20 。考虑到本程序登录系统需要时间，请在抢课开放前提前约30秒至1分钟即开始运行本程序。

有关用户文件 'account.txt'：第一行为模式选择，此处为模式1；第二行为抢课开始时间；第三行为最大尝试抢课次数；第四行及以后为所需要抢选的课程，行与行依次排列，行内同时指定课程名称及所属类型，并以',' 或 '，'隔开。

下面是文件 'account.txt'的一个很好的例子:

1
2021-05-24 17:35:20
1000
(2021-2022-1)-EE234-2，主修课程
世界民族音乐鉴赏，通识课

## 模式2：持续捡漏

**用于抢课已经开放后持续查询。**

有关用户文件 'account.txt'：第一行为模式选择，此处为模式2；第二行为抢课开始时间，模式2不需要指定此时间，在此无论写下什么都不会影响程序运行，留空此行也可以（但绝对不可删去此行，会导致用户数据读入出错）；第三行为最大尝试抢课次数；第四行及以后为所需要抢选的课程，行与行依次排列，行内同时指定课程名称及所属类型，并以',' 或 '，'隔开。

下面是文件 'account.txt'的一个很好的例子:

2
2021-05-24 17:35:20
1000
(2021-2022-1)-EE234-2，主修课程
世界民族音乐鉴赏，通识课

## 模式3：替换抢课

**注意！此处课程写法有关键变化！注意！此处课程写法有关键变化！注意！此处课程写法有关键变化！！！！**

**为了保险，模式三只支持课号查询！请先确定需要替换的即被替换的课程课号，并确保您已经选上了您准备“被替换”的课程！！！**

该模式致力于提供这样一种服务：

**在用户已经选择好课程B的情况下，他可能有一门更想去的但是由于某些原因没法同时选择的课A（如通识课只能选一门、时间冲突等），且课A此时已经属于满员状态。**

**程序持续刷新课程A的情况，一旦课程A有空余名额，立即退掉课程B并选择课程A，即“替换抢课”，从而帮助使用者确保：即使抢不到更好的课A，至少原来选上的课程B不会丢失。**

**在使用模式3时，请自行确保您已经选上课程A，否则程序或许会报错而不能执行。为保险起见，请在运行完此模式后立即自行前往教学信息服务网确认抢课结果。**

有关用户文件 'account.txt'：第一行为模式选择，此处为模式3；第二行为抢课开始时间，由用户指定开抢的时间，格式为'%Y-%m-%d %H:%M:%S'。范例如：2021-05-24 17:35:20 。考虑到本程序登录系统需要时间，请在抢课开放前提前约30秒至1分钟即开始运行本程序；第三行为最大尝试抢课次数；第四行及以后为所需要替换抢选的课程，行与行依次排列，行内同时指定课程名称及所属类型，并以',' 或 '，'隔开。

注意！此处课程写法有关键变化！对于两门相互对应的、需要替换抢课的课程，请将这两门课程写在同一行内，并用三个英文大于号隔开，即'>>>'。行内左侧为您的已经选上的课程B，右侧为您希望在有名额时能退课程B而去选择的课程A。

下面是文件 'account.txt'的一个很好的例子:

3
2021-05-24 17:35:20
1000
(2021-2022-1)-EE234-2，主修课程  >>> (2020-2021-2)-SO949-1，通识课
(2020-2021-3)-HI951-1，交叉课程 >>> (2020-2021-3)-HI954-1，任选课程

# 使用说明

上海交通大学全自动抢课脚本，支持准点开抢与抢课后持续捡漏两种模式。2021/06/03更新v3.0版本。

这是一个上海交通大学定时自动抢课系统，由Daniel-ChenJH(邮箱:13760280318@163.com)编写，于2021年2月25日首次编辑，2021年6月8日再次修改。

该可执行程序(qiangke.exe文件)目前只能在Windows x86_64电脑上运行，但源代码脚本也可以在mac电脑上运行。该程序基于https://i.sjtu.edu.cn 网站的当前结构编写。 https://i.sjtu.edu.cn  是上海交通大学学生处理个人事务的网站，学生可以在此选择下学期的课程。

本程序支持准点开抢、持续捡漏、替换抢课三种模式。但是，您应该只在抢课开放时间段附近时段使用它，否则该程序可能无法工作并抛出错误。

通过使用这个程序，您将能够立即选择您指定的课程。如果您想选择的课程目前已经满员,程序将会持续刷新网站页面,以每分钟80次左右的刷新速度检查是否有剩余名额,一旦有空余名额,程序将立即帮您选择这门课。

您不需要手动输入验证码来登录,本程序将为您代劳!

请注意不要经常使用这个程序，因为凭借它您几乎可以在任何时间持续刷新检查所有您想要的课程，您的同学可能会因此而生气。

---

# 声明

作者(@Daniel-ChenJH)对可能使用本程序的潜在用户不承担任何责任。

至少目前学校不会禁止短时间内不断刷新页面的IP或Jaccount，所以您可以放心使用它。

# 使用方法

1. 解压zip文件;
2. 确保您的电脑上有最新版本的Chrome浏览器(91.0.4472系列)。您可以通过访问chrome://settings/help来检查版本。
   本程序将会用到谷歌浏览器自动控制程序chromedriver，属于本程序的必须文件。请将您本机的谷歌浏览器升级至最新版本（91.0.4472系列）。如果您执意要选择其它的chrome版本，可前往http://npm.taobao.org/mirrors/chromedriver/ ，下载对应版本的chromedriver并做替换。
3. 按以下步骤编辑解压文件中的account.txt文件。重要！
4. 在第一行输入您希望本程序的运行模式。本程序支持准点开抢与抢课已经开始后持续捡漏两种模式。在第一行输入1代表使用准点开抢模式，输入2代表使用持续捡漏模式。
5. 若选择模式2（持续捡漏），第二行内容将不影响程序运行，但千万不可删去此行；若选择准点开抢模式或替换抢课模式，请在第二行中写入开抢的时间，格式为'%Y-%m-%d %H:%M:%S'。范例如：2021-05-24 17:35:20 。如果您希望程序一运行就立即开始抢课，您当然可以再次填入一个过去的时间。
6. 将第三行更改为您希望程序检查空余名额的总刷新次数。
   您可以通过设置这个值来保持它的运行，但是记住要给它一个整数。
7.

请记住，在下面几行中添加您想要选择的课程!!
每行为一个课程和它的课程类别!（如主修课程，民族生课程，留学生及港澳台生，通识课通选课，交叉课程，任选课程等。）
您可以在此写您想要的课程名称,老师名称或者课程编号，对于每一个您想选的课程您只需写上述三条信息之一。
但是我强烈建议您在这里写下课程编号，这样可以得到最准确的课程信息。
对于模糊课程名如：“高等数学，主修课程“，程序会默认为您刷新系统返回的第一个班级的空余名额。
如果此班级没有空余名额，程序也不会找寻相应课程的其它老师的班级，以免带来不必要的麻烦。
因此如果您想选择特定时间段、特定老师的课程，请您提前查询好相应的课程编号并写在account.txt文件的相应位置。

如果您想在抢选阶段开放时立刻使用本程序，请在海选阶段留个心眼，将您很想选上的课程编号记录下来，以便在海选阶段开始前写入account.txt文件中。

8. 如果您想选择多个班级，只需在下面几行中输入它们和它们的课程类别。
   然而，太多的课程可能会导致程序的效率下降，不建议同时抢四门或以上的课程。
9. 虽然本程序的模式1、模式2不会退掉您目前所选的课程，但还是强烈建议您确保您的目标课程预期时间表没有时间冲突。

下面是文件 'account.txt'的一个很好的例子:

1
2021-05-24 17:35:20
1000
(2021-2022-1)-EE234-2，主修课程世界民族音乐鉴赏，通识课

10. 双击'qiangke.exe'启动进程，并耐心等待程序运行。
11. 若程序以任何形式终止，请您先自行登录教学信息服务网，并尝试选课操作。请确保您已经：

（1）您的jaccount信息完全正确！！！
（2）完成所有上学期评教
（3）您的课程信息输入均正确，这些课程目前都已经可以被选择，且与您目前的时间表没有时间冲突
（4）您的网络环境良好
在完成上述检查后请尝试再次运行程序。

12.若因为抢课人数过多导致学校教学信息服务网服务器崩溃，本程序也无能为力。因此建议您在运行此程序的同时也自行前往教学信息服务网尝试抢课，以增加成功率。

13.请注意，请不要同时运行多次本程序，这将导致其中只有一个运行窗口能正常运行。

14.非常重要！！！
本exe程序文件由于在cmd中运行，然而Windows10系统的cmd默认开启了“快速编辑模式”，即只要当鼠标点击cmd任何区域时，就自动进入了编辑模式，
之后的程序向控制台输入内容甚至后台的程序都会被阻塞。表现为程序暂停运行或不运行。而此时在控制台内按下回车键或鼠标右键或方向键“下”后，就自动退出了编辑模式。此后，控制又恢复输出内容，服务端又正常了。

因此，在运行本程序且抢课未完成时，若非想退出程序，请不要在任何时候点击程序运行时展现的命令行窗口，会导致程序阻塞！而如果您发现您不小心点了命令行窗口，窗口内出现了白色选中光标，请及时在窗口中点击鼠标右键即可，程序会恢复正常。

# 程序运行效果

![](image/README/1622264022887.png)

![](image/README/1622264029887.png)

程序的运行状况会被实时更新到log文件：qiangke_log_file.log中。下图展示了程序成功执行模式3的情况。

![](image/README/1622728897337.png)

v3.1版本中更改为二维码+cookie登录的程序效果：可以看到，使用cookie大大提升了登录速度。

扫码登录：

![](image/README/1623130087035.png)

使用本地cookie登录：

![](image/README/1623130163702.png)

# 脚本执行

如果您希望执行程序的源代码脚本qiangke.py，请在cmd切换到当前程序所在目录，并执行操作：

pip install -r requirements.txt

如果您是mac操作系统，您需要前往http://npm.taobao.org/mirrors/chromedriver/ ，下载对应版本的chromedriver并做替换（删除原来的）。并且，您将不能运行此qiangke.exe程序文件，而只能在python环境下运行qiangke.py源代码。

# 鼓励--创作不易，请勿白嫖!

Daniel-ChenJH学艺尚浅，这是他个人在Github的第一个大项目。

本项目的几次大更新花费了他非常多的时间，甚至占用了期末考试复习时间。

如果您觉得Daniel-ChenJH的程序不错，请在Github上点亮“star”以给他一点鼓励。
项目链接：https://github.com/Daniel-ChenJH/Course-Bullying-in-SJTU

祝君好运!

Daniel-ChenJH,
2021.06.08.

# 联系

对于任何使用问题或讨论，请随时联系13760280318@163.com，如果是关于程序运行失败的讨论，请于附件中加上您的使用日志log文件‘qiangke_log_file.log‘，并于邮件中注明具体是哪一次运行（程序开始运行的时间）出了问题。
