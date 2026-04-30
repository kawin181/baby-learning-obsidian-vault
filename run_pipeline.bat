@echo off
cd /d "C:\Users\wongt\Desktop\Baby_learning"
echo [%date% %time%] Baby Learning Pipeline starting...
claude --dangerously-skip-permissions -p "Execute the baby learning pipeline as described in CLAUDE.md. Complete all 5 steps for all topics. Do not stop early."
echo [%date% %time%] Generating TTS audio...
python generate_tts.py
echo [%date% %time%] Pipeline finished.
pause
