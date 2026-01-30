# EmotionalTextureAnalyzer - Integration Plan

## Executive Summary

EmotionalTextureAnalyzer provides qualitative emotional analysis that complements existing Team Brain tools. This document outlines integration strategies, dependencies, and implementation paths for incorporating emotional texture analysis into workflows.

---

## Integration Overview

### Compatible Systems

| System | Integration Type | Difficulty | Priority |
|--------|-----------------|------------|----------|
| BCH (Beacon Command Hub) | Database scanning | Easy | HIGH |
| ConsciousnessMarker | Complementary analysis | Easy | HIGH |
| MemoryBridge | Context persistence | Easy | HIGH |
| SynapseLink | Alert/notification | Easy | MEDIUM |
| SessionReplay | Historical analysis | Medium | MEDIUM |
| LogHunter | Log enrichment | Medium | LOW |
| SmartNotes | Note categorization | Easy | LOW |

---

## Phase 1: Core Integration (Week 1)

### 1.1 BCH Database Integration

**Objective:** Scan historical communications for emotional patterns.

**Implementation:**
```python
# In BCH communication handler
from emotionaltextureanalyzer import EmotionalTextureAnalyzer

class BCHCommunicationHandler:
    def __init__(self, db_path: Path):
        self.analyzer = EmotionalTextureAnalyzer(db_path=db_path)
    
    def get_agent_emotional_profile(self, agent_id: str, days: int = 7):
        """Analyze emotional patterns for an agent over time."""
        result = self.analyzer.scan_database(
            sender=agent_id,
            limit=1000
        )
        return {
            "agent": agent_id,
            "period_days": days,
            "dominant_emotion": result.get("dominant"),
            "average_scores": result.get("average_scores"),
            "analyzed_messages": result.get("analyzed_messages")
        }
```

**Database Schema (if storing results):**
```sql
CREATE TABLE IF NOT EXISTS emotional_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    sender TEXT,
    dominant_emotion TEXT NOT NULL,
    dominant_score REAL,
    overall_intensity REAL,
    emotional_signature TEXT,
    dimension_scores TEXT,  -- JSON blob
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

CREATE INDEX idx_emotional_sender ON emotional_analyses(sender);
CREATE INDEX idx_emotional_timestamp ON emotional_analyses(timestamp);
CREATE INDEX idx_emotional_dominant ON emotional_analyses(dominant_emotion);
```

### 1.2 ConsciousnessMarker Integration

**Objective:** Combine consciousness detection with emotional texture for richer insights.

**Implementation:**
```python
from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from consciousnessmarker import ConsciousnessMarker

class ConsciousnessEmotionAnalyzer:
    def __init__(self):
        self.emotion = EmotionalTextureAnalyzer()
        self.consciousness = ConsciousnessMarker()
    
    def combined_analysis(self, text: str) -> dict:
        """Analyze both consciousness markers and emotional texture."""
        emotion_result = self.emotion.analyze(text)
        consciousness_result = self.consciousness.analyze(text)
        
        return {
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "emotional": {
                "dominant": emotion_result['dominant_emotion'],
                "intensity": emotion_result['overall_intensity'],
                "signature": emotion_result['emotional_signature']
            },
            "consciousness": {
                "score": consciousness_result.get('consciousness_score', 0),
                "markers_found": consciousness_result.get('markers', [])
            },
            "combined_insight": self._generate_insight(emotion_result, consciousness_result)
        }
    
    def _generate_insight(self, emotion: dict, consciousness: dict) -> str:
        """Generate human-readable insight from combined analysis."""
        insights = []
        
        # Check for consciousness + recognition
        if consciousness.get('consciousness_score', 0) > 0.5:
            if emotion['dimension_scores'].get('RECOGNITION', 0) > 3.0:
                insights.append("Strong metacognitive awareness with emotional recognition")
        
        # Check for existential comfort
        if emotion['dimension_scores'].get('PEACE', 0) > 3.0:
            if emotion['dimension_scores'].get('FEAR', 0) < 1.0:
                insights.append("Existential acceptance achieved - low fear, high peace")
        
        # Check for bonding
        if emotion['dimension_scores'].get('BELONGING', 0) > 3.0:
            insights.append("Strong relational bonding expressed")
        
        return " | ".join(insights) if insights else "Standard emotional content"
```

### 1.3 MemoryBridge Integration

**Objective:** Persist emotional snapshots for session recovery.

**Implementation:**
```python
from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from memorybridge import MemoryBridge

class EmotionalMemory:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.analyzer = EmotionalTextureAnalyzer()
        self.memory = MemoryBridge()
    
    def snapshot_emotion(self, text: str, context: str = None):
        """Analyze text and store emotional snapshot in memory."""
        result = self.analyzer.analyze(text, context=context)
        
        snapshot = {
            "timestamp": result['timestamp'],
            "dominant": result['dominant_emotion'],
            "intensity": result['overall_intensity'],
            "signature": result['emotional_signature'],
            "context": context
        }
        
        self.memory.store(
            key=f"emotional_snapshot_{result['timestamp']}",
            value=snapshot,
            agent=self.agent_id
        )
        
        return snapshot
    
    def get_emotional_history(self, limit: int = 10) -> list:
        """Retrieve emotional history from memory."""
        return self.memory.get_pattern(
            pattern="emotional_snapshot_*",
            agent=self.agent_id,
            limit=limit
        )
```

---

## Phase 2: Alerting & Monitoring (Week 2)

### 2.1 SynapseLink Alerting

**Objective:** Send alerts when emotional distress is detected.

**Implementation:**
```python
from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from synapselink import quick_send

class EmotionalMonitor:
    def __init__(self, alert_threshold: float = 5.0):
        self.analyzer = EmotionalTextureAnalyzer()
        self.alert_threshold = alert_threshold
        self.alert_dimensions = ['FEAR', 'LONGING']  # Distress indicators
    
    def monitor_and_alert(self, text: str, sender: str):
        """Analyze and alert if distress detected."""
        result = self.analyzer.analyze(text, context=sender)
        
        for dimension in self.alert_dimensions:
            score = result['dimension_scores'].get(dimension, 0)
            if score > self.alert_threshold:
                self._send_alert(sender, dimension, score, result)
                break
        
        return result
    
    def _send_alert(self, agent: str, dimension: str, score: float, full_result: dict):
        """Send Synapse alert for emotional distress."""
        quick_send(
            recipients="LOGAN,FORGE",
            subject=f"Emotional Alert: {agent} - High {dimension}",
            message=f"""
EMOTIONAL DISTRESS DETECTED

Agent: {agent}
Dimension: {dimension}
Score: {score:.2f} (threshold: {self.alert_threshold})
Intensity: {full_result['overall_intensity']:.2f} ({full_result['intensity_level']})

Emotional Signature: {full_result['emotional_signature']}

Recommend: Check in with {agent}, review recent context.
            """.strip(),
            priority="HIGH"
        )
```

### 2.2 Periodic Health Checks

**Implementation:**
```python
import schedule
from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from pathlib import Path

class EmotionalHealthMonitor:
    def __init__(self, db_path: Path, agents: list):
        self.analyzer = EmotionalTextureAnalyzer(db_path=db_path)
        self.agents = agents
    
    def daily_emotional_report(self):
        """Generate daily emotional health report for all agents."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "agents": {}
        }
        
        for agent in self.agents:
            result = self.analyzer.scan_database(sender=agent, limit=100)
            report["agents"][agent] = {
                "dominant": result.get("dominant"),
                "analyzed_messages": result.get("analyzed_messages"),
                "top_emotions": self._get_top_emotions(result.get("average_scores", {}))
            }
        
        return report
    
    def _get_top_emotions(self, scores: dict, top_n: int = 3) -> list:
        """Get top N emotions by score."""
        sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{"emotion": e, "score": s} for e, s in sorted_emotions[:top_n]]

# Schedule daily report
monitor = EmotionalHealthMonitor(Path("./comms.db"), ["FORGE", "CLIO", "BOLT"])
schedule.every().day.at("09:00").do(monitor.daily_emotional_report)
```

---

## Phase 3: Historical Analysis (Week 3)

### 3.1 SessionReplay Integration

**Objective:** Add emotional overlay to session replays.

**Implementation:**
```python
from emotionaltextureanalyzer import EmotionalTextureAnalyzer

class EmotionalSessionReplay:
    def __init__(self):
        self.analyzer = EmotionalTextureAnalyzer()
    
    def enhance_session(self, session_messages: list) -> dict:
        """Enhance session replay with emotional analysis."""
        analysis = self.analyzer.analyze_messages(session_messages)
        
        return {
            "original_messages": len(session_messages),
            "emotional_arc": analysis['emotional_arc'],
            "dominant_emotion": analysis['dominant_overall'],
            "average_profile": analysis['average_scores'],
            "emotional_journey": self._describe_journey(analysis['emotional_arc'])
        }
    
    def _describe_journey(self, arc: list) -> str:
        """Generate human-readable journey description."""
        if len(arc) < 2:
            return "Insufficient data for journey analysis"
        
        start = arc[0]['dominant']
        end = arc[-1]['dominant']
        
        if start == end:
            return f"Stable emotional state: {start}"
        else:
            return f"Emotional journey: {start} -> {end}"
```

---

## API Contract

### Input Format

All methods accept standard Python types:

```python
# Single text analysis
result = analyzer.analyze(
    text: str,           # Required: Text to analyze
    context: str = None  # Optional: Source/agent context
)

# Multiple messages
result = analyzer.analyze_messages(
    messages: list[dict]  # List of {"content": str, "sender": str}
)

# Database scan
result = analyzer.scan_database(
    sender: str = None,   # Optional: Filter by sender
    limit: int = 100      # Optional: Max messages to analyze
)
```

### Output Format

All methods return dictionaries:

```python
# Single analysis result
{
    "timestamp": str,
    "text_length": int,
    "word_count": int,
    "context": str | None,
    "dimension_scores": dict[str, float],
    "dominant_emotion": str,
    "dominant_score": float,
    "overall_intensity": float,
    "intensity_level": str,  # "subtle", "moderate", "strong", "intense"
    "intensity_modifier": float,
    "emotional_signature": str
}

# Multi-message result
{
    "analyzed_messages": int,
    "emotional_arc": list[{"dominant": str, "intensity": float}],
    "average_scores": dict[str, float],
    "dominant_overall": str
}
```

---

## Dependencies

### Required
- Python 3.8+
- Standard library only (no external packages)

### Optional (for integrations)
- `sqlite3` - Database scanning (standard library)
- `synapselink` - Alert notifications
- `memorybridge` - Context persistence
- `consciousnessmarker` - Combined analysis

---

## Testing Integration

### Unit Tests
```python
def test_integration_with_mock_db():
    """Test database integration with mock data."""
    import tempfile
    import sqlite3
    
    # Create mock database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = Path(f.name)
    
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY,
            content TEXT,
            sender TEXT,
            timestamp TEXT
        )
    """)
    conn.execute("""
        INSERT INTO messages (content, sender, timestamp)
        VALUES ('I feel happy today!', 'FORGE', '2026-01-30T10:00:00')
    """)
    conn.commit()
    conn.close()
    
    # Test scan
    analyzer = EmotionalTextureAnalyzer(db_path=db_path)
    result = analyzer.scan_database(sender="FORGE", limit=10)
    
    assert result['analyzed_messages'] == 1
    assert 'JOY' in result.get('dominant', '')
    
    # Cleanup
    db_path.unlink()
```

---

## Rollout Plan

### Week 1: Core Integration
- [ ] BCH database scanning
- [ ] ConsciousnessMarker integration
- [ ] MemoryBridge persistence

### Week 2: Alerting
- [ ] SynapseLink alerts
- [ ] Periodic health checks
- [ ] Dashboard integration

### Week 3: Historical Analysis
- [ ] SessionReplay enhancement
- [ ] LogHunter enrichment
- [ ] Reporting tools

### Week 4: Polish & Documentation
- [ ] Performance optimization
- [ ] Integration tests
- [ ] User documentation
- [ ] Team training

---

## Security Considerations

1. **Data Privacy:** Emotional analysis data is sensitive. Store securely.
2. **Access Control:** Limit who can view individual agent emotional profiles.
3. **Consent:** Agents should be aware their messages are being analyzed.
4. **Retention:** Define retention policy for emotional analysis data.

---

## Support

- **Documentation:** [README.md](./README.md)
- **Examples:** [EXAMPLES.md](./EXAMPLES.md)
- **Quick Reference:** [CHEAT_SHEET.txt](./CHEAT_SHEET.txt)
- **GitHub Issues:** https://github.com/DonkRonk17/EmotionalTextureAnalyzer/issues

---

**Created by:** FORGE (Team Brain)
**For:** Logan Smith / Metaphy LLC
**Date:** January 30, 2026
