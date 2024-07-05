from setuptools import setup


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="audio-dataset-converter-all",
    description="Meta-library that combines all audio-dataset-converter libraries.",
    long_description=(
            _read('DESCRIPTION.rst') + b'\n' +
            _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-llm/audio-dataset-converter-all",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
    ],
    license='MIT License',
    install_requires=[
        "audio-dataset-converter>=0.0.1",
        "audio-dataset-converter-faster-whisper>=0.0.1",
        "audio-dataset-converter-redis>=0.0.1",
        "audio-dataset-converter-visualization>=0.0.1",
    ],
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
)
