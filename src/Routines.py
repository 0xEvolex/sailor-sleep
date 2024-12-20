from Input import detect_image
from Globals import Globals
from Utilities import get_resource_path
import time
import pygame

def autodisconnect(AudioFilePath, delay, stop_event, scan_disconnect, scan_death, scan_ingame):
    pygame.mixer.init()
    imgs = {
        "disconnect": get_resource_path("images/disconnect.png"),
        "death": get_resource_path("images/death.png"),
        "ingame": get_resource_path("images/ingame.png"),
    }

    while Globals.scan_running:
        if stop_event.wait(timeout=0):
            print("[DEBUG] stop_event set, breaking loop.")
            break

        disconnect_found = scan_disconnect and detect_image(imgs["disconnect"], step_name="Scanning for disconnect", find_img_only=True)
        death_found = scan_death and detect_image(imgs["death"], step_name="Scanning for death", find_img_only=True)
        ingame_not_found = scan_ingame and not detect_image(imgs["ingame"], step_name="Scanning for third image", find_img_only=True)

        if disconnect_found:
            print("Found disconnect.png")
            pygame.mixer.music.load(AudioFilePath)
            pygame.mixer.music.play(-1)
            Globals.alarm_active = True
            print("[DEBUG] Alarm active, breaking loop.")
            break

        if death_found:
            print("Found death.png, waiting for delay")
            if stop_event.wait(timeout=delay):
                print("[DEBUG] stop_event set during delay, breaking loop.")
                break
            if detect_image(imgs["death"], step_name="Confirming death", find_img_only=True):
                print("Confirmed death.png after delay")
                pygame.mixer.music.load(AudioFilePath)
                pygame.mixer.music.play(-1)
                Globals.alarm_active = True
                print("[DEBUG] Alarm active after delay, breaking loop.")
                break
            else:
                print("death.png not found after delay")

        if ingame_not_found:
            print("Third image not found, reaffirming...")
            reaffirmed = True
            for i in range(2):
                if stop_event.wait(timeout=3):
                    print("[DEBUG] stop_event set during reaffirmation, breaking loop.")
                    reaffirmed = False
                    break
                if detect_image(imgs["ingame"], step_name="Reaffirming third image", find_img_only=True):
                    print("Third image found during reaffirmation")
                    reaffirmed = False
                    break
            if reaffirmed:
                pygame.mixer.music.load(AudioFilePath)
                pygame.mixer.music.play(-1)
                Globals.alarm_active = True
                print("[DEBUG] Alarm active, breaking loop.")
                break

        if not disconnect_found and not death_found and not ingame_not_found:
            print("No relevant images found")

        if stop_event.wait(timeout=3):
            print("[DEBUG] stop_event set during wait, breaking loop.")
            break

    if not Globals.alarm_active:
        pygame.mixer.music.stop()
        print("Scanning stopped and music stopped")
        print("[DEBUG] Scanning stopped and music stopped.")