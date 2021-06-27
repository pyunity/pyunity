from pyunity import SceneManager

def main():
    scene = SceneManager.AddScene("Scene")

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
