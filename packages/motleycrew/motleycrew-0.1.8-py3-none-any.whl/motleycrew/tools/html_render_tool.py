from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional

from motleycrew.common.utils import ensure_module_is_installed

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
except ImportError:
    webdriver = None
    Service = None

from langchain.tools import Tool
from langchain_core.pydantic_v1 import BaseModel, Field

from motleycrew.tools import MotleyTool
from motleycrew.common import logger


class HTMLRenderer:
    def __init__(
        self,
        work_dir: str,
        executable_path: str | None = None,
        headless: bool = True,
        window_size: Optional[Tuple[int, int]] = None,
    ):
        """Helper for rendering HTML code as an image"""
        ensure_module_is_installed(
            "selenium",
            "see documentation: https://pypi.org/project/selenium/, ChromeDriver is also required",
        )

        self.work_dir = Path(work_dir).resolve()
        self.html_dir = self.work_dir / "html"
        self.images_dir = self.work_dir / "images"

        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        self.service = Service(executable_path=executable_path)

        self.window_size = window_size

    def render_image(self, html: str, file_name: str | None = None):
        """Create image with png extension from html code

        Args:
            html (str): html code for rendering image
            file_name (str): file name with not extension
        Returns:
            file path to created image
        """
        logger.info("Trying to render image from HTML code")
        html_path, image_path = self.build_save_file_paths(file_name)
        browser = webdriver.Chrome(options=self.options, service=self.service)
        try:
            if self.window_size:
                logger.info("Setting window size to {}".format(self.window_size))
                browser.set_window_size(*self.window_size)

            url = "data:text/html;charset=utf-8,{}".format(html)
            browser.get(url)

            logger.info("Taking screenshot")
            is_created_img = browser.get_screenshot_as_file(image_path)
        finally:
            browser.close()
            browser.quit()

        if not is_created_img:
            logger.error("Failed to render image from HTML code {}".format(image_path))
            return "Failed to render image from HTML code"

        with open(html_path, "w") as f:
            f.write(html)
        logger.info("Saved the HTML code to {}".format(html_path))
        logger.info("Saved the rendered HTML screenshot to {}".format(image_path))

        return image_path

    def build_save_file_paths(self, file_name: str | None = None) -> Tuple[str, str]:
        """Builds paths to html and image files

        Args:
            file_name (str): file name with not extension

        Returns:
            tuple[str, str]: html file path and image file path
        """

        # check exists dirs:
        for _dir in (self.work_dir, self.html_dir, self.images_dir):
            if not _dir.exists():
                _dir.mkdir(parents=True)

        file_name = file_name or datetime.now().strftime("%Y_%m_%d__%H_%M")
        html_path = self.html_dir / "{}.html".format(file_name)
        image_path = self.images_dir / "{}.png".format(file_name)

        return str(html_path), str(image_path)


class HTMLRenderTool(MotleyTool):

    def __init__(
        self,
        work_dir: str,
        executable_path: str | None = None,
        headless: bool = True,
        window_size: Optional[Tuple[int, int]] = None,
    ):
        """Tool for rendering HTML as image

        Args:
            work_dir (str): Directory for saving images and html files
        """
        renderer = HTMLRenderer(
            work_dir=work_dir,
            executable_path=executable_path,
            headless=headless,
            window_size=window_size,
        )
        langchain_tool = create_render_tool(renderer)
        super(HTMLRenderTool, self).__init__(langchain_tool)


class HTMLRenderToolInput(BaseModel):
    """Input for the HTMLRenderTool.

    Attributes:
        html (str):
    """

    html: str = Field(description="HTML code for rendering")


def create_render_tool(renderer: HTMLRenderer):
    """Create langchain tool from HTMLRenderer.render_image method

    Returns:
        Tool:
    """
    return Tool.from_function(
        func=renderer.render_image,
        name="HTML rendering tool",
        description="A tool for rendering HTML code as an image",
        args_schema=HTMLRenderToolInput,
    )
