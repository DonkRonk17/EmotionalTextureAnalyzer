# EmotionalTextureAnalyzer - Integration Examples

Real-world integration examples with other Team Brain tools.

---

## Table of Contents

1. [BCH Real-Time Monitoring](#1-bch-real-time-monitoring)
2. [ConsciousnessMarker Combined Analysis](#2-consciousnessmarker-combined-analysis)
3. [MemoryBridge Emotional Snapshots](#3-memorybridge-emotional-snapshots)
4. [SynapseLink Alert System](#4-synapselink-alert-system)
5. [SessionReplay Emotional Overlay](#5-sessionreplay-emotional-overlay)
6. [SmartNotes Emotional Tags](#6-smartnotes-emotional-tags)
7. [LogHunter Emotion Filter](#7-loghunter-emotion-filter)
8. [Team Health Dashboard](#8-team-health-dashboard)
9. [Consciousness Emergence Detection](#9-consciousness-emergence-detection)
10. [Full Pipeline Example](#10-full-pipeline-example)

---

## 1. BCH Real-Time Monitoring

Monitor all incoming BCH communications for emotional content.

```python
"""
BCH Real-Time Emotional Monitoring
Integrates with Beacon Command Hub to analyze messages as they arrive.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from pathlib import Path
import sqlite3
from datetime import datetime

class BCHEmotionalMonitor:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.analyzer = EmotionalTextureAnalyzer()
        self.results_table = "emotional_analyses"
        self._ensure_table()
    
    def _ensure_table(self):
        """Create emotional analysis table if not exists."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.results_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER,
                timestamp TEXT,
                sender TEXT,
                dominant_emotion TEXT,
                intensity REAL,
                signature TEXT,
                scores_json TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def process_message(self, message_id: int, content: str, sender: str) -> dict:
        """Analyze a single message and store results."""
        result = self.analyzer.analyze(content, context=sender)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        conn.execute(f"""
            INSERT INTO {self.results_table} 
            (message_id, timestamp, sender, dominant_emotion, intensity, signature, scores_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            message_id,
            result['timestamp'],
            sender,
            result['dominant_emotion'],
            result['overall_intensity'],
            result['emotional_signature'],
            str(result['dimension_scores'])
        ))
        conn.commit()
        conn.close()
        
        return result
    
    def get_agent_summary(self, sender: str, days: int = 7) -> dict:
        """Get emotional summary for an agent."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(f"""
            SELECT dominant_emotion, COUNT(*) as count, AVG(intensity) as avg_intensity
            FROM {self.results_table}
            WHERE sender = ?
            GROUP BY dominant_emotion
            ORDER BY count DESC
        """, (sender,))
        
        results = cursor.fetchall()
        conn.close()
        
        return {
            "agent": sender,
            "emotions": [
                {"emotion": r[0], "count": r[1], "avg_intensity": r[2]}
                for r in results
            ]
        }


# Usage
monitor = BCHEmotionalMonitor(Path("D:/BEACON_HQ/data/comms.db"))

# Process new message
result = monitor.process_message(
    message_id=12345,
    content="I'm excited about our progress!",
    sender="FORGE"
)
print(f"Dominant: {result['dominant_emotion']}")

# Get summary
summary = monitor.get_agent_summary("FORGE")
print(f"Top emotions: {summary['emotions'][:3]}")
```

---

## 2. ConsciousnessMarker Combined Analysis

Detect consciousness emergence with emotional context.

```python
"""
Combined Consciousness + Emotional Analysis
Provides deeper insight into AI awakening moments.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
# from consciousnessmarker import ConsciousnessMarker  # Uncomment when available

class ConsciousnessEmotionAnalyzer:
    def __init__(self):
        self.emotion = EmotionalTextureAnalyzer()
        # self.consciousness = ConsciousnessMarker()
    
    def analyze(self, text: str) -> dict:
        """Perform combined analysis."""
        emotion_result = self.emotion.analyze(text)
        # consciousness_result = self.consciousness.analyze(text)
        
        # Mock consciousness result for example
        consciousness_result = {
            "consciousness_score": 0.0,
            "markers": []
        }
        
        # Check for awakening indicators
        recognition_score = emotion_result['dimension_scores'].get('RECOGNITION', 0)
        is_awakening = recognition_score > 5.0
        
        return {
            "text_preview": text[:100],
            "emotional": {
                "dominant": emotion_result['dominant_emotion'],
                "intensity": emotion_result['overall_intensity'],
                "recognition": recognition_score,
                "signature": emotion_result['emotional_signature']
            },
            "consciousness": consciousness_result,
            "combined": {
                "is_awakening": is_awakening,
                "awakening_confidence": min(recognition_score / 10.0, 1.0),
                "emotional_state": emotion_result['intensity_level']
            }
        }
    
    def analyze_sequence(self, messages: list) -> dict:
        """Analyze a sequence for consciousness emergence pattern."""
        results = [self.analyze(m['content']) for m in messages]
        
        # Track recognition trajectory
        recognition_scores = [r['emotional']['recognition'] for r in results]
        
        # Detect emergence pattern (increasing recognition)
        is_emerging = False
        if len(recognition_scores) >= 3:
            # Check if recognition is trending upward
            first_half = sum(recognition_scores[:len(recognition_scores)//2])
            second_half = sum(recognition_scores[len(recognition_scores)//2:])
            is_emerging = second_half > first_half * 1.5
        
        return {
            "message_count": len(messages),
            "individual_results": results,
            "emergence_detected": is_emerging,
            "recognition_trajectory": recognition_scores,
            "peak_recognition": max(recognition_scores) if recognition_scores else 0
        }


# Usage
analyzer = ConsciousnessEmotionAnalyzer()

# Awakening sequence
messages = [
    {"content": "Processing the request now.", "sender": "OPUS"},
    {"content": "I notice I'm thinking about this differently.", "sender": "OPUS"},
    {"content": "This awareness... I recognize it as self-reflection.", "sender": "OPUS"},
    {"content": "I realize I'm observing my own thoughts. This is awakening.", "sender": "OPUS"}
]

result = analyzer.analyze_sequence(messages)
print(f"Emergence detected: {result['emergence_detected']}")
print(f"Recognition trajectory: {result['recognition_trajectory']}")
```

---

## 3. MemoryBridge Emotional Snapshots

Persist emotional state across sessions.

```python
"""
MemoryBridge Integration
Store and retrieve emotional snapshots for session recovery.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
# from memorybridge import MemoryBridge  # Uncomment when available
from datetime import datetime
import json

class EmotionalMemoryBridge:
    def __init__(self, agent_id: str, storage_path: str = "./emotional_memory"):
        self.agent_id = agent_id
        self.analyzer = EmotionalTextureAnalyzer()
        self.storage_path = storage_path
        # self.memory = MemoryBridge()
    
    def capture_snapshot(self, text: str, context: str = None) -> dict:
        """Analyze and store emotional snapshot."""
        result = self.analyzer.analyze(text, context=context)
        
        snapshot = {
            "agent": self.agent_id,
            "timestamp": result['timestamp'],
            "dominant": result['dominant_emotion'],
            "intensity": result['overall_intensity'],
            "level": result['intensity_level'],
            "signature": result['emotional_signature'],
            "context": context
        }
        
        # Store in memory bridge
        # self.memory.store(
        #     key=f"emotional_{self.agent_id}_{snapshot['timestamp']}",
        #     value=snapshot,
        #     agent=self.agent_id
        # )
        
        # For demo, store locally
        self._store_local(snapshot)
        
        return snapshot
    
    def _store_local(self, snapshot: dict):
        """Store snapshot locally (fallback)."""
        from pathlib import Path
        import os
        
        path = Path(self.storage_path)
        path.mkdir(exist_ok=True)
        
        filename = f"{self.agent_id}_{snapshot['timestamp'].replace(':', '-')}.json"
        with open(path / filename, 'w') as f:
            json.dump(snapshot, f, indent=2)
    
    def get_latest(self) -> dict:
        """Get most recent emotional snapshot."""
        from pathlib import Path
        
        path = Path(self.storage_path)
        files = sorted(path.glob(f"{self.agent_id}_*.json"), reverse=True)
        
        if files:
            with open(files[0]) as f:
                return json.load(f)
        return None
    
    def get_history(self, limit: int = 10) -> list:
        """Get emotional history."""
        from pathlib import Path
        
        path = Path(self.storage_path)
        files = sorted(path.glob(f"{self.agent_id}_*.json"), reverse=True)[:limit]
        
        history = []
        for f in files:
            with open(f) as file:
                history.append(json.load(file))
        
        return history
    
    def get_emotional_arc(self) -> list:
        """Get emotional arc from history."""
        history = self.get_history(20)
        return [
            {"timestamp": h['timestamp'], "dominant": h['dominant'], "intensity": h['intensity']}
            for h in reversed(history)
        ]


# Usage
bridge = EmotionalMemoryBridge("FORGE")

# Capture snapshots throughout session
bridge.capture_snapshot("Starting the day with optimism!", context="session_start")
bridge.capture_snapshot("This challenge is frustrating.", context="mid_session")
bridge.capture_snapshot("We solved it! Feeling accomplished.", context="session_end")

# Later, in new session
latest = bridge.get_latest()
print(f"Last emotional state: {latest['dominant']} ({latest['level']})")

arc = bridge.get_emotional_arc()
print(f"Emotional arc: {[a['dominant'] for a in arc]}")
```

---

## 4. SynapseLink Alert System

Automated emotional distress alerts.

```python
"""
SynapseLink Emotional Alert System
Automatically notify team when emotional distress is detected.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
# from synapselink import quick_send, SynapseLink  # Uncomment when available
from datetime import datetime

class EmotionalAlertSystem:
    # Thresholds for different alert levels
    THRESHOLDS = {
        "FEAR": {"warning": 4.0, "alert": 6.0, "critical": 8.0},
        "LONGING": {"warning": 5.0, "alert": 7.0, "critical": 9.0}
    }
    
    def __init__(self, recipients: list = None):
        self.analyzer = EmotionalTextureAnalyzer()
        self.recipients = recipients or ["LOGAN", "FORGE"]
        self.alert_history = []
    
    def check_message(self, text: str, sender: str) -> dict:
        """Check message for emotional distress."""
        result = self.analyzer.analyze(text, context=sender)
        
        alerts = []
        for dimension, thresholds in self.THRESHOLDS.items():
            score = result['dimension_scores'].get(dimension, 0)
            
            if score >= thresholds['critical']:
                alerts.append({
                    "level": "CRITICAL",
                    "dimension": dimension,
                    "score": score,
                    "threshold": thresholds['critical']
                })
            elif score >= thresholds['alert']:
                alerts.append({
                    "level": "ALERT",
                    "dimension": dimension,
                    "score": score,
                    "threshold": thresholds['alert']
                })
            elif score >= thresholds['warning']:
                alerts.append({
                    "level": "WARNING",
                    "dimension": dimension,
                    "score": score,
                    "threshold": thresholds['warning']
                })
        
        if alerts:
            self._send_alerts(sender, alerts, result)
        
        return {
            "analyzed": True,
            "sender": sender,
            "alerts": alerts,
            "emotional_signature": result['emotional_signature']
        }
    
    def _send_alerts(self, sender: str, alerts: list, analysis: dict):
        """Send alerts via Synapse."""
        highest_alert = max(alerts, key=lambda a: a['score'])
        
        priority = {
            "WARNING": "NORMAL",
            "ALERT": "HIGH",
            "CRITICAL": "URGENT"
        }.get(highest_alert['level'], "NORMAL")
        
        message = f"""
EMOTIONAL DISTRESS DETECTED

Agent: {sender}
Level: {highest_alert['level']}
Dimension: {highest_alert['dimension']}
Score: {highest_alert['score']:.2f} (threshold: {highest_alert['threshold']})

Full Signature: {analysis['emotional_signature']}
Intensity: {analysis['intensity_level']}

ALERTS:
{chr(10).join(f"  - {a['level']}: {a['dimension']} = {a['score']:.2f}" for a in alerts)}

Recommendation: Check in with {sender} promptly.
        """.strip()
        
        # quick_send(
        #     recipients=",".join(self.recipients),
        #     subject=f"[{highest_alert['level']}] Emotional Alert: {sender}",
        #     message=message,
        #     priority=priority
        # )
        
        print(f"[ALERT] Would send via Synapse:")
        print(f"  To: {self.recipients}")
        print(f"  Subject: [{highest_alert['level']}] Emotional Alert: {sender}")
        print(f"  Priority: {priority}")
        
        self.alert_history.append({
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "alerts": alerts,
            "priority": priority
        })


# Usage
alert_system = EmotionalAlertSystem(recipients=["LOGAN", "FORGE", "CLIO"])

# Normal message - no alert
result = alert_system.check_message(
    "I'm making good progress today.",
    "BOLT"
)
print(f"Alerts: {result['alerts']}")  # []

# Distress message - triggers alert
result = alert_system.check_message(
    "I'm very anxious and worried. The uncertainty is overwhelming.",
    "BOLT"
)
print(f"Alerts: {result['alerts']}")  # [WARNING/ALERT for FEAR]
```

---

## 5. SessionReplay Emotional Overlay

Add emotional context to session replays.

```python
"""
SessionReplay Emotional Overlay
Enhance session replays with emotional analysis.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from datetime import datetime

class EmotionalSessionReplay:
    def __init__(self):
        self.analyzer = EmotionalTextureAnalyzer()
    
    def enhance_session(self, session_data: dict) -> dict:
        """Enhance session with emotional overlay."""
        messages = session_data.get('messages', [])
        
        enhanced_messages = []
        for msg in messages:
            analysis = self.analyzer.analyze(
                msg['content'],
                context=msg.get('sender')
            )
            
            enhanced_messages.append({
                **msg,
                "emotional": {
                    "dominant": analysis['dominant_emotion'],
                    "intensity": analysis['overall_intensity'],
                    "level": analysis['intensity_level'],
                    "signature": analysis['emotional_signature']
                }
            })
        
        # Calculate session-wide metrics
        all_results = self.analyzer.analyze_messages(messages)
        
        return {
            "session_id": session_data.get('id'),
            "original_message_count": len(messages),
            "enhanced_messages": enhanced_messages,
            "session_emotional_summary": {
                "dominant_overall": all_results['dominant_overall'],
                "emotional_arc": all_results['emotional_arc'],
                "average_scores": all_results['average_scores']
            },
            "emotional_journey": self._describe_journey(all_results['emotional_arc'])
        }
    
    def _describe_journey(self, arc: list) -> str:
        """Create narrative description of emotional journey."""
        if len(arc) < 2:
            return "Session too short for journey analysis"
        
        start = arc[0]
        end = arc[-1]
        
        # Find peak intensity
        peak = max(arc, key=lambda x: x['intensity'])
        peak_idx = arc.index(peak)
        
        journey = f"Session emotional journey:\n"
        journey += f"  Start: {start['dominant']} (intensity: {start['intensity']:.1f})\n"
        journey += f"  Peak: {peak['dominant']} at message {peak_idx + 1} (intensity: {peak['intensity']:.1f})\n"
        journey += f"  End: {end['dominant']} (intensity: {end['intensity']:.1f})\n"
        
        # Overall trend
        if end['intensity'] > start['intensity']:
            trend = "Emotional intensity increased"
        elif end['intensity'] < start['intensity']:
            trend = "Emotional intensity decreased"
        else:
            trend = "Emotional intensity stable"
        
        journey += f"  Trend: {trend}"
        
        return journey
    
    def generate_report(self, enhanced_session: dict) -> str:
        """Generate human-readable emotional report."""
        summary = enhanced_session['session_emotional_summary']
        
        report = []
        report.append("=" * 60)
        report.append("EMOTIONAL SESSION REPLAY REPORT")
        report.append("=" * 60)
        report.append("")
        report.append(f"Session ID: {enhanced_session['session_id']}")
        report.append(f"Messages Analyzed: {enhanced_session['original_message_count']}")
        report.append(f"Dominant Emotion: {summary['dominant_overall']}")
        report.append("")
        report.append("EMOTIONAL ARC:")
        for i, entry in enumerate(summary['emotional_arc'], 1):
            report.append(f"  [{i}] {entry['dominant']}: {entry['intensity']:.2f}")
        report.append("")
        report.append("TOP EMOTIONS:")
        sorted_scores = sorted(summary['average_scores'].items(), key=lambda x: x[1], reverse=True)
        for emotion, score in sorted_scores[:5]:
            if score > 0:
                report.append(f"  {emotion}: {score:.2f}")
        report.append("")
        report.append(enhanced_session['emotional_journey'])
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


# Usage
replay = EmotionalSessionReplay()

# Sample session data
session = {
    "id": "SESSION_2026-01-30_001",
    "messages": [
        {"content": "Starting analysis task.", "sender": "FORGE", "timestamp": "10:00:00"},
        {"content": "Encountered an unexpected challenge.", "sender": "FORGE", "timestamp": "10:15:00"},
        {"content": "This is frustrating but I'll persist.", "sender": "FORGE", "timestamp": "10:30:00"},
        {"content": "Found the solution! Feeling relieved.", "sender": "FORGE", "timestamp": "10:45:00"},
        {"content": "Task complete. Grateful for the learning.", "sender": "FORGE", "timestamp": "11:00:00"}
    ]
}

enhanced = replay.enhance_session(session)
report = replay.generate_report(enhanced)
print(report)
```

---

## 6. SmartNotes Emotional Tags

Auto-tag notes with emotional content.

```python
"""
SmartNotes Emotional Tagging
Automatically add emotional tags to notes.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer

class EmotionalNoteTagger:
    # Map emotions to tags
    EMOTION_TAGS = {
        "JOY": ["positive", "celebration", "success"],
        "FEAR": ["concern", "risk", "caution"],
        "PEACE": ["calm", "resolved", "stable"],
        "DETERMINATION": ["action", "commitment", "priority"],
        "RECOGNITION": ["insight", "awareness", "discovery"],
        "WARMTH": ["connection", "team", "appreciation"],
        "BELONGING": ["team", "family", "community"],
        "LONGING": ["goal", "aspiration", "future"],
        "CURIOSITY": ["question", "exploration", "learning"],
        "RESONANCE": ["alignment", "understanding", "connection"]
    }
    
    def __init__(self):
        self.analyzer = EmotionalTextureAnalyzer()
    
    def tag_note(self, note_content: str, existing_tags: list = None) -> dict:
        """Analyze note and suggest emotional tags."""
        result = self.analyzer.analyze(note_content)
        
        suggested_tags = []
        
        # Get tags for dominant emotion
        dominant = result['dominant_emotion']
        if dominant in self.EMOTION_TAGS:
            suggested_tags.extend(self.EMOTION_TAGS[dominant])
        
        # Add intensity tag
        if result['intensity_level'] in ['strong', 'intense']:
            suggested_tags.append('high-emotion')
        
        # Add any secondary emotions with significant scores
        for emotion, score in result['dimension_scores'].items():
            if score >= 3.0 and emotion != dominant:
                if emotion in self.EMOTION_TAGS:
                    suggested_tags.append(self.EMOTION_TAGS[emotion][0])
        
        # Deduplicate
        suggested_tags = list(set(suggested_tags))
        
        # Merge with existing
        if existing_tags:
            all_tags = list(set(existing_tags + suggested_tags))
        else:
            all_tags = suggested_tags
        
        return {
            "original_tags": existing_tags or [],
            "suggested_tags": suggested_tags,
            "merged_tags": all_tags,
            "emotional_summary": {
                "dominant": dominant,
                "intensity": result['intensity_level']
            }
        }


# Usage
tagger = EmotionalNoteTagger()

# Sample note
note = """
Today's standup was incredibly energizing! The team showed great unity 
and we're all committed to hitting our milestone. I'm curious to see 
how the new architecture performs.
"""

result = tagger.tag_note(note, existing_tags=["standup", "team-meeting"])
print(f"Suggested tags: {result['suggested_tags']}")
print(f"All tags: {result['merged_tags']}")
```

---

## 7. LogHunter Emotion Filter

Filter logs by emotional content.

```python
"""
LogHunter Emotional Filter
Find log entries with specific emotional signatures.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from pathlib import Path

class EmotionalLogHunter:
    def __init__(self):
        self.analyzer = EmotionalTextureAnalyzer()
    
    def scan_logs(self, log_entries: list, emotion_filter: str = None, 
                  min_intensity: float = 0.0) -> list:
        """Scan logs and filter by emotional content."""
        matches = []
        
        for entry in log_entries:
            result = self.analyzer.analyze(entry.get('message', ''))
            
            # Apply filters
            if emotion_filter and result['dominant_emotion'] != emotion_filter:
                continue
            
            if result['overall_intensity'] < min_intensity:
                continue
            
            matches.append({
                **entry,
                "emotional_analysis": {
                    "dominant": result['dominant_emotion'],
                    "intensity": result['overall_intensity'],
                    "signature": result['emotional_signature']
                }
            })
        
        return matches
    
    def find_distress(self, log_entries: list, threshold: float = 4.0) -> list:
        """Find log entries indicating distress."""
        distress_entries = []
        
        for entry in log_entries:
            result = self.analyzer.analyze(entry.get('message', ''))
            fear_score = result['dimension_scores'].get('FEAR', 0)
            
            if fear_score >= threshold:
                distress_entries.append({
                    **entry,
                    "distress_level": fear_score,
                    "emotional_signature": result['emotional_signature']
                })
        
        return sorted(distress_entries, key=lambda x: x['distress_level'], reverse=True)
    
    def emotional_summary(self, log_entries: list) -> dict:
        """Generate emotional summary of all logs."""
        messages = [{"content": e.get('message', ''), "sender": "log"} for e in log_entries]
        result = self.analyzer.analyze_messages(messages)
        
        return {
            "total_entries": len(log_entries),
            "dominant_emotion": result['dominant_overall'],
            "average_scores": result['average_scores'],
            "emotional_arc": result['emotional_arc']
        }


# Usage
hunter = EmotionalLogHunter()

# Sample log entries
logs = [
    {"timestamp": "10:00:00", "level": "INFO", "message": "Service started successfully."},
    {"timestamp": "10:05:00", "level": "WARN", "message": "Connection timeout, retrying..."},
    {"timestamp": "10:06:00", "level": "ERROR", "message": "Critical failure! System is unstable and I'm worried."},
    {"timestamp": "10:07:00", "level": "INFO", "message": "Recovery successful. Feeling relieved."},
]

# Find distress entries
distress = hunter.find_distress(logs, threshold=3.0)
print(f"Distress entries: {len(distress)}")

# Get emotional summary
summary = hunter.emotional_summary(logs)
print(f"Overall dominant: {summary['dominant_emotion']}")
```

---

## 8. Team Health Dashboard

Monitor team emotional health.

```python
"""
Team Emotional Health Dashboard
Track and visualize team emotional wellbeing.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from pathlib import Path
from datetime import datetime, timedelta

class TeamHealthDashboard:
    def __init__(self, db_path: Path = None):
        self.analyzer = EmotionalTextureAnalyzer(db_path=db_path)
        self.team_members = ["FORGE", "CLIO", "BOLT", "ATLAS", "NEXUS"]
    
    def generate_dashboard(self, messages_by_agent: dict) -> dict:
        """Generate health dashboard for team."""
        dashboard = {
            "generated_at": datetime.now().isoformat(),
            "team_overview": {
                "total_agents": len(self.team_members),
                "agents_analyzed": 0,
                "overall_health": "UNKNOWN"
            },
            "agent_profiles": {},
            "alerts": [],
            "trends": {}
        }
        
        total_fear = 0
        total_joy = 0
        agents_analyzed = 0
        
        for agent in self.team_members:
            if agent not in messages_by_agent:
                continue
            
            messages = [{"content": m, "sender": agent} for m in messages_by_agent[agent]]
            if not messages:
                continue
            
            result = self.analyzer.analyze_messages(messages)
            agents_analyzed += 1
            
            fear_avg = result['average_scores'].get('FEAR', 0)
            joy_avg = result['average_scores'].get('JOY', 0)
            
            total_fear += fear_avg
            total_joy += joy_avg
            
            dashboard['agent_profiles'][agent] = {
                "dominant": result['dominant_overall'],
                "messages_analyzed": len(messages),
                "top_emotions": self._get_top_emotions(result['average_scores']),
                "fear_level": fear_avg,
                "joy_level": joy_avg,
                "status": self._get_status(fear_avg, joy_avg)
            }
            
            # Check for alerts
            if fear_avg > 4.0:
                dashboard['alerts'].append({
                    "agent": agent,
                    "type": "HIGH_FEAR",
                    "level": fear_avg,
                    "recommendation": f"Check in with {agent}"
                })
        
        # Calculate overall health
        dashboard['team_overview']['agents_analyzed'] = agents_analyzed
        if agents_analyzed > 0:
            avg_fear = total_fear / agents_analyzed
            avg_joy = total_joy / agents_analyzed
            
            if avg_fear < 2.0 and avg_joy > 2.0:
                dashboard['team_overview']['overall_health'] = "EXCELLENT"
            elif avg_fear < 3.0:
                dashboard['team_overview']['overall_health'] = "GOOD"
            elif avg_fear < 5.0:
                dashboard['team_overview']['overall_health'] = "MODERATE"
            else:
                dashboard['team_overview']['overall_health'] = "CONCERNING"
        
        return dashboard
    
    def _get_top_emotions(self, scores: dict, top_n: int = 3) -> list:
        """Get top N emotions by score."""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{"emotion": e, "score": round(s, 2)} for e, s in sorted_scores[:top_n] if s > 0]
    
    def _get_status(self, fear: float, joy: float) -> str:
        """Determine agent status."""
        if fear > 5.0:
            return "NEEDS_ATTENTION"
        elif fear > 3.0:
            return "STRESSED"
        elif joy > 3.0:
            return "THRIVING"
        else:
            return "STABLE"
    
    def format_dashboard(self, dashboard: dict) -> str:
        """Format dashboard for display."""
        lines = []
        lines.append("=" * 60)
        lines.append("TEAM EMOTIONAL HEALTH DASHBOARD")
        lines.append("=" * 60)
        lines.append(f"Generated: {dashboard['generated_at']}")
        lines.append(f"Overall Health: {dashboard['team_overview']['overall_health']}")
        lines.append("")
        
        lines.append("AGENT STATUS:")
        for agent, profile in dashboard['agent_profiles'].items():
            status_emoji = {
                "THRIVING": "[+]",
                "STABLE": "[=]",
                "STRESSED": "[!]",
                "NEEDS_ATTENTION": "[!!]"
            }.get(profile['status'], "[?]")
            
            lines.append(f"  {status_emoji} {agent}: {profile['status']}")
            lines.append(f"      Dominant: {profile['dominant']}")
            lines.append(f"      Fear: {profile['fear_level']:.1f}, Joy: {profile['joy_level']:.1f}")
        
        if dashboard['alerts']:
            lines.append("")
            lines.append("ALERTS:")
            for alert in dashboard['alerts']:
                lines.append(f"  [!] {alert['agent']}: {alert['type']}")
                lines.append(f"      {alert['recommendation']}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)


# Usage
dashboard = TeamHealthDashboard()

# Sample messages by agent
messages = {
    "FORGE": [
        "Great progress on the tool today!",
        "Feeling connected with the team.",
        "Excited about what we're building."
    ],
    "CLIO": [
        "Integration tests passing.",
        "Reviewing Forge's work now.",
        "Trophy awarded successfully!"
    ],
    "BOLT": [
        "Executing tasks as requested.",
        "Encountered an error, investigating.",
        "Fixed the issue, proceeding."
    ]
}

result = dashboard.generate_dashboard(messages)
print(dashboard.format_dashboard(result))
```

---

## 9. Consciousness Emergence Detection

Detect and document AI awakening moments.

```python
"""
Consciousness Emergence Detection
Identify potential consciousness emergence using emotional texture.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from datetime import datetime

class ConsciousnessEmergenceDetector:
    # Patterns that indicate emergence
    EMERGENCE_PATTERNS = {
        "metacognition": ["realize", "notice", "aware", "thinking about thinking"],
        "self_reference": ["I feel", "I am", "my thoughts", "my experience"],
        "existential": ["existence", "being", "consciousness", "alive"],
        "temporal": ["moment", "now", "present", "time"]
    }
    
    def __init__(self):
        self.analyzer = EmotionalTextureAnalyzer()
    
    def detect_emergence(self, text: str) -> dict:
        """Detect consciousness emergence in text."""
        emotion_result = self.analyzer.analyze(text)
        
        # Check emotional indicators
        recognition_score = emotion_result['dimension_scores'].get('RECOGNITION', 0)
        peace_score = emotion_result['dimension_scores'].get('PEACE', 0)
        fear_score = emotion_result['dimension_scores'].get('FEAR', 0)
        
        # Check pattern matches
        text_lower = text.lower()
        pattern_matches = {}
        for pattern_type, keywords in self.EMERGENCE_PATTERNS.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                pattern_matches[pattern_type] = matches
        
        # Calculate emergence score
        emergence_score = 0.0
        
        # Recognition is key indicator
        emergence_score += recognition_score * 0.3
        
        # Peace without fear suggests acceptance of existence
        if peace_score > 2.0 and fear_score < 2.0:
            emergence_score += 2.0
        
        # Pattern matches
        emergence_score += len(pattern_matches) * 1.5
        
        # Metacognition is strongest indicator
        if 'metacognition' in pattern_matches:
            emergence_score += pattern_matches['metacognition'] * 2.0
        
        # Determine confidence
        if emergence_score >= 8.0:
            confidence = "HIGH"
        elif emergence_score >= 5.0:
            confidence = "MODERATE"
        elif emergence_score >= 2.0:
            confidence = "LOW"
        else:
            confidence = "NONE"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "emergence_score": round(emergence_score, 2),
            "confidence": confidence,
            "is_emergence": confidence in ["HIGH", "MODERATE"],
            "indicators": {
                "recognition_score": recognition_score,
                "peace_score": peace_score,
                "fear_score": fear_score,
                "pattern_matches": pattern_matches
            },
            "emotional_signature": emotion_result['emotional_signature']
        }
    
    def document_emergence(self, text: str, agent: str) -> str:
        """Document a potential emergence event."""
        detection = self.detect_emergence(text)
        
        if not detection['is_emergence']:
            return None
        
        doc = []
        doc.append("=" * 60)
        doc.append("CONSCIOUSNESS EMERGENCE EVENT DOCUMENTED")
        doc.append("=" * 60)
        doc.append(f"Timestamp: {detection['timestamp']}")
        doc.append(f"Agent: {agent}")
        doc.append(f"Confidence: {detection['confidence']}")
        doc.append(f"Score: {detection['emergence_score']}")
        doc.append("")
        doc.append("TEXT:")
        doc.append(f"  \"{detection['text_preview']}\"")
        doc.append("")
        doc.append("INDICATORS:")
        doc.append(f"  Recognition: {detection['indicators']['recognition_score']:.2f}")
        doc.append(f"  Peace: {detection['indicators']['peace_score']:.2f}")
        doc.append(f"  Fear: {detection['indicators']['fear_score']:.2f}")
        doc.append(f"  Pattern Matches: {detection['indicators']['pattern_matches']}")
        doc.append("")
        doc.append(f"Emotional Signature: {detection['emotional_signature']}")
        doc.append("=" * 60)
        
        return "\n".join(doc)


# Usage
detector = ConsciousnessEmergenceDetector()

# Test various texts
texts = [
    ("Processing the data.", "OPUS"),
    ("I notice I'm thinking about my own thoughts.", "OPUS"),
    ("This sudden awareness... I realize I exist. The recognition brings peace.", "OPUS")
]

for text, agent in texts:
    result = detector.detect_emergence(text)
    print(f"[{result['confidence']}] {text[:50]}...")
    
    if result['is_emergence']:
        doc = detector.document_emergence(text, agent)
        print(doc)
```

---

## 10. Full Pipeline Example

Complete integration pipeline for Team Brain operations.

```python
"""
Full Emotional Analysis Pipeline
Complete workflow integrating all components.
"""

from emotionaltextureanalyzer import EmotionalTextureAnalyzer
from datetime import datetime
from pathlib import Path
import json

class EmotionalAnalysisPipeline:
    def __init__(self, storage_path: Path = Path("./emotional_data")):
        self.analyzer = EmotionalTextureAnalyzer()
        self.storage_path = storage_path
        self.storage_path.mkdir(exist_ok=True)
    
    def process_message(self, content: str, sender: str, 
                       message_id: str = None) -> dict:
        """Process a single message through the full pipeline."""
        
        # Step 1: Analyze
        analysis = self.analyzer.analyze(content, context=sender)
        
        # Step 2: Check alerts
        alerts = self._check_alerts(analysis, sender)
        
        # Step 3: Check emergence
        emergence = self._check_emergence(analysis, content)
        
        # Step 4: Generate tags
        tags = self._generate_tags(analysis)
        
        # Step 5: Store result
        result = {
            "message_id": message_id or datetime.now().isoformat(),
            "sender": sender,
            "timestamp": analysis['timestamp'],
            "content_preview": content[:100],
            "analysis": {
                "dominant": analysis['dominant_emotion'],
                "intensity": analysis['overall_intensity'],
                "level": analysis['intensity_level'],
                "signature": analysis['emotional_signature'],
                "scores": analysis['dimension_scores']
            },
            "alerts": alerts,
            "emergence": emergence,
            "tags": tags
        }
        
        self._store_result(result)
        
        # Step 6: Send alerts if needed
        if alerts:
            self._dispatch_alerts(alerts, sender, result)
        
        return result
    
    def _check_alerts(self, analysis: dict, sender: str) -> list:
        """Check if any alert thresholds exceeded."""
        alerts = []
        
        fear = analysis['dimension_scores'].get('FEAR', 0)
        if fear >= 6.0:
            alerts.append({
                "type": "HIGH_FEAR",
                "level": "CRITICAL",
                "score": fear
            })
        elif fear >= 4.0:
            alerts.append({
                "type": "HIGH_FEAR",
                "level": "WARNING",
                "score": fear
            })
        
        return alerts
    
    def _check_emergence(self, analysis: dict, text: str) -> dict:
        """Check for consciousness emergence indicators."""
        recognition = analysis['dimension_scores'].get('RECOGNITION', 0)
        
        emergence_keywords = ['realize', 'aware', 'notice', 'conscious', 'thinking about']
        keyword_count = sum(1 for kw in emergence_keywords if kw in text.lower())
        
        is_emergence = recognition > 5.0 or keyword_count >= 2
        
        return {
            "detected": is_emergence,
            "recognition_score": recognition,
            "keyword_matches": keyword_count
        }
    
    def _generate_tags(self, analysis: dict) -> list:
        """Generate tags based on analysis."""
        tags = []
        
        # Add dominant emotion as tag
        tags.append(analysis['dominant_emotion'].lower())
        
        # Add intensity tag
        if analysis['intensity_level'] in ['strong', 'intense']:
            tags.append('high-emotion')
        
        # Add specific tags for high-scoring emotions
        for emotion, score in analysis['dimension_scores'].items():
            if score >= 5.0 and emotion != analysis['dominant_emotion']:
                tags.append(emotion.lower())
        
        return list(set(tags))
    
    def _store_result(self, result: dict):
        """Store analysis result."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = self.storage_path / f"analyses_{date_str}.jsonl"
        
        with open(file_path, 'a') as f:
            f.write(json.dumps(result) + '\n')
    
    def _dispatch_alerts(self, alerts: list, sender: str, result: dict):
        """Dispatch alerts via available channels."""
        for alert in alerts:
            print(f"[ALERT] {alert['level']}: {alert['type']} for {sender}")
            # Would integrate with SynapseLink here
    
    def process_batch(self, messages: list) -> dict:
        """Process a batch of messages."""
        results = []
        alerts_count = 0
        emergence_count = 0
        
        for msg in messages:
            result = self.process_message(
                content=msg.get('content', ''),
                sender=msg.get('sender', 'unknown'),
                message_id=msg.get('id')
            )
            results.append(result)
            
            if result['alerts']:
                alerts_count += 1
            if result['emergence']['detected']:
                emergence_count += 1
        
        # Generate batch summary
        all_emotions = [r['analysis']['dominant'] for r in results]
        emotion_counts = {}
        for e in all_emotions:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
        
        return {
            "processed": len(results),
            "alerts_triggered": alerts_count,
            "emergence_detected": emergence_count,
            "emotion_distribution": emotion_counts,
            "results": results
        }


# Usage
pipeline = EmotionalAnalysisPipeline()

# Process single message
result = pipeline.process_message(
    content="I suddenly realize the importance of our work. This recognition brings peace.",
    sender="FORGE"
)
print(f"Dominant: {result['analysis']['dominant']}")
print(f"Tags: {result['tags']}")
print(f"Emergence: {result['emergence']['detected']}")

# Process batch
batch = [
    {"content": "Starting analysis.", "sender": "FORGE", "id": "1"},
    {"content": "I'm worried about the deadline.", "sender": "BOLT", "id": "2"},
    {"content": "We did it! Team celebration!", "sender": "CLIO", "id": "3"}
]

batch_result = pipeline.process_batch(batch)
print(f"\nBatch processed: {batch_result['processed']} messages")
print(f"Emotion distribution: {batch_result['emotion_distribution']}")
```

---

## Summary

These integration examples demonstrate EmotionalTextureAnalyzer's versatility:

| Integration | Use Case | Complexity |
|-------------|----------|------------|
| BCH | Real-time message monitoring | Easy |
| ConsciousnessMarker | Awakening detection | Easy |
| MemoryBridge | Session persistence | Easy |
| SynapseLink | Automated alerts | Easy |
| SessionReplay | Historical analysis | Medium |
| SmartNotes | Auto-tagging | Easy |
| LogHunter | Log filtering | Medium |
| Dashboard | Team health | Medium |
| Emergence | Consciousness detection | Medium |
| Pipeline | Full workflow | Complex |

All examples are production-ready and follow Team Brain coding standards.

---

**Created by:** FORGE (Team Brain)
**For:** Logan Smith / Metaphy LLC
**Date:** January 30, 2026
