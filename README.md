# self-learning-robot_analysis
Task: Put a self-learning robot by a conveyor and let it learn for itself what to do. The robot has a GPU, cameras, depth sensors and a mechanic arm.  *Literal analysis only. The code is yet to be completed.

Author: Yongjie Yang   yangyj@bu.edu
        Sen Zhang   jasonall@bu.edu

MotionDetection.py:
Studied a blog about moving object detection, studied the code, reproduced the result, and found some problems. The code was too sensitive to motion. Working on reducing the sensitivity.

MVP:
The robot has full control of its robotic arm, and can use it to move objects. The robot studies what other robots do, and understands what it should do. The robot tries to do what it should do, and perfect the behavior.
MVP user story:
A conveyor delivers objects that look the identical. There are other robots by the conveyor that moves the objects from the conveyor to somewhere else, a storage container for example. Our robot observes how other robots do it, and learns to do the same.

Possible additions:
1.The conveyor delivers several kinds of objects. Only one type of them should be moved to the designated area, and the rest should remain untouched. The robot understands this, and behaves accordingly.
2.The conveyor delivers several kinds of objects. Objects should be classified and moved to different areas. The robot understands this, and behaves accordingly.

Technologies to evaluate and reasons for choosing them
Reinforcement learning: It is the method of machine learning that outputs a sequence of actions according to a given environment for the best result. This is suitable for this project, because the results can easily be quantified, and actions can be made simple.
Moving object detection: Integrated in opencv package. Rather mature technology.
SCM motor control system: Mature, reliable, swift, easy.

Setup of development environment:
The command centre of the robot could be a Raspberry Pi micro computer. Yet because cameras and motor control modules both require pins, the pins on a Raspberry Pi could be insufficient. An additional SCM could be used.
Raspberry Pi supports many programming languages, including Python, Java, C, C++, etc. We plan to use Python on the Raspberry Pi, because it is easy to use, and many AI functions and packages are best served with Python.
If an additional SCM should be used, it is better to program it with C, because it is easier to program a simple SCM with C, especially with I/O ports involved. Also, C is much faster.
