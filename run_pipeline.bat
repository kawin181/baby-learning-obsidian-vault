@echo off
cd /d "C:\Users\wongt\Desktop\Baby_learning"
echo ================================================
echo   Baby Learning Pipeline
echo   %date% %time%
echo ================================================
echo.
echo Running... (pipeline takes 10-30 min, watch progress below)
echo.
claude --dangerously-skip-permissions -p "Execute the baby learning pipeline as described in CLAUDE.md. Complete all 5 steps for all topics. Do not stop early. IMPORTANT: Before starting each step, print a clear progress marker exactly like this format: >>> STEP 1/5: Load and Check ... then >>> STEP 2/5: Topic Selection ... etc. Also print when each topic starts: >>> TOPIC: [topic name]. This helps the user track progress."
echo.
echo ================================================
echo   Pipeline finished! %date% %time%
echo ================================================
pause
