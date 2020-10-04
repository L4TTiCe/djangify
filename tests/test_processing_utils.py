from djangify import processing_utils


def test_stylesheet_keywords_check_line():
    stylesheet_string = '<link rel="stylesheet" href="style.css">'
    processed_line = processing_utils.check_line(stylesheet_string)
    expected = [
        (True, 'href')
    ]
    assert processed_line == expected


def test_javascript_keyword_check_line():
    javascript_string = '<script src="js/bootstrap/bootstrap.min.js">' \
                        '</script> <script src="js/plugins/plugins.js"></script>'
    processed_line = processing_utils.check_line(javascript_string)
    expected = [
        (True, 'src')
    ]
    assert processed_line == expected


def test_image_keyword_check_line():
    image_string = '< img src = "img/img.jpg" alt = "Nice image" >'
    inline_image_string = ' <div class="hero-blog-post" ' \
                          'style="background-image: url(img/img.jpg);">'
    processed_image_tag = processing_utils.check_line(image_string)
    processed_inline_image_tag = processing_utils.check_line(inline_image_string)
    expected = [
        (True, 'src')
    ]
    expected_inline = [
        (True, 'url')
    ]
    assert processed_image_tag == expected
    assert processed_inline_image_tag == expected_inline


def test_null_check_line():
    random_string = "A lazy fox jumped over the brown frog"
    processed_random_string = processing_utils.check_line(random_string)
    assert processed_random_string is None


def test_contains_url():
    urls = [
        "https://ohuru.tech/",
        "https://abs.com/",
        "http://www.hello.com/",
        "abcd.cd",
        "https://github.io",
        "random_string",
        "string2"
    ]
    expected = [
        True,
        True,
        True,
        False,
        True,
        False,
        False
    ]
    result = [processing_utils.contains_url(url) for url in urls]
    assert result == expected


def test_get_index_on_stylesheet():
    stylesheet_string = '<link rel="stylesheet" href="style.css">'
    positions = processing_utils.get_index(
        stylesheet_string,
        "href"
    )
    expected = (29, 38)
    assert positions == expected


def test_get_index_on_javascript():
    javascript_string = '<script src="js/bootstrap/bootstrap.min.js">'
    positions = processing_utils.get_index(
        javascript_string,
        "src"
    )
    expected = (13, 42)
    assert positions == expected


def test_get_index_on_image():
    image_string = '< img src = "img/img.jpg" alt = "Nice image" >'
    positions = processing_utils.get_index(
        image_string,
        "src"
    )
    expected = (11, 30)
    assert positions == expected


def test_get_index_on_inline_image():
    inline_image_string = ' <div class="hero-blog-post" ' \
                          'style="background-image: url(img/img.jpg);">'
    positions = processing_utils.get_index(
        inline_image_string,
        "url"
    )
    expected = (58, 69)
    assert expected == positions


def test_process_line_on_external_link():
    image_external = '<img class="img-profile rounded-circle"' \
                     ' src="https://source.unsplash.com/NftWwc-oY2M/60x60">'
    result = processing_utils.process_line(image_external, '')
    assert result == image_external


def test_process_line_on_stylesheet():
    stylesheet_string = '<link rel="stylesheet" href="style.css">'
    expected = '<link rel="stylesheet" href=" {% static \'style.css\' %} ">'
    result = processing_utils.process_line(stylesheet_string, '')
    assert result == expected


def test_process_line_on_js():
    js_string = '<script src="js/bootstrap/bootstrap.min.js">'
    expected = '<script src=" {% static \'js/bootstrap/bootstrap.min.js\' %} ">'
    result = processing_utils.process_line(js_string, '')
    assert result == expected


def test_process_line_on_image():
    image_string = '< img src = "img/img.jpg" alt = "Nice image" >'
    expected = '< img src = {% static \' "img/img.jpg" alt \' %} = "Nice image" >'
    result = processing_utils.process_line(image_string, '')
    assert result == expected


def test_process_line_on_inline_image():
    inline_image_string = '<div style="background-image: url(img/img.jpg);">'
    expected = '<div style="background-image: url( {% static \'img/img.jpg\' %} );">'
    result = processing_utils.process_line(inline_image_string, '')
    assert result == expected


def test_process_stylesheet_with_app_name():
    # The main file automatically appends / at the end of app_name

    stylesheet_string = '<link rel="stylesheet" href="style.css">'
    expected = '<link rel="stylesheet" href=" {% static \'main/style.css\' %} ">'
    result = processing_utils.process_line(stylesheet_string, 'main/')
    assert result == expected
