# importing vlc module
import copy
import tkinter as tk
from functools import partial
from tkinter import *

import streamlink
import vlc


def startStream(streamEntry, vlcInstance):
    streams = streamlink.streams(streamEntry.get())

    print(streams["best"].url)

    Media = vlcInstance.media_new(streams["best"].url)
    # LayoutWindow.vlcPlayer1.set_hwnd(LayoutWindow.runnerFrame1.winfo_id())  # tkinter label or frame
    vlcInstance.set_media(Media)
    vlcInstance.audio_set_volume(30)

    vlcInstance.play()


def smooth_resize_and_move(frame, target_width, target_height, target_x, target_y, step=10):
    """
    Smoothly resizes and moves the frame to the target dimensions and position.
    Uses incremental steps to create a smooth animation effect.
    """
    current_width = frame.winfo_width()
    current_height = frame.winfo_height()
    current_x = frame.winfo_x()
    current_y = frame.winfo_y()

    # Calculate the increments
    width_increment = (target_width - current_width) / step
    height_increment = (target_height - current_height) / step
    x_increment = (target_x - current_x) / step
    y_increment = (target_y - current_y) / step

    # Function to update the size and position in steps
    def animate_frame(step_count):
        if step_count <= step:
            frame.config(
                width=current_width + width_increment * step_count,
                height=current_height + height_increment * step_count
            )
            frame.place(x=current_x + x_increment * step_count, y=current_y + y_increment * step_count)

            # Schedule the next frame update
            frame.after(20, animate_frame, step_count + 1)
        else:
            # Ensure final position and size
            frame.config(width=target_width, height=target_height)
            frame.place(x=target_x, y=target_y)

    animate_frame(1)  # Start the animation from step 1

# Smooth resize and move functions for focusing on runners
def runner1Focus():
    # Smoothly resize and move the frames for focusing on Runner 1
    smooth_resize_and_move(LayoutWindow.runnerFrame1, int(960 * 1.3), int(540 * 1.3), 0, 200)
    smooth_resize_and_move(LayoutWindow.runnerFrame2, int(960 / 1.3), int(540 / 1.3), int(960 * 1.3), 200)

def runner2Focus():
    # Smoothly resize and move the frames for focusing on Runner 2
    smooth_resize_and_move(LayoutWindow.runnerFrame2, int(960 * 1.3), int(540 * 1.3), int(960 / 1.3), 200)
    smooth_resize_and_move(LayoutWindow.runnerFrame1, int(960 / 1.3), int(540 / 1.3), 0, 200)

def equalRunnerFocus():
    # Smoothly resize and move both frames to equal focus
    smooth_resize_and_move(LayoutWindow.runnerFrame1, 960, 540, 0, 200)
    smooth_resize_and_move(LayoutWindow.runnerFrame2, 960, 540, 960, 200)


# def equalRunnerFocus():
#     LayoutWindow.runnerFrame1.config(width=960, height=540)
#     LayoutWindow.runnerFrame2.config(width=960, height=540)
#     LayoutWindow.runnerFrame2.place(x=960, y=200)
#
#
# def runner1Focus():
#     LayoutWindow.runnerFrame1.config(width=int(960 * 1.3), height=int(540 * 1.3))
#
#     LayoutWindow.runnerFrame2.config(width=int(960 / 1.3), height=int(540 / 1.3))
#     LayoutWindow.runnerFrame2.place(x=int(960 * 1.3), y=200)
#
#
# def runner2Focus():
#     LayoutWindow.runnerFrame2.config(width=int(960 * 1.3), height=int(540 * 1.3))
#     LayoutWindow.runnerFrame2.place(x=int(960 / 1.3), y=200)
#     LayoutWindow.runnerFrame1.config(width=int(960 / 1.3), height=int(540 / 1.3))


def setProgressRunner(progressLabels, holdOrTake, i):
    for x in range(i):
        progressLabels[x].config(fg="green")
    for x in range(i + 1, 5):
        progressLabels[x].config(fg="black")
    if holdOrTake == 0:
        progressLabels[i].config(fg="blue")
    else:
        progressLabels[i].config(fg="orange")



class LayoutWindow:
    root =tk.Tk()
    root.geometry("1920x1080")
    root.title("Stream Layout Window")
    runnerFrame1 = Frame(root, width=960, height=540)
    runnerFrame1.place(x=0, y=200)
    runnerFrame2 = Frame(root, width=960, height=540)
    runnerFrame2.place(x=960, y=200)

    vlcInstance1 = vlc.Instance()
    vlcInstance2 = vlc.Instance()

    vlcPlayer1 = vlcInstance1.media_player_new()
    vlcPlayer2 = vlcInstance2.media_player_new()
    vlcPlayer1.set_hwnd(runnerFrame1.winfo_id())
    vlcPlayer2.set_hwnd(runnerFrame2.winfo_id())

    progressBarRunner1 = Frame(root, width=960, height=100, bg="grey")

    runnerNameLabel1 = Label(progressBarRunner1, text="bdsab", font=("Roboto", 30), background="blue")
    runnerNameLabel1.place(x=0, y=0)
    progressLabels1 = []
    for i in range(5):
        progressLabels1 += [
            Label(progressBarRunner1, text="hold " + str(i + 1), font=("Roboto", 30), background="grey")]
        progressLabels1[-1].place(x=30 + i * 150, y=50)

    progressBarRunner2 = Frame(root, width=960, height=100, bg="grey")
    runnerNameLabel2 = Label(progressBarRunner2, text="bdsab", font=("Roboto", 30), background="blue",width=30)
    runnerNameLabel2.place(x=0, y=0)

    progressLabels2 = []
    for i in range(5):
        progressLabels2 += [
            Label(progressBarRunner2, text="hold " + str(i + 1), font=("Roboto", 30), background="grey")]
        progressLabels2[-1].place(x=30 + i * 150, y=50)
    progressBarRunner1.place(x=0, y=50)

    progressBarRunner2.place(x=960, y=50)

    # player.set_xwindow(display.winfo_id())
    # tkinter label or frame
    # player.set_media(Media)
    # player.audio_set_volume(30)

    # player.play()

class ControlWindow:
    toplevel = Toplevel(LayoutWindow.root)
    toplevel.title("Control Window")
    toplevel.geometry("1000x500")
    frame = Frame(toplevel)
    frame.pack(fill="both", expand="yes")

    streamlinks = LabelFrame(frame, text="Stream Links")

    streamEntry1 = Entry(streamlinks)
    streamEntry1.pack()

    streamEntry1Start = Button(streamlinks, command=partial(startStream, streamEntry1, LayoutWindow.vlcInstance1), text="Start Runner 1 Stream")
    streamEntry1Start.pack()

    streamEntry2 = Entry(streamlinks)
    streamEntry2.pack()

    streamEntry2Start = Button(streamlinks, command=partial(startStream, streamEntry2, LayoutWindow.vlcInstance2), text="Start Runner 2 Stream")
    streamEntry2Start.pack()

    streamlinks.pack(side=tk.RIGHT)

    runnerFocus = LabelFrame(frame, text="Focus runners")
    noRunnerFocus = Button(runnerFocus, text="Keep focus equal", command=equalRunnerFocus)
    noRunnerFocus.pack()
    runner1FocusButton = Button(runnerFocus, text="Focus on Runner 1", command=runner1Focus)
    runner1FocusButton.pack()
    runner2FocusButton = Button(runnerFocus, text="Focus on Runner 2", command=runner2Focus)
    runner2FocusButton.pack()
    runnerFocus.pack()

    progressRunner1 = LabelFrame(frame, text="Progress control Runner 1")
    progressButtons1 = []
    for i in range(5):
        progressButtons1 += [
            Button(progressRunner1, text="take " + str(i + 1), command=partial(setProgressRunner, LayoutWindow.progressLabels1, 0, i))]
        progressButtons1[-1].pack(side=tk.LEFT)
        progressButtons1 += [
            Button(progressRunner1, text="hold " + str(i + 1), command=partial(setProgressRunner, LayoutWindow.progressLabels1, 1, i))]
        progressButtons1[-1].pack(side=tk.LEFT)
    progressRunner1.pack(side=tk.TOP)

    progressRunner2 = LabelFrame(frame, text="Progress control Runner 2")
    progressButtons2 = []
    for i in range(5):
        progressButtons2 += [
            Button(progressRunner2, text="take " + str(i + 1), command=partial(setProgressRunner, LayoutWindow.progressLabels2, 0, i))]
        progressButtons2[-1].pack(side=tk.LEFT)
        progressButtons2 += [
            Button(progressRunner2, text="hold " + str(i + 1), command=partial(setProgressRunner, LayoutWindow.progressLabels2, 1, i))]
        progressButtons2[-1].pack(side=tk.LEFT)
    progressRunner2.pack(side=tk.TOP)

LayoutWindow.root.mainloop()

"""

def printwhat(x):
    if x < 2:
        LayoutWindow.labelframe1.config(height=100)
        LayoutWindow.label1.config(foreground="orange")
        print(x)
    else:
        LayoutWindow.labelframe1.config(height=400)
        LayoutWindow.label1.config(foreground="blue")
        print(x)


def makeSmaller():
    LayoutWindow.labelframe1.config(height=640)


# toplevel.overrideredirect(True)

    display = tk.Frame(toplevel, bd=0, bg="black")
    display.place(relwidth=1, relheight=1)

    labelframe1 = Frame(display, width=800, height=1000, background='blue', bg='blue')
    labelframe1.place(x=600, y=0)

    labelframe2 = LabelFrame(display, bg='blue', width=500, height=600)

    labelframe2.place(x=0,y=0)
    button=tk.Button(labelframe2, text="make smaller", command=makeSmaller)
    button.place(x=150, y=150)


    label1=Label(labelframe2 , text="hold 1",foreground="blue", bg="black")
    label1.place(x=0, y=0)

ControlWindow.hold = []
for i in range(5):
    ControlWindow.hold += [Button(ControlWindow.root, text="hello " + str(i), width=25, command=partial(printwhat, i))]
    ControlWindow.hold[-1].pack()

streams = streamlink.streams("https://www.twitch.tv/joshimuz")

print(streams["best"].url)

Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(streams["best"].url)
# player.set_xwindow(display.winfo_id())
player.set_hwnd(LayoutWindow.labelframe1.winfo_id())  # tkinter label or frame
player.set_media(Media)
player.audio_set_volume(30)

player.play()

# p=vlc.MediaPlayer(streams["best"].url)
# p.play()
# vlc.libvlc_audio_set_volume(p,30)
# p.audio_set_volume(30)
"""

"""
# Open a sample video available in sample-videos
vcap = cv2.VideoCapture(streams["best"].url)
#if not vcap.isOpened():
#    print "File Cannot be Opened"

while(True):
    # Capture frame-by-frame
    ret, frame = vcap.read()
    #print cap.isOpened(), ret
    if frame is not None:
        # Display the resulting frame
        cv2.imshow('frame',frame)
        # Press q to close the video windows before it ends if you want
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


    else:
        print ("Frame is None")
        break

# When everything done, release the capture
vcap.release()
cv2.destroyAllWindows()
print ("Video stop")
"""
