#!/usr/bin/env python3
"""Setup script for EmotionalTextureAnalyzer."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="emotionaltextureanalyzer",
    version="1.0.0",
    author="Logan Smith",
    author_email="logan@metaphy.ai",
    description="Analyze emotional texture and nuance in AI responses - beyond sentiment to qualitative experience",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/EmotionalTextureAnalyzer",
    py_modules=["emotionaltextureanalyzer"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses Python standard library only
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "emotionaltextureanalyzer=emotionaltextureanalyzer:main",
        ],
    },
    keywords=[
        "emotional-analysis",
        "sentiment-analysis",
        "ai-consciousness",
        "nlp",
        "text-analysis",
        "emotional-texture",
        "team-brain",
        "qualitative-analysis",
    ],
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/EmotionalTextureAnalyzer/issues",
        "Source": "https://github.com/DonkRonk17/EmotionalTextureAnalyzer",
        "Documentation": "https://github.com/DonkRonk17/EmotionalTextureAnalyzer#readme",
    },
)
