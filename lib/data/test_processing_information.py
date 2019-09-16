from .processing_information import ProcessingInformation

def test_initial_description():
    pi = ProcessingInformation()

    assert "https://github.com/HelgeKrueger/video" in pi.get_description()

def test_description_with_style_transfer():
    image_url = 'http://url'
    pi = ProcessingInformation()
    pi.set_style_transfer_image(image_url)

    description = pi.get_description()

    assert image_url in description
    assert "\n\n" in description

def test_description_with_style_transfer():
    image_url = 'http://url'
    pi = ProcessingInformation(filename='/tmp/test_file.json')
    pi.set_style_transfer_image(image_url)
    pi.save()

    pi2 = ProcessingInformation(filename='/tmp/test_file.json')
    assert image_url in pi2.get_description()

    pi2.done()

def test_calling_done_without_save():
    pi = ProcessingInformation()
    pi.done()
