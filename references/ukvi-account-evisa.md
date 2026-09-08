# 出签后：建 UKVI 账户、链接 eVisa（逐屏配方，2026-09 真机跑通）

适用：英国访问签获批（2026-02-25 起只发 eVisa，护照不贴签证页）之后，申请人要在自己手机上建 UKVI 账户并把 eVisa 链接上去，才能查看签证和出行。**这一步必须本人做**（扫护照芯片 + 刷脸），agent 替不了，agent 的活是：逐屏给答案、实时看截图纠错、把答案记进本机档案。

## 0. 三个先说清的事实
- **护照不押在签证中心。** eVisa 时代 VFS 录完指纹当场把护照还给申请人。VFS 当晚那封「The passport … was collected from the Visa Application Centre」= 申请人本人取走。出签后**没有任何取件环节**，别让人等「ready for collection」邮件（这个错我犯过一整周）。
- **UKVI 账户 ≠ 申请时登录 gov.uk 的账号**，要新建。免费。VFS 现场推销的「查看签证账户」就是它，别买。
- **给申请人「操作示意」必须逐屏给答案**，不能按 gov.uk 概述页给大纲。真人会在每一屏停下来问「我对吗」，而且会把 Given/Surname 填反。下面就是逐屏。

## 1. 分流页（gov.uk/get-access-evisa → Start now）
| 屏 | 答 |
|---|---|
| When were you granted your most recent permission | 选 **on or after 1st November 2024**（按出签日期判） |
| Do you have your visa application number | Yes，填 **GWF 号**（申请时的 GWF…，UAN 也行） |
| Do you have a valid passport | Yes |
| 到「Create a UK Visas and Immigration (UKVI) account」说明页 | 点绿色 **Create an account**（「Sign in」是已有账户的人用的） |

## 2. 建账户（confirm-your-identity.homeoffice.gov.uk）
| 屏 | 答 |
|---|---|
| Who are you creating the account for | **Me** |
| What is your name | **Given names = 名，Surname = 姓**（按护照 MRZ；中国护照极易填反） |
| Country of nationality | 打 China 选 **China - CHN** |
| Identity document | **Passport** |
| Passport details | 护照号、Country of issue = China、Expiry date（照护照） |
| Date of birth | 日 月 年 |
| Email | 填后去邮箱收 6 位码 |
| Phone | **+86 直接接号码，不留空格**。然后大概率收不到码，见 §5 坑 1 |
| Do you want someone else to have access to your account | **No** |
| Check your answers | 核对护照号/到期/姓名顺序/生日，点 **Create account** |

建完会收到邮件「Finish linking your eVisa to your UKVI account」——这是**自动提醒**，让你去做 §3，不是出问题。

## 3. 登录并链接 eVisa
- 登录入口：分流页底部 Sign in，或邮件里的链接。**Which identity document** 选 Passport → 护照号 → 生日 → 码选发邮箱。
- 登进去若掉到「You are already logged in」页，点第二条 **View your forms and applications**（第一条跳的是 gov.uk 说明页，不是首页）。
- 首页 Your form 里「**Link your eVisa to your account**」点 Start，出现 7 项任务清单：

| 任务 | 答 |
|---|---|
| Confirm your identity | 说明页 Continue → 护照有芯片 **Yes** → 有合适手机 **Yes** → 跳到 ID Check 应用（见 §4） |
| Confirm your BRP or application number | BRP = **No** → 知道申请号 = **Yes** → 填 GWF |
| Your location | 不在英国，国家 China |
| Contact preferences | 邮箱选申请时那个；电话「Choose a different phone number」填 +86 常用号（此处只留联系方式，不发码） |
| Account security questions | 三组各选一题。**agent 替申请人选答案能从档案查到的题**（婚礼城市、出生城市、配偶母亲姓名这类），答案用拼音一个词，**当场记进本机档案**；申请人选错题也没关系，记住「题→答」即可 |
| Declaration | **I am the person submitting the information and I am aged 18 or over** |
| Submit | 提交 → 「Your information has been submitted」+ reference number |

提交后 1 分钟内收到邮件「We are linking your eVisa to your account」= 受理回执。**下一封「your eVisa is ready to view」才是能看了**，一般当天到三天内。到了登 gov.uk/view-prove-immigration-status 核对四项：姓名拼写、护照号、类型 Visit、有效期。错了走 gov.uk/evisa/report-error-evisa。

## 4. ID Check 应用（UK Immigration: ID Check）
- **一台手机就能做完，不用扫二维码**：网页点 Continue 会直接唤起应用，做完自动跳回网页显示「Identity information submitted」。两台设备扫码那条路只在电脑上开网页时才用。
- 应用里顺序：拍护照信息页（横拍）→ 护照合上、手机贴护照封底读芯片（不动等几秒，厚壳先摘）→ 刷脸 → 拍一张不笑的正脸（浅色墙，这张会印在 eVisa 上）→ Submit。

## 5. 三个实测的坑（全部有解，别卡住）
1. **国内手机收不到 6 位短信码**（开了国际短信接收也一样，运营商拦）：在「Check your phone」页点最下面 **My code has not arrived**，能跳过手机验证，账户照建；以后登录码选发邮箱。这是最省事的解，比借号快。
2. **ID Check 应用一开就弹「Sorry, there is a problem with the service」**：不是资料问题，是国内网络连不上。把应用彻底关掉，**换一种网络状态**（代理开↔关、WiFi↔流量）再开，一次就过。
3. **邮件读错**：「Finish linking」= 建完账户的自动提醒；「We are linking」= 受理回执；只有「ready to view」才是完成。别把前两封当异常。

## 6. agent 该做的收尾
- 把 reference number、登录方式（护照号+生日+邮箱码）、安全问题的题与答记进本机档案（不进 git、不进长期记忆）。
- 邮箱哨兵重新挂上，盯「ready to view」，到了再撤。
- 家庭成员每人一个账户，重复以上；把逐屏答案连同各自的值（姓名顺序、护照号、到期、邮箱、GWF）用聊天消息发给对方，比口头转述省一半来回。
