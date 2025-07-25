#Requires AutoHotkey v2.0
#SingleInstance Force

CoordMode "Mouse", "Screen"

Run "C:\Users\mjkuo\AppData\Local\Programs\Obsidian\Obsidian.exe"
Run "C:\Users\mjkuo\AppData\Local\Programs\Obsidian\Obsidian.exe"

Sleep 1000

WinActivate("Obsidian",, "- Obsidian ")

Sleep 500

Click 2620, 1190

Sleep 100
WinWait("Open folder as vault", "", 1, "", "")
vault_path := "C:\Users\mjkuo\Documents\MITES_Summer_ML\MLFP\Obsidian_Vaults\Healthcare_2024_Sub_Vaults\abbott_laboratories"
Sleep 500
Send vault_path
Sleep 500
Send "{Tab}{Enter}"
