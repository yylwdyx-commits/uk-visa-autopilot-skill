# 英国签证 gov.uk + VFS 全流程浏览器自动化配方（2026-08 一天跑通实录，全部真机验证；2026-09 出签闭环）

适用：UK 访客签从「表已提交」到「出签后」的一切线上动作——付款后续步、VFS 约录指纹、材料自传、补传、盯邮箱、出签后 eVisa。
实战：10 年签，当天完成 付款确认→约号→近 30 份材料自传，零人工点击（除申请人自选时段）。录指纹后 5 个工作日出签。

## 0. 浏览器铁律
- **必须 `puppeteer_launch stealth:true` + 真 Chrome**（`/Applications/Google Chrome.app/.../Google Chrome`，headless:false）。普通模式会被 VFS 的 Cloudflare 掐 JS 分片（206.js 等 403），现象＝点 Continue 死在 landing 页不动。
- 页面操作全走 `puppeteer_evaluate`；click/screenshot 工具易 120s 超时挂后台，慎用。
- Chrome 若开了自动翻译，按钮文字会变中文（Continue→继续），匹配文案要双语兜底；翻译不影响表单数据。

## 1. gov.uk 进门（会话 25 分钟过期，过期就重走，幂等）
续传链接（resume/<uuid>，记在本机进度文件里）→ 可能遇到：
- cookie 横幅 → `#reject-cookies`
- 「Do you want to resume your old application?」拦截页 → 点「Resume my old application」（同账号两份申请互踢会话，正常）
- 密码页 → `input[type=password]` → `input#submit`
- 落到 /nextSteps「Further actions」即成功。**必验右上角人名**，确认进的是谁的申请。
下载：checklist=`/coverSheet?externalReference=<uuid>`，提交版申请表=`/pdf?...`（cookie 用 UKV&I_SESSION 直接 curl 可拉 coverSheet；/pdf 时灵时不灵，页面「Download PDF」为准）。

## 2. 跳 VFS（握手一次性！）
/fesAppointmentBooking → `input#book-appointment` → 自动带 GWF 握手到 atlantis-abs-uk.vfsglobal.com。
- **握手 URL 一次性**：VFS 页面一刷新就 403201 整页 JSON，救法＝回 gov.uk 重走上面一节，几十秒。
- 首次握手出中国 PDPL 同意书：勾 `squaredTwo-2/3/4`（同意）+`squaredTwo-6`（未成年条款「不适用」），点 Agree and Proceed。
- VFS 自己的 sign-in 页（GWF+邮箱）带 **Cloudflare Turnstile，自动化下不渲染，别硬磕**，一律走 gov.uk 重握手。

## 3. 约录指纹（landing → date-selection → avs → review-pay → pay-status）
- landing：location 是 ng-select，`#location input` 打字触发 input 事件→点 `.ng-option` 选城市（北京有免费场；银行网点那个只有付费）→Continue（用 puppeteer_click 的 ::-p-text，evaluate 里 .click() 有时不触发路由）。
- date-selection：免费场＝「Standard Assisted (Free)」；日期条点日→点整点→出「Selected」。顶部「You have crossed limit of scheduling」红字是它的老 bug，时段能显示就无视。
- avs 页：**必点免费的「Document Self Upload / 文件自行上传」的 添加**（这是之后自传材料的开关！），其余全是付费推销（几百到一千多一项）一律不加。
- review-pay：country-code=+86、mobile-number=11 位手机（预填可能带 86 前缀 13 位，会超限，重写），勾 `squaredTwo-1` 条款，点 确认/Confirm → pay-status「感谢您预约」＝成功，确认邮件即达。免费场总价 ¥0，无支付步骤。
- 每份申请单独约（group size 锁 1）；同一时段可两人各占一个名额。

## 4. 材料自传（dashboard/document-upload）——踩坑最多，照抄别改
- 入口：dashboard/my-account → Document Self Upload → Upload Files。
- 10 个 input[type=file] 按固定序对应分类：**0住宿 1护照 2教育 3财务 4其他 5申请证明 6人生大事 7营业 8就业 9医疗**。
- 上传用 CDP（MCP 浏览器工具没有上传能力）：`node scripts/cdp-upload-multi.mjs <ws> <inputIndex> <file...>`（ws 取法：ps 找 Chrome 的 user-data-dir → 读 DevToolsActivePort → curl /json/list 找 document-upload 页）。
- **五个必踩的坑**：
  1. **「uploaded」小票只是暂存，必点底部 Save and Upload 才真提交**；页面刷新/会话过期＝暂存全丢。成功判据＝跳到 list-of-uploaded-documents 页且文件名在列。
  2. **重名 Error 109**（临时库按文件名去重，连丢失的暂存也占名）→ 换文件名（-2/-B 后缀）重传，别纠结。
  3. **带保护的 PDF 被静默拒或提交时才报**：移民局出入境记录＝RC4 加密（pdfinfo 看 Encrypted），某些盖章件带"安全头"（pdfinfo 看不出，Save 时报 malicious）→ 一律 `gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=out.pdf in.pdf` 重写，内容不变即过。
  4. 文件名必须英文无特殊字符、单个 ≤5MB、PDF/JPG/PNG；HEIC 用 sips 转 jpg，超 5MB 用 `sips -Z 2200` 缩。
  5. 传完批次里最后一个文件偶发被弹窗打断丢失 → 传完必逐分类核对 chips，缺谁单独补谁。
- **脚本报 OK ≠ VFS 收到**：CDP 设完文件只证明挂到了 DOM input。每传一份等页面真出现该文件条目再算数；传完回读 list 页核份数。
- **提交后上传口仍开放**（可补传/删除），直到录指纹当场才关；每次补传后重新勾条款+Save and Upload，会收「updated Appointment Confirmation」邮件。

## 5. 材料规范（官方 Checklist 读全后的口径）
- Mandatory 只有护照原件（有效+完好+≥1 空白页，录指纹当天带）；材料全线上，现场零纸质。
- 到场三样：护照原件+预约确认（邮箱可）+**GOV.UK Checklist 打印件（到现场才签字）**；提前 15 分钟，别更早。
- 非英文材料官方要求认证翻译（声明句+日期+签章+联系方式+资质页）；译名/证号/地址必须与申请表逐字一致。同一份证件若两人各持一本（如结婚证），译件的 Holder 要对应各自那本，别一份译件改名传两个账户。
- 自雇补强三件套：营业执照+已签章在职证明+近期经营证据（销项发票合成单 PDF 最好使）。
- **护照押在签证中心直到出签，期间不能出境**。★别把 VFS 当晚那封「The passport … was collected from the Visa Application Centre」读成还给申请人了——那是快递从中心收走送审（旁证：同日 e-ICR 回执写着取护照时间，次日 UKVI 发「application has arrived at the UK Visa Section」）。出签后等 VFS「ready for collection」通知再去取，本人带身份证+预约确认。★实测：录指纹→出签 **5 个工作日**（官方口径 3 周是上限，别按 3 周排行程）。

## 6. 邮箱监控
所有通知走申请时填的那个邮箱。`scripts/visa-mail-check.py N` 列近 N 天签证相关邮件；`scripts/visa-mail-watch.py` 是哨兵（UID 去重+系统弹窗+心跳日志），配 cron 一天三跑，出签后撤。凭据一律走环境变量，不写进脚本。
关注：payment confirmation / Your Visa Application Centre appointment（预约确认，HTML 无附件，打印用 Chrome --print-to-pdf 渲）/ Your Document Upload / 出签与补料通知。

## 7. 出签后
- 出签邮件＝noreply@fcdos.gov.uk「Your Visa Application: GWF…」，正文原句 "YOUR APPLICATION … HAS BEEN SUCCESSFUL … granted entry clearance to the UK as VISIT from X until Y"。**没有附件**，这封不是旅行凭证，存档进可复用材料库并挂到期日。
- 2026-02-25 起访问签只发 **eVisa**，护照上不贴签证页。出签后三步：①等 VFS 通知后去 VAC 取护照（工作日营业时段，本人带身份证+预约确认）；②本人手机装「UK Immigration: ID Check」扫护照芯片+刷脸建 **UKVI 账户**（gov.uk/evisa/set-up-ukvi-account，免费，≠申请时的 gov.uk 登录账号；VFS 现场推销的「查签证账户」就是这个，别买）；③登进 view-evisa 核对姓名/护照号/类型 VISIT/有效期，错了走 gov.uk/evisa/report-error-evisa 报错。
- **护照换新后必须在 UKVI 账户 update travel document**（gov.uk/evisa/update-ukvi-account），eVisa 绑护照号，否则航司查不到状态拒登机。证件总账里给这条挂到期规则。
- 这轮配方的真值：主申请人选零拒签的一方、有拒签史的如实申报并说明当时情境、自雇三件套、认证翻译逐字对齐，**结果拿满 10 年**。下次英联邦系（澳/新/加）照这套抄。
