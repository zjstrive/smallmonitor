from selenium import webdriver
import unittest
import time


class SmallMonitor(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://0.0.0.0:2332/")

    def test_home_manager_page(self):
        self.assertIn("Small Monitor", self.driver.title)
        time.sleep(5)
        self.driver.find_element_by_id("filter").send_keys("test6")
        manager_url = self.driver.find_element_by_name("operation_app").get_attribute("href")
        time.sleep(5)
        self.driver.get(manager_url)
        self.assertIn("Manger", self.driver.title)
        time.sleep(5)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
