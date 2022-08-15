**Hand Gesture**
---
Small tools to visualize how you can use your own hand gestures to interact with your computer. 

*The following can be tried out:*

 - Scrolling up and down by opening and closing fist
 - Volume control by pinching fingers
 - Mouse movement with pointer finger

How does it work
---
I'm using Google’s framework – MediaPipe, which provided me with a 3D Hand Landmark model. Using machine learning techniques, it pinpoints the location of 21 landmarks on the hand in every single frame. However, the actual movements themselves are carried out by Python’s automation library - pyautogui, which is mainly used for clicking, dragging, scrolling, moving, etc.

*Installation guide*
--- 
The installation is pretty straightforward:
The basic requirement is to have [Python](https://www.python.org/) running on your machine and [pip](https://pypi.org/project/pip/).

    python get-pip.py

I recommend using venv to better manage separate package installations.

    python venv 

Activate your venv,

    .\venv\Scripts\activate

And then just install the requirements

    pip install -r requirements.txt
---
That's it, run the files either through command promt or a code-editor and have fun.
