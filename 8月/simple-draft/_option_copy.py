# -*- coding: utf-8 -*-
from pathlib import Path
import json
import subprocess

ROOT = Path(r"C:\Users\ryuta-kusaka\Documents\GitHub\kyodo-lp-deta")

locale_updates = {
    "en": {
        "optionCatch": "Paid options (8 total)",
        "optionLabel": "Services worth ¥10,000+/mo — all included",
        "optionMonth": "August",
        "itemInitial": 'At signup, an initial fee of <strong class="cond-em">¥5,500 (tax incl.)</strong> is charged separately',
        "item1": '<strong class="cond-em">[Through end of Feb 2027]</strong> membership is required',
        "item2": 'If you cancel during the period, an <strong class="cond-em">[early cancellation fee of ¥33,660 (tax incl.)]</strong> will apply.',
        "item3": 'All 8 free options are <strong class="cond-em">auto-enrolled</strong> at signup. Cancel unwanted options by <strong class="cond-em">end of August</strong>.',
        "noticeBody": 'Options are <strong class="cond-em">auto-enrolled</strong> at signup<br />Cancel unwanted options by <strong class="cond-em" id="campaign-notice-deadline">end of August</strong><br /><br />Cancel anytime after joining via <strong>[JOYFIT APP]</strong><br />You can use services through month-end after canceling',
        "noticeDeadline": "end of August",
    },
    "ko": {
        "optionCatch": "유료 옵션(총 8개)",
        "optionLabel": "합계 월 1만 엔 이상 서비스를 모두",
        "optionMonth": "8월",
        "itemInitial": '입회 시 초기 비용 <strong class="cond-em">5,500엔(세금 포함)</strong>이 별도로 발생합니다',
        "item1": '<strong class="cond-em">【2027년 2월 말일】</strong>까지의 재적이 필수 조건입니다',
        "item2": '기간 내 탈퇴 시 <strong class="cond-em">【해약금 33,660엔(세금 포함)】</strong>이 발생합니다.',
        "item3": '무료 옵션 8개는 입회 시 <strong class="cond-em">자동 계약</strong>됩니다. 불필요한 경우 <strong class="cond-em">8월 말까지</strong> 반드시 해약해 주세요.',
        "noticeBody": '옵션은 입회 시 <strong class="cond-em">자동 계약</strong>됩니다<br />불필요한 경우 <strong class="cond-em" id="campaign-notice-deadline">8월 말까지</strong> 반드시 해약해 주세요<br /><br />입회 후 <strong>[JOYFIT APP]</strong>에서 해약 가능<br />해약 후에도 월말까지 이용 가능합니다',
        "noticeDeadline": "8월 말까지",
    },
    "zh-CN": {
        "optionCatch": "付费选项（共8项）",
        "optionLabel": "合计每月1万日元以上服务全部",
        "optionMonth": "8月",
        "itemInitial": '入会时另收初期费用<strong class="cond-em">5,500日元(含税)</strong>',
        "item1": '必须在籍至<strong class="cond-em">【2027年2月末日】</strong>',
        "item2": '期间内退会需支付<strong class="cond-em">【解约金33,660日元(含税)】</strong>。',
        "item3": '8项免费选项入会时<strong class="cond-em">自动签约</strong>。不需要请务必于<strong class="cond-em">8月末前</strong>解约。',
        "noticeBody": '选项在入会时<strong class="cond-em">自动签约</strong><br />不需要请务必于<strong class="cond-em" id="campaign-notice-deadline">8月末前</strong>解约<br /><br />入会后可通过<strong>[JOYFIT APP]</strong>解约<br />解约后仍可使用至月末',
        "noticeDeadline": "8月末前",
    },
    "zh-TW": {
        "optionCatch": "付費選項（共8項）",
        "optionLabel": "合計每月1萬日圓以上服務全部",
        "optionMonth": "8月",
        "itemInitial": '入會時另收初期費用<strong class="cond-em">5,500日圓(含稅)</strong>',
        "item1": '必須在籍至<strong class="cond-em">【2027年2月末日】</strong>',
        "item2": '期間內退會需支付<strong class="cond-em">【解約金33,660日圓(含稅)】</strong>。',
        "item3": '8項免費選項入會時<strong class="cond-em">自動簽約</strong>。不需要請務必於<strong class="cond-em">8月末前</strong>解約。',
        "noticeBody": '選項在入會時<strong class="cond-em">自動簽約</strong><br />不需要請務必於<strong class="cond-em" id="campaign-notice-deadline">8月末前</strong>解約<br /><br />入會後可透過<strong>[JOYFIT APP]</strong>解約<br />解約後仍可使用至月末',
        "noticeDeadline": "8月末前",
    },
}

for lang, upd in locale_updates.items():
    path = ROOT / "locales" / "campaign" / f"{lang}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["pricing"]["optionCatch"] = upd["optionCatch"]
    data["pricing"]["optionLabel"] = upd["optionLabel"]
    data["pricing"]["optionMonth"] = upd["optionMonth"]
    data["conditions"]["itemInitial"] = upd["itemInitial"]
    data["conditions"]["item1"] = upd["item1"]
    data["conditions"]["item2"] = upd["item2"]
    data["conditions"]["item3"] = upd["item3"]
    data["options"]["noticeBody"] = upd["noticeBody"]
    data["pricing"]["noticeDeadline"] = upd["noticeDeadline"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(lang)

subprocess.run(["python", str(ROOT / "build_locales.py")], check=True)

html = (ROOT / "index.html").read_text(encoding="utf-8")
aug = html
for a, b in [
    ('href="i18n.css"', 'href="../i18n.css"'),
    ('src="locales.bundle.js"', 'src="../locales.bundle.js"'),
    ('src="i18n.js"', 'src="../i18n.js"'),
    ('src="campaign-i18n.js"', 'src="../campaign-i18n.js"'),
    ('src="joylogo.jpg"', 'src="../joylogo.jpg"'),
]:
    aug = aug.replace(a, b)
(ROOT / "8月" / "index.html").write_text(aug, encoding="utf-8")
print("synced")
