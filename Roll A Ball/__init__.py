from pyunity import *
import os

project = Loader.LoadProject(os.path.abspath(os.path.dirname(__file__)))
firstScene = SceneManager.GetSceneByIndex(project.firstScene)
