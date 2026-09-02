#!/usr/bin/env python3
# 签证邮箱哨兵: 发现 UKVI/VFS 新邮件即 macOS 弹窗 + 记日志(UID 去重, 只读)
# 环境变量: VISA_MAIL_USER / VISA_MAIL_PASS / VISA_MAIL_HOST(默认 imap.qq.com) / VISA_WATCH_DIR(状态与日志目录, 默认 ~/visa-mail-watch)
# cron 示例(一天三跑, 出签后删掉):
#   7 10,14,19 * * * VISA_MAIL_USER=... VISA_MAIL_PASS=... /usr/bin/python3 /path/visa-mail-watch.py >>/path/watch.log 2>&1
import imaplib, email, re, os, subprocess, socket, sys, traceback
from datetime import datetime
from email.header import decode_header
socket.setdefaulttimeout(30)
USER=os.environ['VISA_MAIL_USER']; CODE=os.environ['VISA_MAIL_PASS']; HOST=os.environ.get('VISA_MAIL_HOST','imap.qq.com')
WD=os.path.expanduser(os.environ.get('VISA_WATCH_DIR','~/visa-mail-watch')); os.makedirs(WD,exist_ok=True)
ST=os.path.join(WD,'.lastuid'); LOG=os.path.join(WD,'watch.log')
def beat(tag, msg=''):
    """每次运行都留痕: 没有心跳=这次没跑成, 而不是'没新邮件'"""
    with open(LOG,'a') as f: f.write(f'{datetime.now():%m-%d %H:%M} {tag} | {msg}\n')
def notify(title, body, sound='Glass'):
    if sys.platform=='darwin':
        subprocess.run(['osascript','-e',f'display notification "{body}" with title "{title}" sound name "{sound}"'])
last=int(open(ST).read().strip()) if os.path.exists(ST) else 0
try:
    M=imaplib.IMAP4_SSL(HOST,993); M.login(USER,CODE); M.select('INBOX',readonly=True)
    _,d=M.uid('search',None,f'UID {last+1}:*')
    def dec(s):
        out=''
        for p,e in decode_header(s or ''): out+=p.decode(e or 'utf8','replace') if isinstance(p,bytes) else p
        return out
    new=[]; mx=last
    for u in d[0].split():
        u=int(u)
        if u<=last: continue
        mx=max(mx,u)
        _,md=M.uid('fetch',str(u),'(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
        m=email.message_from_bytes(md[0][1])
        frm,sub=dec(m['From']),dec(m['Subject'])
        if re.search(r'ukvi|vfs|gov\.uk|visa|homeoffice|worldpay',frm+sub,re.I):
            new.append((m['Date'],frm,sub))
    M.logout()
    open(ST,'w').write(str(mx))
    if new:
        for dt,frm,sub in new: beat('NEW', f'{dt} | {frm} | {sub}')
        urgent=any(re.search(r'decision|ready|collect|refus|grant|action|required|withdraw',s,re.I) for _,_,s in new)
        notify('签证邮件[重要]' if urgent else '签证邮件', '; '.join(s[:60] for _,_,s in new)[:180])
    beat('OK', f'巡检完成 lastUID={mx} 新邮件{len(new)}封')
except Exception as e:
    beat('FAIL', f'{type(e).__name__}: {str(e)[:120]}')
    notify('签证哨兵故障', '这次没跑成, 去看 watch.log', 'Basso')
    traceback.print_exc(file=sys.stderr); sys.exit(1)
