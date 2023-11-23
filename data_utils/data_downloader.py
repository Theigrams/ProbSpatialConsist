import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)


class DataDownloader:
    def __init__(self, url, data_dir=BASE_DIR, file_name=None):
        self.url = url
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if file_name is None:
            file_name = os.path.basename(self.url)
        self.file_path = os.path.join(self.data_dir, file_name)

    def download(self):
        if not os.path.exists(self.file_path):
            print(f"Downloading {self.url} to {self.file_path}")
            subprocess.check_call(
                ["wget", "-q", "-c", "--show-progress", self.url, "--no-check-certificate", "-O", self.file_path]
            )
        else:
            print(f"Data file {self.file_path} already exists.")

    def unzip(self):
        print(f"Unzipping {self.file_path}")
        subprocess.check_call(["unzip", self.file_path, "-d", self.data_dir])

    def delete_zip(self):
        os.remove(self.file_path)
        print(f"Deleted zip file {self.file_path}")


# ModelNet40Downloader
class ModelNet40Downloader(DataDownloader):
    def __init__(self, root_dir=ROOT_DIR):
        url = "https://shapenet.cs.stanford.edu/media/modelnet40_normal_resampled.zip"
        data_dir = os.path.join(root_dir, "data", "modelnet40")
        super().__init__(url, data_dir=data_dir, file_name="modelnet40.zip")


class ThreeDMatchDownloader(DataDownloader):
    def __init__(self, root_dir=ROOT_DIR):
        url = "http://node2.chrischoy.org/data/datasets/registration/threedmatch.tgz"
        data_dir = os.path.join(root_dir, "data", "3DMatch")
        super().__init__(url, data_dir=data_dir, file_name="threedmatch.tgz")

    def unzip(self):
        print(f"Unzipping {self.file_path}")
        subprocess.check_call(
            [
                "tar",
                "-xvzf",
                self.file_path,
                "-C",
                self.data_dir,
            ]
        )


class ThreeDMatchTestDownloader:
    def __init__(self, root_dir=ROOT_DIR):
        base_url = "http://vision.princeton.edu/projects/2016/3DMatch/downloads/scene-fragments"
        scene_list = [
            "7-scenes-redkitchen",
            "7-scenes-redkitchen-evaluation",
            "sun3d-home_at-home_at_scan1_2013_jan_1",
            "sun3d-home_at-home_at_scan1_2013_jan_1-evaluation",
            "sun3d-home_md-home_md_scan9_2012_sep_30",
            "sun3d-home_md-home_md_scan9_2012_sep_30-evaluation",
            "sun3d-hotel_uc-scan3",
            "sun3d-hotel_uc-scan3-evaluation",
            "sun3d-hotel_umd-maryland_hotel1",
            "sun3d-hotel_umd-maryland_hotel1-evaluation",
            "sun3d-hotel_umd-maryland_hotel3",
            "sun3d-hotel_umd-maryland_hotel3-evaluation",
            "sun3d-mit_76_studyroom-76-1studyroom2",
            "sun3d-mit_76_studyroom-76-1studyroom2-evaluation",
            "sun3d-mit_lab_hj-lab_hj_tea_nov_2_2012_scan1_erika",
            "sun3d-mit_lab_hj-lab_hj_tea_nov_2_2012_scan1_erika-evaluation",
        ]
        self.urls = [f"{base_url}/{scene}.zip" for scene in scene_list]
        data_dir = os.path.join(root_dir, "data", "3DMatch", "fragments")
        self.scene_downloaders = [DataDownloader(url, data_dir=data_dir) for url in self.urls]

    def download(self):
        for scene_downloader in self.scene_downloaders:
            scene_downloader.download()

    def unzip(self):
        for scene_downloader in self.scene_downloaders:
            scene_downloader.unzip()

    def delete_zip(self):
        for scene_downloader in self.scene_downloaders:
            scene_downloader.delete_zip()


class TestDownloader(DataDownloader):
    def __init__(self, root_dir=ROOT_DIR):
        url = "http://vision.princeton.edu/projects/2016/3DMatch/downloads/scene-fragments/7-scenes-redkitchen.zip"
        data_dir = os.path.join(root_dir, "data", "modelnet40")
        super().__init__(url, data_dir=data_dir)


if __name__ == "__main__":
    ThreeDMatch = ThreeDMatchDownloader()
    ThreeDMatch.download()
    ThreeDMatch.unzip()
    # ThreeDMatch.delete_zip()

    ThreeDMatchTest = ThreeDMatchTestDownloader()
    ThreeDMatchTest.download()
    ThreeDMatchTest.unzip()
