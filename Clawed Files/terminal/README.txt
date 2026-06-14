CLAWED — CRT FIELD TERMINAL
===========================

WHAT IT IS
  A self contained CRT terminal experience that boots from the "Num47"
  floppy and reveals the DOCUMENTED FINDINGS one slide at a time,Green phosphor, scanlines, flicker,typewriter reveal, and glitches that intensify the deeper you go.

HOW TO OPEN
  Double-click  index.html  (works offline; no internet, no server).
  Or:  xdg-open index.html

CONTROLS
  ENTER / SPACE / CLICK / →   advance
  ←                           previous file
  M                           toggle sound (synth hum + key clicks; off
                              by default so it never autoplays)

THE FLOW
  insert floppy → boot sequence → 17 findings → signal-degrades outro → rewind to start.

REGENERATING (after you add/edit findings)
  1. Drop the new "finding NNN - ....txt" in the parent Clawed Files dir.
  2. Open  build.py  and add its filename to the ORDER list at the spot
     in the sequence where you want it to play.
  3. Run:   python3 build.py
  This re-reads every finding and rewrites index.html. Content is baked
  in at build time, so editing a .txt means re-running build.py.

CURRENT ORDER
  004 first bug · 005 glitch · 006 black cat · 010 demon cat ·
  008 constellation · 009 buzzer · 007 tulpa · 011 scp-529 ·
  003 entity 1000 · 012 the nothing · 013 loom · 014 the 432 ·
  015 hyperstition · 016 infinite game · 017 golem · 018 nine fragments ·
  019 void research station (finale)
