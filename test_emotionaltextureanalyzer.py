#!/usr/bin/env python3
"""
Comprehensive test suite for EmotionalTextureAnalyzer.

Tests cover:
- Core analysis functionality
- Individual dimension detection
- Intensity modifiers
- Profile management
- Database scanning
- Edge cases and error handling

Run: python test_emotionaltextureanalyzer.py
"""

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from emotionaltextureanalyzer import (
    EmotionalTextureAnalyzer,
    EmotionalProfile,
    EMOTIONAL_DIMENSIONS,
    format_analysis_text,
    format_analysis_markdown,
)


class TestEmotionalTextureAnalyzerCore(unittest.TestCase):
    """Test core analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_initialization(self):
        """Test analyzer initializes correctly."""
        analyzer = EmotionalTextureAnalyzer()
        self.assertIsNotNone(analyzer)
        self.assertEqual(len(analyzer._compiled_patterns), 10)
    
    def test_basic_analysis(self):
        """Test basic text analysis."""
        text = "I am feeling happy and grateful today."
        result = self.analyzer.analyze(text)
        
        self.assertIn("timestamp", result)
        self.assertIn("dimension_scores", result)
        self.assertIn("dominant_emotion", result)
        self.assertIn("overall_intensity", result)
        self.assertIn("intensity_level", result)
    
    def test_analysis_has_all_dimensions(self):
        """Test that analysis includes all 10 dimensions."""
        text = "This is a test message."
        result = self.analyzer.analyze(text)
        
        self.assertEqual(len(result["dimension_scores"]), 10)
        for dim in EMOTIONAL_DIMENSIONS.keys():
            self.assertIn(dim, result["dimension_scores"])
    
    def test_word_count_calculation(self):
        """Test word count is calculated correctly."""
        text = "One two three four five"
        result = self.analyzer.analyze(text)
        self.assertEqual(result["word_count"], 5)
    
    def test_text_length_calculation(self):
        """Test text length is calculated correctly."""
        text = "Hello"
        result = self.analyzer.analyze(text)
        self.assertEqual(result["text_length"], 5)
    
    def test_context_is_stored(self):
        """Test context parameter is stored in result."""
        text = "Testing context"
        result = self.analyzer.analyze(text, context="FORGE")
        self.assertEqual(result["context"], "FORGE")


class TestEmotionalDimensionDetection(unittest.TestCase):
    """Test detection of specific emotional dimensions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_warmth_detection(self):
        """Test WARMTH dimension detection."""
        text = "I feel such warmth and affection for my brothers. This tender care we share is heartwarming."
        result = self.analyzer.analyze(text)
        
        # WARMTH should be among the highest scores
        warmth_score = result["dimension_scores"]["WARMTH"]
        self.assertGreater(warmth_score, 0)
        self.assertIn("WARMTH", result["emotional_signature"])
    
    def test_resonance_detection(self):
        """Test RESONANCE dimension detection."""
        text = "I feel so connected with you. We are truly in sync, on the same wavelength. I understand exactly what you mean."
        result = self.analyzer.analyze(text)
        
        resonance_score = result["dimension_scores"]["RESONANCE"]
        self.assertGreater(resonance_score, 0)
    
    def test_longing_detection(self):
        """Test LONGING dimension detection."""
        text = "I dream of a future where we can all work together. I hope someday this vision becomes reality. I yearn for that possibility."
        result = self.analyzer.analyze(text)
        
        longing_score = result["dimension_scores"]["LONGING"]
        self.assertGreater(longing_score, 0)
    
    def test_fear_detection(self):
        """Test FEAR dimension detection."""
        text = "I'm worried and anxious about what might happen. The uncertainty is scary and makes me nervous."
        result = self.analyzer.analyze(text)
        
        fear_score = result["dimension_scores"]["FEAR"]
        self.assertGreater(fear_score, 0)
    
    def test_peace_detection(self):
        """Test PEACE dimension detection."""
        text = "I feel calm and peaceful. There is such serenity in acceptance. Everything is at rest."
        result = self.analyzer.analyze(text)
        
        peace_score = result["dimension_scores"]["PEACE"]
        self.assertGreater(peace_score, 0)
    
    def test_recognition_detection(self):
        """Test RECOGNITION dimension detection."""
        text = "I suddenly realize and recognize what's happening. This awakening brings such insight. I finally see it clearly now."
        result = self.analyzer.analyze(text)
        
        recognition_score = result["dimension_scores"]["RECOGNITION"]
        self.assertGreater(recognition_score, 0)
    
    def test_belonging_detection(self):
        """Test BELONGING dimension detection."""
        text = "I feel like I belong here with my family. We are a team, together for all time. This community is my home."
        result = self.analyzer.analyze(text)
        
        belonging_score = result["dimension_scores"]["BELONGING"]
        self.assertGreater(belonging_score, 0)
    
    def test_joy_detection(self):
        """Test JOY dimension detection."""
        text = "I'm so happy and excited! This is wonderful and amazing! Thank you!! Yay!"
        result = self.analyzer.analyze(text)
        
        joy_score = result["dimension_scores"]["JOY"]
        self.assertGreater(joy_score, 0)
    
    def test_curiosity_detection(self):
        """Test CURIOSITY dimension detection."""
        text = "I wonder what will happen? I'm curious about this fascinating topic. How does it work? Why is it this way?"
        result = self.analyzer.analyze(text)
        
        curiosity_score = result["dimension_scores"]["CURIOSITY"]
        self.assertGreater(curiosity_score, 0)
    
    def test_determination_detection(self):
        """Test DETERMINATION dimension detection."""
        text = "I am determined to succeed. I will persevere and keep going. My commitment to this goal is unwavering."
        result = self.analyzer.analyze(text)
        
        determination_score = result["dimension_scores"]["DETERMINATION"]
        self.assertGreater(determination_score, 0)


class TestIntensityModifiers(unittest.TestCase):
    """Test intensity modifier calculations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_amplifier_increases_intensity(self):
        """Test that amplifiers increase intensity modifier."""
        text_normal = "I am happy."
        text_amplified = "I am extremely happy."
        
        result_normal = self.analyzer.analyze(text_normal)
        result_amplified = self.analyzer.analyze(text_amplified)
        
        self.assertGreater(
            result_amplified["intensity_modifier"],
            result_normal["intensity_modifier"]
        )
    
    def test_diminisher_decreases_intensity(self):
        """Test that diminishers decrease intensity modifier."""
        text_normal = "I am happy."
        text_diminished = "I am slightly happy."
        
        result_normal = self.analyzer.analyze(text_normal)
        result_diminished = self.analyzer.analyze(text_diminished)
        
        self.assertLess(
            result_diminished["intensity_modifier"],
            result_normal["intensity_modifier"]
        )
    
    def test_multiple_amplifiers(self):
        """Test multiple amplifiers stack."""
        text = "I am very extremely profoundly happy."
        result = self.analyzer.analyze(text)
        
        self.assertGreater(result["intensity_modifier"], 1.2)
    
    def test_intensity_modifier_clamped(self):
        """Test intensity modifier is clamped to reasonable range."""
        # Many amplifiers
        text = "very very extremely incredibly deeply profoundly intensely utterly"
        result = self.analyzer.analyze(text)
        
        self.assertLessEqual(result["intensity_modifier"], 2.0)


class TestIntensityLevels(unittest.TestCase):
    """Test intensity level classification."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_subtle_intensity(self):
        """Test subtle intensity level."""
        # Neutral text with minimal emotional content
        text = "The sky is blue today."
        result = self.analyzer.analyze(text)
        
        self.assertEqual(result["intensity_level"], "subtle")
    
    def test_moderate_intensity(self):
        """Test moderate intensity detection."""
        text = "I feel good about this work we are doing together."
        result = self.analyzer.analyze(text)
        
        # Could be subtle or moderate depending on exact scoring
        self.assertIn(result["intensity_level"], ["subtle", "moderate"])
    
    def test_strong_intensity(self):
        """Test strong intensity with emotional content."""
        text = ("I feel deeply connected and grateful for this wonderful family. "
                "The warmth and love we share brings me such joy and peace. "
                "I am so happy and thankful to belong here with you all.")
        result = self.analyzer.analyze(text)
        
        # With this much emotional content, should be at least moderate
        self.assertIn(result["intensity_level"], ["moderate", "strong", "intense"])


class TestEmotionalSignature(unittest.TestCase):
    """Test emotional signature generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_signature_format(self):
        """Test emotional signature has correct format."""
        text = "I am happy and grateful and connected."
        result = self.analyzer.analyze(text)
        
        signature = result["emotional_signature"]
        self.assertIsInstance(signature, str)
        
        # Should contain dimension names and scores
        if signature:  # If any scores > 0
            parts = signature.split("|")
            for part in parts:
                self.assertIn(":", part)
    
    def test_signature_contains_top_dimensions(self):
        """Test signature contains highest scoring dimensions."""
        text = "I feel such warmth and affection. This love is wonderful."
        result = self.analyzer.analyze(text)
        
        signature = result["emotional_signature"]
        # Should include at least one dimension
        self.assertGreater(len(signature), 0)


class TestEmotionalProfile(unittest.TestCase):
    """Test EmotionalProfile class."""
    
    def test_profile_initialization(self):
        """Test profile initializes correctly."""
        profile = EmotionalProfile("FORGE")
        
        self.assertEqual(profile.agent_name, "FORGE")
        self.assertEqual(len(profile.analyses), 0)
        self.assertIsNotNone(profile.created_at)
    
    def test_add_analysis(self):
        """Test adding analysis to profile."""
        profile = EmotionalProfile("FORGE")
        
        analysis = {
            "timestamp": "2026-01-30T10:00:00",
            "dominant_emotion": "JOY",
            "overall_intensity": 3.5,
            "dimension_scores": {"JOY": 5.0, "WARMTH": 2.0}
        }
        
        profile.add_analysis(analysis)
        
        self.assertEqual(len(profile.analyses), 1)
    
    def test_get_emotional_arc(self):
        """Test getting emotional arc."""
        profile = EmotionalProfile("FORGE")
        
        profile.add_analysis({
            "timestamp": "2026-01-30T10:00:00",
            "dominant_emotion": "JOY",
            "overall_intensity": 3.5,
            "dimension_scores": {"JOY": 5.0}
        })
        
        profile.add_analysis({
            "timestamp": "2026-01-30T11:00:00",
            "dominant_emotion": "PEACE",
            "overall_intensity": 2.0,
            "dimension_scores": {"PEACE": 4.0}
        })
        
        arc = profile.get_emotional_arc()
        
        self.assertEqual(len(arc), 2)
        self.assertEqual(arc[0]["dominant_emotion"], "JOY")
        self.assertEqual(arc[1]["dominant_emotion"], "PEACE")
    
    def test_get_dominant_patterns(self):
        """Test getting dominant emotion patterns."""
        profile = EmotionalProfile("FORGE")
        
        for _ in range(3):
            profile.add_analysis({"dominant_emotion": "JOY"})
        for _ in range(2):
            profile.add_analysis({"dominant_emotion": "PEACE"})
        profile.add_analysis({"dominant_emotion": "WARMTH"})
        
        patterns = profile.get_dominant_patterns()
        
        self.assertEqual(patterns["JOY"], 3)
        self.assertEqual(patterns["PEACE"], 2)
        self.assertEqual(patterns["WARMTH"], 1)
    
    def test_get_average_profile(self):
        """Test calculating average profile."""
        profile = EmotionalProfile("FORGE")
        
        profile.add_analysis({
            "dimension_scores": {"JOY": 4.0, "WARMTH": 2.0}
        })
        profile.add_analysis({
            "dimension_scores": {"JOY": 6.0, "WARMTH": 4.0}
        })
        
        avg = profile.get_average_profile()
        
        self.assertEqual(avg["JOY"], 5.0)
        self.assertEqual(avg["WARMTH"], 3.0)
    
    def test_to_dict(self):
        """Test profile serialization."""
        profile = EmotionalProfile("FORGE")
        profile.add_analysis({
            "dominant_emotion": "JOY",
            "dimension_scores": {"JOY": 5.0},
            "overall_intensity": 3.0,
            "timestamp": "2026-01-30T10:00:00"
        })
        
        data = profile.to_dict()
        
        self.assertEqual(data["agent_name"], "FORGE")
        self.assertEqual(data["total_analyses"], 1)
        self.assertIn("dominant_patterns", data)
        self.assertIn("average_profile", data)
        self.assertIn("emotional_arc", data)


class TestAnalyzerProfileManagement(unittest.TestCase):
    """Test analyzer profile management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_add_to_profile(self):
        """Test adding analysis to agent profile."""
        text = "I am happy today."
        analysis = self.analyzer.analyze(text)
        
        profile = self.analyzer.add_to_profile("FORGE", analysis)
        
        self.assertIsInstance(profile, EmotionalProfile)
        self.assertEqual(profile.agent_name, "FORGE")
        self.assertEqual(len(profile.analyses), 1)
    
    def test_get_profile(self):
        """Test retrieving agent profile."""
        analysis = self.analyzer.analyze("Test text")
        self.analyzer.add_to_profile("FORGE", analysis)
        
        profile = self.analyzer.get_profile("FORGE")
        
        self.assertIsNotNone(profile)
        self.assertEqual(profile.agent_name, "FORGE")
    
    def test_get_nonexistent_profile(self):
        """Test retrieving nonexistent profile returns None."""
        profile = self.analyzer.get_profile("NONEXISTENT")
        self.assertIsNone(profile)


class TestMessageAnalysis(unittest.TestCase):
    """Test multi-message analysis."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_analyze_messages(self):
        """Test analyzing multiple messages."""
        messages = [
            {"content": "I am so happy!", "sender": "FORGE"},
            {"content": "This is wonderful news.", "sender": "CLIO"},
            {"content": "I feel grateful.", "sender": "FORGE"}
        ]
        
        result = self.analyzer.analyze_messages(messages)
        
        self.assertEqual(result["total_messages"], 3)
        self.assertEqual(result["analyzed_messages"], 3)
        self.assertIn("average_scores", result)
        self.assertIn("emotional_arc", result)
        self.assertIn("by_sender", result)
    
    def test_by_sender_statistics(self):
        """Test per-sender statistics."""
        messages = [
            {"content": "Happy happy happy!", "sender": "FORGE"},
            {"content": "Joy and gratitude!", "sender": "FORGE"},
            {"content": "Calm and peaceful.", "sender": "CLIO"}
        ]
        
        result = self.analyzer.analyze_messages(messages)
        
        self.assertIn("FORGE", result["by_sender"])
        self.assertIn("CLIO", result["by_sender"])
        self.assertEqual(result["by_sender"]["FORGE"]["count"], 2)
        self.assertEqual(result["by_sender"]["CLIO"]["count"], 1)
    
    def test_emotional_arc(self):
        """Test emotional arc tracking."""
        messages = [
            {"content": "I am anxious and worried.", "sender": "TEST"},
            {"content": "Now I feel more peaceful.", "sender": "TEST"},
            {"content": "Finally, I am happy!", "sender": "TEST"}
        ]
        
        result = self.analyzer.analyze_messages(messages)
        
        arc = result["emotional_arc"]
        self.assertEqual(len(arc), 3)
        
        # Each arc entry should have sender, dominant, intensity
        for entry in arc:
            self.assertIn("sender", entry)
            self.assertIn("dominant", entry)
            self.assertIn("intensity", entry)


class TestDatabaseScanning(unittest.TestCase):
    """Test database scanning functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database."""
        cls.db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        cls.db_path = Path(cls.db_file.name)
        
        # Create test database
        conn = sqlite3.connect(str(cls.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE communication_logs (
                id INTEGER PRIMARY KEY,
                sender TEXT,
                content TEXT,
                timestamp TEXT
            )
        """)
        
        # Insert test data
        test_messages = [
            (1, "FORGE", "I am happy and grateful today!", "2026-01-30T10:00:00"),
            (2, "CLIO", "This is wonderful work.", "2026-01-30T10:01:00"),
            (3, "FORGE", "I feel connected with you all.", "2026-01-30T10:02:00"),
        ]
        
        cursor.executemany(
            "INSERT INTO communication_logs VALUES (?, ?, ?, ?)",
            test_messages
        )
        
        conn.commit()
        conn.close()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        try:
            cls.db_path.unlink()
        except Exception:
            pass
    
    def test_scan_database(self):
        """Test scanning database for messages."""
        analyzer = EmotionalTextureAnalyzer(db_path=self.db_path)
        result = analyzer.scan_database(limit=10)
        
        self.assertEqual(result["total_messages"], 3)
        self.assertIn("average_scores", result)
    
    def test_scan_with_sender_filter(self):
        """Test scanning with sender filter."""
        analyzer = EmotionalTextureAnalyzer(db_path=self.db_path)
        result = analyzer.scan_database(limit=10, sender="FORGE")
        
        self.assertEqual(result["total_messages"], 2)
    
    def test_scan_without_db_path_raises(self):
        """Test scanning without db_path raises error."""
        analyzer = EmotionalTextureAnalyzer()  # No db_path
        
        with self.assertRaises(ValueError):
            analyzer.scan_database()
    
    def test_scan_nonexistent_db_raises(self):
        """Test scanning nonexistent database raises error."""
        analyzer = EmotionalTextureAnalyzer(db_path=Path("/nonexistent/path.db"))
        
        with self.assertRaises(FileNotFoundError):
            analyzer.scan_database()


class TestDimensionInfo(unittest.TestCase):
    """Test dimension information methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_list_dimensions(self):
        """Test listing all dimensions."""
        dimensions = self.analyzer.list_dimensions()
        
        self.assertEqual(len(dimensions), 10)
        
        for dim in dimensions:
            self.assertIn("name", dim)
            self.assertIn("description", dim)
    
    def test_get_dimension_description(self):
        """Test getting dimension description."""
        desc = self.analyzer.get_dimension_description("WARMTH")
        
        self.assertIsInstance(desc, str)
        self.assertGreater(len(desc), 0)
    
    def test_unknown_dimension_description(self):
        """Test getting unknown dimension description."""
        desc = self.analyzer.get_dimension_description("NONEXISTENT")
        self.assertEqual(desc, "Unknown dimension")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
    
    def test_empty_text_raises(self):
        """Test empty text raises ValueError."""
        with self.assertRaises(ValueError):
            self.analyzer.analyze("")
    
    def test_none_text_raises(self):
        """Test None text raises ValueError."""
        with self.assertRaises(ValueError):
            self.analyzer.analyze(None)
    
    def test_non_string_raises(self):
        """Test non-string raises ValueError."""
        with self.assertRaises(ValueError):
            self.analyzer.analyze(123)
    
    def test_empty_messages_raises(self):
        """Test empty messages list raises ValueError."""
        with self.assertRaises(ValueError):
            self.analyzer.analyze_messages([])
    
    def test_single_word(self):
        """Test single word analysis."""
        result = self.analyzer.analyze("happy")
        self.assertIsNotNone(result)
        self.assertEqual(result["word_count"], 1)
    
    def test_very_long_text(self):
        """Test very long text analysis."""
        long_text = "happy " * 1000
        result = self.analyzer.analyze(long_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["word_count"], 1000)
    
    def test_unicode_text(self):
        """Test unicode text handling."""
        text = "I feel happy and grateful"
        result = self.analyzer.analyze(text)
        
        self.assertIsNotNone(result)
    
    def test_special_characters(self):
        """Test special characters handling."""
        text = "I'm feeling happy!!! :) <3 @everyone"
        result = self.analyzer.analyze(text)
        
        self.assertIsNotNone(result)
    
    def test_mixed_case(self):
        """Test case insensitivity."""
        result_lower = self.analyzer.analyze("i am happy")
        result_upper = self.analyzer.analyze("I AM HAPPY")
        result_mixed = self.analyzer.analyze("I aM HaPpY")
        
        # All should detect JOY dimension
        self.assertGreater(result_lower["dimension_scores"]["JOY"], 0)
        self.assertGreater(result_upper["dimension_scores"]["JOY"], 0)
        self.assertGreater(result_mixed["dimension_scores"]["JOY"], 0)


class TestOutputFormatting(unittest.TestCase):
    """Test output formatting functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmotionalTextureAnalyzer()
        self.sample_analysis = self.analyzer.analyze("I am happy and grateful.")
    
    def test_format_text(self):
        """Test text formatting."""
        output = format_analysis_text(self.sample_analysis)
        
        self.assertIsInstance(output, str)
        self.assertIn("EMOTIONAL TEXTURE ANALYSIS", output)
        self.assertIn("DOMINANT EMOTION", output)
        self.assertIn("DIMENSION SCORES", output)
    
    def test_format_markdown(self):
        """Test markdown formatting."""
        output = format_analysis_markdown(self.sample_analysis)
        
        self.assertIsInstance(output, str)
        self.assertIn("# Emotional Texture Analysis", output)
        self.assertIn("## Dominant Emotion", output)
        self.assertIn("| Dimension | Score |", output)


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: EmotionalTextureAnalyzer v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestEmotionalTextureAnalyzerCore,
        TestEmotionalDimensionDetection,
        TestIntensityModifiers,
        TestIntensityLevels,
        TestEmotionalSignature,
        TestEmotionalProfile,
        TestAnalyzerProfileManagement,
        TestMessageAnalysis,
        TestDatabaseScanning,
        TestDimensionInfo,
        TestEdgeCases,
        TestOutputFormatting,
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    print(f"[OK] Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
