import tesserpy, cv2
class captcha_utils: 
    def __init__(self, filename = 'vcode.jpg'):
        self.filename = filename
        pass
    
    def verifyCode(self):
        import platform,os
        if platform.system() == 'Darwin':
            tesser = tesserpy.Tesseract('/usr/local/share/tessdata/', language="eng")
        else:
            tesser = tesserpy.Tesseract("/usr/share/tessdata/", language="eng")
        tesser.tessedit_char_whitelist = ""'"!@#$%^&*()_+-=[]{};,.<>/?`~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"""
        path = os.path.dirname(os.path.abspath(__file__))
        img = cv2.imread(path + "/vcode.jpg", cv2.IMREAD_GRAYSCALE)
        tesser.set_image(img);
        page_info = tesser.orientation();
        print(page_info)
        return tesser.get_utf8_text()

if __name__ == '__main__':
    validator = captcha_utils(); 
    print(validator.verifyCode())