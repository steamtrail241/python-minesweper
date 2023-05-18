import pyautogui, time
time.sleep(5)
for i in range(100000):
    pyautogui.keyDown("space")
    time.sleep(1)
    pyautogui.keyUp("space") 