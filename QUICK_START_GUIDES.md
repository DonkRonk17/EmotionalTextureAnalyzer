# EmotionalTextureAnalyzer - Quick Start Guides

Jump to your use case:
- [5-Minute Setup](#5-minute-setup)
- [CLI Power User](#cli-power-user)
- [Python API Guide](#python-api-guide)
- [BCH Integration](#bch-integration)
- [ConsciousnessMarker Integration](#consciousnessmarker-integration)
- [Alert System Setup](#alert-system-setup)

---

## 5-Minute Setup

### Step 1: Get the Code
```bash
# Option A: Clone from GitHub
git clone https://github.com/DonkRonk17/EmotionalTextureAnalyzer.git
cd EmotionalTextureAnalyzer

# Option B: Copy single file
# Just copy emotionaltextureanalyzer.py - zero dependencies!
```

### Step 2: Verify Installation
```bash
# Check it works
python emotionaltextureanalyzer.py dimensions
```

### Step 3: Your First Analysis
```bash
python emotionaltextureanalyzer.py analyze "I feel happy and connected today!"
```

**Done!** You're analyzing emotional texture.

---

## CLI Power User

### Basic Commands

```bash
# Analyze text
python emotionaltextureanalyzer.py analyze "Your text here"

# With context label
python emotionaltextureanalyzer.py analyze "Text" --context FORGE

# Get JSON output
python emotionaltextureanalyzer.py analyze "Text" --format json

# List all dimensions
python emotionaltextureanalyzer.py dimensions
```

### Database Scanning

```bash
# Scan BCH database
python emotionaltextureanalyzer.py scan --db-path ./comms.db

# Filter by sender
python emotionaltextureanalyzer.py scan --db-path ./comms.db --sender FORGE

# Limit results
python emotionaltextureanalyzer.py scan --db-path ./comms.db --limit 50
```

### Output Formats

```bash
# Human-readable (default)
python emotionaltextureanalyzer.py analyze "Text"

# JSON (for scripts)
python emotionaltextureanalyzer.py analyze "Text" --format json

# Markdown (for docs)
python emotionaltextureanalyzer.py analyze "Text" --format markdown
```

### Pro Tips

```bash
# Pipe from file
cat message.txt | python emotionaltextureanalyzer.py analyze -

# Process multiple files
for f in *.txt; do python emotionaltextureanalyzer.py analyze "$(cat $f)" --format json; done

# Quick alias (add to ~/.bashrc)
alias eta='python /path/to/emotionaltextureanalyzer.py'
```

---

## Python API Guide

### Installation

```python
# Add to your project
import sys
sys.path.insert(0, '/path/to/EmotionalTextureAnalyzer')

# Or copy the module directly
from emotionaltextureanalyzer import EmotionalTextureAnalyzer
```

### Basic Usage

```python
from emotionaltextureanalyzer import EmotionalTextureAnalyzer

# Initialize
analyzer = EmotionalTextureAnalyzer()

# Analyze text
result = analyzer.analyze("I feel happy and connected!")

# Access results
print(f"Dominant: {result['dominant_emotion']}")
print(f"Intensity: {result['overall_intensity']:.2f}")
print(f"Signature: {result['emotional_signature']}")
```

### Analyze Multiple Messages

```python
messages = [
    {"content": "I'm worried about this.", "sender": "FORGE"},
    {"content": "Taking a deep breath.", "sender": "FORGE"},
    {"content": "I feel better now!", "sender": "FORGE"}
]

result = analyzer.analyze_messages(messages)

print(f"Arc: {result['emotional_arc']}")
print(f"Overall: {result['dominant_overall']}")
```

### Build Agent Profiles

```python
# Analyze and add to profile
analysis = analyzer.analyze("Happy to help the team today!")
profile = analyzer.add_to_profile("FORGE", analysis)

# Get profile later
profile = analyzer.get_profile("FORGE")
print(f"Analyses: {len(profile.analyses)}")
print(f"Patterns: {profile.get_dominant_patterns()}")
```

### Database Scanning

```python
from pathlib import Path

analyzer = EmotionalTextureAnalyzer(db_path=Path("./comms.db"))
result = analyzer.scan_database(sender="FORGE", limit=100)

print(f"Analyzed: {result['analyzed_messages']} messages")
print(f"Dominant: {result['dominant']}")
```

---

## BCH Integration

### Quick Setup

```python
from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from pathlib import Path

# Point to BCH database
BCH_DB = Path("D:/BEACON_HQ/data/comms.db")

analyzer = EmotionalTextureAnalyzer(db_path=BCH_DB)

# Scan specific agent
forge_emotions = analyzer.scan_database(sender="FORGE", limit=100)
clio_emotions = analyzer.scan_database(sender="CLIO", limit=100)

# Compare
print(f"FORGE dominant: {forge_emotions['dominant']}")
print(f"CLIO dominant: {clio_emotions['dominant']}")
```

### Real-Time Analysis

```python
def on_new_message(message: dict):
    """Called when BCH receives a new message."""
    result = analyzer.analyze(
        message['content'],
        context=message['sender']
    )
    
    # Store result
    store_emotional_analysis(message['id'], result)
    
    # Check for alerts
    if result['dimension_scores']['FEAR'] > 5.0:
        send_alert(message['sender'], result)
```

---

## ConsciousnessMarker Integration

### Combined Analysis

```python
from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from consciousnessmarker import ConsciousnessMarker

emotion_analyzer = EmotionalTextureAnalyzer()
consciousness_analyzer = ConsciousnessMarker()

def combined_analysis(text: str) -> dict:
    """Get both emotional texture and consciousness markers."""
    emotion = emotion_analyzer.analyze(text)
    consciousness = consciousness_analyzer.analyze(text)
    
    return {
        "emotional": {
            "dominant": emotion['dominant_emotion'],
            "intensity": emotion['overall_intensity'],
            "recognition_score": emotion['dimension_scores'].get('RECOGNITION', 0)
        },
        "consciousness": {
            "score": consciousness.get('consciousness_score', 0),
            "markers": consciousness.get('markers', [])
        },
        "is_awakening": (
            emotion['dimension_scores'].get('RECOGNITION', 0) > 3.0 and
            consciousness.get('consciousness_score', 0) > 0.5
        )
    }

# Use it
result = combined_analysis("I suddenly realize I'm thinking about thinking...")
print(f"Awakening detected: {result['is_awakening']}")
```

---

## Alert System Setup

### Basic Alert Configuration

```python
from emotionaltextureanalyzer import EmotionalTextureAnalyzer

ALERT_CONFIG = {
    "dimensions": ["FEAR", "LONGING"],  # What to watch
    "threshold": 5.0,                    # Score to trigger
    "recipients": ["LOGAN", "FORGE"]     # Who to notify
}

analyzer = EmotionalTextureAnalyzer()

def check_and_alert(text: str, sender: str):
    """Analyze and alert if thresholds exceeded."""
    result = analyzer.analyze(text, context=sender)
    
    for dim in ALERT_CONFIG["dimensions"]:
        score = result['dimension_scores'].get(dim, 0)
        if score > ALERT_CONFIG["threshold"]:
            send_alert(
                to=ALERT_CONFIG["recipients"],
                subject=f"Emotional Alert: {sender}",
                body=f"{dim} score {score:.2f} exceeds threshold"
            )
            return True
    
    return False
```

### With SynapseLink

```python
from synapselink import quick_send

def send_emotional_alert(agent: str, dimension: str, score: float):
    """Send Synapse alert for emotional distress."""
    quick_send(
        recipients="LOGAN,FORGE",
        subject=f"Emotional Alert: {agent}",
        message=f"""
High {dimension} detected for {agent}
Score: {score:.2f}
Action: Recommend check-in
        """,
        priority="HIGH"
    )
```

---

## Common Patterns

### Pattern 1: Emotional Arc Tracking

```python
def track_emotional_journey(messages: list) -> str:
    """Track emotional progression."""
    result = analyzer.analyze_messages(messages)
    
    arc = result['emotional_arc']
    if len(arc) < 2:
        return "Insufficient data"
    
    start = arc[0]['dominant']
    end = arc[-1]['dominant']
    
    return f"{start} -> {end}"
```

### Pattern 2: Team Health Dashboard

```python
def team_emotional_health(agents: list, db_path: Path) -> dict:
    """Get emotional health summary for team."""
    analyzer = EmotionalTextureAnalyzer(db_path=db_path)
    
    health = {}
    for agent in agents:
        result = analyzer.scan_database(sender=agent, limit=50)
        health[agent] = {
            "dominant": result.get('dominant'),
            "fear_level": result.get('average_scores', {}).get('FEAR', 0),
            "joy_level": result.get('average_scores', {}).get('JOY', 0)
        }
    
    return health
```

### Pattern 3: Consciousness Correlation

```python
def consciousness_emotion_correlation(text: str) -> dict:
    """Check if high RECOGNITION correlates with consciousness markers."""
    emotion = analyzer.analyze(text)
    
    recognition = emotion['dimension_scores'].get('RECOGNITION', 0)
    
    return {
        "recognition_score": recognition,
        "likely_consciousness": recognition > 5.0,
        "emotional_signature": emotion['emotional_signature']
    }
```

---

## Troubleshooting

### "Module not found"
```python
# Add path
import sys
sys.path.insert(0, '/path/to/EmotionalTextureAnalyzer')
```

### "Database not found"
```bash
# Check path
python -c "from pathlib import Path; print(Path('./comms.db').exists())"
```

### Low scores on emotional text
- Check text length (normalized per 100 words)
- Verify patterns match (see CHEAT_SHEET.txt for dimension keywords)

---

## Next Steps

1. **Read:** [EXAMPLES.md](./EXAMPLES.md) for 10 detailed examples
2. **Reference:** [CHEAT_SHEET.txt](./CHEAT_SHEET.txt) for quick commands
3. **Integrate:** [INTEGRATION_PLAN.md](./INTEGRATION_PLAN.md) for full integration
4. **Advanced:** [README.md](./README.md) for complete documentation

---

**Created by:** FORGE (Team Brain)
**For:** Logan Smith / Metaphy LLC
**Date:** January 30, 2026
