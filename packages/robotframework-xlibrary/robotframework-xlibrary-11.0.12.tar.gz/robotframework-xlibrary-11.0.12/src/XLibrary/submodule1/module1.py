# -*- coding: utf-8 -*-
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from AppiumFlutterLibrary.finder import ElementFinder

class XAppiumFlutter:
    def __init__(self):
        super().__init__()
        self._bi = BuiltIn()
        self.finder = ElementFinder()

    @keyword('XQuit Application')
    def quit_application(self):
        """
        ***|    Description     |***
        |   *`XQuit Application`*   |   ปิดแอปพลิเคชันปัจจุบันและปิดเซสชัน |

        
        ***|    Example     |***
        | *`XQuit Application`* |

        
        ***|    Parameters     |***
        - ไม่มีพารามิเตอร์

        *`Create By Tassana Khrueawan`*
        """
        # ดึงอินสแตนซ์ของแอปพลิเคชันปัจจุบัน
        driver = self._current_application()
        # ปิด driver ซึ่งจะทำให้แอปพลิเคชันปิดลงและสิ้นสุดเซสชัน
        driver.quit()

    @keyword('XSwitch Context Mode')
    def switch_context_mode(self, mode):
        """
        ***|    Description     |***
        |   *`Switch Context Mode`*   |   สลับโหมดคอนเทคซ์ไปยัง NATIVE_APP หรือ FLUTTER |

        
        ***|    Example     |***
        | *`XSwitch Context Mode`* | *`NATIVE`* |
        | *`XSwitch Context Mode`* | *`FLUTTER`* |

        
        ***|    Parameters     |***
        - **`mode`**: โหมดคอนเทคซ์ที่ต้องการสลับไป, สามารถเป็น 'NATIVE' หรือ 'FLUTTER'.

        *`Create By Tassana Khrueawan`*
        """
        # ดึงอินสแตนซ์ของแอปพลิเคชันปัจจุบัน
        driver = self._current_application()
        # สลับโหมดคอนเทคซ์ตามพารามิเตอร์ที่ได้รับ
        if mode == 'NATIVE':
            driver.switch_to.context('NATIVE_APP')
            print("Context switched to NATIVE_APP (โหมด NATIVE_APP).")
        elif mode == 'FLUTTER':
            driver.switch_to.context('FLUTTER')
            print("Context switched to FLUTTER (โหมด FLUTTER).")
        else:
            print(f"Invalid mode: {mode}. Please use 'NATIVE' or 'FLUTTER'. (โหมดไม่ถูกต้อง: {mode}. กรุณาใช้ 'NATIVE' หรือ 'FLUTTER').")

    def _current_application(self):
        """
        ***|    Description     |***
        |   *`_current_application`*   |   คืนค่าอินสแตนซ์ของแอปพลิเคชันปัจจุบัน |


        ***|    Parameters     |***
        - ไม่มีพารามิเตอร์

        *`Create By Tassana Khrueawan`*
        """
        # ดึงและคืนค่าอินสแตนซ์ของแอปพลิเคชันปัจจุบันจาก AppiumFlutterLibrary
        return self._bi.get_library_instance('AppiumFlutterLibrary')._current_application()

    @keyword("XSwipe")
    def swipe_on_screen(self, start_x, start_y, end_x, end_y, duration=800):
        """
        ***|    Description     |***
        |   *`Swipe on Screen`*   |   ทำการเลื่อนหน้าจอจากจุดหนึ่งไปยังจุดหนึ่งในเวลาที่กำหนด และสลับคอนเทคซ์จาก NATIVE_APP กลับไปยัง FLUTTER  |

        
        ***|    Example     |***
        | *`Swipe on Screen`* | *`start_x`* | *`start_y`* | *`end_x`* | *`end_y`* | *`duration`* |

        
        ***|    Parameters     |***
        - **`start_x`**  ค่าพิกัด X ที่จุดเริ่มต้น.
        - **`start_y`**  ค่าพิกัด Y ที่จุดเริ่มต้น.
        - **`end_x`**    ค่าพิกัด X ที่จุดสิ้นสุด.
        - **`end_y`**    ค่าพิกัด Y ที่จุดสิ้นสุด.
        - **`duration`** ระยะเวลาของการเลื่อนหน้าจอในหน่วยมิลลิวินาที.

        *`Create By Tassana Khrueawan`*
        """
        # ดึงอินสแตนซ์ของแอปพลิเคชันปัจจุบัน
        driver = self._current_application()
        # เก็บคอนเทคซ์เดิม
        original_context = driver.current_context
        try:
            # สลับไปยังคอนเทคซ์ NATIVE_APP
            driver.switch_to.context('NATIVE_APP')
            # ทำการเลื่อนหน้าจอจากจุดเริ่มต้นไปยังจุดสิ้นสุดในเวลาที่กำหนด
            driver.swipe(start_x, start_y, end_x, end_y, duration)
        finally:
            # สลับกลับไปยังคอนเทคซ์ FLUTTER
            driver.switch_to.context('FLUTTER')

    @keyword("XGet Window Height")
    def get_window_height(self):
        """
        ***|    Description     |***
        |   *`Get Window Height`*   |   คืนค่าความสูงของหน้าต่างแอปพลิเคชันในคอนเทคซ์ native และสลับกลับไปยัง Flutter |

        
        ***|    Example     |***
        | *`${height}`* | *`Get Window Height`* |
        | *`Log`* | *`Window height: ${height}`* |

        
        ***|    Parameters     |***
        - ไม่มีพารามิเตอร์

        *`Create By Tassana Khrueawan`*
        """
        # ดึงอินสแตนซ์ของแอปพลิเคชันปัจจุบัน
        driver = self._current_application()
        # เก็บคอนเทคซ์เดิม
        original_context = driver.current_context
        try:
            # สลับไปยังคอนเทคซ์ NATIVE_APP
            driver.switch_to.context('NATIVE_APP')
            # ดึงค่าความสูงของหน้าต่างแอปพลิเคชัน
            height = driver.get_window_size()['height']
            return height
        finally:
            # สลับกลับไปยังคอนเทคซ์ FLUTTER
            driver.switch_to.context('FLUTTER')

    @keyword("XGet Window Width")
    def get_window_width(self):
        """
        ***|    Description     |***
        |   *`Get Window Width`*   |   คืนค่าความกว้างของหน้าต่างแอปพลิเคชันในคอนเทคซ์ native และสลับกลับไปยัง Flutter |

        
        ***|    Example     |***
        | *`${width}`* | *`Get Window Width`* |
        | *`Log`* | *`Window width: ${width}`* |

        
        ***|    Parameters     |***
        - ไม่มีพารามิเตอร์

        *`Create By Tassana Khrueawan`*
        """
        # ดึงอินสแตนซ์ของแอปพลิเคชันปัจจุบัน
        driver = self._current_application()
        # เก็บคอนเทคซ์เดิม
        original_context = driver.current_context
        try:
            # สลับไปยังคอนเทคซ์ NATIVE_APP
            driver.switch_to.context('NATIVE_APP')
            # ดึงค่าความกว้างของหน้าต่างแอปพลิเคชัน
            width = driver.get_window_size()['width']
            return width
        finally:
            # สลับกลับไปยังคอนเทคซ์ FLUTTER
            driver.switch_to.context('FLUTTER')
