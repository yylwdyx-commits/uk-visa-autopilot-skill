# uk-visa-autopilot-skill

**A Claude Code skill that runs a UK visitor-visa application end to end.** You say "I'm going to the UK on the 15th, back on the 22nd". The agent checks the current rules, audits your documents, fills the form, writes the cover letter, books the biometrics slot, uploads everything to VFS, watches your inbox, and hands you a checklist of the only three things a human must do: confirm, sign, show up.

Field-tested in 2026 on real applications, including an applicant with a prior US refusal and self-employed income. **Result: 10-year multi-entry visas. Five working days from biometrics to decision.**

[中文说明在下面](#中文)

## Why this exists

Visa applications are 90% clerical work and 10% judgement. The clerical part (60 form fields, 25 documents, three portals, a dozen emails) is exactly what an agent should absorb. The judgement part (what the visa officer actually checks, what counts as misrepresentation) is encoded here as rules and a pre-submission review gate, so the agent applies it instead of guessing.

## What's inside

| File | What it does |
|---|---|
| `SKILL.md` | The workflow: hard rules, cheapest-path search (do you even need this visa?), document audit, rule lookup, deliverables, travel-history from official exit-entry records, six known traps |
| `references/uk-gov-vfs-automation.md` | Browser automation recipe for gov.uk and VFS Global: resume links, the one-shot handshake, free biometrics slots, the 10 file inputs, the five upload traps, what to do after the decision (eVisa, UKVI account) |
| `references/review-gate.md` | **The pre-submission review gate.** 21 agents in four roles (visa officer, immigration lawyer, consistency auditor, English editor), each blocker re-argued by an adversarial "defence" agent. Ships with the anonymised findings from a real run so you can calibrate severity |
| `references/material-standards.md` | Pass/fail criteria per document: bank statements, deposits, self-employment proof, bookings, the four money figures |
| `scripts/md2docx.py` | Markdown deliverables to .docx for the applicant to read (macOS `textutil`) |
| `scripts/visa-mail-check.py` / `visa-mail-watch.py` | IMAP inbox scan and a cron sentinel that pings you on decision mail. Credentials via env vars only |
| `scripts/cdp-upload-multi.mjs` | File upload over Chrome DevTools Protocol, for when your MCP browser tool cannot upload |

## Install

```
git clone https://github.com/yylwdyx-commits/uk-visa-autopilot-skill ~/.claude/skills/visa
```

Open Claude Code and say what trip you're taking. The skill triggers on words like 签证 / visa / ETA / 要不要签证.

## Three rules the agent will not break

1. **It never clicks the declaration and never pays.** The form is filled to the last screen, then it stops. The declaration is the applicant's legal statement.
2. **It never lies for you.** Refusal history and overstays are declared as they are. In the UK/US/AU/CA systems concealment is "deception" and costs far more than one refusal.
3. **It never answers rules from memory.** Fees, ETA scope, waiver schemes and lead times change several times a year. Every rule is fetched live and stamped "verified on YYYY-MM-DD".

## Privacy

This repository contains no real names, document numbers, reference numbers, email addresses, credentials or financial figures. Personal data belongs in one local directory with `700` permissions (written as `<PROFILE_DIR>` throughout) and never enters git, cloud storage or the agent's long-term memory. Keep it that way.

## Adapting to other countries

The workflow, the review gate and the material standards are country-agnostic. Only `references/uk-gov-vfs-automation.md` is UK-specific. Australia, New Zealand and Canada share the same evidential logic and are the obvious next targets.

---

## 中文

一套给 Claude Code 用的「办签证」skill。你只说「去哪、几号」，agent 负责查规则、盘证件、组材料、填表、写说明信、约录指纹、传材料、盯邮箱，人只做三件事：确认、签字、到场录指纹。

2026 年在真实申请上跑通，含拒签史申报和自雇补强这类不利条件的处理办法。**结果：10 年多次签。录指纹到出签 5 个工作日。**

最值钱的一份是 `references/review-gate.md`：递交前用 21 个 agent 分四个角色（签证官、移民律师、一致性审计、英文编辑）把材料撕一遍，每条 blocker 再派一个反方 agent 尽力推翻。附带真实一轮的脱敏发现，供校准严重度。

三条铁律：agent 绝不点 declaration、绝不付款；绝不替你撒谎；规则一律联网现查不凭记忆。

隐私：仓库里没有任何真实姓名、证号、申请号、邮箱、账号、财务数字。个人信息只放本机 700 权限目录，永远不进 git、云端和 agent 长期记忆。

## License

MIT
