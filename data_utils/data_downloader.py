import subprocess
from pathlib import Path

from loguru import logger

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


class DataDownloader:
    def __init__(self, urls, data_dir=BASE_DIR):
        self.urls = urls
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            Path.mkdir(self.data_dir)
        self.file_names = [Path(url).name for url in self.urls]
        self.file_paths = [self.data_dir / file_name for file_name in self.file_names]

    def download(self):
        for url, file in zip(self.urls, self.file_paths):
            self._download_single_url(url, file)

    def _download_single_url(self, url, file):
        if not file.exists():
            logger.info(f"Downloading {url} to {file}")
            try:
                subprocess.check_call(
                    [
                        "wget",
                        "-q",
                        "-c",
                        "--show-progress",
                        url,
                        "--no-check-certificate",
                        "-O",
                        str(file),
                    ]
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to download {url}: {e}")
        else:
            logger.info(f"Data file {file} already exists.")

    def unzip(self):
        for file in self.file_paths:
            self._unzip_single_file(file)

    def _unzip_single_file(self, file):
        logger.info(f"Unzipping {file}")
        try:
            subprocess.check_call(["unzip", str(file), "-d", str(self.data_dir)])
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to unzip {file}: {e}")

    def delete_zip(self):
        for file in self.file_paths:
            self._delete_single_zip(file)

    def _delete_single_zip(self, file):
        try:
            file.unlink()
            logger.info(f"Deleted zip file {file}")
        except FileNotFoundError:
            logger.warning(f"Zip file {file} not found.")


# ModelNet40Downloader
class ModelNet40Downloader(DataDownloader):
    def __init__(self, root_dir=ROOT_DIR):
        urls = ["https://shapenet.cs.stanford.edu/media/modelnet40_normal_resampled.zip"]
        data_dir = Path(root_dir) / "data" / "modelnet40"
        super().__init__(urls, data_dir=data_dir)


class ThreeDMatchDownloader(DataDownloader):
    def __init__(self, root_dir=ROOT_DIR):
        url = ["http://node2.chrischoy.org/data/datasets/registration/threedmatch.tgz"]
        data_dir = Path(root_dir) / "data" / "3DMatch"
        super().__init__(url, data_dir=data_dir)

    def _unzip_single_file(self, file):
        logger.info(f"Unzipping {file}")
        try:
            subprocess.check_call(["tar", "-xvzf", str(file), "-C", str(self.data_dir)])
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to unzip {file}: {e}")


class ThreeDMatchTestSceneDownloader(DataDownloader):
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
        urls = [f"{base_url}/{scene}.zip" for scene in scene_list]
        data_dir = Path(root_dir) / "data" / "3DMatch" / "fragments"
        super().__init__(urls, data_dir=data_dir)


if __name__ == "__main__":
    logger.add("logs/data.log")

    ThreeDMatch = ThreeDMatchDownloader()
    ThreeDMatch.download()
    ThreeDMatch.unzip()
    ThreeDMatch.delete_zip()

    ThreeDMatchTest = ThreeDMatchTestSceneDownloader()
    ThreeDMatchTest.download()
    ThreeDMatchTest.unzip()
    # ThreeDMatchTest.delete_zip()
