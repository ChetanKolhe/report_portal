from logging import Logger
import os


def test_pass(rp_logger:Logger):
    rp_logger.info("Pass Test Case")
    assert "sample" == "sample", "Pass Message"


def test_fail(rp_logger:Logger):
    rp_logger.info("Pass Test Case")
    assert "sample" == "not sample", "Pass Message"

def test_attachment(rp_logger:Logger):
    rp_logger.info("Attachment test case")
    rp_logger.error("Attachemtn error ")


    image_path = os.path.join(os.path.dirname(__file__),"sample.jpg")
    with open(image_path, "rb") as image_file:
        rp_logger.info("Some Text Here",
                       attachment={"name": "test_name_screenshot.jpg",
                                   "data": image_file.read(),
                                   "mime": "image/png"})

    ini_file = os.path.join(os.path.dirname(__file__),"pytest.ini")
    with open(ini_file, "rb") as image_file:
        rp_logger.info("Some Text Here",
                       attachment={"name": "test_name_screenshot.ini",
                                   "data": image_file.read(),
                                   "mime": "application/octet-stream"})