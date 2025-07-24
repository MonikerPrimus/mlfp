#Requires AutoHotkey v2.0
#SingleInstance Force

Loop {
    if WinExist("- Obsidian ") {
        WinClose("- Obsidian ")
    }
    else {
        break
    }
}