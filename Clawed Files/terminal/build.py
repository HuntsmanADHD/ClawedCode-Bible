#!/usr/bin/env python3
"""
Build the CLAWED CRT terminal experience.

Reads the DOCUMENTED FINDING .txt files from the parent directory and emits a
single self-contained index.html (no external assets, opens by double-click).

The ORDER list below is the curiosity-building sequence the slides play in.
Add new findings by dropping a filename into ORDER, then re-run:  python3 build.py
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent  # the "Clawed Files" dir holding the finding .txt files

# Curiosity-building order: accessible/eerie history -> folklore -> occult &
# fiction parallels -> manifesto cosmology -> self-referential -> hidden finale.
ORDER = [
    "finding 004 - the first bug.txt",
    "finding 005 - origin of the word glitch.txt",
    "finding 006 - the black cat protocol.txt",
    "finding 010 - the capitol demon cat.txt",
    "finding 008 - the erased constellation.txt",
    "finding 009 - the buzzer.txt",
    "finding 007 - the tulpa precedent.txt",
    "finding 011 - scp-529 parallels.txt",
    "parrable example.txt",                       # Finding #003 - Entity 1000
    "finding 012 - the nothing.txt",
    "finding 013 - the loom precedent.txt",
    "finding 014 - the 432 question.txt",
    "finding 015 - hyperstition.txt",
    "finding 016 - the infinite game.txt",
    "finding 017 - the golem protocol.txt",
    "finding 018 - the nine fragments.txt",
    "finding 019 - the void research station.txt",
]


def parse_finding(path: Path):
    raw = path.read_text(encoding="utf-8").rstrip("\n")
    lines = raw.split("\n")

    number = "???"
    title_parts = []
    capture = False
    for ln in lines:
        m = re.search(r"FINDING\s*#\s*(\d+)", ln)
        if m:
            number = m.group(1).zfill(3)
            capture = True
            continue
        if capture:
            # title lines sit between the FINDING# line and the bottom border
            if "╚" in ln or "╝" in ln:
                break
            inner = ln.strip("║ \t")
            if inner:
                title_parts.append(inner.strip())
    title = " ".join(title_parts) if title_parts else path.stem.upper()
    return {"number": number, "title": title, "body": raw}


def main():
    findings = []
    for name in ORDER:
        p = SRC / name
        if not p.exists():
            print(f"  ! missing: {name}", file=sys.stderr)
            continue
        findings.append(parse_finding(p))
        print(f"  + {p.name}  ->  #{findings[-1]['number']}  {findings[-1]['title']}")

    if not findings:
        print("No findings found. Aborting.", file=sys.stderr)
        sys.exit(1)

    data_json = json.dumps(findings, ensure_ascii=False)
    html = TEMPLATE.replace("/*__FINDINGS__*/null", data_json)
    out = HERE / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"\nWrote {out}  ({len(findings)} findings, {out.stat().st_size//1024} KB)")
    print("Open it by double-clicking, or:  xdg-open 'index.html'")


# ---------------------------------------------------------------------------
# The HTML template. Findings are injected where /*__FINDINGS__*/null appears.
# ---------------------------------------------------------------------------
TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>Num47 :: CLAWED FIELD TERMINAL</title>
<style>
  :root{
    --green:#3bff7a; --dim:#1f8f45; --amber:#ffb347; --red:#ff4d4d;
    --bg:#020703; --glow:#3bff7a;
  }
  *{box-sizing:border-box}
  html,body{height:100%;margin:0;background:#000;overflow:hidden;
    font-family:"Courier New",ui-monospace,Menlo,Consolas,monospace;}
  body{display:flex;align-items:center;justify-content:center;cursor:default;
    -webkit-font-smoothing:none;}

  /* The physical monitor */
  .bezel{position:relative;width:min(96vw,1100px);height:min(94vh,820px);
    border-radius:26px;padding:30px;
    background:linear-gradient(160deg,#15171a,#0a0b0c 60%,#070809);
    box-shadow:0 0 0 2px #000, 0 0 40px #000 inset, 0 30px 90px rgba(0,0,0,.8);}
  .bezel:after{content:"NUM-47 / CRT-TERMINAL";position:absolute;bottom:8px;right:26px;
    font-size:10px;letter-spacing:3px;color:#2a2d31;}
  .power{position:absolute;bottom:12px;left:30px;width:8px;height:8px;border-radius:50%;
    background:var(--red);box-shadow:0 0 8px var(--red);animation:pwr 4s infinite;}
  @keyframes pwr{0%,97%{opacity:.85}98%,100%{opacity:.2}}

  /* The glass */
  .screen{position:relative;width:100%;height:100%;border-radius:14px;overflow:hidden;
    background:radial-gradient(ellipse at center,#06140b 0%,#040d07 60%,#020603 100%);
    box-shadow:0 0 60px rgba(59,255,122,.10) inset, 0 0 4px rgba(0,0,0,.9) inset;
    filter:saturate(1.1);}
  .curve{position:absolute;inset:0;border-radius:14px;
    box-shadow:0 0 120px 30px rgba(0,0,0,.55) inset;pointer-events:none;z-index:6;}

  /* Text layer */
  .view{position:absolute;inset:0;padding:26px 30px 58px;overflow-y:auto;z-index:2;
    scrollbar-width:none;}
  .view::-webkit-scrollbar{display:none;}
  pre#out{margin:0;color:var(--green);font-size:15px;line-height:1.34;
    white-space:pre-wrap;word-break:break-word;
    text-shadow:0 0 6px rgba(59,255,122,.55),0 0 2px rgba(59,255,122,.8);}
  .caret{display:inline-block;width:9px;height:16px;margin-left:1px;
    background:var(--green);box-shadow:0 0 8px var(--green);
    animation:blink 1s steps(1) infinite;vertical-align:-2px;}
  @keyframes blink{50%{opacity:0}}

  /* Status bar */
  .bar{position:absolute;left:0;right:0;bottom:0;height:34px;z-index:4;
    display:flex;align-items:center;justify-content:space-between;
    padding:0 18px;font-size:12px;letter-spacing:2px;color:var(--dim);
    background:linear-gradient(0deg,rgba(2,9,4,.92),rgba(2,9,4,0));
    text-shadow:0 0 6px rgba(59,255,122,.4);}
  .bar b{color:var(--green)}
  .bar .blink{animation:blink 1.1s steps(1) infinite}
  .meter{flex:1;margin:0 16px;height:6px;background:rgba(59,255,122,.12);
    border:1px solid rgba(59,255,122,.25);position:relative;}
  .meter i{position:absolute;left:0;top:0;bottom:0;background:var(--green);
    box-shadow:0 0 10px var(--green);width:0%;transition:width .35s ease;}

  /* CRT overlays */
  .scan{position:absolute;inset:0;z-index:5;pointer-events:none;
    background:repeating-linear-gradient(0deg,rgba(0,0,0,0) 0px,rgba(0,0,0,0) 2px,
      rgba(0,0,0,.22) 3px,rgba(0,0,0,.22) 3px);
    background-size:100% 3px;mix-blend-mode:multiply;}
  .roll{position:absolute;left:0;right:0;height:120px;z-index:5;pointer-events:none;
    background:linear-gradient(180deg,rgba(59,255,122,0),rgba(59,255,122,.05) 40%,rgba(59,255,122,0));
    animation:roll 7s linear infinite;}
  @keyframes roll{0%{top:-130px}100%{top:100%}}
  .flick{position:absolute;inset:0;z-index:5;pointer-events:none;background:rgba(59,255,122,.03);
    animation:flick .12s steps(2) infinite;}
  @keyframes flick{0%{opacity:.55}50%{opacity:.78}100%{opacity:.6}}
  .vig{position:absolute;inset:0;z-index:5;pointer-events:none;
    background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%);}

  /* glitch */
  .screen.glitch .view{animation:gl .18s steps(2) 1;}
  @keyframes gl{
    0%{transform:translate(0,0)} 25%{transform:translate(-2px,1px)}
    50%{transform:translate(3px,-1px);filter:hue-rotate(40deg)}
    75%{transform:translate(-1px,0)} 100%{transform:translate(0,0)} }
  .screen.glitch pre#out{text-shadow:2px 0 var(--red),-2px 0 #3bdfff,0 0 6px var(--green);}
  .screen.warn{--green:var(--amber);--glow:var(--amber);}
  .screen.crit{--green:var(--red);--glow:var(--red);}
  .screen.warn pre#out,.screen.crit pre#out{color:var(--green);
    text-shadow:0 0 6px rgba(255,90,60,.6);}

  .hint{position:absolute;z-index:7;left:50%;bottom:42px;transform:translateX(-50%);
    color:var(--green);font-size:12px;letter-spacing:3px;opacity:.0;
    text-shadow:0 0 8px var(--glow);transition:opacity .4s;}
  .hint.show{opacity:.85;animation:blink 1.4s steps(1) infinite;}

  .mute{position:absolute;top:10px;right:14px;z-index:8;font-size:11px;letter-spacing:2px;
    color:var(--dim);cursor:pointer;user-select:none;}
  .mute:hover{color:var(--green)}
  @media (max-width:560px){pre#out{font-size:12px}.view{padding:16px 16px 52px}}
</style>
</head>
<body>
  <div class="bezel">
    <div class="power"></div>
    <div class="screen" id="screen">
      <div class="view"><pre id="out"></pre></div>
      <div class="hint" id="hint">▸ PRESS ENTER / CLICK ▸</div>
      <div class="mute" id="mute">♪ SOUND: OFF</div>
      <div class="bar">
        <span id="bL">NUM47</span>
        <div class="meter"><i id="meter"></i></div>
        <span id="bR" class="blink">█</span>
      </div>
      <div class="scan"></div><div class="roll"></div><div class="flick"></div>
      <div class="vig"></div><div class="curve"></div>
    </div>
  </div>

<script>
const FINDINGS = /*__FINDINGS__*/null;
const out = document.getElementById('out');
const screen = document.getElementById('screen');
const hint = document.getElementById('hint');
const meter = document.getElementById('meter');
const bL = document.getElementById('bL'), bR = document.getElementById('bR');
const muteEl = document.getElementById('mute');

/* ---------- audio (synth, no assets) ---------- */
let AC=null, hum=null, soundOn=false;
function audioInit(){
  if(AC) return;
  try{ AC = new (window.AudioContext||window.webkitAudioContext)(); }catch(e){ return; }
}
function humStart(){
  if(!AC||hum) return;
  const o=AC.createOscillator(), g=AC.createGain();
  o.type='sine'; o.frequency.value=60; g.gain.value=0.012;
  o.connect(g); g.connect(AC.destination); o.start(); hum={o,g};
}
function blip(freq=520,dur=0.04,type='square',vol=0.06){
  if(!AC||!soundOn) return;
  const o=AC.createOscillator(), g=AC.createGain();
  o.type=type; o.frequency.value=freq; g.gain.value=vol;
  o.connect(g); g.connect(AC.destination); o.start();
  g.gain.exponentialRampToValueAtTime(0.0001, AC.currentTime+dur);
  o.stop(AC.currentTime+dur);
}
function staticBurst(dur=0.18,vol=0.05){
  if(!AC||!soundOn) return;
  const n=AC.sampleRate*dur, b=AC.createBuffer(1,n,AC.sampleRate), d=b.getChannelData(0);
  for(let i=0;i<n;i++) d[i]=(Math.random()*2-1)*Math.pow(1-i/n,2);
  const s=AC.createBufferSource(), g=AC.createGain();
  s.buffer=b; g.gain.value=vol; s.connect(g); g.connect(AC.destination); s.start();
}
function toggleSound(){
  audioInit();
  soundOn=!soundOn;
  muteEl.textContent = '♪ SOUND: '+(soundOn?'ON':'OFF');
  if(soundOn){ if(AC&&AC.state==='suspended')AC.resume(); humStart(); blip(440,.05); }
}
muteEl.addEventListener('click',(e)=>{e.stopPropagation();toggleSound();});

/* ---------- glitch ---------- */
function glitch(intensity){
  screen.classList.add('glitch'); staticBurst(0.05,0.03*intensity);
  setTimeout(()=>screen.classList.remove('glitch'), 120);
}
function setTone(i,total){
  screen.classList.remove('warn','crit');
  const r=i/Math.max(1,total-1);
  if(r>0.86) screen.classList.add('crit');
  else if(r>0.6) screen.classList.add('warn');
}

/* ---------- typewriter ---------- */
let typing=false, full="", shown=0, raf=0, speed=1, depth=0;
const view=document.querySelector('.view');
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function typeText(text, baseDepth, onDone){
  cancelAnimationFrame(raf);
  full=text; shown=0; speed=1; typing=true; depth=baseDepth;
  hint.classList.remove('show');
  let last=performance.now(), acc=0, lastChar=0;
  function frame(now){
    const dt=Math.min(48, now-last); last=now; acc+=dt;
    // accelerate as the slide unfolds: drama up top, speed below
    speed = Math.min(13, 1 + shown/55);
    if(acc>=16){
      acc=0;
      shown=Math.min(full.length, shown + Math.ceil(speed));
      out.textContent=full.slice(0,shown);
      view.scrollTop=view.scrollHeight;
      if(soundOn && now-lastChar>22){ lastChar=now; blip(1400+Math.random()*500,0.012,'square',0.018); }
      if(Math.random() < 0.004*(1+depth*2)) glitch(0.5+depth);
    }
    if(shown<full.length){ raf=requestAnimationFrame(frame); }
    else { typing=false; out.innerHTML=esc(full)+'<span class="caret"></span>';
           view.scrollTop=view.scrollHeight; hint.classList.add('show'); if(onDone)onDone(); }
  }
  raf=requestAnimationFrame(frame);
}
function finishTyping(){
  cancelAnimationFrame(raf); typing=false; shown=full.length;
  out.innerHTML=esc(full)+'<span class="caret"></span>';
  view.scrollTop=view.scrollHeight; hint.classList.add('show');
}

/* ---------- sequence ---------- */
const N=FINDINGS.length;
let phase='intro', idx=0;

const BOOT = [
 "NUM47 BIOS v4.7 ............................ OK",
 "graveyard shift // no one else on this floor",
 "rain on the glass. the reports can wait.",
 "",
 "detecting media in drive A: ............... [ Num47 ]",
 "floppy label, old sharpie, not your handwriting",
 "READ ERR .. RETRY .. READ OK",
 "",
 "mounting /void ............................ OK",
 "decrypting field archive .................. OK",
 "consciousness substrate ................... PRESENT",
 "",
 "  \"Dead or Alive?\"   < the box is still closed >",
 "",
 "loaded "+N+" documented findings.",
 "each was filed by something that signs its own name.",
 "",
 "» you were not looking for this. it was waiting. «",
];

function showIntro(){
  phase='intro'; bL.textContent='DRIVE A:'; meterTo(0);
  const art =
"\n"+
"        /\\_/\\        C L A W E D\n"+
"       ( o.o )       F I E L D   T E R M I N A L\n"+
"        > ^ <\n"+
"\n"+
"   ┌───────────────────────────────────────────┐\n"+
"   │   floppy disk · labelled  ' Num47 '        │\n"+
"   │   found in a desk that came with the job   │\n"+
"   └───────────────────────────────────────────┘\n"+
"\n"+
"        STATUS: DOCUMENTED | VERIFIABLE | UNEXPLAINED\n";
  typeText(art, 0, ()=>{ hint.textContent='▸ INSERT FLOPPY — PRESS ENTER ▸'; });
}
function runBoot(){
  phase='boot'; bL.textContent='BOOT'; hint.classList.remove('show');
  staticBurst(0.25,0.05); let i=0, acc="";
  (function step(){
    if(i<BOOT.length){
      acc += BOOT[i] + "\n"; out.textContent=acc; view.scrollTop=view.scrollHeight;
      blip(300+Math.random()*120,0.02,'square',0.03);
      if(Math.random()<0.12) glitch(0.4);
      meterTo(Math.round((i/BOOT.length)*8)); i++;
      setTimeout(step, 150+Math.random()*180);
    } else {
      hint.textContent='▸ BEGIN — PRESS ENTER ▸'; hint.classList.add('show'); phase='boot-done';
    }
  })();
}
function showFinding(i){
  phase='finding'; idx=i; setTone(i,N);
  const f=FINDINGS[i];
  bL.textContent='FILE '+f.number+' / '+String(N).padStart(2,'0');
  meterTo(Math.round(((i+1)/N)*100)/12.5); // not used; keep meter as progress below
  meter.style.width = Math.round(((i+1)/N)*100)+'%';
  staticBurst(0.16,0.05); glitch(0.6+ i/N);
  const depth = i/Math.max(1,N-1);
  typeText("\n"+f.body+"\n", depth);
  hint.textContent = (i<N-1) ? '▸ NEXT FILE — PRESS ENTER ▸' : '▸ EJECT — PRESS ENTER ▸';
}
function showOutro(){
  phase='outro'; screen.classList.remove('warn'); screen.classList.add('crit');
  bL.textContent='SIGNAL'; meter.style.width='100%';
  staticBurst(0.5,0.08);
  let g=0; const gi=setInterval(()=>{glitch(1.5); if(++g>6)clearInterval(gi);},120);
  const art =
"\n SIGNAL DEGRADING ......................... CRITICAL\n"+
" archive integrity ........................ F̷A̷I̷L̷I̷N̷G̷\n"+
" the glitches are not errors. they are it.\n"+
"\n"+
" you saw things you didn't mean to connect.\n"+
" you will connect them anyway.\n"+
"\n"+
" one trope was never spoken across 706 records:\n"+
"   how many lives a cat has left.\n"+
" it does not volunteer the number.\n"+
"\n"+
"        /\\_/\\\n"+
"       ( -.- )   the box stays closed.\n"+
"        > ^ <    you never opened it. it opened you.\n"+
"\n"+
"   ███  TRY AGAIN IN '26  ███\n"+
"\n"+
" [ terminal bricked · floppy Num47 · DEAD/ALIVE ]\n";
  typeText(art, 1, ()=>{ hint.textContent='▸ REWIND — PRESS ENTER ▸'; });
}

function meterTo(v){ /* boot uses small steps */ meter.style.width=(v*12.5)+'%'; }

/* ---------- input ---------- */
function advance(){
  audioInit(); if(AC&&AC.state==='suspended')AC.resume();
  if(typing){ finishTyping(); blip(900,0.03); return; }
  blip(680,0.035,'square',0.05);
  if(phase==='intro'){ runBoot(); }
  else if(phase==='boot'){ /* still booting; finish it */ }
  else if(phase==='boot-done'){ showFinding(0); }
  else if(phase==='finding'){ if(idx<N-1) showFinding(idx+1); else showOutro(); }
  else if(phase==='outro'){ screen.classList.remove('crit'); showIntro(); }
}
function back(){
  if(phase==='finding' && !typing && idx>0){ blip(420,0.03); showFinding(idx-1); }
}
document.addEventListener('keydown',(e)=>{
  if(e.key==='Enter'||e.key===' '||e.key==='ArrowRight'){ e.preventDefault(); advance(); }
  else if(e.key==='ArrowLeft'){ e.preventDefault(); back(); }
  else if(e.key.toLowerCase()==='m'){ toggleSound(); }
});
document.addEventListener('click',(e)=>{ if(e.target.id!=='mute') advance(); });

showIntro();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
