#Requires AutoHotkey v2.0

windowClass := "UnityWndClass"
processName := "7dsgc.exe"
windowName := "7DS"

HawkCheckX := 960
HawkCheckY := 540
HawkColor := 0xFFFFFF

PerformClick(hwnd, x, y, interval, doubleClick)
{
    WinActivate(hwnd)
    MouseMove(x, y)
    Sleep(500)

    HawkCheck := PixelGetColor(HawkCheckX, HawkCheckY)
    if (HawkCheck = HawkColor) {
        Sleep(500)
    }

    ControlClick(hwnd, X := x, Y := y)
    if (doubleClick) {
        Sleep(200)
        ControlClick(hwnd, X := x, Y := y)
    }
    Sleep(interval)
}

if 0 ; Vérifie si des arguments ont été passés
{
    MsgBox("Aucun argument fourni.", "Arguments", 64)
}
else
{
    clickX := A_Args[1]
    clickY := A_Args[2]
    interval := (A_Args[3] + 0) * 1000
    doubleClick := A_Args[4] + 0

    hwnd := WinExist("ahk_class " windowClass)
    if !hwnd
    {
        MsgBox("Target application not found!", "Error", 16)
        return
    }

    PerformClick(hwnd, clickX, clickY, interval, doubleClick)
}
