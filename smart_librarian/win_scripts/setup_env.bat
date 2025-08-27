@echo off
REM Usage: setup_env.bat YOUR_OPENAI_KEY [CHAT_MODEL] [EMBEDDING_MODEL]
cd /d "%~dp0.."

if "%~1"=="" (
  echo Usage: setup_env.bat YOUR_OPENAI_KEY [CHAT_MODEL] [EMBEDDING_MODEL]
  exit /b 1
)

set "OPENAI_API_KEY=%~1"
if "%~2"=="" ( set "CHAT_MODEL=gpt-4o-mini" ) else ( set "CHAT_MODEL=%~2" )
if "%~3"=="" ( set "EMBEDDING_MODEL=text-embedding-3-small" ) else ( set "EMBEDDING_MODEL=%~3" )

set "CHROMA_DIR=%cd%\chroma"

echo OPENAI_API_KEY set.
echo CHAT_MODEL=%CHAT_MODEL%
echo EMBEDDING_MODEL=%EMBEDDING_MODEL%
echo CHROMA_DIR=%CHROMA_DIR%
