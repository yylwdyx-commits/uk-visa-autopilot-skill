# uk-visa-autopilot-skill

一套给 Claude Code 用的「办签证」skill。目标只有一个：申请人只说「去哪、几号」，剩下的查规则、盘证件、组材料、填表、写说明信、约录指纹、传材料、盯邮箱，全部由 agent 完成，人只做三件事：确认、签字、到场录指纹。

这套流程办过英国标准访问签，含拒签史申报、自雇补强这类不利条件的处理办法，实测按它递交的申请**获批 10 年多次**。从录指纹到出签 5 个工作日。

## 装法

```
cp -r uk-visa-autopilot-skill ~/.claude/skills/visa
```

然后在 Claude Code 里说「我要去英国，下个月 15 号走 22 号回」即可触发。

## 里面有什么

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 主流程：铁律、省事路径、盘证件、查规则、出成品、出行史真源、已知的坑 |
| `references/uk-gov-vfs-automation.md` | 英国线 gov.uk + VFS 全流程浏览器自动化配方（付款后续步、约录指纹、材料自传、出签后 eVisa） |
| `references/review-gate.md` | ★ 审查团队操作办法：递交前用多 agent 模拟签证官、移民律师、一致性审计、文书编辑四视角评审，每条 blocker 再派反方推翻 |
| `references/material-standards.md` | 每样材料「什么算合格」：签证官只判三件事、流水红线、自雇补强、交表闸门 |
| `scripts/md2docx.py` | markdown 成品转 docx 给申请人过目（macOS textutil） |
| `scripts/visa-mail-check.py` | 列近 N 天签证相关邮件（IMAP 只读） |
| `scripts/visa-mail-watch.py` | 邮箱哨兵：新邮件弹系统通知 + 心跳日志，配 cron 一天三跑 |
| `scripts/cdp-upload-multi.mjs` | VFS 材料自传用的 CDP 文件上传（MCP 浏览器工具没有上传能力时用） |

## 关于隐私

这份包里没有任何真实申请人的姓名、证件号、申请号、邮箱、账号或财务数字。所有个人信息都应放在**本机一个 700 权限的档案目录**（skill 里写作 `<PROFILE_DIR>`），永远不进 git、不进云端、不进 agent 的长期记忆。请照做。

## 三条铁律（再说一遍）

1. agent 绝不替申请人点 declaration、绝不付款。表可以填到最后一屏，然后停下。
2. 绝不替申请人撒谎。拒签史、逾期史一律如实申报，隐瞒在英美澳加体系里叫 deception，代价远重于一次拒签。
3. 签证规则每次联网现查，禁止凭记忆作答，成品里标注「核于 YYYY-MM-DD」。
