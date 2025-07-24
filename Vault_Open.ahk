#Requires AutoHotkey v2.0
#SingleInstance Force

CoordMode "Mouse", "Screen"

Run "C:\Users\mjkuo\AppData\Local\Programs\Obsidian\Obsidian.exe"
Run "C:\Users\mjkuo\AppData\Local\Programs\Obsidian\Obsidian.exe"

WinActivate("Obsidian",, "- Obsidian ")

Sleep 1000

Click 2620, 1190

Sleep 100
WinWait("Open folder as vault", "", 1, "", "")
vault_folder := "C:\Users\mjkuo\Documents\MITES_Summer_ML\MLFP\Obsidian_Vaults\Healthcare_2024_Sub_Vaults\"
vault_name := "acera_surgical__inc_"
Sleep 500
Send vault_folder . vault_name
Sleep 500
Send "{Tab}{Enter}"
