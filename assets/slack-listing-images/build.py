#!/usr/bin/env python3
"""Build the Bratrax Slack Marketplace listing images.

Emits self-contained HTML (shared CSS inlined, only Google Fonts external) at
exactly 1600x1000, then Chromium renders each to PNG at that size. No cropping.

The message content is transcribed verbatim from real @bratrax exchanges in the
demo workspace — same numbers, same wording, same button rows. Slack returns a
submission for images "completely unrelated to your app", and reviewers compare
the listing against what they see when they test it, so nothing here is invented.
"""

from pathlib import Path

HERE = Path(__file__).parent
SHARED = (HERE / "_shared.css").read_text()

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Outfit:wght@400;700;900&family=Space+Mono:wght@400;700"
    "&family=Lato:wght@400;700;900&display=swap"
)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1600">
<title>{title}</title>
<link href="{fonts}" rel="stylesheet">
<style>
{shared}
{extra}
</style>
</head>
<body>
  <div class="graph-paper"></div>
  <div class="vignette"></div>
  <div class="frame">
{body}
    <div class="wordmark">bratrax &nbsp;·&nbsp; attribution that adds up</div>
  </div>
</body>
</html>
"""

# --- the bratrax avatar, repeated ------------------------------------------

BOT_AV = '<div class="avatar avatar-bot"><span>B</span><i></i></div>'


def user_av(initial: str) -> str:
    return f'<div class="avatar avatar-user">{initial}</div>'


# --- 01 · chart -----------------------------------------------------------
# Slack renders this one as a native `data_visualization` block: 5 points, one
# series, well inside the 12x20 cap in slack/brain/charts.py. Native charts are
# styled by Slack, not by us — hence the orange bars and Slack's own axis
# formatting. Restyling it to the Bratrax palette would misrepresent what a
# customer actually sees, so it is reproduced as-is.

BARS = [
    ("Meta", 23.2),
    ("Google Ads", 21.5),
    ("Subscription", 9.8),
    ("Outbrain", 8.6),
    ("Taboola", 7.7),
]
PLOT_H = 160
AXIS_MAX = 25.0

CHART_EXTRA = """
  .chart {
    border: 1px solid #E8E8E8; border-radius: 8px;
    padding: 16px 22px 10px 22px; margin-top: 16px;
  }
  .chart-title { font-family:'Lato',sans-serif; font-weight:900; font-size:21px; color:#1D1C1D; margin-bottom:12px; }
  .plot { display:flex; }
  .ylab {
    width: 62px; flex: 0 0 62px; position: relative;
    font-family:'Lato',sans-serif; font-size:15px; color:#616061;
  }
  .ylab span { position:absolute; right:10px; transform:translateY(-50%); }
  .yaxis-name {
    font-family:'Lato',sans-serif; font-size:15px; color:#616061;
    writing-mode: vertical-rl; transform: rotate(180deg);
    align-self:center; margin-right:4px; white-space:nowrap;
  }
  .bars { flex:1; position:relative; border-left:1px solid #E8E8E8; }
  .gridline { position:absolute; left:0; right:0; height:1px; background:#EFEFEF; }
  .gridline.base { background:#D9D9D9; }
  .barrow { position:absolute; left:0; right:0; bottom:0; display:flex; align-items:flex-end; }
  .bar-cell { flex:1; display:flex; justify-content:center; }
  .bar { width: 70px; background:#E8912D; }
  .xlabs { display:flex; margin-left:62px; }
  .xlab-cell { flex:1; height:70px; position:relative; }
  /* Slack angles these ascending left-to-right with the label ENDING at the
     tick. Anchoring right-top and rotating counter-clockwise swings the start
     of the text down and to the left, clear of the bar it labels; anchoring
     left-top instead sends the text up into the plot area. */
  .xlab {
    position:absolute; right:50%; top:6px;
    font-family:'Lato',sans-serif; font-size:15px; color:#616061;
    transform-origin: right top; transform: rotate(-40deg);
    white-space:nowrap;
  }
  .legend {
    display:flex; align-items:center; justify-content:center; gap:8px;
    font-family:'Lato',sans-serif; font-size:16px; color:#616061; margin-top:6px;
  }
  .legend i { width:9px; height:9px; border-radius:50%; background:#E8912D; display:block; }
"""


def chart_block() -> str:
    ticks = ["25k", "20k", "15k", "10k", "5,000", "0"]
    ylabs = "".join(
        f'<span style="top:{i * (PLOT_H / (len(ticks) - 1)):.0f}px">{t}</span>'
        for i, t in enumerate(ticks)
    )
    grids = "".join(
        '<div class="gridline{cls}" style="top:{y:.0f}px"></div>'.format(
            cls=" base" if i == len(ticks) - 1 else "",
            y=i * (PLOT_H / (len(ticks) - 1)),
        )
        for i in range(len(ticks))
    )
    bars = "".join(
        f'<div class="bar-cell"><div class="bar" style="height:{v / AXIS_MAX * PLOT_H:.0f}px"></div></div>'
        for _, v in BARS
    )
    xlabs = "".join(
        f'<div class="xlab-cell"><div class="xlab">{name}</div></div>' for name, _ in BARS
    )
    return f"""      <div class="chart">
        <div class="chart-title">Revenue by Channel — Last 14 Days</div>
        <div class="plot">
          <div class="yaxis-name">Revenue ($)</div>
          <div class="ylab" style="height:{PLOT_H}px">{ylabs}</div>
          <div class="bars" style="height:{PLOT_H}px">
            {grids}
            <div class="barrow">{bars}</div>
          </div>
        </div>
        <div class="xlabs">{xlabs}</div>
        <div class="legend"><i></i> Attributed Revenue</div>
      </div>"""


IMG1_BODY = f"""    <div class="headline">See what actually drove <span class="pill">revenue</span></div>
    <div class="slack-card">
      <div class="msg">
        {user_av("Y")}
        <div class="msg-body">
          <div class="msg-who"><span class="who">Yuliya</span><span class="stamp">2:12 PM</span></div>
          <div class="msg-text">Chart revenue by channel for the last 14 days</div>
        </div>
      </div>
      <div class="replies"><a>2 replies</a><div class="rule"></div></div>
      <div class="msg">
        {BOT_AV}
        <div class="msg-body">
          <div class="msg-who"><span class="who">bratrax</span><span class="badge">Agent</span><span class="stamp">2:12 PM</span></div>
          <div class="msg-text">Over the last 14 days (Aug 8–21), <b>Meta</b> leads attributed revenue at ~$23.2K, closely followed by <b>Google Ads</b> at ~$21.5K, then <b>Subscription</b> (~$9.8K), <b>Outbrain</b> (~$8.6K), and <b>Taboola</b> (~$7.7K).</div>
{chart_block()}
          <div class="meta">Bratrax · UTC · 14:26</div>
          <div class="actions">
            <div class="btn">View in Bratrax</div>
            <div class="btn">Last 7 days</div>
            <div class="btn">Last 30 days</div>
            <div class="btn">Last 90 days</div>
          </div>
        </div>
      </div>
    </div>"""


# --- 02 · follow-up -------------------------------------------------------

IMG2_BODY = f"""    <div class="headline">Ask the obvious <span class="pill">follow-up</span></div>
    <div class="slack-card">
      <div class="msg">
        {user_av("Y")}
        <div class="msg-body">
          <div class="msg-who"><span class="who">Yuliya</span><span class="stamp">2:24 PM</span></div>
          <div class="msg-text">What was my spend today vs yesterday?</div>
        </div>
      </div>
      <div class="replies"><a>3 replies</a><div class="rule"></div></div>
      <div class="msg">
        {BOT_AV}
        <div class="msg-body">
          <div class="msg-who"><span class="who">bratrax</span><span class="badge">Agent</span><span class="stamp">2:24 PM</span></div>
          <div class="msg-text">Today's ad spend (Aug 21, so far) is <b>$467.19</b>, vs <b>$612.47</b> yesterday (Aug 20) — down about 24% ($145 less). Note today's figure is still accumulating since the day isn't over yet.</div>
          <div class="meta">Bratrax · UTC · 14:24</div>
          <div class="actions"><div class="btn">View in Bratrax</div></div>
        </div>
      </div>
      <div class="msg">
        {user_av("Y")}
        <div class="msg-body">
          <div class="msg-who"><span class="who">Yuliya</span><span class="stamp">2:25 PM</span></div>
          <div class="msg-text">How about spend this month so far?</div>
        </div>
      </div>
      <div class="msg">
        {BOT_AV}
        <div class="msg-body">
          <div class="msg-who"><span class="who">bratrax</span><span class="badge">Agent</span><span class="stamp">2:25 PM</span></div>
          <div class="msg-text"><p>Month-to-date spend (Aug 1 – Aug 21) is <b>$15,863.05</b>.</p><p>For reference, that's across 21 days, averaging ~$755/day so far this month.</p></div>
          <div class="meta">Bratrax · UTC · 14:25</div>
          <div class="actions"><div class="btn">View in Bratrax</div></div>
        </div>
      </div>
    </div>"""


# --- 03 · suggested prompts / Messages tab --------------------------------

IMG3_EXTRA = """
  .apphead {
    display:flex; align-items:center; gap:12px;
    padding-bottom: 16px; border-bottom: 1px solid #E8E8E8; margin-bottom: 4px;
  }
  .apphead .name { font-family:'Lato',sans-serif; font-weight:900; font-size:24px; color:#1D1C1D; }
  .tabs { display:flex; gap:26px; margin-top:16px; }
  .tab { font-family:'Lato',sans-serif; font-weight:700; font-size:20px; color:#616061; padding-bottom:10px; }
  .tab.on { color:#1D1C1D; box-shadow: inset 0 -3px 0 #1264A3; }
  /* This card carries the least content of the three, so it is scaled up and
     centred on the artboard rather than left hanging under the headline with
     250px of dead cream below it. Bigger type here also survives the listing
     thumbnail better. */
  .slack-card { margin-top: auto; margin-bottom: auto; padding: 36px 44px 46px 44px; }
  .intro { font-family:'Lato',sans-serif; font-size:25px; color:#1D1C1D; margin: 28px 0 0 0; }
  .intro .mention { background:#E8F5FA; color:#1264A3; padding:1px 3px; }
  .prompts { display:flex; flex-direction:column; align-items:flex-start; gap:14px; margin-top:26px; }
  .prompt {
    font-family:'Lato',sans-serif; font-weight:700; font-size:23px; color:#1D1C1D;
    border:1px solid #DDDDDD; border-radius:4px; padding:13px 24px; background:#FFFFFF;
  }
  .bigav { width:78px; height:78px; flex:0 0 78px; border-radius:10px; }
  .bigav span { font-size:60px; }
  .bigav i { right:10px; bottom:12px; width:13px; height:13px; }
  .liveline {
    display:flex; align-items:center; gap:9px; margin-top:18px;
    font-family:'Lato',sans-serif;
  }
  .liveline .who { font-weight:900; font-size:24px; }
  .liveline .dot { width:10px; height:10px; border-radius:50%; background:#1D9BD1; display:block; }
"""

IMG3_BODY = f"""    <div class="headline">Know what to ask on <span class="pill">day one</span></div>
    <div class="slack-card">
      <div class="apphead">
        <div class="avatar avatar-bot" style="width:38px;height:38px;flex:0 0 38px;border-radius:6px">
          <span style="font-size:28px">B</span><i style="right:5px;bottom:6px;width:7px;height:7px"></i>
        </div>
        <div class="name">bratrax</div>
      </div>
      <div class="tabs"><div class="tab on">Messages</div><div class="tab">About</div></div>
      <div class="msg" style="margin-top:30px">
        <div class="avatar avatar-bot bigav"><span>B</span><i></i></div>
        <div class="msg-body">
          <div class="liveline">
            <span class="who">bratrax</span><span class="badge">Agent</span><span class="dot"></span>
          </div>
          <div class="intro">This is the very beginning of your direct message history with <span class="mention">@bratrax</span></div>
          <div class="prompts">
            <div class="prompt">Today's spend</div>
            <div class="prompt">Top campaigns</div>
            <div class="prompt">Revenue chart</div>
          </div>
        </div>
      </div>
    </div>"""


FILES = [
    ("01-revenue-chart", "Bratrax in Slack — revenue by channel", CHART_EXTRA, IMG1_BODY),
    ("02-follow-up", "Bratrax in Slack — follow-up questions", "", IMG2_BODY),
    ("03-suggested-prompts", "Bratrax in Slack — suggested prompts", IMG3_EXTRA, IMG3_BODY),
]

for slug, title, extra, body in FILES:
    out = HERE / f"{slug}.html"
    out.write_text(
        PAGE.format(title=title, fonts=FONTS, shared=SHARED, extra=extra, body=body)
    )
    print(f"wrote {out.name}")
