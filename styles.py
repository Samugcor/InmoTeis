
def load_stylesheet():
    with open('styles.qss', 'r') as style_file:
        return style_file.read()