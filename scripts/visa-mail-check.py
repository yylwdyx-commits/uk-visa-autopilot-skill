#!/usr/bin/env python3
# 签证邮箱巡检: 列出近 N 天 UKVI/VFS 相关邮件(IMAP 只读, 不动邮件状态)
# 用法: VISA_MAIL_USER=you@example.com VISA_MAIL_PASS=<IMAP授权码> VISA_MAIL_HOST=imap.example.com python3 visa-mail-check.py 3
import imaplib, email, sys, re, os
from email.header import decode_header
from datetime import datetime, timedelta
USER=os.environ['VISA_MAIL_USER']; CODE=os.environ['VISA_MAIL_PASS']; HOST=os.environ.get('VISA_MAIL_HOST','imap.qq.com')
days=int(sys.argv[1]) if len(sys.argv)>1 else 3
M=imaplib.IMAP4_SSL(HOST,993); M.login(USER,CODE); M.select('INBOX',readonly=True)
since=(datetime.now()-timedelta(days=days)).strftime('%d-%b-%Y')
_,d=M.search(None,f'(SINCE {since})')
ids=d[0].split()
def dec(s):
    out=''
    for part,enc in decode_header(s or ''):
        out+=part.decode(enc or 'utf8','replace') if isinstance(part,bytes) else part
    return out
hits=[]
for i in ids[-60:]:
    _,md=M.fetch(i,'(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
    m=email.message_from_bytes(md[0][1])
    frm,sub,dt=dec(m['From']),dec(m['Subject']),m['Date']
    if re.search(r'ukvi|vfs|gov\.uk|visa|appointment|decision|homeoffice',frm+sub,re.I):
        hits.append(f'{dt} | {frm[:45]} | {sub[:80]}')
M.logout()
print(f'{len(hits)} visa-related in last {days}d:')
[print(' ',h) for h in hits]
