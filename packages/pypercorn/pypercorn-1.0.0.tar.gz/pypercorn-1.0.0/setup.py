from distutils.core import setup
setup(
    name="pypercorn",
    packages=["pypercorn"],
    version="1.0.0",
    description="Easy wrapper for HyperCornAPI , and powerful API for image and spectrum processing.",
    long_description="This is a wrapper for HyperCornAPI, developed by HyperCorn. It serves as a foundational API designed for seamless integration with HyperCorn, an advanced application specializing in crop classification.",
    author="HyperCorn",
    author_email="hypercorncordoba@gmail.com",      # Type in your E-Mail
    url="https://github.com/HyperCorn/PyperCorn",
    download_url="https://github.com/HyperCorn/PyperCorn/releases/tag/v1.0.0",
    keywords=["IMAGES", "SPECTRUMS", "CROPS","SENTINEL"],
    install_requires=[            # I get to this in a second
        "requests", "msgpack_numpy", "numpy"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
)
