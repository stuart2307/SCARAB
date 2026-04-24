::SCARAB Main
::Copyright (C) 2026 Stuart Rossiter
::You should have received a copy of the GNU General Public License
::along with this program.  If not, see <https://www.gnu.org/licenses/>.

@echo off

setlocal enabledelayedexpansion

echo Running from: %CD%
pause
for /f "delims=" %%f in ('dir /b "GUI QtCreator\SCARAB_UI\*.ui"') do (
    set name=%%~nf
    echo Converting %%f
    pyside6-uic "GUI QtCreator\SCARAB_UI\%%f" -o "GUI_Screens\!name!.py"
)

echo Done!
pause